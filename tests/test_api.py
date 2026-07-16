from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_endpoint():
    payload = {
        "subject": "Product setup issue",
        "description": "I'm having an issue with the product setup. Please help me with the setup instructions."
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "type" in data
    assert "priority" in data
    assert "type_exp" in data
    assert "prio_exp" in data
    assert "resolutions" in data
    
    assert isinstance(data["type"], str)
    assert isinstance(data["priority"], str)
    assert len(data["resolutions"]) == 3
    
    # Check resolution keys
    for res in data["resolutions"]:
        assert "subject" in res
        assert "description" in res
        assert "resolution" in res
        assert "similarity" in res
        assert isinstance(res["similarity"], float)
