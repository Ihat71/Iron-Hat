from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.workout_templates import WorkoutTemplate
    from backend.models.exercises import Exercises

class WorkoutTemplateExercise(Base):
    __tablename__ = "workout_template_exercises"

    id: Mapped[int] = mapped_column(primary_key = True)
    workout_template_id: Mapped[int] = mapped_column(
        ForeignKey("workout_templates.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"), nullable=False
    )

    workout_template: Mapped["WorkoutTemplate"] = relationship(back_populates="exercises")
    exercise: Mapped["Exercises"] = relationship()
