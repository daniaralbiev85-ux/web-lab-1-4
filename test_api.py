import sys
from pathlib import Path

# make `main`, `data`, `models` importable when running `pytest` from the project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)


def ids(response):
    return [c["id"] for c in response.json()]


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Course Catalog API is running"}


def test_list_default_is_sorted_by_likes():
    r = client.get("/courses")
    assert r.status_code == 200
    assert len(r.json()) == 6
    assert ids(r)[0] == "ai-integration"
    assert ids(r)[-1] == "api-design"
    assert r.headers["X-Total-Count"] == "6"


def test_filter_elective():
    assert set(ids(client.get("/courses?is_elective=true"))) == {
        "ai-integration",
        "api-design",
    }
    assert len(client.get("/courses?is_elective=false").json()) == 4


def test_sort_by_title():
    assert ids(client.get("/courses?sort=title")) == [
        "ai-integration",
        "api-design",
        "backend-fastapi",
        "modern-frontend",
        "databases-postgresql",
        "web-security",
    ]


def test_pagination():
    assert ids(client.get("/courses?page=1&page_size=2")) == [
        "ai-integration",
        "modern-frontend",
    ]
    assert ids(client.get("/courses?page=4&page_size=2")) == []


def test_search():
    r = client.get("/courses?q=fastapi")
    assert "backend-fastapi" in ids(r)
    assert r.headers["X-Total-Count"] == str(len(r.json()))


def test_invalid_params_return_422():
    assert client.get("/courses?page=0").status_code == 422
    assert client.get("/courses?page_size=1000").status_code == 422
    assert client.get("/courses?sort=nonsense").status_code == 422


def test_get_course_and_404():
    assert client.get("/courses/web-security").json()["id"] == "web-security"
    r = client.get("/courses/nope")
    assert r.status_code == 404
    assert r.json() == {"detail": "Course not found"}


def test_like_increments():
    before = client.get("/courses/api-design").json()["likes"]
    after = client.post("/courses/api-design/like").json()["likes"]
    assert after == before + 1
    assert client.post("/courses/nope/like").status_code == 404
