from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Integer, Float, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.workout_log_exercises import WorkoutLogExercise
    from backend.models.exercises import Exercises
class ExerciseHistory(Base):
    __tablename__ = "exercise_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )
    workout_log_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("workout_log_exercises.id"),
        nullable=True,
        unique=True, 
    )

    # Summary statistics
    exercise_type: Mapped[Optional[str]] = mapped_column(String(50))
    top_weight: Mapped[float] = mapped_column(Float)
    sets: Mapped[int | None] = mapped_column(Integer)
    max_reps: Mapped[int] = mapped_column(Integer)
    max_rpe: Mapped[float | None] = mapped_column(Float)

    total_volume: Mapped[float | None] = mapped_column(Float)

    # Every performed set
    detailed_sets: Mapped[Optional[dict]] = mapped_column(JSONB)

    # Optional notes
    notes: Mapped[str | None] = mapped_column(String(150))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    user: Mapped[list["User"]] = relationship(back_populates="exercise_histories")
    log: Mapped[list["WorkoutLogExercise"]] = relationship(back_populates="exercise_history")
    exercise: Mapped[list["Exercises"]] = relationship()
