from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.crud.workout_templates import (create_workout_template,
update_workout_template, delete_workout_template,
get_workout_template, get_user_workout_templates,
get_user_workout_template_by_value, get_all_user_workout_templates, get_all_user_workout_templates_by_program_id)
from backend.crud.workout_template_exercises import create_workout_template_exercise, get_workout_template_exercises_by_workout_id
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.models.workout_template_exercises import WorkoutTemplateExercise
from backend.schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateUpdate, WorkoutTemplateRead
from typing import Any

async def is_valid(db: AsyncSession, user_id: int, workout_id: int, program_id: int) -> bool:
    workout = await get_workout_template(db, workout_id, program_id)
    if not workout:
        raise ValueError("workout does not exist or cant be authorized")
    program = await get_program(db, workout.program_id)

    if not program:
        raise ValueError("program does not exist")
    if program.user_id != user_id:
        return False

    if  program.id != program_id:
        return False

    return True

async def add_workout_template_service(db: AsyncSession, data: WorkoutTemplateCreate, program_id: int, user: User):
    program = await get_program(db, program_id)

    if program.user_id != user.id:
        raise ValueError("cannot access that")



    workout_data = WorkoutTemplate(
        program_id = program_id,
        day_number = data.day_number,
        workout_type = data.workout_type
    )
    created_template = await create_workout_template(db, workout_data)

    exercises_data = [
        WorkoutTemplateExercise(workout_template_id=created_template.id, **exercise.model_dump())
        for exercise in data.exercises
    ]

    # exercises_data = [
    #     WorkoutTemplateExercise(workout_template_id=created_template.id, **exercise.model_dump())
    #     for exercise in data.exercises
    # ]

    created_exercises = await create_workout_template_exercise(db, exercises_data)

    return created_template

# def get_workout_templates_by_program_service(db: Session, user: User, program_id: int):
#     return get_user_workout_template_by_value(db, user.id, "program_id", program_id)

# def get_workout_templates_by_day_service(db: Session, user: User, day: int):
#     return get_user_workout_template_by_value(db, user.id, "day_number", day)

# def get_workout_templates_by_type_service(db: Session, user: User, type: str):
#     return get_user_workout_template_by_value(db, user.id, "workout_type", type)

async def get_workout_template_by_params_service(program_id: int, workout_type: str | None, day_number: int | None, db: AsyncSession, user: User):
    return await get_user_workout_template_by_value(db, workout_type, day_number, program_id, user.id)

async def get_all_workout_templates_service(program_id: int, db: AsyncSession, user: User):

    workout_templates = await get_all_user_workout_templates_by_program_id(db, user.id, program_id)
    workout_read_list = []
    for workout in workout_templates:
        exercises = await get_workout_template_exercises_by_workout_id(workout.id, db)
        workout_read = WorkoutTemplateRead(
            id=workout.id,
            program_id=workout.program_id,
            day_number=workout.day_number,
            workout_type=workout.workout_type,
            inserted_at=workout.inserted_at,
            exercises=exercises
        )
        workout_read_list.append(workout_read)

    return workout_read_list

async def get_workout_template_service(db: AsyncSession, program_id: int, workout_id: int, user: User):

    return await get_workout_template(db, workout_id, program_id)

async def update_workout_template_service(db: AsyncSession, data: WorkoutTemplateUpdate, program_id: int, workout_id: int, user: User):
    if not await is_valid(db, user.id, workout_id, program_id):
        raise ValueError("cant access that")

    return await update_workout_template(db, workout_id, data)

async def delete_workout_template_service(db: AsyncSession, program_id: int, workout_id: int, user: User):
    if not await is_valid(db, user.id, workout_id, program_id):
        raise ValueError("cant access that")

    return await delete_workout_template(db, workout_id)
