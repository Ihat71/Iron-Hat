from sqlalchemy import select
from sqlalchemy.orm import Session

from models.program_templates import ProgramTemplates
from models.workout_templates import WorkoutTemplate
from models.workout_template_exercises import WorkoutTemplateExercise
from schemas.workout_template_exercises import WorkoutTemplateExerciseCreate, WorkoutTemplateExerciseUpdate
from typing import Any


def create_workout_template_exercise(db: Session, exercise_data: WorkoutTemplateExerciseCreate) -> WorkoutTemplateExercise:
    exercise = WorkoutTemplateExercise(**exercise_data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_workout_template_exercise(db: Session, exercise_id: int) -> WorkoutTemplateExercise:
    return db.get(WorkoutTemplateExercise, exercise_id)

def get_all_workout_template_exercises(db: Session) -> list[WorkoutTemplateExercise] :

    results = db.execute(select(WorkoutTemplateExercise)).scalars().all()

    return results

def get_all_user_workout_template_exercises(db: Session, user_id):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_template_exercises(db: Session, user_id: int, template_exercise: WorkoutTemplateExercise) -> list[WorkoutTemplateExercise]:
    stmt = select(WorkoutTemplateExercise).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutTemplateExercise.id == template_exercise.workout_template_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_template_exercises_by_program(db: Session, user_id: int, program_id: int):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_template_exercises_by_workout_value(db: Session, user_id: int, workout_id: int):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutTemplate.id == workout_id)
    return db.execute(stmt).scalars().all()

# def update_workout_template_exercise(db: Session, exercise_id: int, exercise_data: WorkoutTemplateExerciseUpdate) -> WorkoutTemplateExercise | None:
#     workout = db.get(WorkoutTemplateExercise, exercise_id)

#     if workout is None:
#         return None

#     update_data = exercise_data.model_dump(exclude_unset=True, exclude={"id"})

#     for field, value in update_data.items():
#         setattr(workout, field, value)

#     db.commit()
#     db.refresh(workout)

#     return workout


def delete_workout_template_exercise(db: Session, exercise_id: int) -> bool:
    exercise = db.get(WorkoutTemplateExercise, exercise_id)

    if exercise is None:
        return False

    db.delete(exercise)
    db.commit()

    return True