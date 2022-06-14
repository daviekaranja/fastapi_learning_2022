from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1256@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionaLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependancy
def get_db():
    db = SessionaLocal()
    try:
        yield db
    finally:
        db.close()