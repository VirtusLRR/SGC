from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import create_agent
from ..utils import load_prompt
from ..utils import get_sql_db
from pydantic import BaseModel
from dotenv import load_dotenv
from ..tools.sql import (
    add_transaction_tool,
    get_transaction_history_tool,
)

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = get_sql_db(DATABASE_URL, ["Transaction"])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)


sql_transaction_writer = create_sql_agent(
    llm, db=db, verbose=True, agent_type="tool-calling",
    handle_parsing_errors=True, prefix_prompt=load_prompt("sql_transaction_writer"),
    extra_tools=[
        add_transaction_tool,
        get_transaction_history_tool,
    ]
)