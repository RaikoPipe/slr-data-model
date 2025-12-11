# AI System Data Model Tests

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:

```bash
pytest test/test_ai_system.py -v
```

Run a specific test:

```bash
pytest test/test_ai_system.py::test_simple_code_generation_agent -v
```

## Test Coverage

The test suite includes:

1. **test_simple_code_generation_agent**: A comprehensive example creating a simple single-agent AI system for code generation, demonstrating all major model components.

2. **test_agent_must_have_reasoning_capabilities**: Validates that agents must have at least one reasoning capability (validation test).

3. **test_multi_agent_requires_orchestration**: Ensures multi-agent systems specify an orchestration pattern (validation test).

4. **test_single_agent_no_orchestration**: Ensures single-agent systems don't have orchestration patterns (validation test).

5. **test_memory_configuration**: Tests various memory configuration options.

6. **test_model_serialization**: Verifies that models can be serialized to/from JSON and dictionaries.

## Example Usage

The main test `test_simple_code_generation_agent` demonstrates how to create a complete AI system model representing a code generation agent with:

- **Paradigm**: Agentic AI (autonomous reasoning)
- **Agent Role**: Coder
- **Reasoning**: ReAct + Chain-of-Thought
- **Tools**: Function calling and API calls
- **Model**: GPT-4 with prompt engineering
- **Validation**: Benchmark and case study methods
- **Domain**: General software development

This example can serve as a template for creating your own AI system specifications.
