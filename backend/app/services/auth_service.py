from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import UnauthorizedException, DuplicateResourceException
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.auth import UserLogin, UserRegister, Token, UserRead


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, login_data: UserLogin) -> Token:
        result = await self.db.execute(select(User).filter(User.email == login_data.email))
        user = result.scalars().first()
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password.")
        
        if not user.is_active:
            raise UnauthorizedException("User account is deactivated.")

        # Record audit log
        audit = AuditLog(
            user_id=user.id,
            action="USER_LOGIN",
            resource_type="USER",
            resource_id=user.id,
            details={"email": user.email, "role": user.role}
        )
        self.db.add(audit)
        await self.db.commit()

        token_str = create_access_token(subject=user.id, roles=[user.role])
        return Token(access_token=token_str)

    async def register_user(self, reg_data: UserRegister) -> UserRead:
        result = await self.db.execute(select(User).filter(User.email == reg_data.email))
        if result.scalars().first():
            raise DuplicateResourceException("User with this email already exists.")

        user = User(
            email=reg_data.email,
            password_hash=get_password_hash(reg_data.password),
            full_name=reg_data.full_name,
            role=reg_data.role,
            hospital_id=reg_data.hospital_id
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # Record audit log
        audit = AuditLog(
            user_id=user.id,
            action="USER_REGISTERED",
            resource_type="USER",
            resource_id=user.id,
            details={"email": user.email, "role": user.role}
        )
        self.db.add(audit)
        await self.db.commit()

        return UserRead.model_validate(user)
