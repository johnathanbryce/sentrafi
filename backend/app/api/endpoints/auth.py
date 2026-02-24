from fastapi import APIRouter, HTTPException, Request, Body, Depends
from fastapi.responses import JSONResponse

# db
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

# utils
from app.auth.jwt import create_access_token, decode_access_token
from app.auth.security import hash_password, verify_password

# schema
from app.auth.schemas import UserCreate, UserResponse


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # check if email is already taken
    email_exists = db.query(User).filter(User.email == user_data.email).first()
    if email_exists:
        raise HTTPException(status_code=409, detail="User already exists in SentraFi")
    # if not, proceed and hash password and save the new user to postgres
    hashed_pword = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_pword)

    # commit to db and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
