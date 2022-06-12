import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

SQLALCHEMY_DATABASE_URL='postgresql://rbivywncdtdppf:ec40827c33c1b54f9204bd60182502c96d63b5e104b33406cb32d1f41b59e1bb@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/db44bsq6ck9o97'
SQLALCHEMY_DATABASE_URL_LOCAL = 'postgresql://postgres:lk1234589@127.0.0.1:5432/Dafttest'

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    print("im in server database")
except:
    print("local_hosting_force")
    engine = create_engine(SQLALCHEMY_DATABASE_URL_LOCAL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
