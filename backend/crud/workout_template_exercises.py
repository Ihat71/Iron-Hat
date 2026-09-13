from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.program_templates import ProgramTemplates
from backend.models.workout_templates import WorkoutTemplate
from backend.models.workout_template_exercises import WorkoutTemplateExercise
from backend.schemas.workout_template_exercises import WorkoutTemplateExerciseCreate, WorkoutTemplateExerciseUpdate, WorkoutTemplateExerciseRead
from typing import Any


async def create_workout_template_exercise(db: AsyncSession, exercise_data: list[WorkoutTemplateExercise]) -> WorkoutTemplateExercise:
    for exercise in exercise_data:
        db.add(exercise)
    await db.commit()
    await db.refresh(exercise_data[-1])

    return exercise_data[-1]

async def get_workout_template_exercise(db: AsyncSession, exercise_id: int) -> WorkoutTemplateExercise:
    return await db.get(WorkoutTemplateExercise, exercise_id)

async def get_workout_template_exercises_by_workout_id(workout_id: int, db: AsyncSession) -> list[WorkoutTemplateExerciseRead]:
    stmt = select(WorkoutTemplateExercise).where(WorkoutTemplateExercise.workout_template_id == workout_id)
    execute_result = await db.execute(stmt)
    result = execute_result.scalars().all()

    return [WorkoutTemplateExerciseRead.model_validate(exercise) for exercise in result]

async def get_all_workout_template_exercises(db: AsyncSession) -> list[WorkoutTemplateExercise] :

    result = await db.execute(select(WorkoutTemplateExercise))

    return result.scalars().all()

async def get_all_user_workout_template_exercises(db: AsyncSession, user_id):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_template_exercises(db: AsyncSession, user_id: int, template_exercise: WorkoutTemplateExercise) -> list[WorkoutTemplateExercise]:
    stmt = select(WorkoutTemplateExercise).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutTemplateExercise.id == template_exercise.workout_template_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_template_exercises_by_program(db: AsyncSession, user_id: int, program_id: int):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_template_exercises_by_workout_value(db: AsyncSession, user_id: int, workout_id: int):
    stmt = select(WorkoutTemplateExercise).join(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutTemplate.id == workout_id)
    result = await db.execute(stmt)
    return result.scalars().all()

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


async def delete_workout_template_exercise(db: AsyncSession, exercise_id: int) -> bool:
    exercise = await db.get(WorkoutTemplateExercise, exercise_id)

    if exercise is None:
        return False

    await db.delete(exercise)
    await db.commit()

    return True
