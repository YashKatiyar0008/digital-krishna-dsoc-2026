# Digital Krishna AI — Public DSOC Backend

This directory contains a sanitized public demonstration of the
Digital Krishna guidance backend.

It demonstrates:

- FastAPI request handling
- Pydantic request and response validation
- English, Hindi, and Hinglish output
- Transparent concern classification
- Structured practical guidance
- Immediate-safety support messaging
- Safe error handling
- Automated API tests
- Separation of reviewed scripture and generated interpretation

## Important limitation

This public backend uses a deterministic demonstration engine.

It does not connect to:

- Private AI models
- Production databases
- Private user records
- Cloud credentials
- Production authentication systems
- Confidential scripture datasets

The public engine returns:

```text
scripture.status = "none"
```

unless a reviewed scripture-retrieval layer is connected.

## Requirements

- Python 3.10 or later
- pip
- A terminal

## Local installation

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Start the API

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Test the guidance endpoint

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/api/guidance" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am worried about my studies and future.",
    "language": "en"
  }'
```

Example response structure:

```json
{
  "request_id": "anonymous-request-id",
  "category": "Academic stress",
  "language": "en",
  "acknowledgement": "An empathetic acknowledgement",
  "scripture": {
    "status": "none",
    "reference": null,
    "original_text": null,
    "translation": null,
    "review_note": "No reviewed scripture record is attached."
  },
  "explanation": "A practical explanation",
  "practical_steps": [
    {
      "title": "Choose one task",
      "description": "Select one small and achievable action."
    }
  ],
  "reflection_question": "What useful action can you take now?",
  "safety_note": null,
  "disclaimer": "Digital Krishna provides spiritual reflection and educational guidance."
}
```

## Supported language values

```text
en
hi
hinglish
```

Unsupported language codes are rejected through request validation.

## Run the automated tests

From the `backend` directory:

```bash
pytest -v
```

The tests check:

- Root API information
- Health endpoint
- English guidance
- Hindi guidance
- Hinglish guidance
- Input validation
- Safety-note behaviour
- Scripture-verification boundaries
- Absence of sensitive response fields

## Project structure

```text
backend/
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── guidance.py
│   ├── main.py
│   └── schemas.py
└── tests/
    └── test_api.py
```

## Environment configuration

The public demonstration does not require API keys.

An optional comma-separated CORS setting can be supplied:

```bash
export CORS_ORIGINS="https://example.com,http://localhost:3000"
```

Do not commit real credentials or private configuration.

## Responsible-use boundary

Digital Krishna is intended for spiritual reflection and educational
guidance.

It is not a replacement for qualified medical, psychological, legal,
financial, or emergency assistance.

Generated interpretation must remain separate from reviewed scripture
content.
