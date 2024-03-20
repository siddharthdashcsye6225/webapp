import uuid
from datetime import datetime
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

@router.get('/v1/user/self', response_model=schemas.ResponseUser)
def get_user(user: Annotated[schemas.ResponseUser, Depends(utils.verification)], db: Session = Depends(get_db)):
    try:
        user = utils.user_service.get_user_by_email_Id(username=user.username, db=db)
        print(user)
        if not user:
            raise utils.DataNotFoundException(f"User with email: {id} Not Found!")
        webapp_logger.info("User retrieved successfully", extra={"user_id": user.id,"taskName": "User Retrieval"})
        return schemas.ResponseUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            account_created=user.created_at,
            account_updated=user.updated_at
        )
    except utils.DataNotFoundException as e:
        webapp_logger.error(f"Failed to retrieve user: {e}",extra={"taskName": "User Retrieval"})
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        webapp_logger.error(f"Failed to retrieve user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


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

        if updateUser.username == current_user.username:
            utils.user_service.update_user(updateUser=updateUser, db=db)
            webapp_logger.info("User updated successfully", extra={"user_id": current_user.id,"taskName": "User Update"})
        else:
            raise HTTPException(status_code=400,
                                detail=f"User with {current_user.username} not authorized to perform requested action "
                                       f"/ not allowed to change username")

    except utils.DataNotFoundException as e:
        webapp_logger.error(f"Failed to update user: {e}",extra={"taskName": "User Update"})
        raise HTTPException(status_code=404, detail=str(e))

    except ValidationError as e:
        webapp_logger.error(f"Failed to update user: {e}",extra={"taskName": "User Update"})
        raise HTTPException(status_code=400, detail="Invalid request body")

    except Exception as e:
        webapp_logger.error(f"Failed to update user: {e}",extra={"taskName": "User Update"})
        raise HTTPException(status_code=400)

