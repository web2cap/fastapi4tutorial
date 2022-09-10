from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DB_URL = "sqlite+pysqlite:///:memory:"
SQLALCHEMY_DB_URL = "sqlite+pysqlite:///./blog.db"


engine = create_engine(SQLALCHEMY_DB_URL, echo=True, future=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
