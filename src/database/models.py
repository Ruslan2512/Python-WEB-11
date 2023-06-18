from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    fullname = Column(String, primary_key=True, index=True)
    lastname = Column(String, index=True)
    email = Column(String)
    phone_number = Column(String)
    birthday = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

