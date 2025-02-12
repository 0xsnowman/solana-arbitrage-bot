from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.session import get_db
from app.db.crud import get_user_by_email
from app.core.config import settings
from app.schemas.user import UserResponse

# Dependency to get the database session
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user from the token
def get_current_user(token: str, db: Session = Depends(get_db_session)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    
    return user
