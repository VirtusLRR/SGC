from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_item_agent
from ..state import AgentState

def structurer_item_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    response = structurer_item_agent.invoke({
        "messages": [
            HumanMessage(content=f'Histórico completo da conversa:\n\n{full_context}\n\nAgora extraia e estruture as receitas mencionadas.')
        ]
    })

    structured_response = response['structured_response']
    items = structured_response.get('items', [])
    items_data = [item['item_data'] for item in items]
    transactions_data = [item['transaction_data'] for item in items]

    return {
        'sql_item_instruction': items_data,
        'sql_transaction_instruction': transactions_data
    }