from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from .models import Business, Symptom, Diagnostic
from sqlalchemy.future import select  
from sqlalchemy.orm import joinedload 

router = APIRouter()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/diagnostics/")
async def get_diagnostics(business_id: int = None, diagnostic: bool = None, db: AsyncSession = Depends(get_db)):
    # Build the query with select()
    query = select(Diagnostic).options(
        joinedload(Diagnostic.business),  # Load related Business
        joinedload(Diagnostic.symptom)   # Load related Symptom
    )

    if business_id:
        query = query.where(Diagnostic.business_id == business_id)

    if diagnostic is not None:
        query = query.where(Diagnostic.diagnostic_value == diagnostic)

    # Execute the query
    results = await db.execute(query)
    diagnostics = results.scalars().all()

    # Return the data in the required format
    return [
        {
            "business_id": diag.business_id,
            "business_name": diag.business.business_name,
            "symptom_code": diag.symptom_code,
            "symptom_name": diag.symptom.symptom_name,
            "diagnostic_value": diag.diagnostic_value,
        }
        for diag in diagnostics
    ]