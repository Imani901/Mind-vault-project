import os
from dotenv import load_dotenv
from pathlib import Path


# Load .env from project root
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class Config:
    ALLOWED_ORIGINS = [
        "https://mind-vault-project.vercel.app",
        "http://localhost:3000",
        ...
    ]
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL not set in environment variables")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-key")
    JWT_ACCESS_TOKEN_EXPIRES = False
