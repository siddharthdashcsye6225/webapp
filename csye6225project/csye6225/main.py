import uuid
from datetime import datetime
from urllib import response

from fastapi import FastAPI, Body, Depends, HTTPException, Request
import psycopg2
from psycopg2._psycopg import IntegrityError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

import utils
import models
from database import engine, SessionLocal, get_db
from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session
import schemas
from routers import users,health_check

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Uncomment below code snippet later, this is the middleware to check for non configured URLS

'''
class MethodNotAllowedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method != "GET" or request.url.path != "/healthz":
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                headers={"Cache-Control": "no-cache"},
                content=None,
            )
        return await call_next(request)
    
app.add_middleware(MethodNotAllowedMiddleware)

'''


class MethodNotAllowedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        allowed_methods = {
            "/healthz": ["GET"],
            "/v1/user/self": ["GET", "PUT"],
            "/v1/user": ["POST"]
        }

        path = request.url.path
        method = request.method

        if path not in allowed_methods or method not in allowed_methods[path]:
            response_405 = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
            response_405.headers["Cache-Control"] = "no-cache"
            return response_405

        return await call_next(request)


app.add_middleware(MethodNotAllowedMiddleware)

app.include_router(users.router)
app.include_router(health_check.router)




