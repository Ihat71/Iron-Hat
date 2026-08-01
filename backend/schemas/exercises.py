from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ExerciseCreate(BaseModel):
    exercise_name: str

class ExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int
    name: str
    equipment: str
    is_variation: str
    utility_type: str
    mechanics_type: str
    force_type: str
    target_muscles:str
    main_muscle: str
    secondary_muscles: str
    difficulty: int
    synergist_muscles: str
    stabilizer_muscles: str
    antagonist_muscles: str
    dynamic_stabilizer_muscles: str
    parent_id: int

class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None

class ExerciseSearch(BaseModel):
    name: str | None = None
    force_type: str | None = None
    main_muscle: str | None = None
    difficulty: str | None = None

