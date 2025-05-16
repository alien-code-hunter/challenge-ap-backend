from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file (ensure .env is in your root directory)
load_dotenv()

app = FastAPI()

# Get the DATABASE_URL from environment variables
database_url = os.getenv("postgresql+asyncpg://postgres@localhost:5432/registration_db")
print("Database URL is:", database_url)  # For debugging only, remove later

from app.routes.registration import router as registration_router

app.include_router(registration_router, prefix="/registrations", tags=["Registrations"])

# Simple root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Registration API"}
