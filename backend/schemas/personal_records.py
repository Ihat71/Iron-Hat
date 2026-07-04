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
    exercise_id: int
    pr_type: PRType
    weight: float
    sets: int | None = None
    reps: int | None = None

class PersonalRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    user_id: int
    exercise_id: int
    pr_type: str
    weight: float
    sets: int | None=None
    reps: int | None=None

class PersonalRecordUpdate(BaseModel):
    pr_type: str | None = None
    weight: float | None = None
    sets: int | None = None
    reps: int | None = None