from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.program_templates import ProgramTemplates
    from backend.models.user_biometrics import Biometric
    from backend.models.personal_records import PersonalRecords
    from backend.models.exercise_history import ExerciseHistory

from backend.core.database import Base
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    full_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    gender: Mapped[Gender] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    last_updated_username: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    programs: Mapped[list["ProgramTemplates"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    biometry: Mapped[list["Biometric"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    records: Mapped[list["PersonalRecords"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    exercise_histories: Mapped[list["ExerciseHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)