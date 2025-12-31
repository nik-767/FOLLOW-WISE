from .user import User
from .lead import Lead
from .followup_suggestion import FollowUpSuggestion
from .sent_email_log import SentEmailLog

# This will ensure all models are imported for SQLAlchemy to register them
__all__ = [
    'User',
    'Lead',
    'FollowUpSuggestion',
    'SentEmailLog',
]
