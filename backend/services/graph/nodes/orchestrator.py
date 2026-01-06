from langchain_core.messages import HumanMessage, AIMessage
from ..agents import orchestrator_agent
from ..state import AgentState

def orchestrator_node(state : AgentState):
    response = orchestrator_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'explanation': response['structured_response'].explanation,
        'messages': [HumanMessage(content=state['user_input'])]
    }