from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user
from services.program_service import get_user_programs_service, create_program_service, update_program_service, delete_program_service
from models.user import User
from schemas.program_templates import ProgramCreate, ProgramRead, ProgramUpdate


router = APIRouter(
    prefix="/programs",
    tags=["Programs"]
)

@router.get("/programs", response_model=list[ProgramRead], status_code=status.HTTP_200_OK)
def get_programs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_programs_service(db, current_user)

@router.post("/create", response_model=ProgramRead, status_code=status.HTTP_201_CREATED)
def create_program_templates(data: ProgramCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_program_service(db, data, current_user)

@router.patch("/update/{program_id}", response_model=ProgramRead, status_code=status.HTTP_200_OK)
def update_programs(program_id: int, data: ProgramUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_program_service(db, program_id, data, current_user)

@router.delete("/delete/{program_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_program(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_program_service(db, program_id, current_user)