from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.schemas.program_templates import ProgramCreate, ProgramUpdate

async def create_program(db: AsyncSession, program: ProgramTemplates) -> ProgramTemplates:

    db.add(program)
    await db.commit()
    await db.refresh(program)

    return program

async def get_program(db: AsyncSession, program_id: int) -> ProgramTemplates :
    return await db.get(ProgramTemplates, program_id)

async def get_user_programs(db: AsyncSession, user_id: int) -> list[ProgramTemplates] | None:
    stmt = select(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_program(db: AsyncSession, program_id: int, program_data: ProgramUpdate) -> ProgramTemplates | None:

    program = await get_program(db, program_id)

    if not program:
        return None

    update_data = program_data.model_dump(exclude_unset=True, exclude={"id"})

    for key, value in update_data.items():
        setattr(program, key, value)

    await db.commit()

    await db.refresh(program)

    return program

async def delete_program(db: AsyncSession, program_id: int) -> bool:
    program = await get_program(db, program_id)

    if program is None:
        return False

    await db.delete(program)
    await db.commit()

    return True
