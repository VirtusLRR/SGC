from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from pydantic import BaseModel
from pathlib import Path
import yaml

def load_prompt(prompt_name: str) -> dict:
    """Carrega um arquivo de prompt YAML"""
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "prompts" / f"{prompt_name}.yaml"

    with open(prompt_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file).get(f'{prompt_name}_prompt', '')



