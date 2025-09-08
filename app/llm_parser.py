import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_text_to_json(raw_text: str):
    prompt = f"""
    Extract the following fields from this marksheet text:
    - Candidate details (Name, Father/Mother’s Name, Roll No, Registration No, DOB, Exam Year, Institution)
    - Subject-wise marks (subject, max marks, obtained marks, grade)
    - Overall result/grade/division
    Return result strictly in JSON with confidence scores (0-1).
    
    Marksheet text:
    {raw_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        return json.loads(response["choices"][0]["message"]["content"])
    except:
        return {"error": "Could not parse JSON"}