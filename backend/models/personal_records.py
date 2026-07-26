from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Float, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

class PersonalRecords(Base):
    __tablename__ = "personal_records"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )
    exercise_history_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercise_history.id")
    )
    pr_type: Mapped[Optional[str]] = mapped_column(String(50)) #1rm, 2rm, bodyweight, etc
    top_weight: Mapped[float] = mapped_column(Float)
    sets: Mapped[Optional[int]] = mapped_column(Integer)
    reps: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(String(150))
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )