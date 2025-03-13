#models.py
#For sqlite3
from sqlalchemy import Column, Integer, String
from database import Base


#user
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Added index for faster search
