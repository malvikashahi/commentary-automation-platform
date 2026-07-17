from fastapi import APIRouter, HTTPException
from backend.models.state import app_state

router = APIRouter()

@router.get("/review/{account_id}")
def get_review_data(account_id: str):
    commentary = app_state.commentaries.get(account_id)
    if not commentary:
        raise HTTPException(404, f"No commentary found for account {account_id}")
    comparison = app_state.comparisons.get(account_id)
    return {
        "commentary": commentary,
        "comparison": comparison,
        "account_id": account_id
    }