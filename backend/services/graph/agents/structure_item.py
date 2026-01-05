from ..schemas import ItemStructuredOutputList
from ..utils import agent_factory

structurer_item_agent = agent_factory("structurer_item", ItemStructuredOutputList)