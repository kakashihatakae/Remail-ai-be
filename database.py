import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# change URL
# SQLALCHEMY_DATABASE_URL = (
#     "mysql+pymysql://root:password@localhost:3306/schooldb?charset=utf8mb4"
# )
SQLALCHEMY_DATABASE_URL = os.getenv("PDB_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
