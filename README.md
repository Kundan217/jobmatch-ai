# JobMatch AI

AI-powered resume and job description semantic matcher built with FastAPI.

## Features

- Upload a PDF resume
- Paste a job description
- Extract resume text with PyMuPDF
- Generate a match score with Sentence Transformers when available
- Fall back to TF-IDF cosine similarity when the embedding model is unavailable
- Identify matching and missing skills
- Produce ATS-style feedback and suggestions
- Store analysis history locally in SQLite for the MVP
- Include a MySQL schema for production migration

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

For the full semantic embedding stack, install the optional AI dependencies:

```bash
pip install -r requirements-ai.txt
```

Without those optional packages, the app still runs with TF-IDF cosine similarity.

## API Endpoints

- `GET /` - Web dashboard
- `POST /analyze` - Upload resume PDF and job description
- `GET /history` - Recent analysis history
- `GET /report/{analysis_id}` - Single analysis report
- `GET /docs` - Swagger documentation

## Project Structure

```text
jobmatch-ai/
  app/
    api/
    database/
    models/
    services/
    static/
    templates/
    utils/
  data/
  uploads/
  requirements.txt
  README.md
```

## Notes

This MVP uses SQLite so it can run immediately. `app/database/schema.sql` contains
the planned MySQL schema for the full stack version.
