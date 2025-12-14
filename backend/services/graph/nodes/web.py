from langchain_core.messages import HumanMessage, AIMessage
from ..agents import web_agent

def web_node(state : AgentState):
    print("Query Web:", state['user_input'])
    response = web_agent.invoke({
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