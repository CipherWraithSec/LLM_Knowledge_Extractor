import sys
from prisma import Prisma, errors as prisma_errors
from ..utils.logging import logger
from ..utils.errors import database_error

# Global Prisma client instance for the application.
prisma = Prisma()


class DatabaseError(Exception):
    # Custom exception for database-related errors.
    pass


async def connect_to_db() -> None:
    logger.info("Attempting to connect to the database...")
    try:
        await prisma.connect()
        logger.info("Database connection established.")
    except prisma_errors.PrismaError as e:
        logger.error(f"Prisma error: {e}")
        raise database_error()
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during database connection: {e}")
        raise database_error()


async def disconnect_from_db() -> None:
    logger.info("Disconnecting from the database...")
    await prisma.disconnect()
