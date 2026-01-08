from langchain_core.messages import HumanMessage, AIMessage
from ..agents import revisor_agent
from ..state import AgentState

def revisor_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    response = revisor_agent.invoke({
        "messages": [
            HumanMessage(content=f"Pergunta inicial: {state['query_sql']}\nResposta SQL: {str(state['sql_response'])}"),
            HumanMessage(content=f'Histórico completo da conversa:\n\n{full_context}')
        ]
    })

    final_answer_value = response['structured_response'].final_answer
    return {
        'next_agent': response['structured_response'].next_agent,
        'user_input': response['structured_response'].query_web,
        'final_answer': final_answer_value,
        'sql_response': "RESET",
        'messages': (
            [HumanMessage(content=final_answer_value)]
            if final_answer_value != "N/A" else state['messages']
        )
    }