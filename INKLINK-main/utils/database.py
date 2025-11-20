import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING")

if not AZURE_SQL_CONNECTION_STRING:
    raise ValueError("Falta la variable de entorno AZURE_SQL_CONNECTION_STRING")

engine = create_engine(
    AZURE_SQL_CONNECTION_STRING,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependencia para FastAPI que entrega una sesión de BD por request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()