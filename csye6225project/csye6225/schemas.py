import datetime
import uuid

from pydantic import BaseModel, EmailStr
from sqlalchemy.sql.sqltypes import UUID

from uuid import UUID


class UUIDModel(BaseModel):
    id: UUID


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    username: EmailStr

    class Config:
        orm_mode = True


class ResponseUser(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    username: EmailStr
    account_created: datetime.datetime
    account_updated: datetime.datetime

    class Config:
        orm_mode = True


class UpdateUserData(BaseModel):
    first_name: str
    last_name: str
    password: str
    username: EmailStr

    class Config:
        # Ensure that extra fields are not allowed
        extra = "forbid"

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=str(obj.id),
            first_name=obj.first_name,
            last_name=obj.last_name,
            username=obj.username,
            account_created=obj.account_created,
            account_updated=obj.account_updated
        )
