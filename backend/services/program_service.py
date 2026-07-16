from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from crud.program_templates import get_user_programs, create_program, update_program, delete_program, get_program
from models.user import User
from models.program_templates import ProgramTemplates
from schemas.program_templates import ProgramCreate, ProgramRead, ProgramUpdate

def is_valid_program(db: Session, user: User, program_id: int) -> bool:
    program = get_program(db, program_id)


    if program.id == program_id and program.user_id == user.id:
        return True
    
    return False

def get_user_programs_service(db: Session, user: User):
    return get_user_programs(db, user.id)

def create_program_service(db: Session, program_data: ProgramCreate, user: User):
    program = ProgramTemplates(
        user_id=user.id,
        program_name=program_data.program_name,
        program_description=program_data.program_description,
    )
    return create_program(db, program)

def update_program_service(db: Session, program_id: int, program_data: ProgramUpdate, user: User):
    if not is_valid_program(db, user, program_id):
        raise ValueError("Cannot access that")
    
    return update_program(db, program_id, program_data)

def delete_program_service(db: Session, program_id: int, user: User):
    if not is_valid_program(db, user, program_id):
        raise ValueError("Cannot access that")
    return delete_program(db, program_id)