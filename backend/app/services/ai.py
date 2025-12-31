"""
This module was the older duplicate AI service implementation and has been
consolidated into ``app.ai.providers``. Importing this module will raise an
ImportError to prevent accidental usage of the deprecated implementation.
"""

raise ImportError(
    "The module app.services.ai has been removed. Use app.ai.providers.get_ai_provider instead."
)
