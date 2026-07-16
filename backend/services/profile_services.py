from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from crud.user import update_user, get_user_by_username, get_user_by_email
from models.user import User
from schemas.user import UserUpdate
from pydantic import EmailStr


def update_username(db: Session, current_user: User, user_data: UserUpdate):
    now = datetime.now()
    account_created = current_user.created_at
    last_updated = current_user.last_updated_username
    user_id = current_user.id

    is_valid = get_user_by_username(db, user_data.username)

    if is_valid is not None and is_valid.id != current_user.id:
        raise ValueError("This username already exists")
    
    difference = now - last_updated

    if account_created == last_updated or difference >= timedelta(days=14):
        user_data.last_updated_username = now
        return update_user(db, user_id, {"username": user_data.username, "last_updated_username": user_data.last_updated_username})
    else:
        raise ValueError("You can only update username every 14 days")

def update_email(db: Session, current_user: User, email: EmailStr):
    user_id = current_user.id

    is_valid = get_user_by_email(db, email)

    if is_valid is not None and is_valid.id != current_user.id:
        raise ValueError("This email already exists")
    
    return update_user(db, user_id, {"email": email})

def update_full_name(db: Session, current_user: User, full_name: str):
    user_id = current_user.id 
    return update_user(db, user_id, {"full_name": full_name})
