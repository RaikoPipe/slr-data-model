from langchain_core.output_parsers import PydanticOutputParser
from src.slr_data_model import AISystem, SystemArchitecture
from rich import print

parser = PydanticOutputParser(pydantic_object=SystemArchitecture)

print(AISystem.model_json_schema())