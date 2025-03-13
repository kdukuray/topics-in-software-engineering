#For sqlite3
from sqlalchemy import Column, Integer, String
from database import Base



#user
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
