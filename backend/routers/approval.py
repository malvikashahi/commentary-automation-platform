from fastapi import APIRouter, HTTPException
from backend.models.schemas import ApprovalRequest, ProcessingStatus
from backend.models.state import app_state
from backend.core.audit_logger import log_audit

router = APIRouter()

@router.post("/approve/{account_id}")
def approve_commentary(account_id: str, req: ApprovalRequest):
    commentary = app_state.commentaries.get(account_id)
    if not commentary:
        raise HTTPException(404, f"Commentary not found for {account_id}")
    commentary.status = (
        ProcessingStatus.APPROVED if req.approved
        else ProcessingStatus.REVIEW
    )
    commentary.reviewer_notes = req.reviewer_notes

    log_audit("approval", "commentary", account_id, {
        "approved": req.approved,
        "reviewer": req.reviewer_id
    })
    return {"status": "updated", "new_status": commentary.status}