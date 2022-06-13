from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# post model
class Post(BaseModel):
    title: str
    content: str
    published : bool = True


my_posts = [{'title': 'title of post1', 'content': 'content of post1', 'id': 1}, {'title': 'favourite foods', 'content': 'I like pizza', 'id':2}]


# functions
def Find_post_by_Id(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# TODO: API STRUCTURE

# getting all the posts
@app.get('/posts')
def get_posts():
    return {"data": my_posts}


# creating posts
@app.post("/posts")
def create_post(post:Post):
    # convert the pyadantic model to a python dictionary
    post_dict = post.dict()
    # adding the id
    post_dict["id"] = randrange(0, 100000000)
    # appending it to my posts
    my_posts.append(post.dict)
    # returning the created post
    return {'data': post_dict}


# getting an individual post
@app.get('/posts/{id}')
def get_post(id : int):
    # a function for findind by id
    post = Find_post_by_Id(id)
    # raise an exception if post not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: ({id}) not found!")
    # return post if found
    return {"detail": post}

