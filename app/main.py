# main.py
from fastapi import FastAPI, UploadFile, Form
from typing import List, Optional
import json
from app.send_email import send_bulk_greetings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

 # CORS
app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)



@app.post("/send-greetings-bulk")
async def send_greetings_bulk(
    employees: str = Form(...),  # JSON string of employees from form
    file: Optional[UploadFile] = None
):
    """
    employees: JSON string, e.g.
    '[{"email":"a@example.com","name":"A"},{"email":"b@example.com","name":"B"}]'
    file: optional file attachment
    """
    try:
        employees_list = json.loads(employees)  # Convert JSON string to Python list
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "details": "Expecting a JSON array of employees"}

    result = await send_bulk_greetings(
        employees_list,
        file=file,
        filename=file.filename if file else None
    )
    return result
