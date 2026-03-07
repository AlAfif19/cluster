from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import os
from dotenv import load_dotenv

from backend.app.core.auth import router

load_dotenv()

app = FastAPI(title="KMeans Engine API")

# Enforce HTTPS in production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Configure CORS
# In development, allow HTTP on localhost
# In production, only allow HTTPS origins
allowed_origins = ["http://localhost:3000"]  # Development
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins = [
        "https://kmeans-engine.example.com",  # Production frontend
        # Add other allowed HTTPS origins
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint returning Hello World message."""
    return {"message": "Hello World from KMeans Engine API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include authentication routes
app.include_router(router)
