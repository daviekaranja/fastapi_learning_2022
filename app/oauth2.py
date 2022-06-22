import time

from jose import JOSEError, jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from dateutil import parser
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# secret key
# algorithm
# expiry_time

SECRET_KEY = settings.secret_key
ALGORITHIM = settings.algorithm
ACCESS_TOKEN_MINUTES = settings.access_token_expire_minutes

# create token
def create_access_token(data: dict):
    to_encode = data.copy() #data to embedd in the token
    # tokens lifespan, after this it wont be valid and api wont allow login
    # TODO: fix server token not expiring
    expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_MINUTES) # had a error where this was not Json serializabe, converted it to a string
    # adding the expiration time to the encoded data
    expires = jsonable_encoder(expires)
    # datetime.strptime(expires)
    to_encode.update({"expire": str(expires)})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)
    # print(to_encode)

    return encoded_jwt

# verify the token
def verify_access_token(token: str, credentials_exception):
    # decode the access token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        # extracting the id from the decoded data
        id: str = payload.get("user_id")
        expires : datetime = payload.get("expire")

        # raise exception if there no id
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #appending the id to the token data
        # token
        #   checking if has the token has an expiration date, raise a http exeception if none
        if expires is None:
            raise credentials_exception
        # converting it to a datetime

        expires = parser.parse(expires)

        # checking if the datetime is expired
        if datetime.now() > expires:
            raise credentials_exception




    # if token not correct
    except JWTError:
        raise credentials_exception
    # return the token data
    return token_data

# returns the current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",headers={"ww-Authenticate": "Bearer"})
    # getting token data
    token = verify_access_token(token, credentials_exception)
    # getting a user by the id which is passed in the token
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # returning the user
    return user