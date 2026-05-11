import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Bulut veritabanı adresi (Neon/Supabase) .env dosyasından okunacak
# Eğer .env içinde yoksa, yerel SQLite çalıştıracak (Geriye Dönük Uyumluluk).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentsync.sqlite3")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
