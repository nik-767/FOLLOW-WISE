from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import models, schemas
from ..ai.providers import DummyAIProvider

ai_provider = DummyAIProvider()

class LeadService:
    @staticmethod
    def get_leads(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[models.Lead]:
        """Get a list of leads for the current user with optional filtering."""
        query = db.query(models.Lead).filter(
            models.Lead.user_id == user_id,
            models.Lead.is_active == True
        )
        
        if status:
            query = query.filter(models.Lead.status == status)
            
        if search:
            search_filter = (
                (models.Lead.contact_name.ilike(f"%{search}%")) |
                (models.Lead.contact_email.ilike(f"%{search}%")) |
                (models.Lead.company.ilike(f"%{search}%"))
            )
            query = query.filter(search_filter)
            
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_lead(db: Session, lead_id: int, user_id: int) -> Optional[models.Lead]:
        """Get a single lead by ID if it belongs to the user."""
        return db.query(models.Lead).filter(
            models.Lead.id == lead_id,
            models.Lead.user_id == user_id,
            models.Lead.is_active == True
        ).first()
    
    @staticmethod
    def create_lead(db: Session, lead: schemas.LeadCreate, user_id: int) -> models.Lead:
        """Create a new lead for the user."""
        db_lead = models.Lead(
            **lead.dict(),
            user_id=user_id
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    
    @staticmethod
    def update_lead(
        db: Session,
        lead_id: int,
        lead_update: schemas.LeadUpdate,
        user_id: int
    ) -> Optional[models.Lead]:
        """Update an existing lead."""
        db_lead = LeadService.get_lead(db, lead_id, user_id)
        if not db_lead:
            return None
            
        update_data = lead_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lead, field, value)
            
        db_lead.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_lead)
        return db_lead
    
    @staticmethod
    def delete_lead(db: Session, lead_id: int, user_id: int) -> bool:
        """Soft delete a lead."""
        db_lead = LeadService.get_lead(db, lead_id, user_id)
        if not db_lead:
            return False
            
        db_lead.is_active = False
        db_lead.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    async def generate_followup_suggestions(
        db: Session,
        lead_id: int,
        user_id: int,
        context: Optional[str] = None,
        tone: str = "polite"
    ) -> List[schemas.FollowUpSuggestion]:
        """Generate AI follow-up suggestions for a lead."""
        # Get the lead and verify ownership
        lead = LeadService.get_lead(db, lead_id, user_id)
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead not found"
            )
        
        # Prepare lead info for the AI
        lead_info = {
            "contact_name": lead.contact_name,
            "contact_email": lead.contact_email,
            "company": lead.company,
            "last_email_snippet": lead.last_email_snippet,
            "user_name": "Your Name"  # In a real app, this would come from the user's profile
        }
        
        # If no context is provided, use the last email snippet or a default
        if not context and lead.last_email_snippet:
            context = f"Previous interaction: {lead.last_email_snippet}"
        elif not context:
            context = f"Following up with {lead.contact_name} about potential collaboration"
        
        # Generate follow-up variants using the AI provider
        try:
            suggestions = await ai_provider.generate_followup_variants(
                context=context,
                tone=tone,
                lead_info=lead_info
            )
            
            # Save the suggestions to the database
            db_suggestions = []
            for suggestion in suggestions:
                db_suggestion = models.FollowUpSuggestion(
                    lead_id=lead_id,
                    variant_index=suggestion.variant_index,
                    subject=suggestion.subject,
                    body=suggestion.body
                )
                db.add(db_suggestion)
                db_suggestions.append(db_suggestion)
            
            db.commit()
            
            # Convert to Pydantic models for response
            return [
                schemas.FollowUpSuggestion.from_orm(suggestion)
                for suggestion in db_suggestions
            ]
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate follow-up suggestions: {str(e)}"
            )
    
    @staticmethod
    def log_sent_email(
        db: Session,
        user_id: int,
        lead_id: int,
        to_email: str,
        subject: str,
        body: str,
        provider: str = "gmail"
    ) -> models.SentEmailLog:
        """Log a sent email to the database."""
        email_log = models.SentEmailLog(
            user_id=user_id,
            lead_id=lead_id,
            to_email=to_email,
            subject=subject,
            body=body,
            provider=provider
        )
        db.add(email_log)
        db.commit()
        db.refresh(email_log)
        return email_log
