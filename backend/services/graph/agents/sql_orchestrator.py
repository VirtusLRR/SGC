from ..schemas import OrchestratorOutputSchema
from ..utils import agent_factory

sql_orchestrator_agent = agent_factory("sql_orchestrator", OrchestratorOutputSchema)