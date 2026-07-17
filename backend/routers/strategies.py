from fastapi import APIRouter
from backend.models.state import app_state

router = APIRouter()

@router.get("/strategies")
def list_strategies():
    return list(app_state.strategies.values())

@router.get("/strategies/{strategy_id}/accounts")
def list_accounts(strategy_id: str):
    strategy = app_state.strategies.get(strategy_id)
    if not strategy:
        return {"error": f"Strategy {strategy_id} not found"}
    return strategy.accounts