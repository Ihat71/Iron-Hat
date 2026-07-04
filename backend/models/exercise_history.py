from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Integer, Float, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base

class ExerciseHistory(Base):
    __tablename__ = "exercise_history"

    id: Mapped[int] = mapped_column(primary_key = True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )
    top_weight: Mapped[float] = mapped_column(Float)
    top_rpe: Mapped[float] = mapped_column(Float)
    top_reps: Mapped[float] = mapped_column(Float)
    detailed_sets: Mapped[Optional[dict]] = mapped_column(JSONB)
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
