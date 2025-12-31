from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class FollowUpSuggestion(Base):
    __tablename__ = "followup_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    variant_index = Column(Integer, nullable=False)  # 0, 1, or 2 for the three variants
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    tone = Column(String, nullable=False)
    
    # Relationships
    lead = relationship("Lead", back_populates="followup_suggestions")
