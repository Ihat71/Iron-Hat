from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExerciseCreate(BaseModel):
    exercise_name: str

class ExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    exercise_name: str

class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None