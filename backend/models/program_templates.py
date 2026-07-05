from datetime import datetime

from sqlalchemy import DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from backend.core.database import Base

class ProgramTemplates(Base):
    __tablename__ = "program_templates"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )
    program_name: Mapped[str] = mapped_column(String(100))
    program_description: Mapped[dict] = mapped_column(JSONB)
