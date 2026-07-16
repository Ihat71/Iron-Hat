from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum

class PType(str, Enum):
    UL = "upper_lower"
    PPL = "push_pull_legs"
    FULLBODY = "full_body"
    CUSTOM = "custom"

class ProgramCreate(BaseModel):
    program_name: PType
    program_description: dict | None = None

class ProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    id: int 
    user_id: int 
    program_name: PType
    program_description: dict 


class ProgramUpdate(BaseModel):
    program_name: PType | None = None
    program_description: dict | None = None