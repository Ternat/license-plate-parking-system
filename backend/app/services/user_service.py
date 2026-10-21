from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from typing import Optional
from app.utils.logger import logger

class UserService:
    """
    Business logic for user management (English function names)
    Handles user creation, authentication, and retrieval
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username
        :param username: Username to query
        :return: User object or None
        """
        return self.db.query(User).filter(User.username == username).first()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user by username and password
        :param username: Username
        :param password: Plain password
        :return: Authenticated user or None
        """
        logger.info(f"Authenticating user: {username}")
        user = self.get_user_by_username(username)
        if not user:
            logger.warning(f"User not found: {username}")
            return None
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {username}")
            return None
        logger.info(f"User authenticated successfully: {username}")
        return user

    def create_user(self, username: str, password: str, is_admin: bool = True) -> User:
        """
        Create new admin user
        :param username: Username
        :param password: Plain password
        :param is_admin: Whether user is admin
        :return: Created user object
        """
        logger.info(f"Creating new user: {username}")
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=is_admin
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User created successfully: {username}")
        return user
user_service = UserService