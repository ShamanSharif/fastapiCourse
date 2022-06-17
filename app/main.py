from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# try:
#     conn = psycopg.connect(
#         conninfo="dbname=fastapi_course_db user=shaman password=", row_factory=dict_row)
#     print("Connection Established")
# except Exception as error:
#     print(error)

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def health_check():
    return {"status": "Health Check - Passed"}
