from langchain_core.messages import HumanMessage, AIMessage
from ..agents import orchestrator_agent

def orquestration_node(state : AgentState):
    response = orchestrator_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'orchestrator_explanation': response['structured_response'].orchestrator_explanation,
        'messages': [HumanMessage(content=state['user_input'])]
    }