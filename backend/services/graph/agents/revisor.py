from ..schemas import RevisorOutputSchema
from ..utils import agent_factory

revisor_agent = agent_factory("revisor", RevisorOutputSchema)