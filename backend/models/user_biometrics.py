from datetime import datetime

from sqlalchemy import DateTime, String, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

class Biometric(Base):
    __tablename__ = "biometrics"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id")
    )
    weight: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    waist: Mapped[float | None] = mapped_column(Float)
    chest: Mapped[float | None] = mapped_column(Float)
    hips: Mapped[float | None] = mapped_column(Float)
    manual_body_fat: Mapped[float | None] = mapped_column(Float)
    calculated_body_fat: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(String(150))
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
