from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from ..schemas import StructurerOutputSchemaList
from ..utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)

structurer_recipe_agent = create_agent(
    model=llm,
    system_prompt=load_prompt("structurer_recipe"),
    response_format=ToolStrategy(StructurerOutputSchemaList)
)

