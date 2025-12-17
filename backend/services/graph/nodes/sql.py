from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_agent
from ..state import AgentState

def sql_node(state : AgentState):
    response = sql_agent.invoke(state['user_input'])

    if isinstance(response, dict):
        if 'output' in response:
            if isinstance(response['output'], list) and len(response['output']) > 0:
                parts = []
                for item in response['output']:
                    if isinstance(item, dict) and 'text' in item:
                        parts.append(item['text'])
                    elif isinstance(item, str):
                        parts.append(item)
                sql_response = ''.join(parts) if parts else str(response['output'])
            else:
                sql_response = response['output']
        else:
            sql_response = str(response)
    else:
        sql_response = str(response)

    return {
        'sql_response': sql_response
    }
