from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.schemas.exercises import ExerciseRead


class TrackedExerciseCreate(BaseModel):
    exercise_id: int


class TrackedExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    program_id: int
    exercise_id: int
    exercise: ExerciseRead
    created_at: datetime
