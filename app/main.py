from datetime import datetime
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware







# models.Base.metadata.create_all(bind=engine)
# app object
app = FastAPI()
origins = ['*']
app.add_middleware(CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



# TODO: API STRUCTURE
print('\n')
print('-----' * 20)
print(datetime.now())
app.include_router(post.router) #access to posts
app.include_router(user.router) # access to users
app.include_router(auth.router) #access to authentication
app.include_router(vote.router) #like a post
print('-----' * 20)

@app.get('/')
def hello():
    return 'Hey, my name is Davie Karanja, \n' \
           'Glad you found me. \n' \
           'this is my web API more is coming..'




