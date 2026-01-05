from ..schemas import OrchestratorOutputSchema
from ..utils import agent_factory

sql_item_agent = agent_factory("sql_item", OrchestratorOutputSchema)