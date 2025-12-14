from pydantic import BaseModel

class OrchestratorOutputSchema(BaseModel):
    next_agent: str
    orchestrator_explanation: str