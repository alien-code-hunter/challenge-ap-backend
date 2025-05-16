from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create a new student
@router.post("/", response_model=schemas.StudentRegistration)
def create_student(student: schemas.StudentRegistrationCreate, db: Session = Depends(get_db)):
    db_student = models.StudentRegistration(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Get all students
@router.get("/", response_model=list[schemas.StudentRegistration])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.StudentRegistration).all()

# Get student by ID
@router.get("/{student_id}", response_model=schemas.StudentRegistration)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Update student by ID
@router.put("/{student_id}", response_model=schemas.StudentRegistration)
def update_student(student_id: int, student_update: schemas.StudentRegistrationCreate, db: Session = Depends(get_db)):
    student = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student_update.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

# Delete student by ID
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"detail": "Student deleted successfully"}
