from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt

from src.database.db_manager import (
    get_user_by_username, get_user_by_id,
    create_user, verify_password, update_last_login
)
from src.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_HOURS

router   = APIRouter()
security = HTTPBearer()

# ── Schemas ───────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email:    str
    password: str
    role:     str = "citizen"

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str
    user:         dict

# ── JWT helpers ───────────────────────────────────────────────
def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = decode_token(credentials.credentials)
    user    = get_user_by_id(user_id)
    if not user or not user["is_active"]:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


# ── Routes ────────────────────────────────────────────────────
@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = get_user_by_username(req.username)
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    update_last_login(user["id"])
    token = create_token(user["id"])
    return {
        "access_token": token,
        "token_type":   "bearer",
        "user": {
            "id":         user["id"],
            "username":   user["username"],
            "email":      user["email"],
            "role":       user["role"],
            "created_at": user["created_at"],
            "last_login": user["last_login"],
        }
    }


@router.post("/signup")
def signup(req: SignupRequest):
    if len(req.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if req.role not in ("citizen", "lawyer", "student"):
        raise HTTPException(status_code=400, detail="Invalid role")
    result = create_user(req.username, req.email, req.password, req.role)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "id":         user["id"],
        "username":   user["username"],
        "email":      user["email"],
        "role":       user["role"],
        "created_at": user["created_at"],
        "last_login": user["last_login"],
    }
