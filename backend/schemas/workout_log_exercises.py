from pydantic import BaseModel, ConfigDict, Field
from backend.schemas.exercise_history import ExerciseHistoryUpdate
from backend.schemas.exercises import ExerciseRead


class WorkoutLogExerciseBase(BaseModel):
    workout_log_id: int
    exercise_id: int


class WorkoutLogExerciseCreate(BaseModel):
    exercise_id: int


class WorkoutLogExerciseUpdate(BaseModel):
    id: int
    exercise_id: int | None = None
    exercise_history: ExerciseHistoryUpdate | None = None

class WorkoutLogExerciseRead(WorkoutLogExerciseBase):
    id: int
    exercise_id: int
    exercise: ExerciseRead

    model_config = ConfigDict(from_attributes=True)