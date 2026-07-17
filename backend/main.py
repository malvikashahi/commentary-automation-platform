# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import (
    strategies,
    upload,
    validation,
    processing,
    comparison,
    review,
    approval,
    export,
    audit
)

app = FastAPI(
    title="Commentary Automation Platform API",
    description="FastAPI backend for Temple portfolio commentary automation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS Middleware ──────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ─────────────────────────────────────────
app.include_router(strategies.router,  prefix="/api", tags=["Strategies"])
app.include_router(upload.router,      prefix="/api", tags=["Upload"])
app.include_router(validation.router,  prefix="/api", tags=["Validation"])
app.include_router(processing.router,  prefix="/api", tags=["Processing"])
app.include_router(comparison.router,  prefix="/api", tags=["Comparison"])
app.include_router(review.router,      prefix="/api", tags=["Review"])
app.include_router(approval.router,    prefix="/api", tags=["Approval"])
app.include_router(export.router,      prefix="/api", tags=["Export"])
app.include_router(audit.router,       prefix="/api", tags=["Audit"])


# ── Health Endpoints ─────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "app": "Commentary Automation Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health():
    from backend.models.state import app_state
    return {
        "status": "healthy",
        "strategies_loaded": len(app_state.strategies),
        "commentaries_generated": len(app_state.commentaries),
        "files_uploaded": len(app_state.uploaded_files)
    }
    