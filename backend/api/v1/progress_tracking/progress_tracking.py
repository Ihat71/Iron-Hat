from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.progress_tracking import (
    get_weight_and_bf_history_service, 
    get_pr_tracking_service,
    get_exercise_history_service,
    get_extra_biometrics_service,
    get_workout_history_service,
    get_tracking_summary

)
from backend.schemas.tracking import WeightTracking
from backend.models.user import User

"""
Requirements for this route:
this route is supposed to be a place where all the data gets tracked in a
convenient place
1- simple weight and bf% history and tracking over time
2- advanced biometrics tracking 
3- PR tracking on important lifts
4- workouts shown like the github thing with an added detailed section
5- small weekly and monthly summary card
6- tracking excercise history
"""

router = APIRouter(
    prefix="/tracking",
    tags=["Tracking"]
)

@router.get("/weight", response_model=list[WeightTracking], status_code=status.HTTP_200_OK)
def get_weight_and_bf_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_weight_and_bf_history_service(db, current_user)

@router.get("/weight/extra", status_code=status.HTTP_200_OK)
def get_extra_biometrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_extra_biometrics_service(db, current_user)

@router.get("/pr-records", status_code=status.HTTP_200_OK)
def get_pr_tracking(exercises: list[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_tracking_service(exercises, db, current_user)

@router.get("/workouts", status_code=status.HTTP_200_OK)
def get_workout_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_history_service(db, current_user)

@router.get("/exercises/{exercise_id}", status_code=status.HTTP_200_OK)
def get_exercise_history(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_exercise_history_service(exercise_id, db, current_user)

@router.get("/summary/{program_id}", status_code=status.HTTP_200_OK)
def get_summary(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tracking_summary(program_id, db, current_user)

