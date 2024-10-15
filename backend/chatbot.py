from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db  # Assuming get_db is correctly defined to provide a database session
from models import Resume  # Assuming the Resume model exists in the models.py file
from transformers import AutoModelForCausalLM, AutoTokenizer

router = APIRouter()

# Load DialoGPT model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Define a Pydantic model for the request
class Message(BaseModel):
    message: str

def fetch_candidates(min_experience: int, domain: str, db: Session):
    # Ensure that experience is an integer and domain is a valid string
    candidates = db.query(Resume).filter(Resume.experience >= min_experience, Resume.domain_of_interest == domain).all()
    return candidates

@router.post("/chatbot")
async def chatbot_query(message: Message, db: Session = Depends(get_db)):
    try:
        # Initialize variables
        min_experience = 0
        domain = ""
        candidates = []  # Initialize the candidates variable

        # Print the incoming message for debugging
        print(f"Received message: {message.message}")

        # Parsing the experience and domain from the message
        if "experience" in message.message:
            words = message.message.split(" ")
            try:
                min_experience = int(words[words.index("with") + 1])
                domain = words[-1]
                print(f"Parsed experience: {min_experience}, domain: {domain}")
            except (ValueError, IndexError):
                return {"response": "Could not parse experience or domain from the message."}
        
        elif "interest in" in message.message:
            domain = message.message.split("interest in")[-1].strip()
            print(f"Parsed domain from interest: {domain}")

        # Fetch candidates based on the parsed values
        candidates = fetch_candidates(min_experience, domain, db)

        # Debugging output for candidates found
        print(f"Candidates found: {[candidate.full_name for candidate in candidates]}")

        # Constructing the response
        if candidates:
            response_text = f"Candidates interested in {domain}:\n"
            for candidate in candidates:
                response_text += f"{candidate.full_name} (Experience: {candidate.experience})\n"
            return {"response": response_text.strip()}
        else:
            return {"response": "No candidates found with the specified criteria."}
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"response": "An error occurred: " + str(e)}
