from jose import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.jwt import decode_access_token
from backend.crud.user import get_user_by_id
from backend.models.user import User
from backend.models.program_templates import ProgramTemplates

#temporarily disabling auth via the login path so that swagger works with form data
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl= "/auth/login"
# )
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "/auth/token"
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        # this exception handles if the token is expired and etc
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))

    if user is None:
        raise credentials_exception

    return user

def get_current_program(
    program_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProgramTemplates:

    stmt = select(ProgramTemplates).where(
        ProgramTemplates.id == program_id,
        ProgramTemplates.user_id == current_user.id,
    )

    program = db.execute(stmt).scalar_one_or_none()

    if program is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found",
        )

    return program