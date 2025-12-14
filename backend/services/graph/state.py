from typing import TypedDict
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
import operator

class AgentState(TypedDict):
    user_input: Annotated[str, "A mensagem enviada pelo usuário."]
    next_agent: Anootated[str, "O próximo agente a ser chamado"]
    orquestration_explaination: Annotated[str, "Instruções do agente orquestrador sobre qual agente especializado foi chamado e o motivo"]
    sql_response: Annotated[str, "A resposta retornada pelo agente SQL"]
    final_answer: Annotated[str, "A resposta final compilada para o usuário."]
    messages: Annotated[list[AnyMessage], operator.add, "Lista de mensagens trocadas entre o usuário e os agentes."]