from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.models.user import User
from backend.models.user_biometrics import Biometric
from backend.schemas.user_biometrics import BiometricCreate, BiometricUpdate

async def add_bio(data: BiometricCreate, db: AsyncSession, user: User) -> User:
    bio = Biometric(
        user_id=user.id,
        **data.model_dump()
    )

    db.add(bio)
    await db.commit()
    await db.refresh(bio)

    return bio

async def get_bio(bio_id: int, db: AsyncSession):
    return await db.get(Biometric, bio_id)

async def get_bio_history(db: AsyncSession, user: User):

    stmt = select(Biometric).where(Biometric.user_id == user.id)
    result = await db.execute(stmt)
    bio_user = result.scalars().all()

    return bio_user

async def get_recent_bio_history(db: AsyncSession, user: User):
    stmt = select(Biometric).where(
        Biometric.user_id == user.id
    ).order_by(desc(Biometric.recorded_at))

    result = await db.execute(stmt)
    return result.scalars().first()

async def get_last_5_bio_history(db: AsyncSession, user: User):
    stmt = select(Biometric).where(
        Biometric.user_id == user.id
    ).order_by(desc(Biometric.recorded_at)).fetch(5)

    result = await db.execute(stmt)
    return result.scalars().all()

async def update_bio(bio: Biometric, update_bio_data: BiometricUpdate, db: AsyncSession):

    update_data = update_bio_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(bio, field, value)
    #setattr is used to dynamically assign attribute values to objects

    await db.commit()
    await db.refresh(bio)

    return bio

async def get_weight_and_bf_history(db: AsyncSession, current_user: User):
    stmt = select(Biometric).where(
        Biometric.user_id == current_user.id,
    ).order_by(Biometric.recorded_at)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_biometrics_in_range(db: AsyncSession, user: User, start: datetime, end: datetime):
    """Biometric entries recorded within [start, end), ordered oldest to newest."""
    stmt = select(Biometric).where(
        Biometric.user_id == user.id,
        Biometric.recorded_at >= start,
        Biometric.recorded_at < end,
    ).order_by(Biometric.recorded_at)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_weights_last_month(db: AsyncSession, user: User):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    stmt = select(Biometric).where(
        Biometric.user_id == user.id,
        Biometric.recorded_at >= thirty_days_ago
    ).order_by(Biometric.recorded_at)

    result = await db.execute(stmt)
    return result.scalars().all()

async def delete_bio(bio: Biometric, db: AsyncSession) -> bool:

    await db.delete(bio)
    await db.commit()

    return True
