from fastapi import APIRouter
from backend.models.state import app_state

router = APIRouter()

@router.get("/audit")
def get_audit_log(skip: int = 0, limit: int = 50):
    entries = app_state.audit_log[skip: skip + limit]
    return {
        "total": len(app_state.audit_log),
        "entries": entries
    }