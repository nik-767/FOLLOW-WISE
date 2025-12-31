from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class FollowUpTone(str, Enum):
    POLITE = "polite"
    ASSERTIVE = "assertive"
    FRIENDLY = "friendly"

class FollowUpSuggestionBase(BaseModel):
    variant_index: int = Field(..., ge=0, le=2, description="Index of the variant (0-2)")
    subject: str
    body: str

class FollowUpSuggestionCreate(FollowUpSuggestionBase):
    pass

class FollowUpSuggestionUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None

class FollowUpSuggestionInDBBase(FollowUpSuggestionBase):
    id: int
    lead_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FollowUpSuggestion(FollowUpSuggestionInDBBase):
    pass

class FollowUpSuggestionInDB(FollowUpSuggestionInDBBase):
    pass

class FollowUpGenerationRequest(BaseModel):
    context: Optional[str] = None
    tone: FollowUpTone = FollowUpTone.POLITE

class FollowUpGenerationResponse(BaseModel):
    suggestions: List[FollowUpSuggestionBase]
