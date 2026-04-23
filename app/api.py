from fastapi import APIRouter, HTTPException

from app.data_models import FlowRequest
from app.flow_engine import FlowEngine


router = APIRouter()


@router.post("/api/v1/flow/execute")
def execute_flow(payload: FlowRequest) -> dict:
    """
    Receives the JSON payload, initializes the engine, and runs the flow.
    Args:
        payload (FlowRequest): The incoming request containing the flow definition.
    Returns:
        dict: The result of the flow execution, including status and logs.
    """
    try:
        engine = FlowEngine(payload.flow)
        result: dict = engine.run()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
