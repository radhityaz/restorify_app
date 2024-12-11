# db_config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import urllib.parse

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Konfigurasi koneksi database
DB_USERNAME = os.getenv('DB_USERNAME') or 'root'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'HARUSNYAGIMANATOD123@'  # Ganti dengan password Anda
DB_HOST = os.getenv('DB_HOST') or 'localhost'
DB_PORT = os.getenv('DB_PORT') or '3306'
DB_NAME = os.getenv('DB_NAME') or 'restorify'

# URL-encode password untuk menghindari masalah dengan karakter khusus
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Membuat engine dan session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)