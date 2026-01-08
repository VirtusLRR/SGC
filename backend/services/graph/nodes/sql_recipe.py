from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_recipe_agent
from ..state import AgentState

def sql_recipe_node(state : AgentState):
    response = sql_recipe_agent.invoke({
        "messages": [
            HumanMessage(content=state['query_sql']),
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'explanation': response['structured_response'].explanation,
        'messages': [HumanMessage(content=state['query_sql'])]
    }