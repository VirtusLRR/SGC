from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_recipe_agent
from ..state import AgentState

def structurer_recipe_node(state: AgentState):
    response = structurer_recipe_agent.invoke({
        "messages": [
            HumanMessage(content=f'Solicitação atual do usuário:\n\n{state['query_sql']}\n\nHistórico completo da conversa:\n\n{full_context}\n\nExtraia e estruture APENAS as receitas mencionadas NESTA solicitação específica. Ignore qualquer receita mencionada anteriormente.')
        ]
    })

    structured_response = response['structured_response']

    return {
        'sql_recipe_instruction': structured_response,
        'messages': state['messages']
    }