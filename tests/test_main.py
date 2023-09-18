from fastapi.testclient import TestClient
from main import app
from dateutil.relativedelta import relativedelta
# from datetime import date
import datetime

client = TestClient(app)
USERNAME = "TestUser"

## Current date tests
def test_save_current_date():
    today_date = datetime.date.today().isoformat()
    response = client.put(f"/hello/{USERNAME}", json={"date_of_birth": today_date})
    print(response.json())
    assert response.status_code == 204

def test_get_current_birthday():
    response = client.get(f"/hello/{USERNAME}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {USERNAME}! Happy birthday!"}

## Future date test
def test_save_future_date():
    future_date = (datetime.date.today() + relativedelta(days=1)).isoformat()
    response = client.put(f"/hello/{USERNAME}", json={"date_of_birth": future_date})
    assert response.status_code == 400
    assert response.json() == {"detail": "date_of_birth must be a date before the today date"}


## Past date tests
def test_save_past_date():
    past_date = (datetime.date.today() - relativedelta(months=1)).isoformat()
    response = client.put(f"/hello/{USERNAME}", json={"date_of_birth": past_date})
    assert response.status_code == 204

def test_get_past_birthday():
    response = client.get(f"/hello/{USERNAME}")
    print(response.json())
    assert response.status_code == 200
    assert "Your birthday is in" in response.json()["message"]

## Incorrect username and date format tests
def test_save_invalid_username():
    response = client.put("/hello/John123", json={"date_of_birth": "2023-01-01"})
    assert response.status_code == 422

def test_retrieve_invalid_username():
    response = client.get("/hello/John123")
    assert response.status_code == 422  # 422 Unprocessable Entity for validation error

def test_save_invalid_date():
    response = client.put(f"/hello/{USERNAME}", json={"date_of_birth": "foobar"})
    assert response.status_code == 422

# Check for a user that doesn't exist
def test_get_nonexistent_username():
    response = client.get("/hello/RandomUser")
    assert response.status_code == 404
    assert response.json() == {"detail": "Username not found"}

