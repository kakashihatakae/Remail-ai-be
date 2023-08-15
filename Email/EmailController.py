from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from Email import CRUD, AIUtils
from Email.schemas import JobDescription


EmailRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@EmailRouter.post("/new_email")
async def NewEmail(JobDescription: JobDescription, db: Session = Depends(get_db)):
    try:
        ai_email = await AIUtils.generateEmail(JobDescription=JobDescription)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"[Email service]: Couldnt generate an email. Try again. Error: {e}.",
        )

    try:
        new_email = CRUD.createNewEmail(
            db=db, ai_email=ai_email, JobDescription=JobDescription
        )
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"[Email service]: Couldn't add email to DB. Error: {e}.",
        )
    return new_email


# TODO; change to put maybe? Need to edit the email
@EmailRouter.get("/regenerate_email/{email_id}")
async def regenerate_email(email_id: int, db: Session = Depends(get_db)):
    try:
        job_description_db = CRUD.get_one_email(email_id=email_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"[Regenrate email service]: Didn't find email in DB. Try again. Error: {e}.",
        )
    try:
        ai_email = await AIUtils.generateEmail(JobDescription=job_description_db)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"[Email service]: Couldnt regenerate an email. Try again. Error: {e}.",
        )
    CRUD.updateEmail(email_id=email_id, regeneratedEmail=ai_email, db=db)
    return {"ai_email": ai_email}


@EmailRouter.get("/get_all_emails/{userId}")
async def getAllEmails(userId: str, db: Session = Depends(get_db)):
    try:
        all_emails = CRUD.getAllEmails(db=db, userId=userId)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"[Email service]: Couldnt get all emails. Error: {e}.",
        )
    return all_emails


@EmailRouter.get("/get_email/{email_id}")
async def getOneEmail(email_id: int, db: Session = Depends(get_db)):
    try:
        email = CRUD.get_one_email(db=db, email_id=email_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=404,
            detail=f"[Email service]: Please try again, email Id not present. Error: {e}.",
        )
    return email
