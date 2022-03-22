from fastapi.testclient import TestClient

from .app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastApi for interview"}

def test_read_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {"Receiver": "Cisco is the best!"}
    
def test_no_url():
    response = client.post("/ping")
    assert response.status_code == 422
    assert response.json() == {'msg': "Doh!: No 'url' attribute in request body None\n", 'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}