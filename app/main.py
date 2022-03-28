from random import randrange
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

try:
    conn = psycopg.connect(
        conninfo="dbname=fastapi_course_db user=shaman password=", row_factory=dict_row)
    print("Connection Established")
except Exception as error:
    print(error)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


posts = [
    {"title": "Initial Post", "content": "Post Content", "id": 1},
    {"title": "Initial Post Two", "content": "Post Content", "id": 2}
]


def get_a_post(id: int):
    for post in posts:
        if(post["id"] == id):
            return post


@app.get('/')
def health_check():
    # health check api
    return {"message": "API health check OK"}


@app.get('/post')
def all_posts():
    posts = conn.execute("""SELECT * FROM posts""").fetchall()
    print(posts)
    return {"posts": posts}


@app.get('/post/{id}', status_code=status.HTTP_302_FOUND)
def get_post(id: int, response: Response):
    # get a post by id
    post = get_a_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"No Post Found For Id {id}", }
    return {"data": post}


@app.post('/post')
def create_post(post: Post):
    # create a post
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    posts.append(post_dict)
    return post.dict()
