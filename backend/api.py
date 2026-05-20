from fastapi import FastAPI
from pydantic import BaseModel

from main import run_pipeline

app = FastAPI()


class CrisisRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "CIRO backend running"}


@app.post("/analyze")
def analyze_crisis(data: CrisisRequest):

    # RUN PIPELINE
    run_pipeline(data.message)

    # IMPORTANT:
    # IMPORT STATE AGAIN AFTER PIPELINE
    import core.state as state_module

    crisis_state = state_module.crisis_state

    return {
        "signals": crisis_state.collected_signals,
        "crisis": crisis_state.detected_crisis,
        "action_plan": crisis_state.action_plan,
        "simulation": crisis_state.simulation,
        "outcome": crisis_state.outcome,
        "logs": crisis_state.logs
    }