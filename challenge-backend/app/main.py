from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get the DATABASE_URL from environment variables
database_url = os.getenv("DATABASE_URL")
print("Database URL is:", database_url)  # You can remove this after testing

from app.routes.registration import router as registration_router

app.include_router(registration_router, prefix="/registrations", tags=["Registrations"])
