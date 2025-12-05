from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    email: str
    name: str

class BulkEmailRequest(BaseModel):
    employees: List[Employee]
