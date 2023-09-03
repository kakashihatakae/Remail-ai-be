from sqlalchemy.orm import Session
from Email import Models
from Email.schemas import Campaign


# def updateEmail(db: Session, email_id: int, regeneratedEmail: str):
#     req = db.query(Models.Email).filter_by(id=email_id).first()
#     req.email = regeneratedEmail
#     db.commit()
#     db.refresh(req)


def createCampaign(db: Session, Campaign: Campaign):
    campaignDict = Campaign.__dict__
    newCampaign = Models.Campaign(**campaignDict)
    db.add(newCampaign)
    db.commit()
    db.refresh(newCampaign)
    return newCampaign


def getAllConversations(db: Session, MSUserId: str):
    return db.query(Models.Campaign).filter_by(MSUserId=MSUserId).all()
