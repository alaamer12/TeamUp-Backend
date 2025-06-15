# TeamUp Backend API

A FastAPI-based backend service for the TeamUp application that manages team formation requests.

## Features

- RESTful API for team formation requests
- MongoDB integration with Beanie ODM
- Async request handling
- Health check and status endpoints
- CORS configuration
- Environment-based configuration
- Production-ready with Uvicorn

## Project Structure

```
python/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py      # Database connection handling
│   ├── models/
│   │   ├── __init__.py
│   │   └── team_request.py  # Data models with Beanie
│   └── api/
│       ├── __init__.py
│       └── endpoints/
│           ├── __init__.py
│           └── requests.py   # API endpoints
├── .env                     # Environment variables
└── requirements.txt         # Python dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on the provided example

## Running Locally

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8080`

## API Documentation

API documentation is automatically generated and available at:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## API Endpoints

- `GET /api/requests`: Get all team requests
- `POST /api/requests`: Create a new team request
- `PUT /api/requests/{request_id}`: Update a team request
- `DELETE /api/requests/{request_id}`: Delete a team request
- `GET /health`: Health check
- `GET /`: API information

## Environment Variables

- `PORT`: Server port (default: 8080)
- `NODE_ENV`: Environment (development, production)
- `MONGODB_URI`: MongoDB connection string
- `CORS_ORIGIN`: Allowed CORS origin 