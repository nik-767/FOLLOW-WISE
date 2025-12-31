from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

# Enums
class LeadStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

class LeadSource(str, Enum):
    EMAIL = "email"
    MANUAL = "manual"
    IMPORT = "import"
    OTHER = "other"

# Base schemas
class LeadBase(BaseModel):
    contact_name: str
    contact_email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    source: LeadSource = LeadSource.MANUAL
    last_email_snippet: Optional[str] = None
    lead_score: int = Field(ge=0, le=100, default=0)
    status: LeadStatus = LeadStatus.NEW
    next_followup_at: Optional[datetime] = None
    notes: Optional[str] = None

# Create/Update schemas
class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[LeadSource] = None
    last_email_snippet: Optional[str] = None
    lead_score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[LeadStatus] = None
    next_followup_at: Optional[datetime] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

# Response schemas
class LeadInDBBase(LeadBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Lead(LeadInDBBase):
    pass

class LeadInDB(LeadInDBBase):
    pass

# For listing leads with pagination
class LeadList(BaseModel):
    total: int
    items: List[Lead]
