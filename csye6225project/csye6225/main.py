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

allowed_routes = {
    "/v1/user/self": ["GET", "PUT"],
    "/v1/user": ["POST"],
    "/healthz": ["GET", "PUT", "POST", "DELETE", "PATCH", "HEAD", "OPTIONS"]
}

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
    def __init__(self, app, allowed_routes):
        super().__init__(app)
        self.allowed_routes = allowed_routes

    async def dispatch(self, request: Request, call_next):
        # Check if the requested path and method are allowed
        path = request.url.path
        method = request.method

        if path in self.allowed_routes and method not in self.allowed_routes[path]:
            response_405 = Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
            response_405.headers["Cache-Control"] = "no-cache"
            return response_405

        return await call_next(request)


app.add_middleware(MethodNotAllowedMiddleware, allowed_routes=allowed_routes)


app.include_router(users.router)
app.include_router(health_check.router)




