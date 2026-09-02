# shortener_app/models.py

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# Define Database Models

# URL Model: maps to the "URLInfo" schema and the "url" table in the database
class URL(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)