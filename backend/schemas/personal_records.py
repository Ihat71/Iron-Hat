from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum

class PRType(str, Enum):
    ONE_RM = "one_rm"
    THREE_RM = "three_rm"
    FIVE_RM = "five_rm"
    AMRAP = "amrap"
    BODYWEIGHT = "bodyweight"

class PersonalRecordCreate(BaseModel):
    user_id: int
    exercise_id: int
    exercise_history_id: int
    pr_type: PRType
    top_weight: float
    sets: int | None = None
    reps: int | None = None
    notes: str | None = None
    date: datetime

class PersonalRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    user_id: int
    exercise_id: int
    exercise_history_id: int
    pr_type: PRType
    top_weight: float
    sets: int 
    reps: int
    notes: str
    date: datetime

class PersonalRecordUpdate(BaseModel):
    pr_type: PRType 
    weight: float | None = None
    sets: int | None = None
    reps: int | None = None