from typing import Optional

class GmailService:
    def __init__(self):
        # In the future, initialize OAuth creds here
        pass

    def create_oauth_url(self):
        # TODO: Implement real Gmail OAuth
        return "https://accounts.google.com/o/oauth2/auth?..."

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Stub that mimics sending an email.
        In a real app, this would use the Gmail API.
        """
        print(f"\n-------- GMAIL SERVICE (STUB) --------")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:50]}...")
        print(f"------------------------------------\n")
        return True

# Singleton instance
gmail_service = GmailService()