from pydantic import BaseModel, ConfigDict


class WorkoutLogExerciseBase(BaseModel):
    workout_log_id: int
    exercise_id: int


class WorkoutLogExerciseCreate(WorkoutLogExerciseBase):
    pass


class WorkoutLogExerciseUpdate(BaseModel):
    workout_log_id: int | None = None
    exercise_id: int | None = None


class WorkoutLogExerciseRead(WorkoutLogExerciseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)