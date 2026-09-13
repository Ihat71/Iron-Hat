from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.workout_templates import (
    WorkoutTemplateCreate,
    WorkoutTemplateRead,
    WorkoutTemplateUpdate,
)
from backend.services.workout_templates_service import (
    add_workout_template_service,
    delete_workout_template_service,
    get_all_workout_templates_service,
    get_workout_template_by_params_service,
    get_workout_template_service,
    update_workout_template_service,
)

from backend.schemas.workout_template_exercises import WorkoutTemplateExerciseRead

router = APIRouter(
    prefix="",
    tags=["Workout Templates"],
)


@router.post("/",response_model=WorkoutTemplateRead,status_code=status.HTTP_201_CREATED,)
async def create_workout_template(program_id: int,data: WorkoutTemplateCreate,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await add_workout_template_service(
        db,
        data,
        program_id,
        current_user,
    )


@router.get("/", response_model=list[WorkoutTemplateRead],status_code=status.HTTP_200_OK,)
async def get_workout_templates(program_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await get_all_workout_templates_service(
        program_id,
        db,
        current_user,
    )


@router.get("/search",response_model=list[WorkoutTemplateRead],status_code=status.HTTP_200_OK,)
async def search_workout_templates(program_id: int,
                             workout_type: str | None = None,
                             day_number: int | None = None,
                             db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user),):
    return await get_workout_template_by_params_service(
        program_id,
        workout_type,
        day_number,
        db,
        current_user,
    )



@router.get("/{workout_template_id}",response_model=WorkoutTemplateRead,status_code=status.HTTP_200_OK,)
async def get_workout_template(program_id: int,workout_template_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await get_workout_template_service(
        db,
        program_id,
        workout_template_id,
        current_user,
    )


@router.patch("/{workout_template_id}",response_model=WorkoutTemplateRead,status_code=status.HTTP_200_OK,)
async def update_workout_template(program_id: int,workout_template_id: int,data: WorkoutTemplateUpdate,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    return await update_workout_template_service(
        db,
        data,
        program_id,
        workout_template_id,
        current_user,
    )


@router.delete(
    "/{workout_template_id}",response_model=bool,status_code=status.HTTP_200_OK,)
async def delete_workout_template(program_id: int, workout_template_id: int,db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user),):
    return await delete_workout_template_service(
        db,
        program_id,
        workout_template_id,
        current_user,
    )
