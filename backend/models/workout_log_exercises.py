from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.workout_logs import WorkoutLog
    from backend.models.exercises import Exercises
    from backend.models.exercise_history import ExerciseHistory

class WorkoutLogExercise(Base):
    __tablename__ = "workout_log_exercises"

    id: Mapped[int] = mapped_column(primary_key = True)
    workout_log_id: Mapped[int] = mapped_column(
        ForeignKey("workout_logs.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"), nullable=False
    )

    exercise_history: Mapped["ExerciseHistory"] = relationship(back_populates="log")
    workout_log: Mapped["WorkoutLog"] = relationship(back_populates="exercises")
    exercise: Mapped["Exercises"] = relationship()