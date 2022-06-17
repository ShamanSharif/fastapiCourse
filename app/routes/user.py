from fastapi import status, Depends, Response, APIRouter
from app import schemas, models, utils
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.User)
def fetch_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": f"User with id {id} not found"}
    return user
