from sqlalchemy import Column, Integer, String

from database import Base


class Campaign(Base):
    __tablename__ = "Campaign"
    id = Column(Integer, primary_key=True, autoincrement=True)
    MSUserId = Column(String(50))
    MSConversationId = Column(String(100))
    vendorName = Column(String(50))
    vendorCompany = Column(String(50))
    vendorEmail = Column(String(50))
