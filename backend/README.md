# Digital Krishna AI — Public DSOC Backend

This directory contains the sanitized public backend demonstration for Digital Krishna AI.

It demonstrates:

- FastAPI request handling
- Pydantic request and response validation
- English, Hindi, and Hinglish guidance
- Transparent concern classification
- Structured practical steps
- Safety-oriented support messaging
- Automated API tests
- Separation of generated guidance from reviewed scripture

## Public-demo limitation

This repository does not contain:

- Production API keys
- Private AI model endpoints
- User records or conversations
- Production databases
- Authentication credentials
- Confidential datasets

The public backend uses a deterministic demonstration engine.

Unless reviewed scripture data is connected, responses return:

```text
scripture.status = "none"
```

## Requirements

- Python 3.10 or later
- pip
- Terminal or command prompt

## Installation

Open the repository in a terminal and run:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

For Windows PowerShell, activate the environment using:

```powershell
.venv\Scripts\Activate.ps1
```

## Start the API

From inside the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The API should open at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health-check endpoint:

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

Supported language values:

```text
en
hi
hinglish
```

## Run automated tests

Remain inside the `backend` directory and run:

```bash
pytest -v
```

The test suite checks:

- Root endpoint
- Health endpoint
- English guidance
- Hindi guidance
- Hinglish guidance
- Request validation
- Safety-support notes
- Scripture verification boundaries
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

## Optional CORS configuration

The API already allows the Digital Krishna website and common local-development addresses.

A custom comma-separated list can be supplied using:

```bash
export CORS_ORIGINS="https://example.com,http://localhost:3000"
```

Never commit real credentials or private configuration.

## Responsible-use boundary

Digital Krishna provides spiritual reflection and educational guidance.

It is not a replacement for qualified medical, psychological, legal, financial, or emergency assistance.

Generated interpretations must remain clearly separated from reviewed scripture content.
