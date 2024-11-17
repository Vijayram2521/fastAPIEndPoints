from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Business Model
class Business(Base):
    __tablename__ = 'business'

    business_id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, unique=True, index=True)

    # One-to-many relationship with Diagnostics
    diagnostics = relationship("Diagnostic", back_populates="business")


# Symptom Model
class Symptom(Base):
    __tablename__ = 'symptom'

    symptom_code = Column(String, primary_key=True, index=True)
    symptom_name = Column(String, unique=True, index=True)

    # One-to-many relationship with Diagnostic
    diagnostics = relationship("Diagnostic", back_populates="symptom")


# Diagnostic Model (Linking Business and Symptom)
class Diagnostic(Base):
    __tablename__ = 'diagnostics'

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to Business
    business_id = Column(Integer, ForeignKey('business.business_id'))
    
    # Foreign key to Symptom (using symptom code as the primary key)
    symptom_code = Column(String, ForeignKey('symptom.symptom_code'))

    # Additional diagnostic information (e.g., whether the symptom is present)
    diagnostic_value = Column(Boolean)

    # Relationships
    business = relationship("Business", back_populates="diagnostics")
    symptom = relationship("Symptom", back_populates="diagnostics")