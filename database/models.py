"""Database models"""

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """Telegram user model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    preferences = relationship("Preference", back_populates="user", uselist=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, chat_id={self.chat_id})"


class Preference(Base):
    """The user's preference model"""

    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    size = Column(String)
    activity = Column(String)
    grooming = Column(String)
    friendliness = Column(String)
    shedding = Column(String)
    vocalization = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"Preference(id={self.id}, user_id={self.user_id})"
