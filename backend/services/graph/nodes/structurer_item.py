from langchain_core.messages import HumanMessage, AIMessage
from ..agents import structurer_item_agent
from ..state import AgentState

def structurer_item_node(state : AgentState):
    print("Past agent:", state['past_agent'])
    response = structurer_item_agent.invoke({
        "messages": [
            HumanMessage(content=f'PAST_AGENT: {state['past_agent']}\nSolicitação atual do usuário:\n\n{state['query_sql']}\n\nExtraia e estruture APENAS os itens mencionados NESTA solicitação específica. Ignore qualquer item mencionado anteriormente.')
        ]
    })

    structured_response = response['structured_response']

    items = structured_response.items if hasattr(structured_response, 'items') else []

    items_data = [item.item_data for item in items]
    transactions_data = [item.transaction_data for item in items]

    return {
        'sql_item_instruction': items_data,
        'sql_transaction_instruction': transactions_data
    }