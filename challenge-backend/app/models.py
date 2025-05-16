from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StudentRegistration(Base):
    __tablename__ = "student_registrations"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)  # I don't think all students have emial addreess. No time to check  
    gender = Column(String)
    student_id = Column(String, unique=True, index=True, nullable=False)
    study_programme = Column(String)
    secondary_school = Column(String)
    registration_date = Column(Date)
    academic_year = Column(Integer)
