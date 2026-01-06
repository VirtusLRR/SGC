import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    orchestrator_node,
    trivial_node,
    sql_node,
    revisor_node,
    web_node,
    sql_item_node,
    sql_item_reader_node,
    sql_item_writer_node,
    sql_recipe_node,
    sql_recipe_reader_node,
    sql_recipe_writer_node,
    sql_transaction_node,
    sql_transaction_reader_node,
    sql_transaction_writer_node,
    sql_orchestrator_node,
    structurer_recipe_node,
    structurer_item_node
)

conn = sqlite3.connect("database/checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(AgentState)

builder.add_node("orchestrator", orchestrator_node)
builder.add_node("sql_orchestrator", sql_orchestrator_node)
builder.add_node("sql_recipe", sql_recipe_node)
builder.add_node("sql_recipe_reader", sql_recipe_reader_node)
builder.add_node("structurer_recipe", structurer_recipe_node)
builder.add_node("sql_recipe_writer", sql_recipe_writer_node)
builder.add_node("sql_item", sql_item_node)
builder.add_node("sql_item_reader", sql_item_reader_node)
builder.add_node("structurer_item", structurer_item_node)
builder.add_node("sql_item_writer", sql_item_writer_node)
builder.add_node("sql_transaction", sql_transaction_node)
builder.add_node("sql_transaction_reader", sql_transaction_reader_node)
builder.add_node("sql_transaction_writer", sql_transaction_writer_node)
builder.add_node("trivial", trivial_node)
builder.add_node("revisor", revisor_node)
builder.add_node("web", web_node)
builder.set_entry_point("orchestrator")

builder.add_conditional_edges(
    "orchestrator",
    lambda state: state['next_agent'],
    {
        "TRIVIAL": "trivial",
        "SQL_ORCHESTRATOR": "sql_orchestrator",
        "WEB": "web",
    }
)

builder.add_conditional_edges(
    "sql_orchestrator",
    lambda state: state['next_agent'],
    {
        "SQL_RECIPE": "sql_recipe",
        "SQL_ITEM": "sql_item",
        "SQL_TRANSACTION": "sql_transaction"
    }
)

builder.add_conditional_edges(
    "sql_recipe",
    lambda state: state['next_agent'],
    {
        "RECIPE_READER": "sql_recipe_reader",
        "STRUCTURER_RECIPE": "structurer_recipe",
        "RECIPE_WRITER": "sql_recipe_writer"
    }
)

builder.add_conditional_edges(
    "sql_item",
    lambda state: state['next_agent'],
    {
        "ITEM_READER": "sql_item_reader",
        "STRUCTURER_ITEM": "structurer_item",
        "ITEM_WRITER": "sql_item_writer"
    }
)

builder.add_conditional_edges(
    "sql_transaction",
    lambda state: state['next_agent'],
    {
        "TRANSACTION_READER": "sql_transaction_reader",
        "TRANSACTION_WRITER": "sql_transaction_writer"
    }
)

builder.add_edge("structurer_recipe", "sql_recipe_writer")
builder.add_edge("structurer_item", "sql_item_writer")
builder.add_edge("structurer_item", "sql_transaction_writer")

builder.add_edge("sql_recipe_reader", "revisor")
builder.add_edge("sql_item_reader", "revisor")
builder.add_edge("sql_transaction_reader", "revisor")
builder.add_edge("sql_recipe_writer", "revisor")
builder.add_edge("sql_item_writer", "revisor")
builder.add_edge("sql_transaction_writer", "revisor")

builder.add_conditional_edges(
    "revisor",
    lambda state: state['next_agent'],
    {
        "FINALIZAR": END,
        "WEB": "web"
    }
)

builder.add_edge("web", END)
builder.add_edge("trivial", END)

graph = builder.compile(checkpointer=memory)


