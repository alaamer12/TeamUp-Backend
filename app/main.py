import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any

from app.api.endpoints.requests import router as requests_router
from app.config.database import Database

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(title="TeamUp API", version="1.0.3")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "*")],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


# Database connection dependency
async def get_db():
    """Connect to database if not already connected."""
    if Database.client is None:
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/teamup")
        await Database.connect(mongodb_uri)
    return Database


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/teamup")
        await Database.connect(mongodb_uri)
    except Exception as e:
        logger.error(f"Failed to connect to database on startup: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    await Database.close()


# Register API routers
app.include_router(requests_router, prefix="/api/requests", tags=["requests"], dependencies=[Depends(get_db)])


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "message": "TeamUp API is running",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now(),
        "environment": os.getenv("NODE_ENV", "development"),
        "version": "1.0.3"
    }


# Not found handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle 404 errors."""
    return JSONResponse(status_code=404, content={"error": "Not found"})


# Main entry point for local development
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
