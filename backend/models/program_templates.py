from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.workout_templates import WorkoutTemplate
    from backend.models.workout_logs import WorkoutLog
    from backend.models.user import User

class ProgramTemplates(Base):
    __tablename__ = "program_templates"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    program_name: Mapped[str] = mapped_column(String(100))
    program_description: Mapped[dict | None] = mapped_column(JSONB) #this is supposed to be a detailed map of the intended program

    workout_templates: Mapped[list["WorkoutTemplate"]] = relationship(back_populates="program", cascade="all, delete-orphan", passive_deletes=True)
    workout_logs: Mapped[list["WorkoutLog"]] = relationship(back_populates="program", cascade="all, delete-orphan", passive_deletes=True)
    user: Mapped["User"] = relationship(back_populates="programs")