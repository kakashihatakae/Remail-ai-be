import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from Email import CRUD, AIUtils
from Email.schemas import IntroEmailInfo, Campaign


EmailRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Divide email creation into
# 1. Intro generation
# generate intro and create draft on FE side
# 2. save email
# if sending is successful on FE then save the email on BE side
@EmailRouter.post("/new-email-intro")
async def CreateNewEmail(IntroEmailInfo: IntroEmailInfo):
    ai_email_string = await AIUtils.generateIntroEmail(IntroEmailInfo)
    return json.loads(ai_email_string, strict=False)


# @EmailRouter.post("/new_email")
# async def NewEmail(JobDescription: JobDescription, db: Session = Depends(get_db)):
#     try:
#         ai_email = await AIUtils.generateEmail(JobDescription=JobDescription)
#     except Exception as e:
#         raise HTTPException(
#             status_code=400,
#             detail=f"[Email service]: Couldnt generate an email. Try again. Error: {e}.",
#         )

#     try:
#         new_email = CRUD.createNewEmail(
#             db=db, ai_email=ai_email, JobDescription=JobDescription
#         )
#     except Exception as e:
#         db.rollback()

#         raise HTTPException(
#             status_code=400,
#             detail=f"[Email service]: Couldn't add email to DB. Error: {e}.",
#         )
#     return new_email


@EmailRouter.post("/campaign")
async def createNewCampaign(
    campaign: Campaign,
    db: Session = Depends(get_db),
    status_code=201,
):
    try:
        CRUD.createCampaign(db=db, Campaign=campaign)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail=f"[Email service]: Wasn't able to create new campaign. Error: {e}.",
        )


@EmailRouter.get("/campaign/{MSUserId}")
async def getAllCampaigns(MSUserId: str, db: Session = Depends(get_db)):
    campaigns = []
    try:
        campaigns = CRUD.getAllConversations(db=db, MSUserId=MSUserId)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"[Email service]: Wasn't able to create new campaign. Error: {e}.",
        )
    return campaigns
