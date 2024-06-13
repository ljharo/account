Authentication and API Project

This project is an authentication and API application developed with FastAPI and SQLAlchemy. The application allows users to register, log in, and log out, and also provides an API to interact with the database.

Requirements

Python 3.9 or higher
FastAPI
SQLAlchemy
dotenv
Installation

Clone the project repository.
Install the required dependencies with pip install -r requirements.txt.
Create a .env file with the necessary environment variables (HOST, PORT, DB_URI, SECRET_KEY, DEBUG).
Run the application with The command:
  - python3 run.py
    
Endpoints

POST /register: Registers a new user.
POST /login: Logs in with an existing user.
POST /logout: Logs out with an existing user.
Database

The application uses a relational database managed by SQLAlchemy. The database is configured using the DB_URI environment variable.

Security

The application uses authentication tokens to protect API requests. Tokens are generated and verified using the secret key configured in the SECRET_KEY environment variable.

Development

The project uses dotenv to load environment variables from a .env file. The application runs in debug mode if the DEBUG environment variable is set to 1.

