from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc

from app.db import get_session
from app.models import StudentRegistration
from app.schemas import StudentRegistrationCreate, StudentRegistrationOut

router = APIRouter()

# GET /registrations/ – Fetch all registrations
@router.get("/", response_model=list[StudentRegistrationOut])
async def read_registrations(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(StudentRegistration))
    registrations = result.scalars().all()
    return registrations

# POST /registrations/ – Create a new registration
@router.post("/", response_model=StudentRegistrationOut, status_code=201)
async def create_registration(
    registration: StudentRegistrationCreate,
    session: AsyncSession = Depends(get_session)
):
    if registration.email:
        existing = await session.execute(
            select(StudentRegistration).where(StudentRegistration.email == registration.email)
        )
        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered.")

    new_registration = StudentRegistration(**registration.dict())
    session.add(new_registration)
    await session.commit()
    await session.refresh(new_registration)
    return new_registration

# GET /registrations/count – Return total number of registrations
@router.get("/count")
async def get_registrations_count(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(func.count(StudentRegistration.id)))
    count = result.scalar_one()
    return {"count": count}

# GET /registrations/by_programme – Get registrations count grouped by study_programme
@router.get("/by_programme")
async def registrations_by_programme(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(StudentRegistration.study_programme, func.count(StudentRegistration.id))
        .group_by(StudentRegistration.study_programme)
    )
    data = [{"study_programme": row[0], "count": row[1]} for row in result.all()]
    return data

# GET /registrations/by_academic_year – Get registrations count grouped by academic_year
@router.get("/by_academic_year")
async def registrations_by_academic_year(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(StudentRegistration.academic_year, func.count(StudentRegistration.id))
        .group_by(StudentRegistration.academic_year)
        .order_by(StudentRegistration.academic_year)
    )
    data = [{"academic_year": row[0], "count": row[1]} for row in result.all()]
    return data

# GET /registrations/top_secondary_schools – Get top 10 secondary schools by registration count
@router.get("/top_secondary_schools")
async def top_secondary_schools(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(StudentRegistration.secondary_school, func.count(StudentRegistration.id))
        .group_by(StudentRegistration.secondary_school)
        .order_by(desc(func.count(StudentRegistration.id)))
        .limit(10)
    )
    data = [{"secondary_school": row[0], "count": row[1]} for row in result.all()]
    return data


