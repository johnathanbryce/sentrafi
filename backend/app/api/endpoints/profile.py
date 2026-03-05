from fastapi import APIRouter, HTTPException, Depends

# db
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.profile import Profile
from app.models.financial_goals import FinancialGoal

# deps
from app.auth.dependencies import get_current_user
from app.database import get_db

# schema
from app.auth.schemas import UserProfileCreate, CreateProfileResponse


router = APIRouter()


@router.post("/profile/create", response_model=CreateProfileResponse, status_code=201)
def create_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user_id = current_user.id

    # check if user already exists, return if so
    does_user_exist = db.query(Profile).filter(Profile.user_id == user_id).first()
    if does_user_exist:
        raise HTTPException(status_code=409, detail="User already exists!")

    # exclude financial goals (separate db table) and create user profile obj with user_id
    user_profile = profile_data.model_dump(exclude={"financial_goals"})
    updated_user_profile = {
        "user_id": user_id,
        **user_profile,
    }
    # create user profile orm obj that aligns with pydantic Profile model
    new_profile = Profile(**updated_user_profile)

    # create financial goals orm obj and add to db
    for goal in profile_data.financial_goals:
        new_goal = FinancialGoal(user_id=user_id, **goal.model_dump())
        db.add(new_goal)

    # commit to db and refresh
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {
        "status": "created",
        "profile": new_profile,
    }
