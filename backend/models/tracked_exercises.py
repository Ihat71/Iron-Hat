from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.exercises import Exercises
    from backend.models.program_templates import ProgramTemplates


class TrackedExercise(Base):
    """An exercise the user chose to track for progressive overload within a specific program."""
    __tablename__ = "tracked_exercises"
    __table_args__ = (UniqueConstraint("program_id", "exercise_id", name="uq_tracked_exercise_program_exercise"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program_templates.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    program: Mapped["ProgramTemplates"] = relationship(back_populates="tracked_exercises")
    exercise: Mapped["Exercises"] = relationship()
