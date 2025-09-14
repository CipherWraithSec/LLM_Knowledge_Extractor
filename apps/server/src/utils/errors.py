from fastapi import HTTPException, status
from typing import Dict, Any, Optional


class StandardError:
   # Utility for creating standardized HTTP exceptions.

    @staticmethod
    def bad_request(message: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": message}
        )

    @staticmethod
    def not_found(message: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": message}
        )

    @staticmethod
    def internal_error(message: str = "An internal server error occurred") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": message}
        )

    @staticmethod
    def validation_error(field_name: str, issue: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"{field_name.title()}: {issue}"}
        )

    @staticmethod
    def service_unavailable(service_name: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": f"{service_name} is temporarily unavailable. Please try again later."}
        )


# Convenience functions for common error scenarios
def empty_text_error() -> HTTPException:
    return StandardError.bad_request("Input text cannot be empty.")


def analysis_failed_error() -> HTTPException:
    return StandardError.internal_error("Text analysis failed. Please try again.")


def llm_unavailable_error() -> HTTPException:
    return StandardError.service_unavailable("AI analysis service")


def database_error() -> HTTPException:
    return StandardError.internal_error("Database temporarily unavailable. Please try again.")
