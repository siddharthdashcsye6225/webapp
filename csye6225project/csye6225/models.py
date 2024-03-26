from database import Base
from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import TIMESTAMP, UUID, Boolean
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=func.now())

    # server_default to
    # enforce default value in pg database using now() function

    # IMPORTANT - MAKE SURE TO CONFIGURE UPDATED_AT PARAMETER APPROPRIATELY

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, username={self.username})>"


class Verification(Base):
    __tablename__ = "verification"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=func.now())

    def __repr__(self):
        return f"<Verification(id={self.id}, email={self.email}, verified={self.verified}, created_at={self.created_at})>"
