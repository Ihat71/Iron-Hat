from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExerciseHistoryBase(BaseModel):
    workout_log_exercise_id: int
    top_weight: float
    max_reps: int
    total_volume: float
    detailed_sets: dict | None = None
    max_rpe: float | None = None
    notes: str | None = None


class ExerciseHistoryCreate(ExerciseHistoryBase):
    pass


class ExerciseHistoryRead(ExerciseHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ExerciseHistoryUpdate(BaseModel):
    top_weight: float | None = None
    max_reps: int | None = None
    total_volume: float | None = None
    detailed_sets: dict | None = None
    max_rpe: float | None = None
    notes: str | None = None