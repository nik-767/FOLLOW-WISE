from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.base import get_db
from app.core.security import get_current_active_user
from app.ai.providers import get_ai_provider, AIProvider

# Models
from app.models.user import User
from app.models.lead import Lead, LeadStatus, LeadSource
from app.models.followup_suggestion import FollowUpSuggestion
from app.models.sent_email_log import SentEmailLog

# Schemas
from app.schemas.lead import Lead as LeadSchema, LeadCreate, LeadUpdate, LeadList, LeadStatus as LeadStatusEnum
from app.schemas.followup import (
    FollowUpSuggestion as FollowUpSuggestionSchema,
    FollowUpGenerateRequest,
    FollowUpGenerateResponse,
    SentEmail as SentEmailSchema,
    SentEmailCreate,
    SentEmailList,
    FollowUpTone
)

router = APIRouter()

# --- Leads CRUD Endpoints ---

@router.get("/", response_model=List[LeadSchema])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    status: Optional[LeadStatusEnum] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve leads with optional filtering and search
    """
    query = db.query(Lead).filter(Lead.user_id == current_user.id)
    
    if status:
        query = query.filter(Lead.status == status)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Lead.contact_name.ilike(search),
                Lead.contact_email.ilike(search),
                Lead.company.ilike(search),
                Lead.notes.ilike(search)
            )
        )
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=LeadSchema, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new lead
    """
    db_lead = Lead(**lead.dict(), user_id=current_user.id)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/{lead_id}", response_model=LeadSchema)
def read_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific lead by ID
    """
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/{lead_id}", response_model=LeadSchema)
def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a lead
    """
    db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = lead_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_lead, field, value)
    
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a lead
    """
    db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(db_lead)
    db.commit()
    return None

# --- Email Scanning Endpoints ---

@router.post("/scan-inbox", status_code=status.HTTP_201_CREATED)
async def scan_inbox(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Scan user's inbox and extract leads from emails (MVP simulation)
    """
    # Simulate email scanning with dummy data
    mock_email_leads = [
        {
            "contact_name": "Sarah Johnson",
            "contact_email": "sarah.j@techcorp.com",
            "company": "TechCorp Solutions",
            "notes": "Interested in AI sales automation tools. Found your website through LinkedIn.",
            "source": "email",
            "status": "new",
            "lead_score": 75
        },
        {
            "contact_name": "Michael Chen",
            "contact_email": "mchen@startuphub.io",
            "company": "StartupHub",
            "notes": "Request for demo of follow-up automation system. Budget: $5,000-10,000.",
            "source": "email",
            "status": "new", 
            "lead_score": 85
        },
        {
            "contact_name": "Emily Rodriguez",
            "contact_email": "emily.r@globaltrade.com",
            "company": "Global Trade Inc",
            "notes": "Follow-up required after initial contact at trade show. Looking for enterprise solution.",
            "source": "email",
            "status": "in_progress",
            "lead_score": 90
        }
    ]
    
    # Create leads from extracted email data
    created_leads = []
    for lead_data in mock_email_leads:
        # Check if lead with this email already exists
        existing_lead = db.query(Lead).filter(
            Lead.contact_email == lead_data["contact_email"],
            Lead.user_id == current_user.id
        ).first()
        
        if not existing_lead:
            lead = Lead(
                user_id=current_user.id,
                **lead_data
            )
            db.add(lead)
            created_leads.append(lead)
    
    db.commit()
    
    return {
        "message": f"Inbox scanned successfully. Found {len(created_leads)} new leads from emails.",
        "leads_created": len(created_leads),
        "leads": [
            {
                "id": lead.id,
                "contact_name": lead.contact_name,
                "contact_email": lead.contact_email,
                "company": lead.company,
                "source": lead.source,
                "lead_score": lead.lead_score
            } for lead in created_leads
        ]
    }

# --- Follow-up Suggestions Endpoints ---

@router.post(
    "/{lead_id}/generate-followups",
    response_model=FollowUpGenerateResponse,
    status_code=status.HTTP_201_CREATED
)
async def generate_followup_suggestions(
    lead_id: int,
    request: FollowUpGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    ai_provider: AIProvider = Depends(get_ai_provider)
):
    """
    Generate AI-powered follow-up email suggestions for a lead
    """
    # Verify lead exists and belongs to user
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Generate follow-up suggestions using AI provider
    context = request.context or f"""
    Lead Name: {lead.contact_name}
    Company: {lead.company or 'N/A'}
    Last Interaction: {lead.last_email_snippet or 'No previous interaction'}
    Notes: {lead.notes or 'No additional notes'}
    """
    
    # Get suggestions from AI provider
    # Generate suggestions (provider returns Pydantic models)
    suggestions_data = await ai_provider.generate_followup_variants(
        context=context,
        tone=request.tone,
        lead_info={
            'contact_name': lead.contact_name,
            'user_name': current_user.email if hasattr(current_user, 'email') else None
        }
    )
    
    # Delete any existing suggestions for this lead
    db.query(FollowUpSuggestion).filter(FollowUpSuggestion.lead_id == lead_id).delete()
    
    # Save new suggestions
    suggestions = []
    for i, suggestion_data in enumerate(suggestions_data):
        suggestion = FollowUpSuggestion(
            lead_id=lead_id,
            variant_index=i,
            subject=suggestion_data.subject,
            body=suggestion_data.body,
            tone=request.tone.value
        )
        db.add(suggestion)
        suggestions.append(suggestion)
    
    db.commit()
    
    # Convert database models to response schema
    from app.schemas.followup import FollowUpSuggestionBase
    suggestion_responses = [
        FollowUpSuggestionBase(
            variant_index=s.variant_index,
            subject=s.subject,
            body=s.body,
            tone=s.tone
        ) for s in suggestions
    ]
    
    # Return the generated suggestions
    return {"suggestions": suggestion_responses}

@router.get("/{lead_id}/followups", response_model=List[FollowUpSuggestionSchema])
def get_followup_suggestions(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all follow-up suggestions for a lead
    """
    # Verify lead exists and belongs to user
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return db.query(FollowUpSuggestion)\
        .filter(FollowUpSuggestion.lead_id == lead_id)\
        .order_by(FollowUpSuggestion.variant_index)\
        .all()

# --- Email Sending Endpoints ---

@router.post(
    "/{lead_id}/send-email",
    response_model=SentEmailSchema,
    status_code=status.HTTP_201_CREATED
)
def send_lead_email(
    lead_id: int,
    email_data: SentEmailCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send an email to a lead and log it
    """
    # Verify lead exists and belongs to user
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Log the email in the database
    sent_email = SentEmailLog(
        user_id=current_user.id,
        lead_id=lead_id,
        to_email=email_data.to_email,
        subject=email_data.subject,
        body=email_data.body,
        provider=email_data.provider
    )
    
    db.add(sent_email)
    
    # Update the lead's last contact date
    lead.next_followup_at = None  # Reset follow-up reminder
    
    db.commit()
    db.refresh(sent_email)
    
    return sent_email

@router.get("/{lead_id}/sent-emails", response_model=List[SentEmailSchema])
def get_lead_sent_emails(
    lead_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all sent emails for a lead
    """
    # Verify lead exists and belongs to user
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return db.query(SentEmailLog)\
        .filter(SentEmailLog.lead_id == lead_id)\
        .order_by(SentEmailLog.sent_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()