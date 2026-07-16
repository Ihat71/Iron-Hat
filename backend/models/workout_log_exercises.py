from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

class WorkoutLogExercise(Base):
    __tablename__ = "workout_log_exercises"

    id: Mapped[int] = mapped_column(primary_key = True)
    workout_log_id: Mapped[int] = mapped_column(
        ForeignKey("workout_logs.id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )