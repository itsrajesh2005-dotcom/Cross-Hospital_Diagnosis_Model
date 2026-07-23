from app.core.security import get_password_hash, verify_password, create_access_token
import jwt
from app.core.config import settings


def test_password_hashing():
    raw_pass = "EnterpriseHealthcarePass2026!"
    hashed = get_password_hash(raw_pass)
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation():
    subject = "user_uuid_12345"
    roles = ["SYSTEM_ADMIN"]
    token = create_access_token(subject=subject, roles=roles)
    
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == subject
    assert "SYSTEM_ADMIN" in decoded["roles"]
