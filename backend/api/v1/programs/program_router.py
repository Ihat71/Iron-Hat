from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.api.dependencies import get_current_user, get_current_program
from backend.services.program_service import get_user_programs_service, create_program_service, update_program_service, delete_program_service
from backend.models.user import User
from backend.schemas.program_templates import ProgramCreate, ProgramRead, ProgramUpdate
from backend.api.v1.workout_logs import workout_logs_router
from backend.api.v1.workout_templates import workout_templates_router


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)

router.include_router(
    workout_logs_router.router,
    prefix="/{program_id}/workout-logs",
    dependencies=[Depends(get_current_program)]
)

router.include_router(
    workout_templates_router.router,
    prefix="/{program_id}/workout-templates",
    dependencies=[Depends(get_current_program)]
)


@router.get("", response_model=list[ProgramRead], status_code=status.HTTP_200_OK)
async def get_programs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_user_programs_service(db, current_user)

@router.post("", response_model=ProgramRead, status_code=status.HTTP_201_CREATED)
async def create_program_templates(data: ProgramCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_program_service(db, data, current_user)

@router.patch("/{program_id}", response_model=ProgramRead, status_code=status.HTTP_200_OK)
async def update_programs(program_id: int, data: ProgramUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await update_program_service(db, program_id, data, current_user)

@router.delete("/{program_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_program(program_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await delete_program_service(db, program_id, current_user)
