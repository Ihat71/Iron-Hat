from sqlalchemy import select, desc, delete
from sqlalchemy.orm import Session

from models.user import User
from models.user_biometrics import Biometric
from schemas.user_biometrics import BiometricCreate, BiometricUpdate

def add_bio(data: BiometricCreate, db: Session, user: User) -> User:
    bio = Biometric(user.id, **data.model_dump())

    db.add(bio)
    db.commit()
    db.refresh(bio)

    return bio

def get_bio(bio_id: int, db: Session):
    return db.get(Biometric, bio_id)

def get_bio_history(db: Session, user: User):

    stmt = select(Biometric).where(Biometric.user_id == user.id)
    bio_user = db.execute(stmt).scalars().all()

    return bio_user

def get_recent_bio_history(db: Session, user: User):
    stmt = select(Biometric).where(
        Biometric.user_id == user.id
    ).order_by(desc(Biometric.recorded_at))

    return db.execute(stmt).scalars().first()

def get_last_5_bio_history(db: Session, user: User):
    stmt = select(Biometric).where(
        Biometric.user_id == user.id
    ).order_by(desc(Biometric.recorded_at)).fetch(5)

    return db.execute(stmt).scalars().all()

def update_bio(bio: Biometric, update_bio_data: BiometricUpdate, db: Session):

    update_data = update_bio_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(bio, field, value) 
    #setattr is used to dynamically assign attribute values to objects

    db.commit()
    db.refresh(bio)

    return bio

def get_weight_and_bf_history(db: Session, current_user: User):
    stmt = select(
        Biometric.id,
        Biometric.weight,
        Biometric.manual_body_fat,
        Biometric.calculated_body_fat,
        Biometric.recorded_at,
        Biometric.created_at
    ).where(
        Biometric.user_id == current_user.id,
    )

    return db.execute(stmt).scalars().all()

def delete_bio(bio: Biometric, db:Session) -> bool:

    db.delete(bio)
    db.commit()

    return True
    
