from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
from backend.services.file_parser import FileParser
from backend.services.commentary_engine import CommentaryEngine
from backend.models.state import app_state
from backend.core.audit_logger import log_audit

router = APIRouter()
parser = FileParser()
engine = CommentaryEngine()

class ProcessRequest(BaseModel):
    account_id: str
    strategy_id: str
    period: str
    attribution_path: Optional[str] = None
    ps_path: Optional[str] = None
    performance_path: Optional[str] = None
    lead_commentary_path: Optional[str] = None

@router.post("/process")
def trigger_processing(req: ProcessRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        _run_processing, req
    )
    return {
        "status": "processing_started",
        "account_id": req.account_id,
        "message": "Commentary generation running in background."
    }

def _run_processing(req: ProcessRequest):
    attribution = None
    ps_data = None
    performance = None
    lead_doc = {"sections": {}, "full_text": "", "paragraphs": [], "placeholders": []}

    if req.attribution_path:
        attribution = parser.parse_attribution(
            req.attribution_path, req.account_id
        )

    if req.ps_path:
        ps_data = parser.parse_purchase_sales(
            req.ps_path, req.account_id
        )

    if req.performance_path:
        records = parser.parse_performance(req.performance_path)
        for r in records:
            if r.account_code == req.account_id:
                performance = r
                break

    if req.lead_commentary_path:
        lead_doc = parser.parse_lead_commentary(req.lead_commentary_path)

    commentary = engine.generate(
        account_id=req.account_id,
        strategy_id=req.strategy_id,
        period=req.period,
        lead_commentary=lead_doc,
        attribution=attribution,
        purchase_sales=ps_data,
        performance=performance
    )

    app_state.commentaries[req.account_id] = commentary
    log_audit("commentary_generated", "account", req.account_id, {
        "sections": len(commentary.sections),
        "period": req.period
    })