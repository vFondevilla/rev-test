import requests
from datetime import date

# Base URL of the remote deployment
BASE_URL = "http://revolut.fondevilla.io"
USERNAME = "TestUser"


def test_save_or_update_user_remote_dob():
    dob = "2023-01-01"
    response = requests.put(f"{BASE_URL}/hello/{USERNAME}", json={"date_of_birth": dob})
    
    assert response.status_code == 204


def test_hello_birthday_remote_dob():
    response = requests.get(f"{BASE_URL}/hello/{USERNAME}")
    
    # If today isn't TestUser's birthday, expect a message telling how many days are left. 
    # Otherwise, expect a happy birthday message.
    json_response = response.json()
    if "Your birthday is in" in json_response["message"]: 
        assert response.status_code == 200 and f"Hello, {USERNAME}! Your birthday is in" in json_response["message"]
    else:
        assert response.status_code == 200 and f"Hello, {USERNAME}! Happy birthday!" == json_response["message"]

def test_save_or_update_user_remote_birthday():
    dob = date.today().isoformat()
    print(dob)
    response = requests.put(f"{BASE_URL}/hello/{USERNAME}", json={"date_of_birth": dob})
    
    assert response.status_code == 204

def test_hello_birthday_remote_birthday():
    response = requests.get(f"{BASE_URL}/hello/{USERNAME}")
    json_response = response.json()
    if "Your birthday is in" in json_response["message"]:
        assert response.status_code == 200 and f"Hello, {USERNAME}! Happy birthday!" == json_response["message"]
