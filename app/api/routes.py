from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.connection import get_report, list_history, save_analysis
from app.services.analysis_service import analyze_resume
from app.services.resume_parser import extract_pdf_text
from app.utils.paths import TEMPLATE_DIR, UPLOAD_DIR


router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "history": list_history(8)})


@router.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> HTMLResponse:
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    safe_name = Path(resume.filename).name
    stored_path = UPLOAD_DIR / f"{uuid4().hex}_{safe_name}"
    stored_path.write_bytes(await resume.read())

    resume_text = extract_pdf_text(stored_path)
    if len(resume_text) < 40:
        raise HTTPException(status_code=422, detail="Could not extract enough readable text from the PDF.")

    result = analyze_resume(safe_name, resume_text, job_description)
    analysis_id = save_analysis(result)
    report = get_report(analysis_id)
    return templates.TemplateResponse("result.html", {"request": request, "report": report})


@router.get("/history")
def history() -> list[dict]:
    return list_history()


@router.get("/report/{analysis_id}")
def report(analysis_id: int) -> dict:
    saved = get_report(analysis_id)
    if not saved:
        raise HTTPException(status_code=404, detail="Report not found.")
    return saved
