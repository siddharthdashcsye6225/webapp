from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from database import get_db
from models import User

from typing import Any, Annotated

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models
import schemas
import os

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Return hashed password to be stored directly in db
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


class AuthorizationException(Exception):
    def __init__(self, message="Not authenticated"):
        self.message = message
        super().__init__(self.message)


class DataNotFoundException(Exception):
    def __init__(self, message="Data not found!"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    def __init__(self, message="User Already Exists!"):
        self.message = message
        super().__init__(self.message)


class VerificationException(Exception):
    def __init__(self, message="User verification failed"):
        self.message = message
        super().__init__(self.message)


# authenticate function first checks if username exists and then checks pass, if all good it returns the user
def authenticate(credentials: HTTPBasicCredentials = Depends(security), db=Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user



def verification(creds: Annotated[HTTPBasicCredentials, Depends(security)], db: Session = Depends(get_db)):
    try:
        username = creds.username
        password = creds.password

        # Allow requests through if running on GitHub Actions
        if os.getenv("GITHUB_ACTIONS") == "true":
            # Check username and password but skip verification
            user = user_service.get_user_by_email_Id(username=username, db=db)
            if user is not None and verify_password(password, user.password):
                return user
            else:
                raise AuthorizationException("Incorrect email or password")
        else:
            user = user_service.get_user_by_email_Id(username=username, db=db)
            if user is not None and verify_password(password, user.password):
                # Check if the user is verified in the database
                verification_record = db.query(models.Verification).filter(models.Verification.email == user.username).first()
                if verification_record and verification_record.verified:
                    return user
                else:
                    raise VerificationException("User not verified")
            else:
                raise AuthorizationException("Incorrect email or password")
    except VerificationException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

class userService:
    def get_user_by_email_Id(self, username: str, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            data = db.query(models.User).filter(
                models.User.username == username).first()
            return data
        except SQLAlchemyError as e:
            print(e)
            return None

    def update_user(self, updateUser: schemas.UserCreate, db: Session) -> Any:
        try:
            db_user = db.query(models.User).filter(
                models.User.username == updateUser.username).first()
            hashed_password = hash_password(str(updateUser.password))
            db_user.first_name = updateUser.first_name
            db_user.last_name = updateUser.last_name
            db_user.username = updateUser.username
            db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def create_user(self, user: schemas.UserCreate, db: Session) -> Any:
        """ Get User Data based on email"""
        try:
            hashed_password = hash_password(str(user.password))
            db_user = models.User(username=user.username,
                                  password=hashed_password,
                                  first_name=user.first_name,
                                  last_name=user.last_name,
                                  )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            print(e)
            return None


user_service = userService()