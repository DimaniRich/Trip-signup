import base64
import sqlite3

import pytest

from app import app


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test.db")
    app.config["ADMIN_PASSWORD"] = "s3cret"
    with app.test_client() as client:
        yield client


def auth(password):
    token = base64.b64encode(f"admin:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_form_page_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'name="email"' in resp.data


def test_signup_saves_and_redirects(client):
    resp = client.post("/", data={"name": "Ada", "email": "ada@example.com", "major": "ISDS"})
    assert resp.status_code == 302
    assert "/thanks" in resp.headers["Location"]

    conn = sqlite3.connect(app.config["DATABASE"])
    rows = conn.execute("SELECT name, email, major FROM signups").fetchall()
    conn.close()
    assert rows == [("Ada", "ada@example.com", "ISDS")]


def test_thanks_page(client):
    resp = client.post("/", data={"name": "Ada", "email": "ada@example.com", "major": "ISDS"},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert b"Thank you, Ada!" in resp.data


def test_missing_field_rejected(client):
    resp = client.post("/", data={"name": "Ada", "email": "", "major": "ISDS"})
    assert resp.status_code == 400
    assert b"All fields are required." in resp.data


def test_admin_requires_password(client):
    resp = client.get("/admin")
    assert resp.status_code == 401
    assert "WWW-Authenticate" in resp.headers


def test_admin_rejects_wrong_password(client):
    resp = client.get("/admin", headers=auth("wrong"))
    assert resp.status_code == 401


def test_admin_lists_signups(client):
    client.post("/", data={"name": "Ada", "email": "ada@example.com", "major": "ISDS"})
    client.post("/", data={"name": "Grace", "email": "grace@example.com", "major": "CS"})
    resp = client.get("/admin", headers=auth("s3cret"))
    assert resp.status_code == 200
    for text in [b"Ada", b"ada@example.com", b"ISDS", b"Grace", b"grace@example.com", b"CS"]:
        assert text in resp.data


def test_admin_locked_when_no_password_configured(client):
    app.config["ADMIN_PASSWORD"] = None
    resp = client.get("/admin", headers=auth(""))
    assert resp.status_code == 401
