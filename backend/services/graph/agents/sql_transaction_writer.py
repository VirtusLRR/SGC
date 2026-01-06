from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from ..utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv
from ..tools.sql import (
    add_transaction_tool,
    get_transaction_history_tool,
)

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

sql_transaction_writer = create_agent(
    model=llm,
    system_prompt=load_prompt("sql_transaction_writer"),
    tools=[
        add_transaction_tool,
        get_transaction_history_tool,
    ]
)