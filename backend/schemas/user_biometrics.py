from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BioBase(BaseModel):
    weight: float
    height: float
    waist: float | None = None
    chest: float | None = None
    hips: float | None = None
    manual_body_fat: float | None = None
    notes: str | None = None
    recorded_at: datetime

class BiometricCreate(BioBase):
    pass

class BiometricRead(BioBase):
    model_config = ConfigDict(from_attributes = True)

    id: int
    created_at: datetime

class BiometricUpdate(BaseModel):
    weight: float | None = None
    height: float | None = None
    waist: float | None = None
    chest: float | None = None
    hips: float | None = None
    manual_body_fat: float | None = None
    notes: str | None = None