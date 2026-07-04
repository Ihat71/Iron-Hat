from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

class WorkoutExercises(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(primary_key = True)
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id")
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id")
    )
    