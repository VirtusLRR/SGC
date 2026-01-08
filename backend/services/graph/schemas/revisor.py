from pydantic import BaseModel
from typing import Optional

class RevisorOutputSchema(BaseModel):
    next_agent: str
    final_answer: Optional[str]
    query_web: str