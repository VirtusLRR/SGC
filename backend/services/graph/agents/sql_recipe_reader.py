from ..tools.sql import add_recipe_tool, check_recipe_availability
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from ..utils import load_prompt
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
)

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = SQLDatabase.from_uri(DATABASE_URL)

sql_recipe_reader = create_sql_agent(
    llm, db=db, verbose=True, agent_type="tool-calling",
    handle_parsing_errors=True, prefix_prompt=load_prompt("sql_recipe_reader"),
    extra_tools=[check_recipe_availability]
)


