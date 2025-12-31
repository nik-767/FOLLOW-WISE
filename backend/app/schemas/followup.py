from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class FollowUpTone(str, Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"
    FRIENDLY = "friendly"

class FollowUpSuggestionBase(BaseModel):
    variant_index: int = Field(..., ge=0, le=2)  # 0, 1, or 2 for the 3 variants
    subject: str
    body: str
    tone: FollowUpTone

class FollowUpSuggestionCreate(FollowUpSuggestionBase):
    pass

class FollowUpSuggestionUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    tone: Optional[FollowUpTone] = None

class FollowUpSuggestionInDBBase(FollowUpSuggestionBase):
    id: int
    lead_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FollowUpSuggestion(FollowUpSuggestionInDBBase):
    pass

class FollowUpSuggestionInDB(FollowUpSuggestionInDBBase):
    pass

class FollowUpGenerateRequest(BaseModel):
    context: Optional[str] = None
    tone: FollowUpTone = FollowUpTone.POLITE

class FollowUpGenerateResponse(BaseModel):
    suggestions: List[FollowUpSuggestionBase]

class SentEmailBase(BaseModel):
    to_email: str
    subject: str
    body: str
    provider: str = "gmail"
    status: str = "sent"

class SentEmailCreate(SentEmailBase):
    lead_id: Optional[int] = None

class SentEmailInDBBase(SentEmailBase):
    id: int
    user_id: int
    lead_id: Optional[int]
    sent_at: datetime

    class Config:
        orm_mode = True

class SentEmail(SentEmailInDBBase):
    pass

class SentEmailInDB(SentEmailInDBBase):
    pass

class SentEmailList(BaseModel):
    total: int
    items: List[SentEmail]
