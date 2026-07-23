from fastapi import HTTPException, status


class EntityNotFoundException(HTTPException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with identifier {entity_id} was not found."
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Invalid credentials or token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedException(HTTPException):
    def __init__(self, detail: str = "Operation not permitted"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class DuplicateResourceException(HTTPException):
    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )
