from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_orchestrator
from ..state import AgentState

def sql_orchestrator_node(state : AgentState):
    response = sql_orchestrator.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'explanation': response['structured_response'].explanation,
        'messages': [HumanMessage(content=state['user_input'])]
    }