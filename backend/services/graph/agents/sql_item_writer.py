from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from ..utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv
from ..tools.sql import (
    list_all_items_tool,
    find_item_by_name_tool,
    add_item_tool,
    update_item_tool,
    delete_item_tool,
    get_low_stock_items_tool,
    get_expired_items_tool
)

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

sql_item_writer = create_agent(
    model=llm,
    system_prompt=load_prompt("sql_item_writer"),
    tools=[
        list_all_items_tool,
        find_item_by_name_tool,
        add_item_tool,
        update_item_tool,
        delete_item_tool,
        get_low_stock_items_tool,
        get_expired_items_tool
    ]
)