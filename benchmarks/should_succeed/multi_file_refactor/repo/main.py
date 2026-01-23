"""Main entry point - has circular import issues."""

from models import User
from services import UserService

def main():
    # Create a user
    user = User("alice", "alice@example.com")
    
    # Use the service
    service = UserService()
    service.register(user)
    service.send_welcome_email(user)
    
    print("All operations completed successfully!")

if __name__ == "__main__":
    main()

