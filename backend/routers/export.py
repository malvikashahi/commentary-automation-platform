from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.models.schemas import ExportRequest
from backend.models.state import app_state
from backend.services.export_engine import ExportEngine
from backend.core.audit_logger import log_audit

router = APIRouter()
export_engine = ExportEngine()

@router.post("/export")
def trigger_export(req: ExportRequest):
    results = []
    for account_id in req.account_ids:
        commentary = app_state.commentaries.get(account_id)
        if not commentary:
            continue
        result = export_engine.export_docx(commentary)
        results.append(result)
        log_audit("export", "commentary", account_id, {
            "format": req.format,
            "file": result.file_path
        })
    return {"exports": results, "count": len(results)}

@router.get("/export/download/{filename}")
def download_file(filename: str):
    path = f"outputs/{filename}"
    if not __import__("os").path.exists(path):
        raise HTTPException(404, "File not found")
    return FileResponse(
        path=path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename
    )