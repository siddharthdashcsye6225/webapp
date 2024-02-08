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
from  database import engine, SessionLocal, get_db
from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session
import schemas
from typing import Annotated

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
        return schemas.ResponseUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            account_created=user.created_at,
            account_updated=user.updated_at
        )
    except utils.DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/v1/user/self", status_code=204)
def update_user(updateUser: schemas.UserCreate,
                current_user: Annotated[schemas.ResponseUser, Depends(utils.verification)],
                db: Session = Depends(get_db)):
    try:
        if updateUser.username == current_user.username:
            utils.user_service.update_user(updateUser=updateUser, db=db)
        else:
            raise HTTPException(status_code=403,
                                detail=f"User with {current_user.username} not authorized to perform requested action")

    except utils.DataNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal Server Error')
