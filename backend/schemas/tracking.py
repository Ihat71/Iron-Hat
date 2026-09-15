from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class WeightTracking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    weight: float
    manual_body_fat: float | None = None
    calculated_body_fat: float | None = None
    recorded_at: datetime


class BodyCompositionChange(BaseModel):
    period_start: date
    period_end: date
    start_weight: float | None = None
    end_weight: float | None = None
    weight_change: float | None = None
    start_body_fat: float | None = None
    end_body_fat: float | None = None
    body_fat_change: float | None = None
    lowest_weight: float | None = None
    highest_weight: float | None = None


class OverloadPoint(BaseModel):
    date: datetime
    top_weight: float
    max_reps: int
    estimated_1rm: float


class ExerciseOverloadTrend(BaseModel):
    exercise_id: int
    exercise_name: str
    points: list[OverloadPoint]
    starting_e1rm: float | None = None
    latest_e1rm: float | None = None
    e1rm_change: float | None = None


class ConsistencyDay(BaseModel):
    date: date
    scheduled: bool
    completed: bool
    workout_log_id: int | None = None
    workout_type: str | None = None


class ConsistencyMatrix(BaseModel):
    program_id: int
    year: int
    month: int
    days: list[ConsistencyDay]
    scheduled_count: int
    completed_count: int
    extra_workout_count: int
    adherence_rate: float | None = None


class StreakInfo(BaseModel):
    current_streak_days: int
    longest_streak_days: int
    last_workout_date: date | None = None


class PeriodSummary(BaseModel):
    period_start: date
    period_end: date
    body_composition: BodyCompositionChange
    workouts_completed: int
    workouts_scheduled: int | None = None
    consistency_rate: float | None = None
    pr_count: int
    overload: list[ExerciseOverloadTrend]
    streak: StreakInfo
