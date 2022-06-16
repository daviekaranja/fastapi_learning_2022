from fastapi import Depends, FastAPI, HTTPException, status, Response, APIRouter
from .. import models, schemas, utils, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['Posts'])


# getting all the posts
@router.get('/', response_model=List[schemas.Post_response])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    """
    gets and returns all the posts from the database
    :return: posts
    """
    # # executing sql command
    # cursor.execute("SELECT * FROM posts")
    # # getting all the posts
    # posts = cursor.fetchall()
    # # returning all the posts on the database
    # with sqlalchemy
    posts = db.query(models.Post).all()  # getting all the posts
    return posts


# creating posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post_response)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Creates new posts, saves and returns the new post
    """
    # cursor.execute("insert into posts (title, content, published) VALUES(%s, %s, %s) Returning *",(
    #     post.title, post.content, post.published))
    # #small note for future me,it wasnt working till i used single double quotes on the cursor execute
    # new_post = cursor.fetchone() # returns the created post
    # conn.commit() #saves changes to the database, commit the changes
    # with sqlalchemy
    new_post = models.Post(**post.dict())  # unpacking the pydantic model to a python dictionary with all the fields
    # adding to the database
    db.add(new_post)
    # saving the changes
    db.commit()
    # returning the created post
    db.refresh(new_post)
    # return statement
    return new_post


# getting an individual post
@router.get('/{id}', response_model=schemas.Post_response)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    """
    searches for a matching pose from the passed id
    :param id:
    :return: matching post
    """
    # # executing sql code
    # cursor.execute("select * from posts where id = %s", (str(id),))
    # # saving the fetched post in a variable
    # post = cursor.fetchone()
    # # raise error if post not found
    # with sqlalchemy
    post = db.query(models.Post).filter(models.Post.id == id).first()  # gets the first post that matches the passed id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: ({id}) does not exist!")
    # return post if found
    return post


# deleting a post:
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    deletes a post from the database, searches for the posts matching the id passed
    :param id:
    :return:
    """
    # # cut, drop the post from database
    # cursor.execute("delete from posts where id = %s returning*", (str(id),))
    # deleted_post = cursor.fetchone() #deleted post
    # conn.commit() #saving changes to the database
    # raise exception if post not found
    post = db.query(models.Post).filter(models.Post.id == id)  # matching a post with supplied id

    if post.first() == None:  # checking if the first post matches the id
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID:({id}) does not exist!")
    # deleting the post
    post.delete(synchronize_session=False)
    # saving the changes to the database
    db.commit()
    # return a 204 when deleted
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating posts
@router.put("/{id}", response_model=schemas.Post_response)
def update_post(updated_post: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("update posts set title = %s, content = %s, published = %s where id = %s returning*",
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # raise a 404 if not found
    # with sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID:({id} does not exist!)")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # return the updated post
    return post_query.first()
