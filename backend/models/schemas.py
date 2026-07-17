from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"


class MatchClassification(str, Enum):
    MIRROR = "Mirror Account"
    MINOR = "Minor Variance"
    MODERATE = "Moderate Variance"
    SIGNIFICANT = "Significant Variance"


class ProcessingStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    EXPORTED = "EXPORTED"
    FAILED = "FAILED"


# ── Strategy & Account ──────────────────────────────────────
class Account(BaseModel):
    account_id: str
    account_name: str
    account_code: str
    is_lead: bool = False
    status: ProcessingStatus = ProcessingStatus.PENDING
    match_score: Optional[float] = None
    match_classification: Optional[MatchClassification] = None


class Strategy(BaseModel):
    strategy_id: str
    strategy_name: str
    period: str
    accounts: List[Account] = []
    lead_account_id: Optional[str] = None


# ── File Upload ─────────────────────────────────────────────
class UploadedFile(BaseModel):
    file_id: str
    filename: str
    file_type: str          # attribution | purchase_sales | performance | lead_commentary
    account_id: Optional[str] = None
    strategy_id: str
    upload_time: datetime = Field(default_factory=datetime.now)
    size_bytes: int = 0
    status: str = "uploaded"


# ── Validation ──────────────────────────────────────────────
class ValidationCheck(BaseModel):
    check_name: str
    layer: int
    status: ValidationStatus
    message: str
    details: Optional[str] = None


class ValidationReport(BaseModel):
    account_id: str
    strategy_id: str
    overall_status: ValidationStatus
    checks: List[ValidationCheck] = []
    validated_at: datetime = Field(default_factory=datetime.now)
    error_count: int = 0
    warning_count: int = 0


# ── Attribution Data ────────────────────────────────────────
class Contributor(BaseModel):
    rank: int
    security_name: str
    contribution: float


class SectorAttribution(BaseModel):
    sector: str
    portfolio_avg_wt: float
    portfolio_return: float
    benchmark_return: float
    total_variance: float


class AttributionData(BaseModel):
    account_id: str
    period: str
    benchmark_name: str
    top_contributors: List[Contributor] = []
    bottom_contributors: List[Contributor] = []
    sector_attribution: List[SectorAttribution] = []
    total_portfolio_return: float = 0.0
    total_benchmark_return: float = 0.0
    total_active_return: float = 0.0


# ── Purchase & Sales Data ───────────────────────────────────
class Transaction(BaseModel):
    security_name: str
    transaction_date: Optional[str] = None
    quantity: Optional[float] = None
    rationale: str


class PurchaseSalesData(BaseModel):
    account_id: str
    purchases: List[Transaction] = []
    sales: List[Transaction] = []


# ── Performance Data ────────────────────────────────────────
class PerformanceRecord(BaseModel):
    account_code: str
    period: str
    portfolio_return: float
    benchmark_return: float
    active_return: float


# ── Commentary ──────────────────────────────────────────────
class CommentarySection(BaseModel):
    section_name: str
    content: str
    is_auto_generated: bool = True
    is_reviewed: bool = False


class GeneratedCommentary(BaseModel):
    commentary_id: str
    account_id: str
    strategy_id: str
    period: str
    sections: List[CommentarySection] = []
    generated_at: datetime = Field(default_factory=datetime.now)
    status: ProcessingStatus = ProcessingStatus.REVIEW
    reviewer_notes: Optional[str] = None


# ── Comparison ──────────────────────────────────────────────
class DiffLine(BaseModel):
    line_type: str          # equal | insert | delete | replace
    lead_text: Optional[str] = None
    account_text: Optional[str] = None


class ComparisonResult(BaseModel):
    account_id: str
    lead_account_id: str
    match_score: float
    classification: MatchClassification
    holdings_overlap: float
    performance_match: float
    transaction_overlap: float
    narrative_match: float
    diff_lines: List[DiffLine] = []
    compared_at: datetime = Field(default_factory=datetime.now)


# ── Export ──────────────────────────────────────────────────
class ExportRequest(BaseModel):
    account_ids: List[str]
    strategy_id: str
    format: str = "docx"    # docx | pdf
    include_cover: bool = True


class ExportResult(BaseModel):
    export_id: str
    file_path: str
    format: str
    account_count: int
    generated_at: datetime = Field(default_factory=datetime.now)


# ── Audit ───────────────────────────────────────────────────
class AuditEntry(BaseModel):
    audit_id: str
    user_id: str = "system"
    activity: str
    entity_type: str
    entity_id: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# ── Approval ────────────────────────────────────────────────
class ApprovalRequest(BaseModel):
    account_id: str
    approved: bool
    reviewer_notes: Optional[str] = None
    reviewer_id: str = "analyst"