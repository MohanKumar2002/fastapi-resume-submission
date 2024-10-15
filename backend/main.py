from fastapi import FastAPI, File, Form, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Resume
import os
from fastapi.responses import Response
from chatbot import router as chatbot_router
import shutil

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings to allow frontend communication
origins = [
    "http://localhost:3000",  # Frontend
    "http://localhost:8000",  # Backend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify ('GET', 'POST', etc.)
    allow_headers=["*"],  # Adjust to specify allowed headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Resume Submission API!"}

@app.get("/favicon.ico", response_class=Response)
async def favicon():
    return Response(status_code=204)  # No content

@app.post("/submit")
async def submit_resume(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    college: str = Form(...),
    qualification: str = Form(...),
    department: str = Form(...),
    year_passed_out: int = Form(...),
    domain_of_interest: str = Form(...),
    skills: str = Form(...),
    experience: int = Form(default=0),
    company: str = Form(default=''),
    resume: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Save the uploaded resume to a local directory
    resume_dir = "uploaded_resumes"
    os.makedirs(resume_dir, exist_ok=True)
    file_location = f"{resume_dir}/{resume.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(resume.file, file_object)

    # Store the resume metadata in the database
    new_resume = Resume(
        full_name=full_name,
        email=email,
        phone=phone,
        dob=dob,
        gender=gender,
        college=college,
        qualification=qualification,
        department=department,
        year_passed_out=year_passed_out,
        domain_of_interest=domain_of_interest,
        skills=skills,
        experience=experience,
        company=company,
        resume_path=file_location
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {"message": "Resume uploaded successfully", "id": new_resume.id}

# Include the chatbot routes
app.include_router(chatbot_router)
@app.options("/chatbot")
def chatbot_options():
    return {"status": "OK"}