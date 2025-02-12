import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SECRET_KEY: str = "f53c4dbb372badaea3c4b3070d060e4f69ac1c924e28a46b8d790fc028fd6c76"
    ALGORITHM: str = "HS256"

settings = Settings()
