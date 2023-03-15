from sqlalchemy import Column, Integer, String, Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "Students"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(23), unique=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    contact= Column(String(10), unique=True, index=True)
    password = Column(String(100))
    address = Column(String(33))

    auth = relationship("DataSecret", back_populates="creator")


class DataSecret(Base):
    __tablename__ = "Secret"

    id = Column(Integer, primary_key=True, index=True)
    jwt = Column(String(255), index= True)
    otp = Column(Integer, index= True)
    created_date =Column(DateTime, default=datetime.utcnow())
    last_updated = Column(DateTime, default=datetime.utcnow())
    studentID = Column(Integer, ForeignKey('Students.id'), unique=True)

    creator= relationship("User", back_populates="auth" )



