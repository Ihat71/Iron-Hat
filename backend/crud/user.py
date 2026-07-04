from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import EmailStr
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user_data: UserCreate) -> User:
    
    user = User(
        full_name=user_data.full_name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=user_data.password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_users(db: Session) -> list[User]:
    stmt = select(User)
    return db.execute(stmt).scalars().all()

def get_user_by_email(db: Session, user_email: EmailStr) -> User | None:

    stmt = select(User).where(User.email == user_email)
    user = db.execute(stmt).scalar_one_or_none()

    return user

def get_user_by_username(db: Session, user_username: str) -> User | None:
    
    stmt = select(User).where(User.username == user_username)
    user = db.execute(stmt).scalar_one_or_none()

    return user

def get_users(db: Session, stmt: select=None) -> list[User]:
    if not stmt:
        result = db.execute(select(User)).scalars().all()
    else:
        result = db.execute(stmt).scalars().all()

    return result
    

# def update_user(db: Session, user_id: int, new_data: UserUpdate):
    
#     stmt = update(User).where(User.user_id == user_id).values(
#         full_name=new_data.full_name,
#         username=new_data.username,
#         email=new_data.email
#     )

#     db.execute(stmt)

#     db.commit()

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:

    user = db.get(User, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value) 
    #setattr is used to dynamically assign attribute values to objects

    db.commit()
    db.refresh(user)

    return user

def delete_user(db:Session, user_id: int) -> bool:

    user = db.get(User, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True

