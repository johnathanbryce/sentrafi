from fastapi import APIRouter, HTTPException, Depends

# db
from sqlalchemy.orm import Session
from app.models.user import User

# utils
from app.auth.jwt import create_access_token
from app.auth.security import hash_password, verify_password

# deps
from app.auth.dependencies import get_current_user
from app.database import get_db

# schema
from app.auth.schemas import UserCreate, UserResponse, UserLogin, Token


router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


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


@router.post("/login", response_model=Token, status_code=200)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # check if user exists via email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="User does not exist. Please register."
        )
    # verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    # user verified, create jwt access token
    jwt_token = create_access_token(str(user.id))
    return {"access_token": jwt_token, "token_type": "bearer"}
