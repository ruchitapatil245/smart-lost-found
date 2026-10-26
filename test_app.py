import os
import tempfile
import pytest
import app as app_module


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    original_db = app_module.DATABASE
    app_module.DATABASE = db_path
    app_module.init_db()

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as client:
        yield client

    app_module.DATABASE = original_db
    os.unlink(db_path)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Smart Lost" in response.data or b"Lost something" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_report_item(client):
    response = client.post("/report", data={
        "type": "Lost",
        "name": "Black wallet",
        "description": "Small black wallet",
        "location": "College library"
    })
    assert response.status_code == 302

    response = client.get("/")
    assert b"Black wallet" in response.data
