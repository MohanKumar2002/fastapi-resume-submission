from sqlalchemy import Column, Integer, String, Text
from database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    dob = Column(String(10), nullable=False)
    gender = Column(String(10), nullable=False)
    college = Column(String(100), nullable=False)
    qualification = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    year_passed_out = Column(Integer, nullable=False)
    domain_of_interest = Column(String(50), nullable=False)
    skills = Column(Text, nullable=False)
    experience = Column(Integer, nullable=True)  
    company = Column(String(100), nullable=True)
    resume_path = Column(Text, nullable=False)
