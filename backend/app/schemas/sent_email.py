from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class EmailProvider(str, Enum):
    GMAIL = "gmail"
    SENDGRID = "sendgrid"
    SMTP = "smtp"
    OTHER = "other"

class SentEmailBase(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    provider: EmailProvider = EmailProvider.GMAIL
    lead_id: int

class SentEmailCreate(SentEmailBase):
    pass

class SentEmailUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    provider: Optional[EmailProvider] = None

class SentEmailInDBBase(SentEmailBase):
    id: int
    user_id: int
    sent_at: datetime

    class Config:
        from_attributes = True

class SentEmail(SentEmailInDBBase):
    pass

class SentEmailInDB(SentEmailInDBBase):
    pass

class SentEmailList(BaseModel):
    total: int
    items: List[SentEmail]
