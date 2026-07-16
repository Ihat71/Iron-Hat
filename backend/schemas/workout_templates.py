from datetime import datetime
from pydantic import BaseModel, ConfigDict
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
    program_id: int
    day_number: int
    workout_type: WType

class WorkoutTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int 
    program_id: int 
    day_number: int 
    workout_type: WType 
    inserted_at: datetime 

class WorkoutTemplateUpdate(BaseModel):
    day_number: int | None = None
    workout_type: WType | None = None