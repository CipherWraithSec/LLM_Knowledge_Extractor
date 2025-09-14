from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from utils.logging import setup_logging, logger
from src.db.database import connect_to_db, disconnect_from_db, DatabaseError, prisma
from src.api.v1.routes.analysis import analysis_router as analysis_v1_router
from src.utils.errors import StandardError

# Setup logging configuration
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Connect to the database on startup and disconnect on shutdown.
    try:
        await connect_to_db()
        logger.info("Server is starting up.")
        yield
    except DatabaseError as e:
        # Handle db specific errors
        logger.critical(
            f"Application failed to start due to a database error: {e}")
        raise
    except Exception as e:
        # Handle any other unexpected errors
        logger.critical(
            f"An unexpected error prevented application startup: {e}")
        raise
    finally:
        logger.info("Shutting down...")
        await disconnect_from_db()

# Initialize the FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(analysis_v1_router, prefix="/api/v1")


@app.get("/")
async def index() -> dict[str, str]:
    # Basic health check
    return {"message": "Server is running"}


# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Internal Server Error for request {request.url}: {exc}", exc_info=True)
    # Use the standardized error approach
    raise StandardError.internal_error("Internal server error")
