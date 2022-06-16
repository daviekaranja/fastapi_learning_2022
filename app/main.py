from fastapi import Depends, FastAPI, HTTPException, status, Response
from typing import List
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionaLocal, get_db
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# connnecting to the database, pysocpg2
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='1256', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('\n--> Database Connection succesful!\n')
        break
    except Exception as error:
        print('\nconnecting to database failed\n')
        print('Error:', error)
        #try again after 3 seconds
        time.sleep(3)



# TODO: API STRUCTURE
app.include_router(post.router) #access to posts
app.include_router(user.router) # access to users
app.include_router(auth.router) #access to authentication




