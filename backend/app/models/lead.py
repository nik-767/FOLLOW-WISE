from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class LeadStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

class LeadSource(str, enum.Enum):
    EMAIL = "email"
    MANUAL = "manual"
    IMPORT = "import"
    OTHER = "other"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False, index=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(Enum(LeadSource), default=LeadSource.MANUAL, nullable=False)
    last_email_snippet = Column(Text, nullable=True)
    lead_score = Column(Integer, default=0, nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    next_followup_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="leads")
    followup_suggestions = relationship("FollowUpSuggestion", back_populates="lead", cascade="all, delete-orphan")
    sent_emails = relationship("SentEmailLog", back_populates="lead", cascade="all, delete-orphan")
