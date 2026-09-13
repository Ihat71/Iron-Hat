from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from backend.crud.user import update_user, get_user_by_username, get_user_by_email
from backend.models.user import User
from backend.schemas.user import UserUpdate, UserNameUpdate
from pydantic import EmailStr


async def update_username_service(db: AsyncSession, current_user: User, user_data: UserNameUpdate):
    now = datetime.now(timezone.utc)
    account_created = current_user.created_at
    last_updated = current_user.last_updated_username
    user_id = current_user.id

    is_valid = await get_user_by_username(db, user_data.username)

    if is_valid is not None and is_valid.id != current_user.id:
        raise ValueError("This username already exists")

    difference = now - last_updated

    if account_created == last_updated or difference >= timedelta(days=14):
        update_data = UserUpdate(username=user_data.username, last_updated_username=now)
        return await update_user(db, user_id, update_data)
    else:
        raise ValueError("You can only update username every 14 days")

async def update_email_service(db: AsyncSession, current_user: User, email: EmailStr):
    user_id = current_user.id

    is_valid = await get_user_by_email(db, email)

    if is_valid is not None and is_valid.id != current_user.id:
        raise ValueError("This email already exists")

    update_data = UserUpdate(email=email)

    return await update_user(db, user_id, update_data)

async def update_full_name_service(db: AsyncSession, current_user: User, full_name: str):
    user_id = current_user.id
    update_data = UserUpdate(full_name=full_name)
    return await update_user(db, user_id, update_data)
