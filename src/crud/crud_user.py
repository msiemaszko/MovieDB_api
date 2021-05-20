from typing import List, Optional

from sqlalchemy.orm import Session

from src.auth.auth_handler import hash_password
from src.models.user import User
from src.schemas.user import UserCreateSchema


class CRUDUser:
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        """
        Return user based on primary key
        Returns:
            user: user object
        """
        try:
            return db.query(User).filter(User.id == user_id).first()
        except:
            return None

    def get_user_by_email(self, db: Session, email: str) -> User:
        """Return user based on email"""
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Return list of users with pagination arguments"""
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, new_user: UserCreateSchema) -> User:
        """Create a new users"""
        fake_hashed_password = hash_password(new_user.password)
        db_user = User(
            email=new_user.email,
            full_name=new_user.full_name,
            hashed_password=fake_hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user = CRUDUser()
