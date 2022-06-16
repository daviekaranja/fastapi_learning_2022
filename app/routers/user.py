from fastapi import Depends, FastAPI, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

# all users



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_response)
def create_user(user: schemas.Create_user, db: Session = Depends(get_db)):
    # hash the password whch is stored in user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())  # user details, email and password
    db.add(new_user)  # adding to the database
    db.commit()  # saving the database
    db.refresh(new_user)  # returning the new user details
    return new_user


# get user info based on id
@router.get("/{id}", response_model=schemas.User_response)
def get_user(id: int, db: Session = Depends(get_db)):
    # filtering by id
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID:({id}) does not exist")
    return user
