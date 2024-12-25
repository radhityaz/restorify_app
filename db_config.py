# db_config.py

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

# URL database SQLite
DATABASE_URL = "sqlite:///./restorify.db"

# Membuat engine SQLAlchemy
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True  # echo=True untuk debugging
)

# Membuat kelas SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Membuat Base kelas deklaratif
Base = declarative_base()

# Mengaktifkan foreign key constraints di SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
