from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from core.config import config


SECRET_KEY = config.secret_key
ALGORITHM = config.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.access_token_expire_minutes


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Create a signed JWT access token.

    Parameters
    ----------
    data:
        Payload to include in the token.
        Usually contains {"sub": username}.

    expires_delta:
        Optional custom expiration time.
    """

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate an access token.

    Raises:
        JWTError
            If the token is invalid or expired.
    """

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )