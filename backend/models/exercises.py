from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


class Exercises(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(75))
    equipment: Mapped[str] = mapped_column(String(75))
    is_variation: Mapped[str] = mapped_column(String(75))
    utility_type: Mapped[str] = mapped_column(String(75))
    mechanics_type: Mapped[str] = mapped_column(String(75))
    force_type: Mapped[str] = mapped_column(String(75))
    target_muscles: Mapped[str] = mapped_column(Text)
    main_muscle: Mapped[str] = mapped_column(String(75))
    secondary_muscles: Mapped[str | None] = mapped_column(String(75))
    difficulty: Mapped[int] = mapped_column(Integer)
    synergist_muscles: Mapped[str | None] = mapped_column(Text)
    stabilizer_muscles: Mapped[str | None] = mapped_column(Text)
    antagonist_muscles: Mapped[str | None] = mapped_column(String(75))
    dynamic_stabilizer_muscles: Mapped[str | None] = mapped_column(String(75))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("exercises.id"))
