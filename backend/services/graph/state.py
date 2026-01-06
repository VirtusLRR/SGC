from typing import TypedDict, Optional, Any
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
import operator

class AgentState(TypedDict):
    user_input: str
    next_agent: str
    explanation: str
    sql_response: Annotated[list[AnyMessage], operator.add]
    final_answer: str
    sql_item_instruction: Optional[Any]
    sql_recipe_instruction: Optional[Any]
    sql_transaction_instruction: Optional[Any]
    messages: Annotated[list[AnyMessage], operator.add]