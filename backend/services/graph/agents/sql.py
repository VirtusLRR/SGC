from ..tools.sql import add_recipe_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from ..utils import load_prompt
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    timeout=None,
)

db = SQLDatabase.from_uri("sqlite:///database/sqlite.db")

sql_agent = create_sql_agent(
    llm, db=db, verbose= True, agent_type="tool-calling",
    handle_parsing_errors=True, prefix_prompt=load_prompt("sql"), extra_tools=[add_recipe_tool]
)