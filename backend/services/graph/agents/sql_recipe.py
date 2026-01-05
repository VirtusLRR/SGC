from ..schemas import OrchestratorOutputSchema
from ..utils import agent_factory

sql_recipe_agent = agent_factory("sql_recipe", OrchestratorOutputSchema)