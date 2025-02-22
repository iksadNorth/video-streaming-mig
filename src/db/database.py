from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from src.config import config


PG_USERNAME = config('PG_USERNAME')
PG_PASSWORD = config('PG_PASSWORD')
PG_DATABASE = config('PG_DATABASE')
PG_HOST     = config('PG_HOST')

DATABASE_URL = f"postgresql+psycopg2://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    finally:
        db.close()