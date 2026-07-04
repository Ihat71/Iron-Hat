from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkoutExerciseCreate(BaseModel):
    workout_id: int
    exercise_id: int

class WorkoutExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    workout_id: int
    exercise_id: int

class WorkoutExerciseUpdate(BaseModel):
    exercise_id: int | None = None