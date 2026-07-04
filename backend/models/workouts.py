from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

class Workouts(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )
    day_number: Mapped[int] = mapped_column(Integer)
    workout_type: Mapped[str] = mapped_column(String(50))
    inserted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )