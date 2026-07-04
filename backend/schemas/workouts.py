from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkoutCreate(BaseModel):
    day_number: int
    workout_type: str

class WorkoutRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    user_id: int
    day_number: int
    workout_type: str
    inserted_at: datetime

class WorkoutUpdate(BaseModel):
    day_number: int | None = None
    workout_type: str | None = None