from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from schemas.token import Token
from core.hashing import hash_password, verify_password
from crud.user import create_user, get_user_by_email, get_user_by_username
from core.jwt import create_access_token


def register_user(db: Session, user_data: UserCreate) -> User:
    
    username = user_data.username
    email = user_data.email

    check_username = get_user_by_username(db, username)
    
    if check_username is not None:
        raise ValueError("username already exists")
    
    check_email = get_user_by_email(db, email)

    if check_email is not None:
        raise ValueError("email already exists")
    
    hashed_password = hash_password(user_data.password)

    reg_user = User(
        full_name = user_data.full_name,
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password
    )

    return create_user(db, reg_user)

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)

    if user is None:
        raise ValueError("invalid username or password")
    
    is_valid = verify_password(password, user.hashed_password)

    if is_valid is False:
        raise ValueError("invalid username or password")
    
    return user

def login_user(db: Session, username: str, password: str) -> Token:
    user = authenticate_user(db, username, password)
    access_token = create_access_token({"sub": user.username})

    return Token(
        access_token = access_token,
        token_type = "bearer"
    )


    


