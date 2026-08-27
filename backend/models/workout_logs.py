from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.workout_log_exercises import WorkoutLogExercise
    from backend.models.program_templates import ProgramTemplates
    from backend.models.workout_templates import WorkoutTemplate

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key = True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program_templates.id")
    )
    workout_template_id: Mapped[int] = mapped_column(
        ForeignKey("workout_templates.id"), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(String(300))
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    exercises: Mapped[list["WorkoutLogExercise"]] = relationship(back_populates="workout_log", cascade="all, delete-orphan", passive_deletes=True)
    program: Mapped["ProgramTemplates"] = relationship(back_populates="workout_logs")
    template: Mapped["WorkoutTemplate"] = relationship(back_populates="log")
