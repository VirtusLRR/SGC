from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_recipe_agent
from ..state import AgentState

def structurer_recipe_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    response = structurer_recipe_agent.invoke({
        "messages": [
            HumanMessage(content=f'Histórico completo da conversa:\n\n{full_context}\n\nAgora extraia e estruture as receitas mencionadas.')
        ]
    })

    sql_instruction = f"Por favor, insira estas receitas no banco de dados:\n{response['structured_response']}"

    return {
        'user_input': sql_instruction,
        'messages': [AIMessage(content=sql_instruction)]
    }