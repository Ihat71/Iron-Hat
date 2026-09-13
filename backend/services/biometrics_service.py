from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from backend.crud.user_biometrics import (
    add_bio, get_bio, get_bio_history, get_recent_bio_history,
    get_last_5_bio_history, update_bio, delete_bio
)
from backend.models.user import User
from backend.models.user_biometrics import Biometric
from backend.schemas.user_biometrics import BiometricCreate, BiometricUpdate
from typing import Any

async def add_bio_service(data: BiometricCreate, db: AsyncSession, user: User):
    # add a bodyfat calculation method to this part later
    return await add_bio(data, db, user)


async def get_bio_history_service(db: AsyncSession, user: User):
    return await get_bio_history(db, user)

async def get_recent_bio_history_service(db: AsyncSession, user: User):
    return await get_recent_bio_history(db, user)

async def get_last_5_bio_history_service(db: AsyncSession, user: User):
    return await get_last_5_bio_history(db, user)

async def update_recent_bio_service(bio_id, update_data: BiometricUpdate, db: AsyncSession, user: User):
    bio = await get_bio(bio_id, db)
    if bio.user_id != user.id:
        raise ValueError("authorization issue")

    return await update_bio(bio, update_data, db)

async def delete_bio_service(bio_id, db: AsyncSession, user: User):
    bio = await get_bio(bio_id, db)
    if bio.user_id != user.id:
        raise ValueError("authorization issue")

    return await delete_bio(bio, db)
