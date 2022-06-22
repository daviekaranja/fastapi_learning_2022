from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# for psycopg2
import time
import psycopg2
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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


# # connnecting to the database, pysocpg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='1256', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('\n--> Database Connection succesful!\n')
#         break
#     except Exception as error:
#         print('\nconnecting to database failed\n')
#         print('Error:', error)
#         #try again after 3 seconds
#         time.sleep(3)
