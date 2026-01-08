from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_item_writer
from ..state import AgentState
import json

def sql_item_writer_node(state : AgentState):
    if state['past_agent'] == 'sql_item':
        full_request = state['query_sql']
    else:
        instruction_data = state['sql_item_instruction']
        if hasattr(instruction_data, 'model_dump'):
            instruction_json = json.dumps(instruction_data.model_dump(), ensure_ascii=False, indent=2)
        elif isinstance(instruction_data, list):
            instruction_json = json.dumps([item.model_dump() if hasattr(item, 'model_dump') else item for item in instruction_data], ensure_ascii=False, indent=2)
        else:
            instruction_json = json.dumps(instruction_data, ensure_ascii=False, indent=2)

        full_request = f"Processe os seguintes dados de itens:\n\n{instruction_json}"

    response = sql_item_writer.invoke(full_request)
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

    elif isinstance(response, str):
        sql_response = response

    else:
        sql_response = str(response)

    return {
        'sql_response': [sql_response],
        'past_agent': 'sql_item_writer'
    }
