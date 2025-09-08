import os
import json
import openai

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def parse_text_to_json(raw_text: str):
    """
    Send OCR text to OpenAI and parse into structured JSON with confidence scores.
    """
    if not openai.api_key:
        return {"error": "OPENAI_API_KEY is not set in environment variables."}

    prompt = f"""
    You are a strict JSON generator.
    Extract the following fields from this marksheet text:

    - Candidate details (Name, Father's/Mother’s Name, Roll No, Registration No, DOB, Exam Year, Institution)
    - Subject-wise marks (subject, max marks, obtained marks, grade)
    - Overall result/grade/division

    Return ONLY valid JSON with this structure:
    {{
        "candidate_name": {{"value": "string", "confidence": 0.95}},
        "roll_no": {{"value": "string", "confidence": 0.92}},
        "dob": {{"value": "string", "confidence": 0.90}},
        "subjects": [
            {{
                "subject": {{"value": "Math", "confidence": 0.94}},
                "max_marks": {{"value": "100", "confidence": 0.95}},
                "obtained_marks": {{"value": "87", "confidence": 0.93}},
                "grade": {{"value": "A", "confidence": 0.91}}
            }}
        ],
        "overall_result": {{"value": "1st Division", "confidence": 0.96}}
    }}

    Marksheet text:
    {raw_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw_output = response["choices"][0]["message"]["content"].strip()

        # Try parsing JSON
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            # Attempt cleanup if GPT wrapped JSON with ```json ```
            cleaned = raw_output.strip("```json").strip("```").strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON returned from OpenAI", "raw_output": raw_output}

    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}
