# Course Catalog API

**Full name:** Фамилия Имя Отчество
**Group:** ВАША_ГРУППА
**Lab:** 4 — First Backend: FastAPI, Pydantic, and Depends

Backend for the course catalog (FastAPI + Pydantic): course list with filtering, sorting and pagination, and a single-course route with a 404 error.

## How to run

Requirements: Python 3.10 or newer.

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS / Linux:        source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

Open http://127.0.0.1:8000 and the interactive docs at http://127.0.0.1:8000/docs.

## Routes

| Route | Description |
| --- | --- |
| `GET /` | checks that the server is alive |
| `GET /courses` | course list: `is_elective`, `sort` (`popular` / `title`), `page`, `page_size` |
| `GET /courses/{course_id}` | a single course or a 404 error |

## What was verified

| Request | Result |
| --- | --- |
| `/courses` | 6 courses; `ai-integration` first (32 likes), `api-design` last (11) |
| `/courses?is_elective=true` | 2 courses: `ai-integration`, `api-design` |
| `/courses?is_elective=false` | 4 courses: `modern-frontend`, `web-security`, `backend-fastapi`, `databases-postgresql` |
| `/courses?sort=title` | 6 courses alphabetically: `ai-integration`, `api-design`, `backend-fastapi`, `modern-frontend`, `databases-postgresql`, `web-security` |
| `/courses?page=1&page_size=2` | `ai-integration`, `modern-frontend` |
| `/courses?page=2&page_size=2` | `web-security`, `backend-fastapi` |
| `/courses?page=3&page_size=2` | `databases-postgresql`, `api-design` |
| `/courses?page=4&page_size=2` | `[]` |
| `/courses/web-security` | the `web-security` course |
| `/courses/nope` | 404, `{"detail": "Course not found"}` |
