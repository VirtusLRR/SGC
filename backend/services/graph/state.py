from typing import TypedDict, Optional, Any, Union
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
import operator


def sql_response_reducer(left: list[AnyMessage], right: Union[list[AnyMessage], str, None]) -> list[AnyMessage]:
    """
    Reducer que permite adicionar ou resetar sql_response
    """
    if isinstance(right, str) and right == "RESET":
        return []
    if isinstance(right, list):
        return left + right
    return left

class AgentState(TypedDict):
    user_input: str
    next_agent: str
    past_agent: str
    explanation: str
    sql_response: Annotated[list[AnyMessage], sql_response_reducer]
    query_sql: Optional[Any]
    final_answer: str
    sql_item_instruction: Optional[Any]
    sql_recipe_instruction: Optional[Any]
    sql_transaction_instruction: Optional[Any]
    messages: Annotated[list[AnyMessage], operator.add]