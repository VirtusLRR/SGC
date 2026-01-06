from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_recipe_agent
from ..state import AgentState

def structurer_recipe_node(state: AgentState):
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

    structured_response = response['structured_response']

    return {
        'sql_recipe_instruction': structured_response,
        'messages': state['messages']
    }