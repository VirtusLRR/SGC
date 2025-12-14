from pydantic import BaseModel

class OrchestratorOutputSchema(BaseModel):
    next_agent: str
    orquestration_explaination: str