from langchain_tavily import TavilySearch
import os

tavily_api_key = os.getenv('TAVILY_API_KEY')

search_web_tool = TavilySearch(api_key=tavily_api_key, num_results=5)