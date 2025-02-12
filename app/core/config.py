import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

settings = Settings()
