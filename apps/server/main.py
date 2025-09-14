from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.logging import setup_logging, logger
from src.db.database import connect_to_db, disconnect_from_db, DatabaseError, prisma
from src.api.v1.routes.analysis import analysis_router as analysis_v1_router

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


# @app.get("/analyses")
# async def get_analyses():
#     """Fetch all Analysis records from the database."""
#     results = await prisma.analysis.find_many()
#     return results

# GET /


@app.get("/")
async def index() -> dict[str, str]:
    """Health check endpoint to verify server is running.
    
    Returns:
        dict: Simple status message indicating server is operational
    """
    return {"message": "Server is running"}


# Global exception handler to catch unhandled exceptions and return a consistent JSON response.
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:

    logger.error(
        f"Internal Server Error for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )
