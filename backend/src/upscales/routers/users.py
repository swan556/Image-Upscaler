from fastapi import APIRouter, status, Depends, Response, HTTPException
from src.upscales.database import get_db
from src.upscales.schemas import *
from sqlalchemy.orm import Session
from src.upscales import models

router = APIRouter(
    tags= ["user"],
    prefix="/user"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: User, db: Session= Depends(get_db)):
    new_user = models.User(
        name = request.username,
        email = request.email,
        password = request.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
def show_user(id, response: Response, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} not found"
        )
    return user

