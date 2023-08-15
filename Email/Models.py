from sqlalchemy import Column, Integer, String

from database import Base


class Email(Base):
    __tablename__ = "campaign"
    userId = Column(String(100))
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    location = Column(String(255), nullable=True)
    onsite_remote = Column(String(255), nullable=True)
    duration = Column(String(50), nullable=True)
    contract_type = Column(String(50), nullable=True)
    visa = Column(String(50), nullable=True)
    experience = Column(String(50), nullable=True)
    rate = Column(String(50), nullable=True)
    skills = Column(String(1000))
    email = Column(String(3000))
