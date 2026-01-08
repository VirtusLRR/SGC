from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain_community.utilities import SQLDatabase
from sqlalchemy.exc import OperationalError
from langchain.agents import create_agent
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
import yaml
import time

def load_prompt(prompt_name: str) -> dict:
    """Carrega um arquivo de prompt YAML"""
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "prompts" / f"{prompt_name}.yaml"

    with open(prompt_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file).get(f'{prompt_name}_prompt', '')

def get_sql_db(url, tables, retries=5, delay=2):
    for i in range(retries):
        try:
            return SQLDatabase.from_uri(url, include_tables=tables)
        except (ValueError, OperationalError) as e:
            print(f"Aguardando tabelas serem criadas... Tentativa {i+1}")
            time.sleep(delay)


