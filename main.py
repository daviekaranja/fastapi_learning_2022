from fastapi import FastAPI
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


# TODO: API STRUCTURE

# getting all the posts
@app.get('/posts')
def get_posts():
    return {"data": my_posts}


# creating posts
@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post.dict)
    return {'data': post_dict}
