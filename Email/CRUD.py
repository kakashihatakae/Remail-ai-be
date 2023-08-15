from sqlalchemy.orm import Session
from Email import Models
from Email.schemas import JobDescription


def get_one_email(db: Session, email_id: int):
    return db.query(Models.Email).filter_by(id=email_id).first()


def getAllEmails(db: Session, userId: str):
    return db.query(Models.Email).filter_by(userId=userId).all()


def createNewEmail(db: Session, ai_email: str, JobDescription: JobDescription):
    JDDict = JobDescription.__dict__
    new_Email = Models.Email(**JDDict, email=ai_email)
    db.add(new_Email)
    db.commit()
    db.refresh(new_Email)
    return new_Email


def updateEmail(db: Session, email_id: int, regeneratedEmail: str):
    req = db.query(Models.Email).filter_by(id=email_id).first()
    req.email = regeneratedEmail
    db.commit()
    db.refresh(req)
