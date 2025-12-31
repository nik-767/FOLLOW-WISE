from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base

class EmailProvider(str, enum.Enum):
    GMAIL = "gmail"
    SENDGRID = "sendgrid"
    SMTP = "smtp"
    OTHER = "other"

class SentEmailLog(Base):
    __tablename__ = "sent_email_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    provider = Column(Enum(EmailProvider), default=EmailProvider.GMAIL, nullable=False)
    status = Column(String, default="sent", nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sent_emails")
    lead = relationship("Lead", back_populates="sent_emails")
