from fastapi import APIRouter, Depends
from src.auth.auth_router import require_admin
from src.database.db_manager import get_all_users, get_analytics, toggle_user_active

router = APIRouter()

@router.get("/users")
def admin_users(admin=Depends(require_admin)):
    return get_all_users()

@router.get("/analytics")
def admin_analytics(admin=Depends(require_admin)):
    return get_analytics()

@router.patch("/users/{user_id}/toggle")
def toggle_user(user_id: int, admin=Depends(require_admin)):
    toggle_user_active(user_id)
    return {"toggled": True}
