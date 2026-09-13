from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.core.enums import PRType

class PersonalRecordCreate(BaseModel):
    exercise_id: int
    exercise_history_id: int | None = None
    pr_type: PRType
    top_weight: float
    reps: int | None = None
    notes: str | None = None
    date: datetime | None = None

class PersonalRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id: int
    user_id: int
    exercise_id: int
    exercise_history_id: int
    pr_type: PRType
    top_weight: float 
    reps: int
    notes: str
    date: datetime
    created_at: datetime

class PersonalRecordUpdate(BaseModel):
    pr_type: PRType 
    weight: float | None = None
    reps: int | None = None
    date: datetime | None = None

class SearchPR(BaseModel):
    exercise_id: int | None = None
    pr_type: PRType | None = None
