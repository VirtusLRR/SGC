from pydantic import BaseModel

class SQLOrchestratorOutputSchema(BaseModel):
    next_agent: str
    query_sql: str
    explanation: str