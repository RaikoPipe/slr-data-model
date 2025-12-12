from langchain_core.output_parsers import PydanticOutputParser
from src.slr_data_model import AISystem
from rich import print

parser = PydanticOutputParser(pydantic_object=AISystem)

print(parser.get_format_instructions())