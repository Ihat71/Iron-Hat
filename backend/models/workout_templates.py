from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.workout_template_exercises import WorkoutTemplateExercise
    from backend.models.program_templates import ProgramTemplates
    from backend.models.workout_logs import WorkoutLog

class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"

    id: Mapped[int] = mapped_column(primary_key = True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program_templates.id", ondelete="CASCADE"), nullable=False
    )
    day_number: Mapped[int | None] = mapped_column(Integer)
    workout_type: Mapped[str] = mapped_column(String(50))
    # Weekdays this template is scheduled on: 0=Monday .. 6=Sunday. Powers the consistency matrix.
    days_of_week: Mapped[list[int] | None] = mapped_column(JSONB)
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    exercises: Mapped[list["WorkoutTemplateExercise"]] = relationship(back_populates="workout_template", cascade="all, delete-orphan", passive_deletes=True)
    program: Mapped["ProgramTemplates"] = relationship(back_populates="workout_templates")
    log: Mapped["WorkoutLog"] = relationship(back_populates="template")

