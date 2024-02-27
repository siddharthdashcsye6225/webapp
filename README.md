# webapp

This is a FastAPI application designed to handle user management and health check endpoints.

Features
User Management: Allows users to create, update, and retrieve their own account details.
Health Check: Provides a health check endpoint to verify the connectivity to the database.
Setup
Clone the Repository: git clone <repository-url>
Install Dependencies: Navigate to the project directory and run pip install -r requirements.txt.
Database Configuration: Ensure PostgreSQL is installed and running. Update the SQLALCHEMY_DATABASE_URL in database.py with your database connection details.
Run the Application: Execute uvicorn main:app --reload to start the FastAPI application.
Usage
User Management
Create User
http
Copy code
POST /v1/user
Creates a new user account.

Request Body:

json
Copy code
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe@example.com",
  "password": "password123"
}
Get User Details
http
Copy code
GET /v1/user/self
Retrieves details of the authenticated user.

Update User Details
http
Copy code
PUT /v1/user/self
Updates details of the authenticated user.

Request Body:

json
Copy code
{
  "first_name": "Jane",
  "last_name": "Smith",
  "username": "janesmith@example.com",
  "password": "newpassword123"
}


assignment 4 demo
Health Check
http
Copy code
GET /healthz
Checks the health status of the application.

Testing
To run tests for the application, execute pytest in the project directory.
