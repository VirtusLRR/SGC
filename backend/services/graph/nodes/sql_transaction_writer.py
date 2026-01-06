from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_transaction_writer
from ..state import AgentState
import json

def sql_transaction_writer_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    # Converter os dados estruturados em mensagem
    instruction_data = state['sql_transaction_instruction']

    # Converter para JSON string para passar ao agente
    if hasattr(instruction_data, 'model_dump'):
        instruction_json = json.dumps(instruction_data.model_dump(), ensure_ascii=False, indent=2)
    elif isinstance(instruction_data, list):
        instruction_json = json.dumps([item.model_dump() if hasattr(item, 'model_dump') else item for item in instruction_data], ensure_ascii=False, indent=2)
    else:
        instruction_json = json.dumps(instruction_data, ensure_ascii=False, indent=2)

    # Adicionar histórico ao request
    full_request = f"Histórico da conversa:\n\n{full_context}\n\nProcesse os seguintes dados de transações:\n\n{instruction_json}"

    response = sql_transaction_writer.invoke({"input": full_request})

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
