from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Integer, Float, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from core.database import Base

class ExerciseHistory(Base):
    __tablename__ = "exercise_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    workout_log_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("workout_log_exercises.id"),
        nullable=False,
        unique=True, 
    )

    # Summary statistics
    top_weight: Mapped[float] = mapped_column(Float)
    max_reps: Mapped[int] = mapped_column()
    max_rpe: Mapped[float | None] = mapped_column(Float)

    total_volume: Mapped[float] = mapped_column(Float)

    # Every performed set
    detailed_sets: Mapped[dict] = mapped_column(JSONB)

    # Optional notes
    notes: Mapped[str | None] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
