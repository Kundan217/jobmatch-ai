import json
import sqlite3
from contextlib import contextmanager
from typing import Iterator

from app.utils.paths import DB_PATH


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                ats_score INTEGER NOT NULL,
                matching_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                resume_summary TEXT NOT NULL,
                suggestions TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_analysis(result: dict) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO analysis_history (
                resume_name, job_title, match_score, ats_score, matching_skills,
                missing_skills, resume_summary, suggestions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result["resume_name"],
                result["job_title"],
                result["match_score"],
                result["ats_score"],
                json.dumps(result["matching_skills"]),
                json.dumps(result["missing_skills"]),
                result["resume_summary"],
                json.dumps(result["suggestions"]),
            ),
        )
        return int(cursor.lastrowid)


def _decode_row(row: sqlite3.Row) -> dict:
    data = dict(row)
    data["matching_skills"] = json.loads(data["matching_skills"])
    data["missing_skills"] = json.loads(data["missing_skills"])
    data["suggestions"] = json.loads(data["suggestions"])
    return data


def list_history(limit: int = 20) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM analysis_history
            ORDER BY datetime(created_at) DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [_decode_row(row) for row in rows]


def get_report(analysis_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM analysis_history WHERE id = ?",
            (analysis_id,),
        ).fetchone()
    return _decode_row(row) if row else None
