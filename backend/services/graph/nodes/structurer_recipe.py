from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_recipe_agent
from ..state import AgentState

def structurer_recipe_node(state: AgentState):
    history = state['messages'][-2:]

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    # Pegar apenas a última mensagem do usuário para a solicitação atual
    user_messages = [msg for msg in history if isinstance(msg, HumanMessage)]
    current_request = user_messages[-1].content if user_messages else state.get('user_input', 'Nenhuma solicitação encontrada.')

    response = structurer_recipe_agent.invoke({
        "messages": [
            HumanMessage(content=f'Solicitação atual do usuário:\n\n{current_request}\n\nHistórico completo da conversa:\n\n{full_context}\n\nExtraia e estruture APENAS as receitas mencionadas NESTA solicitação específica. Ignore qualquer receita mencionada anteriormente.')
        ]
    })

    structured_response = response['structured_response']

    return {
        'sql_recipe_instruction': structured_response,
        'messages': state['messages']
    }