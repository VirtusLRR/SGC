from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from ..utils import load_prompt
from pydantic import BaseModel
from dotenv import load_dotenv
from ..tools.sql import (
    check_recipe_availability,
    list_all_recipes_tool,
    find_recipe_by_name_tool,
    add_recipe_tool,
    delete_recipe_tool,
    update_recipe_tool
)

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

sql_recipe_writer = create_agent(
    model=llm,
    system_prompt=load_prompt("sql_recipe_writer"),
    tools=[
        check_recipe_availability,
        list_all_recipes_tool,
        find_recipe_by_name_tool,
        add_recipe_tool,
        delete_recipe_tool,
        update_recipe_tool
    ]
)