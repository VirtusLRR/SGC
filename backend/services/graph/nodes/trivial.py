from langchain_core.messages import HumanMessage, AIMessage
from ..agents import trivial_agent

def trivial_node(state : AgentState):
    response = trivial_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]
    })
    return {
        'final_answer': response['messages'][-1].content,
        'messages': [
            HumanMessage(content=state['user_input']),
            AIMessage(content=response['messages'][-1].content)
        ]
    }