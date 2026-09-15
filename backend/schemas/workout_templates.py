from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.schemas.workout_template_exercises import WorkoutTemplateExerciseCreate, WorkoutTemplateExerciseRead
from enum import Enum

class WType(str, Enum):
    PUSH = "push_day"
    PULL =  "pull_day"
    LEGS = "leg_day"
    UPPER = "upper"
    LOWER = "lower"
    FULLBODY = "full_body"
    CUSTOM = "custom"

class WorkoutTemplateCreate(BaseModel):
    day_number: int
    workout_type: WType
    days_of_week: list[int] | None = None
    exercises: list[WorkoutTemplateExerciseCreate] = Field(default_factory=list)

class WorkoutTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    program_id: int
    day_number: int | None=None
    workout_type: WType | None = None
    days_of_week: list[int] | None = None
    inserted_at: datetime
    exercises: list[WorkoutTemplateExerciseRead] = Field(default_factory=list)


class WorkoutTemplateUpdate(BaseModel):
    day_number: int | None = None
    workout_type: WType | None = None
    days_of_week: list[int] | None = None
    exercises: list[WorkoutTemplateExerciseCreate] | None = None