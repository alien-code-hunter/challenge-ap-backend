from pydantic import BaseModel, EmailStr
from datetime import date

class StudentRegistrationBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    gender: str | None = None
    student_id: str
    study_programme: str | None = None
    secondary_school: str | None = None
    registration_date: date
    academic_year: int

class StudentRegistrationCreate(StudentRegistrationBase):
    pass

class StudentRegistrationOut(StudentRegistrationBase):
    id: int

    class Config:
        orm_mode = True
