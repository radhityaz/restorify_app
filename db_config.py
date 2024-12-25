from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Menggunakan SQLite dengan nama file 'restorify.db' (terletak di folder yang sama)
engine = create_engine("sqlite:///restorify.db", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
