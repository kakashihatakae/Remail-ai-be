from pydantic import BaseModel
from typing import Union


class IntroEmailInfo(BaseModel):
    vendorName: str
    vendorCompany: str
    vendorEmail: str
    senderName: Union[str, None] = None
    senderCompany: Union[str, None] = None
    senderEmail: Union[str, None] = None


class PersionInfo(BaseModel):
    name: str
    address: str


class ReplyEmailInfo(BaseModel):
    prevBodySent: str
    prevSender: Union[PersionInfo, None] = None
    meetingLink: Union[str, None] = None
    isMeFollowUp: bool
    extraNotes: Union[str, None] = None


class Campaign(BaseModel):
    MSUserId: str
    MSConversationId: str
    vendorName: str
    vendorCompany: str
    vendorEmail: str
