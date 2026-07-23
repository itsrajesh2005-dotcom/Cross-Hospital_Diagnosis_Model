from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserLogin, UserRegister, Token, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.authenticate_user(login_data)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(reg_data: UserRegister, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(reg_data)
