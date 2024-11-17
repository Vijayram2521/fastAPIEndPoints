from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal
from .models import Business, Symptom, Diagnostic
from sqlalchemy.future import select  
from sqlalchemy.orm import joinedload 
import csv

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

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV file should be uploaded.")
    contents = await file.read()
    csv_reader = csv.reader(contents.decode("utf-8").splitlines())
    next(csv_reader)
    for row in csv_reader :
        business_id, business_name, symptom_code, symptom_name, diagnostic_value = row 
        business_id = int(business_id)
        business = await db.execute(select(Business).filter(Business.business_id == business_id))
        business = business.scalars().first()
        if not business : 
            business = Business(business_id=business_id, business_name=business_name)
            db.add(business)

        symptom = await db.execute(select(Symptom).filter(Symptom.symptom_code == symptom_code))
        symptom = symptom.scalars().first()
        if not symptom : 
            symptom = Symptom(symptom_code=symptom_code, symptom_name=symptom_name)
            db.add(symptom)

        diagnostic_record = Diagnostic(
            business_id=business_id,
            symptom_code=symptom_code,
            diagnostic_value=(diagnostic_value.lower() in ["true", "yes"])  
        )
        db.add(diagnostic_record)
    await db.commit()
    return {"message": "Data uploaded successfully"}