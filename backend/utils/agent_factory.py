from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from services.graph.schemas import OrchestratorOutputSchema
from services.graph.utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

def agent_factory(prompt_name: str, output_schema: BaseModel):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5)

    agent = create_agent(
        model=llm,
        system_prompt=load_prompt(prompt_name),
        response_format=ToolStrategy(output_schema)
    )
    return agent


