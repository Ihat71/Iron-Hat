from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.program_templates import ProgramTemplates
from backend.schemas.program_templates import ProgramCreate, ProgramUpdate

def create_program(db: Session, program_data: ProgramCreate) -> ProgramTemplates:

    program = ProgramTemplates(**program_data.model_dump())

    db.add(program)
    db.commit()
    db.refresh(program)

    return program

def get_program(db: Session, program_id: int) -> ProgramTemplates :
    return db.get(ProgramTemplates, program_id)

def get_user_programs(db: Session, user_id: int) -> list[ProgramTemplates] | None:
    stmt = select(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def update_program(db: Session, program_id: int, program_data: ProgramUpdate) -> ProgramTemplates | None:
    
    program = get_program(db, program_id)

    if not program:
        return None
    
    update_data = program_data.model_dump(exclude_unset=True, exclude={"id"})
    
    for key, value in update_data.items():
        setattr(program, key, value)
    
    db.commit()

    db.refresh(program)

    return program

def delete_program(db: Session, program_id: int) -> bool:
    program = get_program(db, program_id)

    if program is None:
        return False
    
    db.delete(program)
    db.commit()

    return True