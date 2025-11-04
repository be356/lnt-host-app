"""
API tests using FastAPI's TestClient.
"""
from fastapi.testclient import TestClient
from app.main import app
import base64

client = TestClient(app)

def test_health_and_version():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

    v = client.get("/version")
    assert "version" in v.json()

def test_serial_echo_endpoint():
    data = base64.b64encode(b"hi").decode()
    r = client.post("/serial/echo", json={"data_b64": data})
    assert r.status_code == 200
    resp = r.json()
    echoed = base64.b64decode(resp["echoed_b64"])
    assert echoed == b"hi"