# In-memory state store (replace with SQL Server in production)
from typing import Dict, List, Any
from backend.models.schemas import (
    Strategy, Account, UploadedFile, ValidationReport,
    GeneratedCommentary, ComparisonResult, AuditEntry
)

class AppState:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.uploaded_files: Dict[str, UploadedFile] = {}
        self.validation_reports: Dict[str, ValidationReport] = {}
        self.commentaries: Dict[str, GeneratedCommentary] = {}
        self.comparisons: Dict[str, ComparisonResult] = {}
        self.audit_log: List[AuditEntry] = []
        self._init_demo_strategies()

    def _init_demo_strategies(self):
        """Pre-load demo strategies from uploaded files."""
        self.strategies["LCG"] = Strategy(
            strategy_id="LCG",
            strategy_name="Large-Cap Growth",
            period="4Q25",
            lead_account_id="LCG_LEAD",
            accounts=[
                Account(account_id="LCG_LEAD", account_name="LCG Lead Account",
                        account_code="LCG", is_lead=True),
                Account(account_id="4686", account_name="Harris Corp - Large-Cap Growth",
                        account_code="4686", is_lead=False),
            ]
        )
        self.strategies["GPAR"] = Strategy(
            strategy_id="GPAR",
            strategy_name="Global Portfolio All",
            period="4Q25",
            accounts=[]
        )

# Global singleton
app_state = AppState()