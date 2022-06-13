from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


# post model
class Post(BaseModel):
    title: str
    content: str
    published : bool = True


# connnecting to the database, pysocpg2
while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='1256', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('\ndatabase conmnection succesfully\n')
        break
    except Exception as error:
        print('\nconnecting to database failed\n')
        print('Error:', error)
        #try again after 3 seconds
        time.sleep(3)



my_posts = [{'title': 'title of post1', 'content': 'content of post1', 'id': 1},
            {'title': 'favourite foods', 'content': 'I like pizza', 'id':2},
            {'title': 'favourite colors', 'content': 'red, blue, green', 'id': 3}]



# TODO: API STRUCTURE

# getting all the posts
@app.get('/posts')
def get_posts():
    # executing sql command
    cursor.execute("SELECT * FROM posts")
    # getting all the posts
    posts = cursor.fetchall()
    # returning all the posts on the database
    return {"data":posts}


# creating posts
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    """
    Creates new posts and passes it to the database
    """
    cursor.execute("insert into posts (title, content, published) VALUES(%s, %s, %s) Returning *",(
        post.title, post.content, post.published)) 
    #small note for future me,it wasnt working till i used single double quotes on the cursor execute
    new_post = cursor.fetchone() # returns the created post
    conn.commit() #saves changes to the database, commit the changes
    return {'data': new_post}



# getting an individual post
@app.get('/posts/{id}')
def get_post(id : int):
    # executing sql code
    cursor.execute("select * from posts where id = %s", (str(id),))
    # saving the fetched post in a variable
    post = cursor.fetchone()
    # raise error if post not found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID: ({id}) does not exist!")
    # return post if found
    return {"detail": post}


# deleting a post:
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # cut, drop the post from database
    cursor.execute("delete from posts where id = %s returning*", (str(id),))
    deleted_post = cursor.fetchone() #deleted post
    conn.commit() #saving changes to the database
    # raise exception if post not found
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID:(id) does not exist!")
    # return a 204 when deleted
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(post: Post, id:int):
    cursor.execute("update posts set title = %s, set content = %s, set published = %s where id = %s returning*", (post.title, post.content, post.published, str(id),))
    
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID:({id} does not exist!)")
    return {"message": updated_post}