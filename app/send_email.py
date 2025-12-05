# app/send_email.py

import base64
from typing import List, Optional
from fastapi import UploadFile
from app.config import settings
import httpx

# Correct ZeptoMail API endpoint
ZEPTO_SEND_EMAIL_URL = "https://api.zeptomail.com/v1.1/email"

async def send_bulk_greetings(
    employees: List[dict],
    file: Optional[UploadFile] = None,
    filename: Optional[str] = None
):
    """
    Send bulk greetings emails via ZeptoMail.
    
    employees: List of dicts [{"email": "...", "name": "..."}]
    file: Optional UploadFile to attach
    filename: Name of the attachment
    """
    
    sent_count = 0

    headers = {
        "Authorization": f"Bearer {settings.ZEPTOMAIL_API_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        for emp in employees:
            message = {
                "from": {"address": settings.ZEPTOMAIL_SENDER_EMAIL},
                "to": [{"email": emp["email"], "name": emp.get("name", "")}],
                "subject": "Greetings!",
                "content": [{"type": "text/plain", "value": f"Hello {emp.get('name', '')}!"}]
            }

            # Attach file if provided
            if file and filename:
                file_content = await file.read()
                encoded_content = base64.b64encode(file_content).decode("utf-8")
                message["attachments"] = [
                    {
                        "name": filename,
                        "content": encoded_content
                    }
                ]
                file.file.seek(0)  # Reset file pointer for next read

            try:
                response = await client.post(
                    ZEPTO_SEND_EMAIL_URL,
                    json=message,
                    headers=headers
                )
                response.raise_for_status()  # Raise exception for non-2xx responses
                sent_count += 1

            except httpx.HTTPStatusError as e:
                print(f"Failed to send to {emp['email']}: {e.response.text}")
            except Exception as e:
                print(f"Unexpected error for {emp['email']}: {str(e)}")

    return {"status": "success", "sent": sent_count}
