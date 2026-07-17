import os, uuid, shutil
from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from backend.models.schemas import UploadedFile
from backend.models.state import app_state
from backend.core.audit_logger import log_audit

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_files(
    strategy_id: str = Form(...),
    account_id: str = Form(...),
    file_types: str = Form(...),   # comma-separated: attribution,purchase_sales
    files: List[UploadFile] = File(...)
):
    types = [t.strip() for t in file_types.split(",")]
    uploaded = []

    for i, file in enumerate(files):
        file_id = str(uuid.uuid4())[:8]
        ext = os.path.splitext(file.filename)[1]
        save_name = f"{file_id}_{file.filename}"
        save_path = os.path.join(UPLOAD_DIR, save_name)

        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        file_type = types[i] if i < len(types) else "unknown"
        size = os.path.getsize(save_path)

        record = UploadedFile(
            file_id=file_id,
            filename=file.filename,
            file_type=file_type,
            account_id=account_id,
            strategy_id=strategy_id,
            size_bytes=size
        )
        app_state.uploaded_files[file_id] = record
        uploaded.append(record)

    log_audit("file_upload", "file", account_id, {
        "count": len(uploaded),
        "strategy_id": strategy_id
    })

    return {
        "status": "success",
        "uploaded_count": len(uploaded),
        "files": uploaded
    }