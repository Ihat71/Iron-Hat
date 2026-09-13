from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_template_exercises import WorkoutTemplateExercise
from backend.schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateUpdate
from typing import Any

VALID_COLUMNS = [
    "day_number",
    "workout_type",
]

async def create_workout_template(db: AsyncSession, workout: WorkoutTemplate) -> WorkoutTemplate:


    db.add(workout)
    await db.commit()
    await db.refresh(workout)

    return workout


async def get_workout_template(db: AsyncSession, workout_id: int | None, program_id: int) -> WorkoutTemplate | None:
    stmt = select(WorkoutTemplate).options(selectinload(WorkoutTemplate.exercises)).where((WorkoutTemplate.id == workout_id) & (WorkoutTemplate.program_id == program_id))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_workout_templates(db: AsyncSession) -> list[WorkoutTemplate] :

    result = await db.execute(select(WorkoutTemplate))

    return result.scalars().all()

async def get_all_user_workout_templates(db: AsyncSession, user_id: int):
    stmt = select(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_all_user_workout_templates_by_program_id(db: AsyncSession, user_id: int, program_id: int):
    stmt = select(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_templates(db: AsyncSession, user_id: int, program_id: int) -> list[WorkoutTemplate]:
    stmt = select(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_workout_template_by_value(db: AsyncSession, workout_type: str | None, day_number: int | None, program_id: int, user_id: int) -> list[WorkoutTemplate]:

    stmt = select(WorkoutTemplate).where(
        WorkoutTemplate.program_id == program_id
    )

    if workout_type is not None:
        stmt = stmt.where(WorkoutTemplate.workout_type == workout_type)
    if day_number is not None:
        stmt = stmt.where(WorkoutTemplate.day_number == day_number)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workout_template_target_consistency_per_week(program_id: int, db: AsyncSession, current_user: User):
    stmt = select(func.count(WorkoutTemplate.id)).join(ProgramTemplates).where(ProgramTemplates.user_id == current_user.id, WorkoutTemplate.program_id == program_id)
    return await db.scalar(stmt)


async def update_workout_template(db: AsyncSession, workout_id: int, workout_data: WorkoutTemplateUpdate) -> WorkoutTemplate | None:
    stmt = select(WorkoutTemplate).options(selectinload(WorkoutTemplate.exercises)).where(WorkoutTemplate.id == workout_id)
    result = await db.execute(stmt)
    workout = result.scalar_one_or_none()

    if workout is None:
        return None



    update_data = workout_data.model_dump(
        exclude_unset=True,
        exclude={"exercises"},
    )

    for field, value in update_data.items():
        setattr(workout, field, value)

    if workout_data.exercises is not None:
        workout.exercises.clear()

        for exercise in workout_data.exercises:
            new_exercise = WorkoutTemplateExercise(workout_template_id=workout.id, **exercise.model_dump())
            workout.exercises.append(new_exercise)



    await db.commit()
    await db.refresh(workout)

    return workout


async def delete_workout_template(db: AsyncSession, workout_id: int) -> bool:
    workout = await db.get(WorkoutTemplate, workout_id)

    if workout is None:
        return False

    await db.delete(workout)
    await db.commit()

    return True
