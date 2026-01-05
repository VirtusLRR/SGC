from ..schemas import StructurerOutputSchemaList
from ..utils import agent_factory

structurer_recipe_agent = agent_factory("structurer_recipe", StructurerOutputSchemaList)