from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.schemas import LLMOutput, ParsedAnswer

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

# This test checks the /data/stats endpoint when no dataset has been uploaded. 
# It sends a GET request to the endpoint and asserts that the response status code is 404, indicating that no dataset is available for statistics.
def test_stats_dataset():
    response = client.get("/data/stats")
    assert response.status_code == 404

# This test checks the /ai/ask endpoint when no dataset has been uploaded.
def test_ask_before_upload():

    response = client.post(
        "/ai/ask",
        json={
            "question": "What is the average score?"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset must be uploaded before asking questions"

# This test checks the /data/upload endpoint when an invalid file is uploaded. 
# It sends a POST request with a file that is not a CSV and asserts that the response status code is 400
#  indicating that the file format is not acceptable for upload.
def test_upload_invalid_file():

    response = client.post(
        "/data/upload",
        files={
            "file": ("bad.txt", b"not csv")
        }
    )

    assert response.status_code == 400

# This test checks the /data/upload endpoint when an empty CSV file is uploaded.
def test_upload_empty_csv():
    response = client.post(
        "/data/upload",
        files={"file": ("empty.csv", b"", "text/csv")}
    )
    assert response.status_code == 400

# This test checks the /ai/ask endpoint when an empty question is sent.
def test_empty_question():

    response = client.post(
        "/ai/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


@patch("app.chain.steps.LLMRunner.invoke")
def test_ai_ask_mocked(mock_llm):

    mock_llm.return_value = LLMOutput(raw_text="Average score is 85")

    csv_data = b"name,score\nAnna,85\nSukaina,90"

    upload_response = client.post(
        "/data/upload",
        files={"file": ("students.csv", csv_data, "text/csv")}
    )
    assert upload_response.status_code == 200

    response = client.post(
        "/ai/ask",
        json={"question": "What is the average score?"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["answer"] == "Average score is 85"
    assert data["model"] == "MockModel"