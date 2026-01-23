"""Services - imports from models, creating circular dependency."""

from models import User  # This import combined with models importing from services = circular!

def validate_email(email: str) -> bool:
    """Validate an email address."""
    return "@" in email and "." in email.split("@")[1]

class UserService:
    """Service for user operations."""
    
    def __init__(self):
        self.users = []
    
    def register(self, user: User):
        """Register a new user."""
        self.users.append(user)
        print(f"Registered user: {user}")
    
    def send_welcome_email(self, user: User):
        """Send welcome email to user."""
        print(f"Sending welcome email to {user.email}")

