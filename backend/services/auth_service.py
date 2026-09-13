from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.schemas.token import Token
from backend.core.hashing import hash_password, verify_password
from backend.crud.user import create_user, get_user_by_email, get_user_by_username
from backend.core.jwt import create_access_token


async def register_user(db: AsyncSession, user_data: UserCreate) -> User:

    username = user_data.username
    email = user_data.email

    check_username = await get_user_by_username(db, username)

    if check_username is not None:
        raise ValueError("username already exists")

    check_email = await get_user_by_email(db, email)

    if check_email is not None:
        raise ValueError("email already exists")

    hashed_password = hash_password(user_data.password)

    reg_user = User(
        full_name = user_data.full_name,
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password,
        gender = user_data.gender,
    )

    return await create_user(db, reg_user)

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_username(db, username)

    if user is None:
        raise ValueError("invalid username or password")

    is_valid = verify_password(password, user.hashed_password)

    if is_valid is False:
        raise ValueError("invalid username or password")

    return user

async def login_user(db: AsyncSession, username: str, password: str) -> Token:
    user = await authenticate_user(db, username, password)
    access_token = create_access_token({"sub": str(user.id)})

    return Token(
        access_token = access_token,
        token_type = "bearer"
    )
