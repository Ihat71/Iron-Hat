from pydantic import BaseModel, ConfigDict


class WorkoutTemplateExerciseBase(BaseModel):
    workout_template_id: int
    exercise_id: int


class WorkoutTemplateExerciseCreate(WorkoutTemplateExerciseBase):
    pass


class WorkoutTemplateExerciseUpdate(BaseModel):
    workout_template_id: int | None = None
    exercise_id: int | None = None


class WorkoutTemplateExerciseRead(WorkoutTemplateExerciseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)