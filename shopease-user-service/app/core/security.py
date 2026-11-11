
import httpx

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """
    Verify the access token through the ShopEase Authentication Service.
    Return the authenticated user's identity.
    """

    # Step 1: Check whether the client provided a Bearer token.
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Step 2: Prepare the Auth Service verification endpoint.
    verify_url = (
        f"{settings.AUTH_SERVICE_URL.rstrip('/')}/api/auth/verify-token"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Step 3: Contact the Auth Service.
    try:
        async with httpx.AsyncClient(
            timeout=settings.AUTH_VERIFY_TIMEOUT_SECONDS
        ) as client:
            response = await client.post(
                verify_url,
                headers=headers
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication Service timed out"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication Service is unavailable"
        )

    # Step 4: Handle unsuccessful upstream responses.
    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication Service encountered an error"
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 5: Read and validate the Auth Service response.
    try:
        auth_data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from Authentication Service"
        )

    user_id = auth_data.get("user_id") if isinstance(auth_data, dict) else None
    role = auth_data.get("role") if isinstance(auth_data, dict) else None

    if (
        not isinstance(auth_data, dict)
        or auth_data.get("valid") is not True
        or not isinstance(user_id, int)
        or isinstance(user_id, bool)
        or user_id <= 0
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 6: Return the verified identity.
    return {
        "user_id": user_id,
        "role": role
    }
