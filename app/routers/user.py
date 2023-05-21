from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

"""
    START USERS ROUTES/PATH OPERATIONS
"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Create password hash
    # could be retrieved from: user.password
    hashed_password = utils.hasher(user.password)
    # Store hashed password into user.password
    user.password = hashed_password

    new_user_to_db = models.User(**user.dict())
    db.add(new_user_to_db)
    db.commit()
    db.refresh(new_user_to_db)  # retrieve recently created user and store it in new_user variable
    return new_user_to_db


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not exist")

    return user

"""
    END USERS ROUTES/PATH OPERATIONS
"""