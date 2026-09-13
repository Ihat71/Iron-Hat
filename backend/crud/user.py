from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate

async def create_user(db: AsyncSession, user: User) -> User:

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    return user

async def get_user_by_email(db: AsyncSession, user_email: EmailStr) -> User | None:

    stmt = select(User).where(User.email == user_email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    return user

async def get_user_by_username(db: AsyncSession, user_username: str) -> User | None:

    stmt = select(User).where(User.username == user_username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    return user

async def get_users(db: AsyncSession, stmt: select=None) -> list[User]:
    if not stmt:
        result = await db.execute(select(User))
    else:
        result = await db.execute(stmt)

    return result.scalars().all()


# def update_user(db: Session, user_id: int, new_data: UserUpdate):

#     stmt = update(User).where(User.user_id == user_id).values(
#         full_name=new_data.full_name,
#         username=new_data.username,
#         email=new_data.email
#     )

#     db.execute(stmt)

#     db.commit()

async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User | None:

    user = await db.get(User, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)
    #setattr is used to dynamically assign attribute values to objects

    await db.commit()
    await db.refresh(user)

    return user

async def delete_user(db: AsyncSession, user_id: int) -> bool:

    user = await db.get(User, user_id)

    if user is None:
        return False

    await db.delete(user)
    await db.commit()

    return True
