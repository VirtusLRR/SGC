from langchain_core.messages import HumanMessage, AIMessage
from ..agents import trivial_agent
from ..state import AgentState

def trivial_node(state : AgentState):
    history = state['messages']

    context_messages = []
    for msg in history:
        if isinstance(msg, HumanMessage):
            context_messages.append(f"Usuário: {msg.content}")
        elif isinstance(msg, AIMessage):
            context_messages.append(f"Assistente: {msg.content}")

    full_context = "\n\n".join(context_messages)

    response = trivial_agent.invoke({
        "messages": [
            HumanMessage(content=state['user_input']),
            HumanMessage(content=f'Histórico completo da conversa:\n\n{full_context}')
        ]
    })
    return {
        'final_answer': response['messages'][-1].content,
        'messages': [
            HumanMessage(content=state['user_input']),
            AIMessage(content=response['messages'][-1].content)
        ]
    }