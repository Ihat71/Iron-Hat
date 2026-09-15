import calendar
from collections import Counter
from datetime import date, datetime, timedelta, UTC

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.crud.user_biometrics import get_bio_history, get_biometrics_in_range
from backend.crud.personal_records import get_pr_history, get_pr_count_in_range
from backend.crud.exercise_history import get_exercise_history, get_exercise_history_for_program_exercise
from backend.crud.workout_logs import get_workout_logs_in_range, get_all_workout_log_dates
from backend.crud.workout_log_exercises import get_user_workout_log_exercise_by_workout
from backend.crud.workout_templates import get_scheduled_weekdays_for_program
from backend.crud.workout_template_exercises import get_user_workout_template_exercises_by_workout_value
from backend.crud.tracked_exercises import (
    create_tracked_exercise,
    get_tracked_exercise,
    get_tracked_exercises_by_program,
    delete_tracked_exercise,
)
from backend.schemas.tracking import (
    BodyCompositionChange,
    OverloadPoint,
    ExerciseOverloadTrend,
    ConsistencyDay,
    ConsistencyMatrix,
    StreakInfo,
    PeriodSummary,
)


def _to_date(value: datetime | date) -> date:
    return value.date() if isinstance(value, datetime) else value


def _day_bounds_utc(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, tzinfo=UTC)


def _estimated_1rm(weight: float, reps: int) -> float:
    """Epley formula. A single-rep set is already the 1RM."""
    if reps <= 1:
        return weight
    return weight * (1 + reps / 30)


def _current_week_bounds() -> tuple[date, date]:
    today = date.today()
    start = today - timedelta(days=today.weekday())  # Monday
    end = start + timedelta(days=7)
    return start, end


def _current_month_bounds() -> tuple[date, date]:
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    start = date(today.year, today.month, 1)
    end = date(today.year, today.month, last_day) + timedelta(days=1)
    return start, end


# --- Weight / body fat -----------------------------------------------------

async def get_weight_and_bf_history_service(db: AsyncSession, current_user: User):
    return await get_bio_history(db, current_user)


async def get_extra_biometrics_service(db: AsyncSession, current_user: User):
    return await get_bio_history(db, current_user)


async def get_body_composition_change_service(
    db: AsyncSession, current_user: User, start: date, end: date
) -> BodyCompositionChange:
    entries = await get_biometrics_in_range(db, current_user, _day_bounds_utc(start), _day_bounds_utc(end))

    result = BodyCompositionChange(period_start=start, period_end=end)
    if not entries:
        return result

    def body_fat(entry):
        return entry.manual_body_fat if entry.manual_body_fat is not None else entry.calculated_body_fat

    weights = [e.weight for e in entries]
    body_fats = [(e, body_fat(e)) for e in entries if body_fat(e) is not None]

    result.start_weight = entries[0].weight
    result.end_weight = entries[-1].weight
    result.weight_change = result.end_weight - result.start_weight
    result.lowest_weight = min(weights)
    result.highest_weight = max(weights)

    if body_fats:
        result.start_body_fat = body_fats[0][1]
        result.end_body_fat = body_fats[-1][1]
        result.body_fat_change = result.end_body_fat - result.start_body_fat

    return result


# --- Tracked exercises -------------------------------------------------------

async def add_tracked_exercise_service(db: AsyncSession, program: ProgramTemplates, exercise_id: int):
    return await create_tracked_exercise(db, program.id, exercise_id)


async def list_tracked_exercises_service(db: AsyncSession, program: ProgramTemplates):
    return await get_tracked_exercises_by_program(db, program.id)


async def remove_tracked_exercise_service(db: AsyncSession, program: ProgramTemplates, tracked_id: int):
    tracked = await get_tracked_exercise(db, program.id, tracked_id)
    if tracked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracked exercise not found")

    return await delete_tracked_exercise(db, tracked)


# --- Progressive overload ----------------------------------------------------

async def get_program_overload_service(
    db: AsyncSession,
    current_user: User,
    program: ProgramTemplates,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[ExerciseOverloadTrend]:
    tracked = await get_tracked_exercises_by_program(db, program.id)

    trends = []
    for entry in tracked:
        history = await get_exercise_history_for_program_exercise(
            db, current_user, program.id, entry.exercise_id, start, end
        )

        points = [
            OverloadPoint(
                date=h.created_at,
                top_weight=h.top_weight,
                max_reps=h.max_reps,
                estimated_1rm=_estimated_1rm(h.top_weight, h.max_reps),
            )
            for h in history
        ]

        trends.append(
            ExerciseOverloadTrend(
                exercise_id=entry.exercise_id,
                exercise_name=entry.exercise.name,
                points=points,
                starting_e1rm=points[0].estimated_1rm if points else None,
                latest_e1rm=points[-1].estimated_1rm if points else None,
                e1rm_change=(points[-1].estimated_1rm - points[0].estimated_1rm) if len(points) >= 2 else None,
            )
        )

    return trends


# --- Consistency matrix -------------------------------------------------------

async def get_consistency_matrix_service(
    db: AsyncSession, current_user: User, program: ProgramTemplates, year: int, month: int
) -> ConsistencyMatrix:
    schedule = await get_scheduled_weekdays_for_program(program.id, db, current_user)

    last_day = calendar.monthrange(year, month)[1]
    month_start = date(year, month, 1)
    month_end = date(year, month, last_day) + timedelta(days=1)

    logs = await get_workout_logs_in_range(
        program.id, _day_bounds_utc(month_start), _day_bounds_utc(month_end), db, current_user
    )
    logs_by_date: dict[date, int] = {}
    for log in logs:
        logs_by_date.setdefault(_to_date(log.inserted_at), log.id)

    today = date.today()
    cutoff = min(today, date(year, month, last_day))

    days = []
    scheduled_count = 0
    completed_on_scheduled_count = 0
    extra_workout_count = 0

    for day_num in range(1, last_day + 1):
        current_date = date(year, month, day_num)
        weekday = current_date.weekday()
        is_scheduled = weekday in schedule
        is_completed = current_date in logs_by_date

        if is_scheduled and current_date <= cutoff:
            scheduled_count += 1
            if is_completed:
                completed_on_scheduled_count += 1
        if is_completed and not is_scheduled:
            extra_workout_count += 1

        days.append(
            ConsistencyDay(
                date=current_date,
                scheduled=is_scheduled,
                completed=is_completed,
                workout_log_id=logs_by_date.get(current_date),
                workout_type=schedule.get(weekday),
            )
        )

    return ConsistencyMatrix(
        program_id=program.id,
        year=year,
        month=month,
        days=days,
        scheduled_count=scheduled_count,
        completed_count=len(logs_by_date),
        extra_workout_count=extra_workout_count,
        adherence_rate=(completed_on_scheduled_count / scheduled_count) if scheduled_count else None,
    )


# --- Streaks -------------------------------------------------------------------

def _compute_streaks(workout_dates: list[date]) -> StreakInfo:
    unique_dates = sorted(set(workout_dates))
    if not unique_dates:
        return StreakInfo(current_streak_days=0, longest_streak_days=0, last_workout_date=None)

    longest = run = 1
    for i in range(1, len(unique_dates)):
        if (unique_dates[i] - unique_dates[i - 1]).days == 1:
            run += 1
        else:
            run = 1
        longest = max(longest, run)

    last = unique_dates[-1]
    today = date.today()
    if (today - last).days > 1:
        current = 0
    else:
        current = 1
        cursor = last
        for i in range(len(unique_dates) - 2, -1, -1):
            if (cursor - unique_dates[i]).days == 1:
                current += 1
                cursor = unique_dates[i]
            else:
                break

    return StreakInfo(current_streak_days=current, longest_streak_days=longest, last_workout_date=last)


async def get_streak_service(db: AsyncSession, current_user: User, program: ProgramTemplates) -> StreakInfo:
    dates = await get_all_workout_log_dates(program.id, db, current_user)
    return _compute_streaks([_to_date(d) for d in dates])


# --- Weekly / monthly period summary --------------------------------------------

async def _build_period_summary(
    db: AsyncSession, current_user: User, program: ProgramTemplates, start: date, end: date
) -> PeriodSummary:
    body_composition = await get_body_composition_change_service(db, current_user, start, end)

    start_dt, end_dt = _day_bounds_utc(start), _day_bounds_utc(end)
    logs = await get_workout_logs_in_range(program.id, start_dt, end_dt, db, current_user)
    completed_dates = {_to_date(log.inserted_at) for log in logs}

    schedule = await get_scheduled_weekdays_for_program(program.id, db, current_user)
    scheduled_dates = []
    cursor = start
    while cursor < end:
        if cursor.weekday() in schedule:
            scheduled_dates.append(cursor)
        cursor += timedelta(days=1)

    workouts_scheduled = len(scheduled_dates) if schedule else None
    consistency_rate = None
    if scheduled_dates:
        completed_on_scheduled = sum(1 for d in scheduled_dates if d in completed_dates)
        consistency_rate = completed_on_scheduled / len(scheduled_dates)

    pr_count = await get_pr_count_in_range(db, current_user, start_dt, end_dt)
    overload = await get_program_overload_service(db, current_user, program, start_dt, end_dt)
    streak = await get_streak_service(db, current_user, program)

    return PeriodSummary(
        period_start=start,
        period_end=end,
        body_composition=body_composition,
        workouts_completed=len(logs),
        workouts_scheduled=workouts_scheduled,
        consistency_rate=consistency_rate,
        pr_count=pr_count,
        overload=overload,
        streak=streak,
    )


async def get_weekly_summary_service(db: AsyncSession, current_user: User, program: ProgramTemplates) -> PeriodSummary:
    start, end = _current_week_bounds()
    return await _build_period_summary(db, current_user, program, start, end)


async def get_monthly_summary_service(db: AsyncSession, current_user: User, program: ProgramTemplates) -> PeriodSummary:
    start, end = _current_month_bounds()
    return await _build_period_summary(db, current_user, program, start, end)


# --- Misc ------------------------------------------------------------------

async def get_pr_tracking_service(exercises: list[int], db: AsyncSession, current_user: User):
    return await get_pr_history(exercises, db, current_user)


async def get_exercise_history_service(exercise_id: int, db: AsyncSession, current_user: User):
    return await get_exercise_history(exercise_id, db, current_user)


async def get_workout_history_service(program_id: int, db: AsyncSession, current_user: User):
    """Last 30 days of workout logs for this program, each flagged for whether it matched its template."""
    now = datetime.now(UTC)
    start = now - timedelta(days=30)
    logs = await get_workout_logs_in_range(program_id, start, now, db, current_user)

    workouts = []
    for log in logs:
        template_exercises = Counter()
        if log.workout_template_id is not None:
            template_rows = await get_user_workout_template_exercises_by_workout_value(
                db, current_user.id, log.workout_template_id
            )
            template_exercises = Counter(row.exercise_id for row in template_rows)

        log_rows = await get_user_workout_log_exercise_by_workout(db, current_user.id, log.id)
        log_exercises = Counter(row.exercise_id for row in log_rows)

        workouts.append(
            {
                "workout_log_id": log.id,
                "date": log.inserted_at,
                "followed_template": (template_exercises <= log_exercises) if template_exercises else None,
                "missing_exercise_ids": list((template_exercises - log_exercises).elements()),
                "extra_exercise_ids": list((log_exercises - template_exercises).elements()),
            }
        )

    return {"workouts": workouts, "count": len(workouts)}
