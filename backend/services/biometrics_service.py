from sqlalchemy.orm import Session
from datetime import datetime

from backend.crud.user_biometrics import (
    add_bio, get_bio, get_bio_history, get_recent_bio_history,
    get_last_5_bio_history, update_bio, delete_bio
)
from backend.models.user import User
from backend.models.user_biometrics import Biometric
from backend.schemas.user_biometrics import BiometricCreate, BiometricUpdate
from typing import Any

def add_bio_service(data: BiometricCreate, db: Session, user: User):
    # add a bodyfat calculation method to this part later
    return add_bio(data, db, user)


def get_bio_history_service(db: Session, user: User):
    return get_bio_history(db, user)

def get_recent_bio_history_service(db: Session, user: User):
    return get_recent_bio_history(db, user)

def get_last_5_bio_history_service(db: Session, user: User):
    return get_last_5_bio_history(db, user)

def update_recent_bio_service(bio_id, update_data: BiometricUpdate, db: Session, user: User): 
    bio = get_bio(bio_id, db)
    if bio.user_id != user.id:
        raise ValueError("authorization issue")
    
    return update_bio(bio, update_data, db)

def delete_bio_service(bio_id, db: Session, user: User):
    bio = get_bio(bio_id, db)
    if bio.user_id != user.id:
        raise ValueError("authorization issue")
    
    return delete_bio(bio, db)