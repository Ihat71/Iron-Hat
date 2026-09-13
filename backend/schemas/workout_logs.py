from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from backend.schemas.workout_log_exercises import WorkoutLogExerciseCreate, WorkoutLogExerciseUpdate, WorkoutLogExerciseRead




class WorkoutLogCreate(BaseModel):
    workout_template_id: int | None = None
    notes: str | None = None
    exercises: list[WorkoutLogExerciseCreate] = Field(default_factory=list)


class WorkoutLogUpdate(BaseModel):
    notes: str | None = None
    exercises: list[WorkoutLogExerciseUpdate] | None = None


class WorkoutLogRead(BaseModel):
    program_id: int
    workout_template_id: int | None = None
    id: int
    notes: str | None
    inserted_at: datetime
    exercises: list[WorkoutLogExerciseRead] 
    model_config = ConfigDict(from_attributes=True)

class SearchLogs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    day_number: int | None = None
    workout_type: str | None = None