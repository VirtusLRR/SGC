from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_transaction_agent
from ..state import AgentState

def sql_transaction_node(state : AgentState):
    response = sql_transaction_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input'])
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'explanation': response['structured_response'].explanation,
        'messages': [HumanMessage(content=state['user_input'])]
    }