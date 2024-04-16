from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import schemas
import base64

client = TestClient(app)

def test_user_lifecycle():
    # Generate Basic authentication token
    username = "johndoe1111@example.com"
    password = "password123"
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    auth_header = f"Basic {encoded_credentials}"

    # Test creating a user
    new_user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe1111@example.com",
        "password": "password123"
    }
    response = client.post("/v2/user", json=new_user_data)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["first_name"] == new_user_data["first_name"]
    assert created_user["last_name"] == new_user_data["last_name"]
    assert created_user["username"] == new_user_data["username"]
    #assert "password" in created_user

    # Test getting user details
    response = client.get("/v2/user/self", headers={"Authorization": auth_header})
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["first_name"] == new_user_data["first_name"]
    assert retrieved_user["last_name"] == new_user_data["last_name"]
    assert retrieved_user["username"] == new_user_data["username"]

    # Test updating user details
    updated_user_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "newpassword123",
        "username": "johndoe1111@example.com"
    }
    response = client.put("/v2/user/self", json=updated_user_data, headers={"Authorization": auth_header})
    assert response.status_code == 204

    # Update the password in the auth_header
    new_password = "newpassword123"
    updated_credentials = f"{username}:{new_password}"
    updated_encoded_credentials = base64.b64encode(updated_credentials.encode("utf-8")).decode("utf-8")
    updated_auth_header = f"Basic {updated_encoded_credentials}"

    # Verify the user details were updated
    updated_response = client.get("/v2/user/self", headers={"Authorization": updated_auth_header})
    assert updated_response.status_code == 200
    updated_user = updated_response.json()
    assert updated_user["first_name"] == updated_user_data["first_name"]
    assert updated_user["last_name"] == updated_user_data["last_name"]

