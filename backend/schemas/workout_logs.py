from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkoutLogBase(BaseModel):
    program_id: int
    day_number: int
    workout_type: str


class WorkoutLogCreate(WorkoutLogBase):
    pass


class WorkoutLogUpdate(BaseModel):
    day_number: int | None = None
    workout_type: str | None = None


class WorkoutLogRead(WorkoutLogBase):
    id: int
    inserted_at: datetime

    model_config = ConfigDict(from_attributes=True)