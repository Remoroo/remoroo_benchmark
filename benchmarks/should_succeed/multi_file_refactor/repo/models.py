"""Data models - causes circular import by importing from services."""

from services import validate_email  # BUG: This causes circular import!

class User:
    """User model."""
    
    def __init__(self, username: str, email: str):
        if not validate_email(email):
            raise ValueError(f"Invalid email: {email}")
        self.username = username
        self.email = email
    
    def __repr__(self):
        return f"User({self.username}, {self.email})"

