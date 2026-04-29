from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from llm_discovery.core.config import settings

# //////////////////////////////
# SQLAlchemy database setup

# create a database URL using settings from the configuration
DATABASE_URL = f"postgresql://{settings.SYSTEM_DB_USER}:{settings.SYSTEM_DB_PASSWORD}@{settings.SYSTEM_DB_HOST}:{settings.SYSTEM_DB_PORT}/{settings.SYSTEM_DB_NAME}"

# create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# define dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()