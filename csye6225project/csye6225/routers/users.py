import uuid
from datetime import datetime, timedelta, timezone
from urllib import response

from fastapi import FastAPI, Body, Depends, HTTPException, Request, APIRouter
import psycopg2
from psycopg2._psycopg import IntegrityError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import utils
import models
from database import engine, SessionLocal, get_db

from sqlalchemy import create_engine, exc, text, false
from sqlalchemy.orm import Session
import schemas
from typing import Annotated
from logger import webapp_logger

router = APIRouter(tags=['authenticated'])

# Adding comment to test
# Get back to this later, this function can't figure out which user details to fetch for


'''def verify_user_status(username: str = Depends(utils.get_current_username), db: Session = Depends(SessionLocal)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=401, detail="User not verified or verification link expired")
    return user
'''


# Define a new endpoint for handling verification link clicks
@router.get("/v1/user/verification/{verification_id}")
def verify_email(verification_id: str, db: Session = Depends(get_db)):
    # Retrieve verification record from the database
    verification_record = db.query(models.Verification).filter(models.Verification.id == verification_id).first()
    if not verification_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verification link not found")

    # Check if the verification link has expired
    now = datetime.now(timezone.utc)
    time_difference = now - verification_record.created_at.replace(tzinfo=timezone.utc)
    if time_difference > timedelta(minutes=2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification link has expired")

    # Update the verification status to True
    verification_record.verified = True
    db.commit()

    return {"message": "Email verified successfully"}


@router.get('/v1/user/self', response_model=schemas.ResponseUser)
def get_user(user: Annotated[schemas.ResponseUser, Depends(utils.verification)], db: Session = Depends(get_db)):
    try:
        # Your existing code to retrieve user data
        user_data = utils.user_service.get_user_by_email_Id(username=user.username, db=db)
        if not user_data:
            raise utils.DataNotFoundException(f"User with email: {id} Not Found!")

        # Your existing code to return user data
        return schemas.ResponseUser(
            id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            account_created=user_data.created_at,
            account_updated=user_data.updated_at
        )
    except utils.VerificationException as e:
        # Handle VerificationException
        raise HTTPException(status_code=403, detail=str(e))
    except utils.DataNotFoundException as e:
        # Handle DataNotFoundException
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=404, detail="Failed to Retrieve User")


@router.put("/v1/user/self", status_code=204)
def update_user(updateUser: schemas.UpdateUserData,
                current_user: Annotated[schemas.ResponseUser, Depends(utils.verification)],
                db: Session = Depends(get_db)):
    try:
        # Validate the request body against the Pydantic schema
        updateUser_data = updateUser.model_dump()
        schemas.UpdateUserData(**updateUser_data)

        invalid_fields = set(updateUser.model_dump().keys()) - {"first_name", "last_name", "password", "username"}
        if invalid_fields:
            raise HTTPException(status_code=400, detail=f"Invalid fields provided: {', '.join(invalid_fields)}")

        # Update the user
        utils.user_service.update_user(updateUser=updateUser, db=db)
        webapp_logger.info("User updated successfully", extra={"user_id": current_user.id})

    except utils.VerificationException as e:
        # Handle VerificationException
        raise HTTPException(status_code=403, detail=str(e))

    except utils.DataNotFoundException as e:
        # Handle DataNotFoundException
        webapp_logger.error(f"Failed to update user: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    except ValidationError as e:
        # Handle ValidationError
        webapp_logger.error(f"Failed to update user: {e}")
        raise HTTPException(status_code=400, detail="Invalid request body")

    except Exception as e:
        # Handle other exceptions
        webapp_logger.error(f"Failed to update user: {e}")
        raise HTTPException(status_code=400)
