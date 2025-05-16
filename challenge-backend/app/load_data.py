import os
import json
import asyncio
from datetime import datetime
from app.models import StudentRegistration
from app.database import async_session

# Correct path to JSON file relative to this script
JSON_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'mock_student_data.json')
)
async def load_data():
    # Read the JSON data
    with open(JSON_FILE, "r") as f:
        students = json.load(f)

    async with async_session() as session:
        for student in students:
            # Convert registration_date string to datetime.date object
            registration_date = datetime.strptime(student["registration_date"], "%m/%d/%Y").date()

            # Create StudentRegistration instance
            new_student = StudentRegistration(
                id=student["id"],
                first_name=student["first_name"],
                last_name=student["last_name"],
                email=student["email"],
                gender=student.get("gender"),
                student_id=student["student_id"],
                study_programme=student.get("study_programme"),
                secondary_school=student.get("secondary_school"),
                registration_date=registration_date,
                academic_year=student["academic_year"],
            )
            session.add(new_student)

        # Commit all inserts at once
        await session.commit()

if __name__ == "__main__":
    asyncio.run(load_data())
