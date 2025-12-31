from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.models.sent_email_log import SentEmailLog
from app.schemas.sent_email import SentEmail as SentEmailSchema
from app.core.security import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[SentEmailSchema])
def read_all_sent_emails(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(SentEmailLog)\
        .filter(SentEmailLog.user_id == current_user.id)\
        .order_by(SentEmailLog.sent_at.desc())\
        .offset(skip).limit(limit).all()