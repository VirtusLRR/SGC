from langchain_core.messages import HumanMessage, AIMessage
from ..agents import revisor_agent

def revisor_node(state : AgentState):
    response = revisor_agent.invoke({
        "messages": [
            HumanMessage(content=f"Pergunta inicial: {state['user_input']}\nResposta SQL: {state['sql_response']}")
        ]
    })
    return {
        'next_agent': response['structured_response'].next_agent,
        'user_input': response['structured_response'].query_web,
        'final_answer': state['sql_response']
    }