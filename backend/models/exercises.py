from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

class Exercises(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key = True)
    exercise_name: Mapped[str] = mapped_column(String(50))