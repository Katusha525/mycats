"""A service for working with users"""

import logging
from typing import Optional, Dict
from sqlalchemy.exc import SQLAlchemyError

from database.session import get_session
from database.models import User, Preference

logger = logging.getLogger(__name__)



class UserService:
    """A service for working with users and their preferences"""

    @staticmethod
    def get_or_create_user(chat_id: int, username: Optional[str] = None,
                           first_name: Optional[str] = None,
                           last_name: Optional[str] = None) -> User:
        """Get or create a user"""
        session = get_session()
        try:
            user = session.query(User).filter_by(chat_id=chat_id).first()
            if not user:
                user = User(
                    chat_id=chat_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                )
                session.add(user)
                session.commit()
                logger.info("Created new user with chat_id: %s", chat_id)
            return user
        except SQLAlchemyError as exc:
            logger.error("DB error in get_or_create_user: %s", exc)
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def save_preferences(chat_id: int, preferences: Dict[str, str]) -> None:
        """Save user preferences"""
        session = get_session()
        try:
            user = session.query(User).filter_by(chat_id=chat_id).first()
            if not user:
                # Create a user if not found
                user = User(chat_id=chat_id)
                session.add(user)
                session.flush()

            # Getting or creating preferences
            if user.preferences:
                pref = user.preferences
            else:
                pref = Preference(user_id=user.id)

            # Updating preferences
            pref.size = preferences.get("size")
            pref.activity = preferences.get("activity")
            pref.grooming = preferences.get("grooming")
            pref.friendliness = preferences.get("friendliness")
            pref.shedding = preferences.get("shedding")
            pref.vocalization = preferences.get("vocalization")

            session.add(pref)
            session.commit()
            logger.info("Saved preferences for user: %s", chat_id)
        except SQLAlchemyError as exc:
            logger.error("DB error in save_preferences: %s", exc)
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_user_preferences(chat_id: int) -> Optional[Dict[str, str]]:
        """Get user preferences"""
        session = get_session()
        try:
            user = session.query(User).filter_by(chat_id=chat_id).first()
            if not user or not user.preferences:
                return None

            return {
                "size": user.preferences.size,
                "activity": user.preferences.activity,
                "grooming": user.preferences.grooming,
                "friendliness": user.preferences.friendliness,
                "shedding": user.preferences.shedding,
                "vocalization": user.preferences.vocalization,
            }
        finally:
            session.close()


# An instance of a service for use in other modules
user_service = UserService()