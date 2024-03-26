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
from starlette.responses import Response
import os
import utils
import models
from database import engine, SessionLocal, get_db
from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session
import schemas
from logger import webapp_logger
import pubsub


router = APIRouter(tags=['public'])


@router.get("/healthz", status_code=status.HTTP_200_OK)
async def healthz(request: Request, db: Session = Depends(get_db)):
    if await request.body() or request.query_params:
        webapp_logger.error("Invalid request received for healthz endpoint")
        response_400 = Response(status_code=status.HTTP_400_BAD_REQUEST)
        response_400.headers["Cache-Control"] = "no-cache"
        return response_400
    try:
        query = text("SELECT 1")
        db.execute(query)
        webapp_logger.info("Database connectivity check succeeded")
        response_200 = Response(status_code=status.HTTP_200_OK)
        response_200.headers["Cache-Control"] = "no-cache"
        return response_200
    except Exception as e:
        webapp_logger.error(f"Database connectivity check failed: {e}")
        response_503 = Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        response_503.headers["Cache-Control"] = "no-cache"
        return response_503


@router.put("/healthz", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("PUT method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


@router.post("/healthz", status_code=405)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("POST method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


@router.delete("/healthz", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("DELETE method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


@router.patch("/healthz", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("PATCH method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


@router.head("/healthz", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("HEAD method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


@router.options("/healthz", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
def healthz(request: Request, db: Session = Depends(get_db)):
    webapp_logger.error("OPTIONS method not allowed for healthz endpoint")
    response = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    response.headers["Cache-Control"] = "no-cache"
    return response


# USER CREATION
#
# FOR NOW THIS CODE IGNORES RANDOM FIELD AND CREATES USERS ANYWAYS
@router.post("/v1/user", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        webapp_logger.error("Failed to create user: Username already exists", extra={"user_id": existing_user.id})
        # If the username already exists, raise an HTTPException with status code 400 and an error message
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass

    new_user = models.User(
        id=uuid.uuid4(),
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        password=user.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    webapp_logger.info("User created successfully", extra={"user_id": new_user.id})

    if os.getenv("GITHUB_ACTIONS") == "true" or os.getenv("CI") == "true":
        webapp_logger.info("Skipping Pub/Sub message publishing because running in GitHub Actions")
        return schemas.ResponseUser(
            id=new_user.id,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            username=new_user.username,
            account_created=new_user.created_at,
            account_updated=new_user.updated_at
        )

        # Publish message to Pub/Sub topic
    pubsub_message = {
        "user_id": str(new_user.id),
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "created_at": str(new_user.created_at),
        "updated_at": str(new_user.updated_at)
    }
    pubsub.publish_message_to_pubsub("dev-siddharth-dash-csye6225", "verify_email", pubsub_message)

    return schemas.ResponseUser(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        username=new_user.username,
        account_created=new_user.created_at,
        account_updated=new_user.updated_at
    )
