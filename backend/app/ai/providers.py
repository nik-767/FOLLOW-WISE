from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..schemas.followup_suggestion import FollowUpTone, FollowUpSuggestionBase
import logging

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Abstract base class for AI providers that generate follow-up suggestions."""
    
    @abstractmethod
    async def generate_followup_variants(
        self,
        context: str,
        tone: FollowUpTone = FollowUpTone.POLITE,
        lead_info: Optional[Dict[str, Any]] = None,
        previous_interactions: Optional[List[Dict[str, Any]]] = None
    ) -> List[FollowUpSuggestionBase]:
        """
        Generate follow-up email variants based on the given context and tone.
        
        Args:
            context: The context for the follow-up email
            tone: The desired tone for the follow-up
            lead_info: Optional information about the lead
            previous_interactions: Optional list of previous interactions with this lead
            
        Returns:
            List of follow-up suggestions (typically 3 variants)
        """
        pass

class DummyAIProvider(AIProvider):
    """Dummy implementation of AIProvider for testing and development."""
    
    async def generate_followup_variants(
        self,
        context: str,
        tone: FollowUpTone = FollowUpTone.POLITE,
        lead_info: Optional[Dict[str, Any]] = None,
        previous_interactions: Optional[List[Dict[str, Any]]] = None
    ) -> List[FollowUpSuggestionBase]:
        """Generate dummy follow-up email variants."""
        logger.info(f"Generating {tone} follow-up variants with context: {context[:100]}...")
        
        # Sample follow-up templates based on tone
        templates = {
            FollowUpTone.POLITE: {
                "subjects": [
                    "Following up on our recent conversation",
                    "Just checking in",
                    "Reconnecting regarding your interest"
                ],
                "bodies": [
                    "Dear {name},\n\nI hope this message finds you well. I'm following up on our recent conversation about {context}. I wanted to check if you had any questions or if there's anything else I can assist you with.\n\nBest regards,\n{user_name}",
                    "Hello {name},\n\nI wanted to follow up regarding {context}. Please let me know if you've had a chance to review the information I sent. I'm happy to provide any additional details you might need.\n\nBest regards,\n{user_name}",
                    "Hi {name},\n\nI hope you're doing well. I'm reaching out to see if you've had any thoughts about {context} since we last spoke. I'm here to help with any questions you might have.\n\nKind regards,\n{user_name}"
                ]
            },
            FollowUpTone.ASSERTIVE: {
                "subjects": [
                    "Action required: Follow-up on our discussion",
                    "Time-sensitive: Need your input",
                    "Following up: Next steps"
                ],
                "bodies": [
                    "{name},\n\nI'm following up on our discussion about {context}. To move forward, I'll need your response by {deadline}. Please let me know if you have any questions.\n\nRegards,\n{user_name}",
                    "{name},\n\nThis is a follow-up regarding {context}. I need to hear back from you by {deadline} to proceed. Let me know if you need any clarification.\n\nBest,\n{user_name}",
                    "{name},\n\nI'm reaching out again about {context}. Your input is needed to take the next steps. Please respond by {deadline}.\n\nThanks,\n{user_name}"
                ]
            },
            FollowUpTone.FRIENDLY: {
                "subjects": [
                    "Hey {first_name}! Just checking in",
                    "Following up on {context}",
                    "Quick update on our conversation"
                ],
                "bodies": [
                    "Hey {first_name}!\n\nI was just thinking about our conversation about {context} and wanted to check in. How's it going? Let me know if you've had any thoughts or questions!\n\nCheers,\n{user_name}",
                    "Hi {first_name}!\n\nHope you're having a great week! I wanted to follow up on {context}. Any updates on your end?\n\nBest,\n{user_name}",
                    "{first_name}!\n\nQuick note to follow up about {context}. Let me know what you think when you get a chance!\n\nTalk soon,\n{user_name}"
                ]
            }
        }
        
        # Get the appropriate templates based on tone
        tone_templates = templates.get(tone, templates[FollowUpTone.POLITE])
        
        # Prepare context variables
        first_name = (lead_info or {}).get('contact_name', '').split(' ')[0] if lead_info and 'contact_name' in lead_info else 'there'
        user_name = (lead_info or {}).get('user_name', 'Your FollowWise Team')
        deadline = (datetime.now() + timedelta(days=3)).strftime('%A, %B %d')
        
        # Generate the three variants
        variants = []
        for i in range(3):
            subject = tone_templates["subjects"][i % len(tone_templates["subjects"])]
            body = tone_templates["bodies"][i % len(tone_templates["bodies"])]
            
            # Format the template with context
            formatted_subject = subject.format(
                first_name=first_name,
                context=context[:50] + ('...' if len(context) > 50 else ''),
                deadline=deadline
            )
            
            formatted_body = body.format(
                name=lead_info.get('contact_name', 'there') if lead_info else 'there',
                first_name=first_name,
                context=context,
                deadline=deadline,
                user_name=user_name
            )
            
            variants.append(FollowUpSuggestionBase(
                variant_index=i,
                subject=formatted_subject,
                body=formatted_body,
                tone=tone
            ))
        
        return variants


# Dependency provider function for FastAPI DI
def get_ai_provider() -> AIProvider:
    """
    Return an AIProvider instance. In production this could be configured
    to return different provider implementations based on settings.
    """
    return DummyAIProvider()
