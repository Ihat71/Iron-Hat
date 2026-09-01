from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.core.enums import ExType
    
class DetailedSets(BaseModel):
    weight: float = Field(ge=0)
    reps: int = Field(gt=0)
    rpe: float | None = Field(default=None, ge=0, le=10)
    set_number: int | None = Field(default=None, ge=0, le=10)

class ExerciseHistorySearch(BaseModel):
    exercise_id: int | None = None
    exercise_type: ExType | None = None
    
class ExerciseHistoryBase(BaseModel):
    workout_log_exercise_id: int
    exercise_type: ExType | None = None
    top_weight: float
    max_reps: int
    sets: int
    detailed_sets: list[DetailedSets] | None = None
    max_rpe: float | None = None
    notes: str | None = None


class ExerciseHistoryCreate(BaseModel):
    exercise_id: int
    workout_log_exercise_id: int |  None = None
    exercise_type: ExType | None = None
    top_weight: float
    reps: int
    sets: int
    detailed_sets: list[DetailedSets] | None = None
    max_rpe: float | None = None
    notes: str | None = None

class ExerciseHistoryRead(ExerciseHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ExerciseHistoryUpdate(BaseModel):
    id: int
    top_weight: float | None = None
    reps: int | None = None
    detailed_sets: dict | None = None
    max_rpe: float | None = None
    notes: str | None = None
    exercise_type: ExType | None = None


