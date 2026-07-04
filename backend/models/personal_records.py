from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, Float, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

class PersonalRecords(Base):
    __tablename__ = "personal_records"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )
    pr_type: Mapped[str] = mapped_column(String(50)) #1rm, 2rm, bodyweight, etc
    weight: Mapped[float] = mapped_column(Float)
    sets: Mapped[Optional[int]] = mapped_column(Integer)
    reps: Mapped[Optional[int]] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )