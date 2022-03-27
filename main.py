from random import randrange
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    report: Optional[int] = None


posts = [
    {"title": "Initial Post", "content": "Post Content", "id": 1},
    {"title": "Initial Post Two", "content": "Post Content", "id": 2}
]


@app.get('/')
def health_check():
    return {"message": "API health check OK"}


@app.get('/post')
def all_posts():
    return {"posts": posts}


@app.post('/post')
def test_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    posts.append(post_dict)
    return post.dict()
