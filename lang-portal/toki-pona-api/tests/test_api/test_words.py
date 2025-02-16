from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_word(client: TestClient, db: Session):
    data = {
        "word": "toki",
        "definition": "language, talk, speak, word, communicate",
        "examples": "toki pona = good language"
    }
    response = client.post("/api/v1/words/", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["word"] == data["word"]
    assert content["definition"] == data["definition"]
    assert content["examples"] == data["examples"]
    assert "id" in content
