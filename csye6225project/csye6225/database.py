from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/csye6225'
DEFAULT_DATABASE_URL = 'postgresql://postgres:password@localhost/csye6225'
CONFIG_FILE_PATH = '/tmp/database_url.ini'

# Read the SQLAlchemy database URL from the configuration file
if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as f:
        for line in f:
            # Check if the line starts with the expected prefix
            if line.startswith('SQLALCHEMY_DATABASE_URL='):
                # Extract the URL part of the line
                SQLALCHEMY_DATABASE_URL = line.split('=', 1)[1].strip()
                break
        else:
            # If the line wasn't found, fallback to the default URL
            SQLALCHEMY_DATABASE_URL = DEFAULT_DATABASE_URL
else:
    # If the file doesn't exist, use the default URL
    SQLALCHEMY_DATABASE_URL = DEFAULT_DATABASE_URL

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

