# SLR Data Model

Pydantic data models for representing AI systems in systematic literature reviews.

## Overview

This package provides comprehensive Pydantic models for representing and validating AI system architectures, including:

- **AI Systems**: Complete system definitions with agents, models, and orchestration
- **Agent Architecture**: Multi-agent systems with collaboration patterns
- **Memory Systems**: Short-term, long-term, and episodic memory models
- **Validation Methods**: Structured validation and outcome reporting
- **Domain Types**: Classification of application domains

## Installation

### From PyPI (once published)

```bash
pip install slr-data-model
```

### From Source

```bash
git clone https://github.com/RaikoPipe/slr-data-model.git
cd slr-data-model
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Usage

```python
from slr_data_model import (
    AISystem,
    AIAgent,
    GenAIModel,
    AutonomyLevel,
    ParadigmType,
    ModalityType
)

# Create a GenAI model
model = GenAIModel(
    name="GPT-4",
    provider="OpenAI",
    model_family="GPT",
    modalities=[ModalityType.Conversational]
)

# Create an AI agent
agent = AIAgent(
    name="Research Assistant",
    role="researcher",
    autonomy_level=AutonomyLevel.SEMI_AUTONOMOUS,
    model=model
)

# Create an AI system
system = AISystem(
    name="Research AI System",
    paradigm=ParadigmType.AGENT_BASED,
    agents=[agent]
)

# Validate and export
print(system.model_dump_json(indent=2))
```

## Key Components

### AISystem
Main container for AI system definitions, including agents, orchestration patterns, and validation methods.

### AIAgent
Represents individual agents with roles, autonomy levels, and capabilities.

### GenAIModel
Defines generative AI models with capabilities, modalities, and parameters.

### Memory
Models for different memory types (short-term, long-term, episodic) with retrieval strategies.

### ValidationMethod
Structured representation of validation approaches and reported outcomes.

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

## Requirements

- Python >= 3.8
- Pydantic >= 2.0.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
