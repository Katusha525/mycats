"""Setting up a database session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
import config


# Creating the engine and session
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_session():
    """Get a database session"""
    return Session()
