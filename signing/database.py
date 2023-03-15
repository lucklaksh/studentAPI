from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:password@localhost:3306/curd")
SessionLocal = sessionmaker(bind=engine,autoflush=False)
Base= declarative_base()

def db_get():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

