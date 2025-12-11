"""
Pytest tests for the AI System data model.
Tests the model using a simple example of a code generation AI agent.
"""

import pytest
import sys
from pathlib import Path

# Add src to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model.ai_system import (
    AISystem,
    AgentArchitecture,
    AIAgent,
    GenAIModel,
    ModelCapabilities,
    ToolUse,
    ContextEngineeringTechniques,
    AutonomyLevel,
)
from model.memory import Memory, MemoryType, MemoryScope, RetrievalStrategy
from model.ai_system_types import (
    ParadigmType,
    AgentRoleType,
    ReasoningCapabilitiesType,
    CapabilityAcquisitionType,
    ModalityType,
    ExternalToolsType,
)
from model.validation import ValidationMethod, ReportedOutcomes
from model.domain import Domain, DomainType


def test_simple_code_generation_agent():
    """
    Test creating a simple single-agent AI system for code generation.
    This represents a basic AI agent that can generate code using ReAct reasoning.
    """

    # Create memory configuration (no memory in this simple example)
    memory = Memory(
        has_memory=False,
        memory_types=set(),
        memory_scopes=set(),
        retrieval_strategies=set(),
        shared_across_agents=False
    )

    # Create tool configuration
    tool_use = ToolUse(
        has_tools=True,
        external_tools={ExternalToolsType.FUNCTION_CALLING, ExternalToolsType.API_CALL},
        choice_reasoning="Agent uses function calling for code execution and API calls for documentation lookup"
    )

    # Create model capabilities
    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.TEXT}
    )

    # Create the GenAI model
    genai_model = GenAIModel(
        model_name="GPT-4",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )

    # Create the AI agent
    agent = AIAgent(
        agent_role=AgentRoleType.CODER,
        reasoning_capabilities={ReasoningCapabilitiesType.REACT, ReasoningCapabilitiesType.CHAIN_OF_THOUGHT},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model,
        multiple_instances=False
    )

    # Create agent architecture
    agent_architecture = AgentArchitecture(
        agents=[agent],
        orchestration_pattern=None,  # Single agent system
        autonomy_level={AutonomyLevel.SEMI_AUTONOMOUS},
        shared_memory=False
    )

    # Create context engineering
    context_engineering = ContextEngineeringTechniques(
        tool_use=tool_use,
        memory=memory,
        prompt_engineering_details="System prompt with coding guidelines and few-shot examples"
    )

    # Create reported outcomes
    reported_outcomes = ReportedOutcomes(
        decision_quality_improvement="Code quality improved by 30% compared to baseline",
        response_time_impact="Average response time: 5 seconds",
        reliability_metrics="95% success rate on benchmark tasks",
        failure_modes={"syntax errors on complex nested structures", "struggles with ambiguous requirements"},
        limitations={"limited to Python and JavaScript", "requires clear specifications"}
    )

    # Create application domain
    domain = Domain(name={DomainType.OTHER})

    # Create the complete AI system
    ai_system = AISystem(
        application_domains={domain},
        application_domains_reasoning="General-purpose code generation across software development tasks",
        paradigm=ParadigmType.AGENTIC_AI,
        paradigm_reasoning="Uses ReAct reasoning with autonomous tool use and iterative problem-solving",
        agent_architecture=agent_architecture,
        context_engineering=context_engineering,
        validation_methods={ValidationMethod.BENCHMARK, ValidationMethod.CASE_STUDY},
        reported_outcomes=reported_outcomes
    )

    # Assertions to verify the system was created correctly
    assert ai_system.paradigm == ParadigmType.AGENTIC_AI
    assert len(ai_system.agent_architecture.agents) == 1
    assert ai_system.agent_architecture.agents[0].agent_role == AgentRoleType.CODER
    assert ReasoningCapabilitiesType.REACT in ai_system.agent_architecture.agents[0].reasoning_capabilities
    assert ai_system.context_engineering.tool_use.has_tools is True
    assert ExternalToolsType.FUNCTION_CALLING in ai_system.context_engineering.tool_use.external_tools
    assert ValidationMethod.BENCHMARK in ai_system.validation_methods


def test_agent_must_have_reasoning_capabilities():
    """Test that an agent must have at least one reasoning capability."""

    memory = Memory(has_memory=False)
    tool_use = ToolUse(has_tools=False)
    model_capabilities = ModelCapabilities()
    genai_model = GenAIModel(
        model_name="Test Model",
        model_capabilities=model_capabilities
    )

    # Should raise validation error for empty reasoning capabilities
    with pytest.raises(ValueError, match="must have at least one reasoning capability"):
        AIAgent(
            agent_role=AgentRoleType.CODER,
            reasoning_capabilities=set(),  # Empty set should fail
            memory=memory,
            tools=tool_use,
            genai_model=genai_model
        )


def test_multi_agent_requires_orchestration():
    """Test that multi-agent systems must specify orchestration pattern."""

    # Create two simple agents
    memory = Memory(has_memory=False)
    tool_use = ToolUse(has_tools=False)
    model_capabilities = ModelCapabilities()
    genai_model = GenAIModel(
        model_name="Test Model",
        model_capabilities=model_capabilities
    )

    agent1 = AIAgent(
        agent_role=AgentRoleType.PLANNER,
        reasoning_capabilities={ReasoningCapabilitiesType.CHAIN_OF_THOUGHT},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model
    )

    agent2 = AIAgent(
        agent_role=AgentRoleType.CODER,
        reasoning_capabilities={ReasoningCapabilitiesType.REACT},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model
    )

    # Should raise validation error for missing orchestration pattern
    with pytest.raises(ValueError, match="Multi-agent system must specify orchestration pattern"):
        AgentArchitecture(
            agents=[agent1, agent2],
            orchestration_pattern=None,  # Should fail for multi-agent
            autonomy_level={AutonomyLevel.SEMI_AUTONOMOUS},
            shared_memory=False
        )


def test_single_agent_no_orchestration():
    """Test that single-agent systems should not have orchestration pattern."""
    from model.ai_system import OrchestrationPattern
    from model.ai_system_types import (
        CollaborationMechanismType,
        CollaborationStructureType,
        CollaborationStrategyType
    )

    memory = Memory(has_memory=False)
    tool_use = ToolUse(has_tools=False)
    model_capabilities = ModelCapabilities()
    genai_model = GenAIModel(
        model_name="Test Model",
        model_capabilities=model_capabilities
    )

    agent = AIAgent(
        agent_role=AgentRoleType.MONOLITHIC,
        reasoning_capabilities={ReasoningCapabilitiesType.RULE_BASED},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model
    )

    orchestration = OrchestrationPattern(
        collaboration_mechanism={CollaborationMechanismType.COOPERATION},
        collaboration_structure={CollaborationStructureType.CENTRALIZED},
        collaboration_strategy={CollaborationStrategyType.RULE_BASED}
    )

    # Should raise validation error for single agent with orchestration
    with pytest.raises(ValueError, match="Single-agent system should not have orchestration pattern"):
        AgentArchitecture(
            agents=[agent],
            orchestration_pattern=orchestration,  # Should fail for single agent
            autonomy_level={AutonomyLevel.FIXED_WORKFLOW},
            shared_memory=False
        )


def test_memory_configuration():
    """Test memory configuration with various settings."""

    # Test memory with full configuration
    memory = Memory(
        has_memory=True,
        memory_types={MemoryType.VECTOR_DATABASE, MemoryType.CONVERSATION_HISTORY},
        memory_scopes={MemoryScope.SHORT_TERM, MemoryScope.LONG_TERM},
        retrieval_strategies={RetrievalStrategy.SEMANTIC_SEARCH, RetrievalStrategy.RERANKING},
        shared_across_agents=True
    )

    assert memory.has_memory is True
    assert MemoryType.VECTOR_DATABASE in memory.memory_types
    assert MemoryScope.LONG_TERM in memory.memory_scopes
    assert RetrievalStrategy.SEMANTIC_SEARCH in memory.retrieval_strategies
    assert memory.shared_across_agents is True


def test_model_serialization():
    """Test that the model can be serialized to and from JSON."""

    # Create a minimal valid AI system
    memory = Memory(has_memory=False)
    tool_use = ToolUse(has_tools=False)
    model_capabilities = ModelCapabilities()
    genai_model = GenAIModel(
        model_name="Test Model",
        model_capabilities=model_capabilities
    )

    agent = AIAgent(
        agent_role=AgentRoleType.MONOLITHIC,
        reasoning_capabilities={ReasoningCapabilitiesType.RULE_BASED},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model
    )

    agent_architecture = AgentArchitecture(
        agents=[agent],
        orchestration_pattern=None,
        autonomy_level={AutonomyLevel.FIXED_WORKFLOW},
        shared_memory=False
    )

    context_engineering = ContextEngineeringTechniques(
        tool_use=tool_use,
        memory=memory
    )

    reported_outcomes = ReportedOutcomes()
    domain = Domain(name={DomainType.PRODUCTION_PLANNING})

    ai_system = AISystem(
        application_domains={domain},
        application_domains_reasoning="Test domain",
        paradigm=ParadigmType.AI_AGENT,
        paradigm_reasoning="Test reasoning",
        agent_architecture=agent_architecture,
        context_engineering=context_engineering,
        validation_methods={ValidationMethod.SIMULATION},
        reported_outcomes=reported_outcomes
    )

    # Serialize to dict
    system_dict = ai_system.model_dump()
    assert isinstance(system_dict, dict)
    assert system_dict["paradigm"] == "ai-agent"

    # Serialize to JSON
    json_str = ai_system.model_dump_json()
    assert isinstance(json_str, str)
    assert "ai-agent" in json_str

    # Deserialize from dict
    recreated_system = AISystem.model_validate(system_dict)
    assert recreated_system.paradigm == ParadigmType.AI_AGENT
    assert recreated_system.paradigm_reasoning == "Test reasoning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
