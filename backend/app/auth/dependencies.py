from app.auth.jwt import decode_access_token
from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

# db
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Dependency to retrieve and verify the current user from the request.

    Raises:
        HTTPException: If the user is not authenticated or user info is missing.

    Returns:
        dict: identified user information
    """

    if not token:
        raise HTTPException(
            status_code=401, detail="User does not have a Bearer Token."
        )

    # grab auth header & decode
    try:

        decoded_token = decode_access_token(token)

        user_id = decoded_token["sub"]
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID not found in token")

        # look up user in database via sub
        identified_user = db.query(User).filter(User.id == user_id).first()

        return identified_user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Expired or invalid token.")
