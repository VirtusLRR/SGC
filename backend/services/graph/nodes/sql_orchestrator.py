from langchain_core.messages import HumanMessage, AIMessage
from ..agents import sql_orchestrator
from ..state import AgentState

def sql_orchestrator_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    response = sql_orchestrator.invoke({
        "messages": [
            HumanMessage(content=state['user_input']),
            HumanMessage(content=f'Histórico completo da conversa:\n\n{full_context}')
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'explanation': response['structured_response'].explanation,
        'query_sql': response['structured_response'].query_sql,
        'sql_response': "RESET",
        'sql_item_instruction': None,
        'sql_recipe_instruction': None,
        'sql_transaction_instruction': None
    }