from fastapi import FastAPI, status, Depends, Response
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# try:
#     conn = psycopg.connect(
#         conninfo="dbname=fastapi_course_db user=shaman password=", row_factory=dict_row)
#     print("Connection Established")
# except Exception as error:
#     print(error)


@app.get('/')
def health_check():
    # health check api
    return {"message": "API health check OK"}


@app.get('/orm')
def orm_health_check(db: Session = Depends(get_db)):
    return {"message": "API health check OK"}


@app.get('/post')
def all_posts(db: Session = Depends(get_db)):
    # posts = conn.execute("""SELECT * FROM posts""").fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get('/post/{id}', status_code=status.HTTP_302_FOUND)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # get a post by id
    # post = conn.execute(
    #     """SELECT * FROM posts WHERE id = %s""", (str(id),)).fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"No Post Found For Id {id}", }
    return post


@app.post('/post', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # post = conn.execute(
    #     """INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published,)).fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put('/post/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post:  schemas.CreatePost, response: Response, db: Session = Depends(get_db)):
    # post = conn.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s
    #     WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id),)).fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"Post with id {id} not found"}

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    # post = conn.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)).fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"Post with id {id} not found"}
    # conn.commit()
    post = post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Post Id {id} was successfully deleted"}
