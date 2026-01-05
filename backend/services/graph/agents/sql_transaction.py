from ..schemas import OrchestratorOutputSchema
from ..utils import agent_factory

sql_transaction_agent = agent_factory("sql_transaction", OrchestratorOutputSchema)