from pydantic import BaseModel, ConfigDict
from backend.schemas.exercises import ExerciseRead

class WorkoutTemplateExerciseBase(BaseModel):
    exercise_id: int
    

class WorkoutTemplateExerciseCreate(WorkoutTemplateExerciseBase):
    pass


class WorkoutTemplateExerciseUpdate(BaseModel):
    workout_template_id: int | None = None
    exercise_id: int | None = None


class WorkoutTemplateExerciseRead(WorkoutTemplateExerciseBase):
    id: int
    exercise_id: int
    exercise: ExerciseRead

    model_config = ConfigDict(from_attributes=True)