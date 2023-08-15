from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from Email import Models
from Email.EmailController import EmailRouter

app = FastAPI()

# change this to allow access frontent
origins = [
    "https://remail-ai-fe-d6c47adb68c1.herokuapp.com",
    "https://www.careersasha.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://www.careersasha.com/*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=EmailRouter)
Models.Base.metadata.create_all(bind=engine)
