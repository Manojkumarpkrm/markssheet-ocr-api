from pydantic import BaseModel
from typing import List

class FieldWithConfidence(BaseModel):
    value: str
    confidence: float

class Subject(BaseModel):
    subject: FieldWithConfidence
    max_marks: FieldWithConfidence
    obtained_marks: FieldWithConfidence
    grade: FieldWithConfidence

class Marksheet(BaseModel):
    candidate_name: FieldWithConfidence
    roll_no: FieldWithConfidence
    dob: FieldWithConfidence
    subjects: List[Subject]
    overall_result: FieldWithConfidence
