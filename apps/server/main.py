from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.logging import setup_logging, logger
from src.db.database import connect_to_db, disconnect_from_db, DatabaseError, prisma

# Setup logging configuration
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
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

# GET /analyses


@app.get("/analyses")
async def get_analyses():
    """Fetch all Analysis records from the database."""
    results = await prisma.analysis.find_many()
    return results

# GET /


@app.get("/")
async def index():
    return {"Server is running"}
