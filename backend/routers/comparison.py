# backend/routers/comparison.py

from fastapi import APIRouter, HTTPException
from backend.models.state import app_state

router = APIRouter()


@router.get("/compare")
def get_all_comparisons(strategy_id: str = None):
    """Retrieve all comparison results, optionally filtered by strategy."""
    comparisons = list(app_state.comparisons.values())

    if strategy_id:
        comparisons = [
            c for c in comparisons
            if hasattr(c, 'account_id') and
            c.account_id in [
                acc.account_id
                for s in app_state.strategies.values()
                if s.strategy_id == strategy_id
                for acc in s.accounts
            ]
        ]

    return {
        "total": len(comparisons),
        "comparisons": comparisons
    }


@router.get("/compare/{account_id}")
def get_comparison(account_id: str):
    """Retrieve comparison result for a specific account."""
    comparison = app_state.comparisons.get(account_id)
    if not comparison:
        # Return a default/pending comparison if not yet computed
        return {
            "account_id": account_id,
            "status": "pending",
            "message": "Comparison not yet computed. Run /api/process first.",
            "match_score": None,
            "classification": None
        }
    return comparison


@router.get("/scores")
def get_all_scores(strategy_id: str = None):
    """Retrieve match scores for all accounts."""
    scores = []

    for account_id, comparison in app_state.comparisons.items():
        scores.append({
            "account_id": account_id,
            "match_score": comparison.match_score,
            "classification": comparison.classification,
            "holdings_overlap": comparison.holdings_overlap,
            "performance_match": comparison.performance_match,
            "transaction_overlap": comparison.transaction_overlap,
            "narrative_match": comparison.narrative_match,
            "compared_at": comparison.compared_at
        })

    # Sort by match score descending
    scores.sort(key=lambda x: x["match_score"] or 0, reverse=True)

    return {
        "total": len(scores),
        "scores": scores
    }


@router.get("/scores/{account_id}")
def get_score(account_id: str):
    """Retrieve match score for a specific account."""
    comparison = app_state.comparisons.get(account_id)
    if not comparison:
        return {
            "account_id": account_id,
            "match_score": None,
            "classification": "Pending",
            "message": "Score not yet computed."
        }
    return {
        "account_id": account_id,
        "match_score": comparison.match_score,
        "classification": comparison.classification,
        "holdings_overlap": comparison.holdings_overlap,
        "performance_match": comparison.performance_match,
        "transaction_overlap": comparison.transaction_overlap,
        "narrative_match": comparison.narrative_match
    }