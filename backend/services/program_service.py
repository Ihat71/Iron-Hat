from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.crud.program_templates import get_user_programs, create_program, update_program, delete_program, get_program
from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.schemas.program_templates import ProgramCreate, ProgramRead, ProgramUpdate

async def is_valid_program(db: AsyncSession, user: User, program_id: int) -> bool:
    program = await get_program(db, program_id)
    if not program:
        raise ValueError("this program does not exist")

    if program.id == program_id and program.user_id == user.id:
        return True

    return False

async def get_user_programs_service(db: AsyncSession, user: User):
    return await get_user_programs(db, user.id)

async def create_program_service(db: AsyncSession, program_data: ProgramCreate, user: User):
    program = ProgramTemplates(
        user_id=user.id,
        program_name=program_data.program_name,
        program_description=program_data.program_description,
    )
    return await create_program(db, program)

async def update_program_service(db: AsyncSession, program_id: int, program_data: ProgramUpdate, user: User):
    if not await is_valid_program(db, user, program_id):
        raise ValueError("Cannot access that")

    return await update_program(db, program_id, program_data)

async def delete_program_service(db: AsyncSession, program_id: int, user: User):
    if not await is_valid_program(db, user, program_id):
        raise ValueError("Cannot access that")
    return await delete_program(db, program_id)
