# SLR Data Model

Pydantic data models for representing AI systems in systematic literature reviews.

## Overview

This package provides comprehensive Pydantic models for representing and validating LLM-based AI system architectures. It is designed for researchers conducting systematic literature reviews (SLRs) of AI systems, offering structured data models with rich enumerations and validation.

### Key Features

- **AI System Architecture**: Complete system definitions with agents, models, orchestration patterns, and human integration
- **Agent Components**: Individual agents with roles, context engineering, tool use, and GenAI models
- **Context Engineering**: Memory systems, retrieval strategies, and prompt engineering techniques
- **Human Integration**: Human oversight mechanisms, interaction modalities, and feedback loops
- **Multi-Agent Coordination**: Collaboration strategies and organizational structures
- **Validation Methods**: Structured validation and outcome reporting
- **Domain Classification**: Comprehensive domain and paradigm type taxonomies

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

### Basic Example

```python
from slr_data_model import (
    AISystem,
    SystemArchitecture,
    AIAgent,
    GenAIModel,
    ToolUse,
    ContextEngineering,
    OrchestrationPattern,
    HumanIntegration,
    ParadigmType,
    AgentRoleType,
    ModalityType,
    ExternalToolsType,
    MemoryType,
    MemoryScopeType,
    RetrievalStrategyType,
    TriggerType,
    TaskExecutionType,
    HumanOversightType,
    FeedbackAndLearningType,
    DomainType,
    ValidationMethodType,
    ReportedOutcomes
)

# Define context engineering (memory and prompting)
context_eng = ContextEngineering(
    memory_types=[MemoryType.CONVERSATION_HISTORY, MemoryType.VECTOR_DATABASE],
    memory_scope=[MemoryScopeType.SHORT_TERM, MemoryScopeType.LONG_TERM],
    retrieval_strategies=[RetrievalStrategyType.SEMANTIC_SEARCH],
    prompt_engineering_techniques=[]
)

# Define tool use
tools = ToolUse(
    has_tools=True,
    external_tools=[ExternalToolsType.API_CALL, ExternalToolsType.DATABASE]
)

# Create a GenAI model
model = GenAIModel(
    model_name="GPT-4",
    supported_modalities=[ModalityType.TEXT],
    finetuning_datasets=[],
    finetuning_dataset_description=None
)

# Create an AI agent
agent = AIAgent(
    description="Main orchestrator agent that coordinates task execution",
    role=AgentRoleType.ORCHESTRATOR,
    context_engineering=context_eng,
    tools=tools,
    genai_model=model,
    generated_workers=False
)

# Define orchestration pattern
orchestration = OrchestrationPattern(
    orchestration_pattern_description="Single-agent system with iterative task execution",
    task_execution=TaskExecutionType.SINGLE_STEP,
    multi_agent_coordination_strategy=None
)

# Define human integration
human_integration = HumanIntegration(
    human_integration_description="Human oversight with feedback loops",
    human_oversight_mechanism=[HumanOversightType.POST_ACTION_REVIEW],
    interaction_modalities=[ModalityType.TEXT],
    feedback_and_learning_methods=[FeedbackAndLearningType.CORRECTIVE_FEEDBACK]
)

# Create system architecture
architecture = SystemArchitecture(
    agents=[agent],
    orchestration_pattern=orchestration,
    trigger=TriggerType.HUMAN_TRIGGERED,
    human_integration=human_integration
)

# Create the complete AI system
system = AISystem(
    paper_id="example_paper_2024",
    system_name="Research Assistant System",
    system_description="An AI-powered research assistant for literature analysis",
    paradigm=ParadigmType.AI_AGENT,
    architecture=architecture,
    domain=[DomainType.EDUCATION],
    validation_method=ValidationMethodType.CASE_STUDY,
    reported_outcomes=ReportedOutcomes(
        reported_outcomes_description="System improved research efficiency by 40%"
    )
)

# Validate and export
print(system.model_dump_json(indent=2))
```

### Multi-Agent System Example

```python
from slr_data_model import (
    MultiAgentCoordinationStrategy,
    AgentCollaborationType,
    OrganizationalStructureType
)

# Define multi-agent coordination
coordination = MultiAgentCoordinationStrategy(
    multi_agent_coordination_strategy_description="Hierarchical coordination with specialized agents",
    task_alignment=AgentCollaborationType.COOPERATION,
    organizational_structure=OrganizationalStructureType.HIERARCHICAL
)

# Create multiple specialized agents (coder, planner, retriever, etc.)
# ... define agents with different roles ...

# Use in orchestration pattern
orchestration = OrchestrationPattern(
    orchestration_pattern_description="Multi-agent collaboration with hierarchical structure",
    task_execution=TaskExecutionType.MULTI_AGENT_COLLABORATION,
    multi_agent_coordination_strategy=coordination
)
```

## Key Components

### AISystem
Top-level model representing a complete AI system from a research paper, including:
- System identification (paper ID, name, description)
- Paradigm classification (Generative AI, AI Agent, Agentic AI)
- System architecture with agents and orchestration
- Domain classification
- Validation methods and reported outcomes

### SystemArchitecture
Defines the overall architecture of an LLM-based system:
- **agents**: List of AIAgent instances (single or multiple)
- **orchestration_pattern**: How agents are coordinated
- **trigger**: System initiation mechanism (human or event-triggered)
- **human_integration**: Human oversight and interaction mechanisms

### AIAgent
Individual agent within the system with:
- **role**: Specialized function (orchestrator, coder, planner, retriever, etc.)
- **context_engineering**: Memory and prompt engineering configuration
- **tools**: External tool access and capabilities
- **genai_model**: Underlying generative AI model
- **generated_workers**: Whether instances are spawned dynamically

### GenAIModel
Specification of the generative AI model:
- Model name and identifier
- Supported modalities (text, image, audio, video)
- Fine-tuning dataset types and descriptions

### ContextEngineering
Memory and prompting architecture:
- **memory_types**: Storage mechanisms (conversation history, vector DB, knowledge graph, etc.)
- **memory_scope**: Temporal scope (short-term, long-term)
- **retrieval_strategies**: Information retrieval methods (semantic search, query decomposition, etc.)
- **prompt_engineering_techniques**: Reasoning approaches (ReAct, CoT, Tree of Thought, RAG, etc.)

### HumanIntegration
Human involvement in the AI system:
- **human_oversight_mechanism**: Types of human oversight (pre-action validation, monitoring, escalation, review)
- **interaction_modalities**: How humans interact with the system
- **feedback_and_learning_methods**: How human feedback is incorporated

### OrchestrationPattern
How the system executes tasks:
- **task_execution**: Processing approach (single-step, planning graph, multi-agent collaboration)
- **multi_agent_coordination_strategy**: Collaboration mechanisms for multi-agent systems

### MultiAgentCoordinationStrategy
For multi-agent systems:
- **task_alignment**: How agents align objectives (cooperation, competition, coopetition)
- **organizational_structure**: Control patterns (distributed, centralized, hierarchical, linear)

### ToolUse
External tool integration:
- Whether the agent uses tools
- Types of external tools (API calls, function calling, databases, knowledge bases, etc.)

### Enumeration Types

The package includes comprehensive enumerations for categorization:

- **ParadigmType**: System paradigm (Generative AI, AI Agent, Agentic AI)
- **AgentRoleType**: Agent specializations (monolithic, orchestrator, coder, planner, etc.)
- **ModalityType**: Input/output modalities (text, image, audio, video)
- **ExternalToolsType**: Tool categories (API, MCP, function calling, database, etc.)
- **MemoryType**: Memory mechanisms (conversation history, vector DB, knowledge graph, etc.)
- **RetrievalStrategyType**: Information retrieval methods
- **PromptEngineeringTechniquesType**: Reasoning approaches (ReAct, CoT, ToT, RAG, etc.)
- **TaskExecutionType**: Task processing patterns
- **TriggerType**: System initiation methods
- **HumanOversightType**: Human oversight mechanisms
- **FeedbackAndLearningType**: Feedback incorporation methods
- **AgentCollaborationType**: Multi-agent alignment patterns
- **OrganizationalStructureType**: Multi-agent organization patterns
- **ValidationMethodType**: Research validation approaches
- **DomainType**: Application domain classifications

All enumerations extend `DescriptiveEnum` and include both a value and a human-readable description.

## Use Cases

This data model is designed for researchers conducting systematic literature reviews of AI systems. It enables:

1. **Structured Data Extraction**: Extract AI system characteristics from research papers into a standardized format
2. **Comparative Analysis**: Compare different AI systems across multiple dimensions (paradigm, architecture, validation, etc.)
3. **Taxonomy Development**: Build consistent taxonomies for AI system classification
4. **Meta-Analysis**: Aggregate and analyze trends across multiple AI systems
5. **Reproducibility**: Provide a machine-readable format for AI system descriptions
6. **Knowledge Synthesis**: Enable automated analysis and visualization of AI system characteristics

## Project Structure

```
slr-data-model/
├── src/slr_data_model/
│   ├── __init__.py                 # Package exports
│   ├── ai_system.py                # Main system models (AISystem, AIAgent, etc.)
│   ├── ai_system_types.py          # Type enumerations (ParadigmType, AgentRoleType, etc.)
│   ├── context_engineering.py      # Memory and prompt engineering models
│   ├── validation.py               # Validation method enumerations
│   ├── domain.py                   # Domain classification enumerations
│   ├── descriptive_enum.py         # Base enumeration with descriptions
│   └── annotation_helper.py        # Helper for type annotations
├── test/                           # Test files
├── pyproject.toml                  # Project configuration
└── README.md                       # This file
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

## DescriptiveEnum

All enumerations in this package extend the `DescriptiveEnum` base class, which provides both a value and a human-readable description for each enum member. This makes the enumerations self-documenting and useful for generating UI elements or documentation.

```python
from slr_data_model import ParadigmType

# Access enum value and description
paradigm = ParadigmType.AI_AGENT
print(paradigm.value)        # "ai-agent"
print(paradigm.description)  # "System with fixed workflows and deterministic decision logic..."

# List all options with descriptions
for paradigm in ParadigmType:
    print(f"{paradigm.value}: {paradigm.description}")
```

## Requirements

- Python >= 3.8
- Pydantic >= 2.0.0

## Version

Current version: 0.3.5

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
