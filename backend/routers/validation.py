from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Dict
from backend.services.validation_engine import ValidationEngine
from backend.models.state import app_state
from backend.core.audit_logger import log_audit

router = APIRouter()
engine = ValidationEngine()

class ValidateRequest(BaseModel):
    account_id: str
    strategy_id: str
    file_paths: Dict[str, str]   # {file_type: path}

@router.post("/validate")
def trigger_validation(req: ValidateRequest):
    report = engine.validate(
        account_id=req.account_id,
        strategy_id=req.strategy_id,
        uploaded_files=req.file_paths
    )
    key = f"{req.strategy_id}_{req.account_id}"
    app_state.validation_reports[key] = report

    log_audit("validation", "account", req.account_id, {
        "status": report.overall_status,
        "errors": report.error_count
    })

    return report