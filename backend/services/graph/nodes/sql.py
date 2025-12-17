from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_agent
from ..state import AgentState

def sql_node(state : AgentState):
    response = sql_agent.invoke(state['user_input'])

    if isinstance(response, dict):
        if 'output' in response:
            if isinstance(response['output'], list) and len(response['output']) > 0:
                sql_response = response['output'][0].get('text', str(response['output']))
            else:
                sql_response = response['output']
        else:
            sql_response = str(response)
    else:
        sql_response = str(response)

    return {
        'sql_response': sql_response
    }
