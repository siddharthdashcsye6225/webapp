from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/csye6225'

CONFIG_FILE_PATH = '/tmp/database_url.ini'

# Read the SQLAlchemy database URL from the configuration file
if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as f:
        SQLALCHEMY_DATABASE_URL = f.read().strip()
else:
    # Default SQLAlchemy database URL if the configuration file doesn't exist
    SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/csye6225'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

