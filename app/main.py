from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.database.connection import init_db
from app.utils.paths import STATIC_DIR


app = FastAPI(
    title="JobMatch AI",
    description="Resume and job description semantic matcher",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    init_db()
