from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExerciseHistoryCreate(BaseModel):
    workout_id: int
    exercise_id: int
    top_weight: float
    top_rpe: float
    top_reps: float
    detailed_sets: dict

class ExerciseHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    workout_id: int
    exercise_id: int
    top_weight: float
    top_rpe: float
    top_reps: float
    detailed_sets: dict
    time: datetime

class ExerciseHistoryUpdate(BaseModel):
    workout_id: int | None = None
    exercise_id: int | None = None
    top_weight: float | None = None
    top_rpe: float | None = None
    top_reps: float | None = None
    detailed_sets: dict | None = None