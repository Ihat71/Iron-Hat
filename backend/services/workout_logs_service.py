from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.crud.workout_logs import (create_workout_log,
        delete_workout_log, get_workout_log,
        get_user_workout_logs, get_user_workout_logs_by_program,
        get_all_user_workout_logs, get_user_workout_logs_by_value,
        )
from backend.services.personal_records_service import check_and_add_pr_service
from backend.crud.workout_templates import get_workout_template
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_logs import WorkoutLog
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogUpdate, SearchLogs
from backend.schemas.personal_records import PersonalRecordCreate
from backend.models.workout_log_exercises import WorkoutLogExercise
from typing import Any

async def is_valid(db: AsyncSession, user: User, workout_id: int, program_id: int):
    #this is fine but redundant ngl
    workout = await get_workout_log(program_id, workout_id, db, user)
    if workout:
        program = await get_program(db, workout.program_id)
    else:
        return False

    if program.user_id != user.id:
        return False

    return True

async def add_workout_log_service(db: AsyncSession, data: WorkoutLogCreate, program_id: int, user: User):
    template = await get_workout_template(db, data.workout_template_id, program_id)
    if not template:
        data.workout_template_id = None
    workout_log_data = WorkoutLog(
        program_id = program_id,
        workout_template_id = data.workout_template_id,
        notes = data.notes
    )
    for exercise in data.exercises:
        exercise_data = WorkoutLogExercise(**exercise.model_dump())
        workout_log_data.exercises.append(exercise_data)

    workout_log = await create_workout_log(db, workout_log_data)
    #this part of the code checks for PRs from the exercises and adds them if they are in fact PRs
    for exercise in workout_log.exercises:
        exercise_history = exercise.exercise_history
        for detailed_set in exercise_history.detailed_sets:
            record = PersonalRecordCreate(
                exercise_id=exercise_history.exercise_id,
                exercise_history_id=exercise_history.id,
                pr_type="1rm",
                reps=detailed_set.reps,
                top_weight=detailed_set.top_weight,
            )
            await check_and_add_pr_service(record, exercise_history.exercise_type, db, user)

    return workout_log


async def get_workout_log_service(program_id: int, workout_id: int, db: AsyncSession, user: User):
    log = await get_workout_log(program_id, workout_id, db, user)
    if not log:
        raise ValueError("There was an error: cant access or doesn't exist")

async def get_workout_log_by_value_service(db: AsyncSession, type: str, value: Any, program_id: int, user: User):
    return await get_user_workout_logs_by_value(db, type, value, program_id, user.id)

async def get_all_workout_logs_service(db: AsyncSession, program_id: int, user: User):
    return await get_all_user_workout_logs(db, program_id)

async def get_workout_logs_service(db: AsyncSession, program_id: int, user: User):
    return await get_user_workout_logs_by_program(db, user.id, program_id)

# def update_workout_log_service(db: Session, data: WorkoutLogUpdate, workout_id: int, program_id: int, user: User):
#     if not is_valid(db, user, workout_id, program_id):
#         raise ValueError("cant access that")

#     return update_workout_log(db, workout_id, data)


async def delete_workout_log_service(program_id: int, workout_id: int, db: AsyncSession, user: User):
    if not await is_valid(db, user, workout_id, program_id):
        raise ValueError("cant access that")

    return await delete_workout_log(db, workout_id)

async def delete_workout_log_exercise_service(program_id: int, workout_id: int, exercise_id: int, db: AsyncSession, user: User):
    if not await is_valid(db, user, workout_id, program_id):
        raise ValueError("cant access that")

    workout = await get_workout_log(program_id, workout_id, db, user)
    if not workout:
        raise ValueError("Workout log not found")

    exercise_to_delete = next((ex for ex in workout.exercises if ex.id == exercise_id), None)
    if not exercise_to_delete:
        raise ValueError("Exercise log not found in this workout")

    workout.exercises.remove(exercise_to_delete)
    await db.commit()
    await db.refresh(workout)

    return True
