# TeamUp Backend

A robust Express.js backend for the TeamUp platform, providing API endpoints for team request management and data persistence.

> **Note**: This is part of the TeamUp monorepo. For the complete project overview and setup instructions, please refer to the [root README](../README.md).

## Features

- **RESTful API**: Endpoints for managing team requests
- **MongoDB Integration**: Database storage for team request data
- **Ownership Verification**: Secure request management with fingerprint-based authentication
- **CORS Support**: Configured for cross-origin requests
- **Request Logging**: Detailed logging with Morgan

## Technology Stack

- Express.js
- Node.js
- MongoDB with Mongoose
- Morgan for request logging
- CORS for cross-origin support
- Dotenv for environment variable management

## Setup

```bash
# Install dependencies
npm install

# Start server in development mode
npm run dev

# Start server in production mode
npm start
```

## API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/requests` | Get all team requests | None |
| POST | `/api/requests` | Create a new team request | None |
| PUT | `/api/requests/:id` | Update an existing team request | Ownership verification |
| DELETE | `/api/requests/:id` | Delete a team request | Ownership verification |
| GET | `/health` | Health check endpoint | None |

## Authentication

The API uses a simple ownership verification system. When creating a team request, a fingerprint is stored with the request. For update and delete operations, this fingerprint must be provided to verify ownership.

## Data Storage

Data is stored in MongoDB. The connection string can be configured using the `MONGODB_URI` environment variable.

## Environment Variables

- `PORT`: The port the server listens on (default: 8080)
- `MONGODB_URI`: MongoDB connection string (default: `mongodb://localhost:27017/teamup`)
- `CORS_ORIGIN`: Allowed origin for CORS (default: `*`)

## Deployment

This backend is configured for deployment on Vercel. The configuration can be found in `vercel.json`. For detailed deployment instructions, see the [Deployment Guide](../DEPLOYMENT.md). 