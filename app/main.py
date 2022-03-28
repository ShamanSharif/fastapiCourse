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


@app.get('/')
def health_check():
    # health check api
    return {"message": "API health check OK"}


@app.get('/post')
def all_posts():
    posts = conn.execute("""SELECT * FROM posts""").fetchall()
    return {"posts": posts}


@app.get('/post/{id}', status_code=status.HTTP_302_FOUND)
def get_post(id: int, response: Response):
    # get a post by id
    post = conn.execute(
        """SELECT * FROM posts WHERE id = %s""", (str(id),)).fetchone()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"No Post Found For Id {id}", }
    return {"data": post}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = conn.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                        (post.title, post.content, post.published,)).fetchone()
    conn.commit()
    return {"data": post}
