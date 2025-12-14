from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_agent

def sql_node(state : AgentState):
    response = sql_agent.invoke(state['user_input'])
    return {
        'sql_response': response['output'][0]['text']
    }