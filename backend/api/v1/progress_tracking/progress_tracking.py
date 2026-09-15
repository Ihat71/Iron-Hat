from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.api.dependencies import get_current_user, get_current_program
from backend.services.progress_tracking import (
    get_weight_and_bf_history_service,
    get_extra_biometrics_service,
    get_body_composition_change_service,
    add_tracked_exercise_service,
    list_tracked_exercises_service,
    remove_tracked_exercise_service,
    get_program_overload_service,
    get_consistency_matrix_service,
    get_streak_service,
    get_weekly_summary_service,
    get_monthly_summary_service,
    get_pr_tracking_service,
    get_exercise_history_service,
    get_workout_history_service,
)
from backend.schemas.tracking import (
    WeightTracking,
    BodyCompositionChange,
    ExerciseOverloadTrend,
    ConsistencyMatrix,
    StreakInfo,
    PeriodSummary,
)
from backend.schemas.tracked_exercises import TrackedExerciseCreate, TrackedExerciseRead
from backend.models.user import User
from backend.models.program_templates import ProgramTemplates

"""
Progress tracking, scoped per program (each program tracks its own consistency/overload):
1- weight and body fat history + change over a period
2- weekly / monthly summary: weight & bf change, workout consistency, PRs, progressive overload, streaks
3- a monthly consistency matrix (github-style) built from the program's workout templates vs logged workouts
4- progressive overload tracking on user-selected exercises (estimated 1RM trend)
5- current/longest workout streaks
"""

router = APIRouter(
    prefix="/tracking/{program_id}",
    tags=["Tracking"]
)


@router.get("/weight", response_model=list[WeightTracking], status_code=status.HTTP_200_OK)
async def get_weight_and_bf_history(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_weight_and_bf_history_service(db, current_user)


@router.get("/weight/extra", status_code=status.HTTP_200_OK)
async def get_extra_biometrics(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_extra_biometrics_service(db, current_user)


@router.get("/weight/change", response_model=BodyCompositionChange, status_code=status.HTTP_200_OK)
async def get_body_composition_change(
    start: date,
    end: date,
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_body_composition_change_service(db, current_user, start, end)


@router.post("/tracked-exercises", response_model=TrackedExerciseRead, status_code=status.HTTP_201_CREATED)
async def add_tracked_exercise(
    data: TrackedExerciseCreate,
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await add_tracked_exercise_service(db, program, data.exercise_id)


@router.get("/tracked-exercises", response_model=list[TrackedExerciseRead], status_code=status.HTTP_200_OK)
async def list_tracked_exercises(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await list_tracked_exercises_service(db, program)


@router.delete("/tracked-exercises/{tracked_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tracked_exercise(
    tracked_id: int,
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await remove_tracked_exercise_service(db, program, tracked_id)


@router.get("/overload", response_model=list[ExerciseOverloadTrend], status_code=status.HTTP_200_OK)
async def get_overload(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_program_overload_service(db, current_user, program)


@router.get("/consistency/{year}/{month}", response_model=ConsistencyMatrix, status_code=status.HTTP_200_OK)
async def get_consistency_matrix(
    year: int,
    month: int,
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_consistency_matrix_service(db, current_user, program, year, month)


@router.get("/streak", response_model=StreakInfo, status_code=status.HTTP_200_OK)
async def get_streak(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_streak_service(db, current_user, program)


@router.get("/summary/weekly", response_model=PeriodSummary, status_code=status.HTTP_200_OK)
async def get_weekly_summary(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_weekly_summary_service(db, current_user, program)


@router.get("/summary/monthly", response_model=PeriodSummary, status_code=status.HTTP_200_OK)
async def get_monthly_summary(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_monthly_summary_service(db, current_user, program)


@router.get("/pr-records", status_code=status.HTTP_200_OK)
async def get_pr_tracking(
    exercises: list[int],
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_pr_tracking_service(exercises, db, current_user)


@router.get("/workouts", status_code=status.HTTP_200_OK)
async def get_workout_history(
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_workout_history_service(program.id, db, current_user)


@router.get("/exercises/{exercise_history_id}", status_code=status.HTTP_200_OK)
async def get_exercise_history(
    exercise_history_id: int,
    program: ProgramTemplates = Depends(get_current_program),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_exercise_history_service(exercise_history_id, db, current_user)
