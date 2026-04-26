from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Ambil DATABASE_URL dari environment variable
# Lokal: isi di .env
# Railway: otomatis diisi oleh Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Railway kadang kasih URL dengan prefix "postgres://" 
# tapi SQLAlchemy butuh "postgresql://" — ini fix otomatisnya
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency untuk mendapatkan koneksi database di setiap request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()