import uuid
from datetime import datetime
from typing import Optional, Dict, Any

def log_audit(
    activity: str,
    entity_type: str,
    entity_id: str,
    details: Optional[Dict[str, Any]] = None,
    user_id: str = "system"
):
    from backend.models.state import app_state
    from backend.models.schemas import AuditEntry

    entry = AuditEntry(
        audit_id=str(uuid.uuid4()),
        user_id=user_id,
        activity=activity,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
        timestamp=datetime.now()
    )
    app_state.audit_log.append(entry)