import pytest
from pydantic import ValidationError
from src import *


def test_minimal_single_agent_system():
    """Test creating a minimal single-agent system."""

    # Create minimal components
    tool_use = ToolUse(
        has_tools=False,
        external_tools=set()
    )

    memory = Memory(
        has_memory=False,
        memory_types=set(),
        memory_scopes=set(),
        retrieval_strategies=set(),
        shared_across_agents=False
    )

    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.TEXT}
    )

    genai_model = GenAIModel(
        model_name="GPT-4",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )

    agent = AIAgent(
        agent_role=AgentRoleType.MONOLITHIC,
        reasoning_capabilities={ReasoningCapabilitiesType.CHAIN_OF_THOUGHT},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model,
        multiple_instances=False
    )

    context_engineering = ContextEngineeringTechniques(
        tool_use=tool_use,
        memory=memory,
        prompt_engineering_details="Uses system prompts with task instructions"
    )

    agent_architecture = AgentArchitecture(
        agents=[agent],
        orchestration_pattern=None,
        autonomy_level={AutonomyLevel.SEMI_AUTONOMOUS},
        shared_memory=False
    )

    outcomes = ReportedOutcomes(
        decision_quality_improvement="20% accuracy improvement",
        response_time_impact=None,
        reliability_metrics=None,
        failure_modes=set(),
        limitations={"Limited to text-only tasks"}
    )

    # Create system
    system = AISystem(
        agent_architecture=agent_architecture,
        context_engineering=context_engineering,
        paradigm=ParadigmType.AGENTIC_AI,
        paradigm_reasoning="Uses chain-of-thought reasoning",
        validation_methods={ValidationMethod.CASE_STUDY},
        reported_outcomes=outcomes,
        application_domains_reasoning="Focused on production logistics tasks",
        application_domains={DomainType.SIMULATION}
    )

    # Assertions
    assert system.paradigm == ParadigmType.AGENTIC_AI
    assert len(system.agent_architecture.agents) == 1
    assert system.agent_architecture.orchestration_pattern is None


def test_multi_agent_with_rag_system():
    """Test creating a multi-agent system with RAG."""

    # RAG-enabled memory
    memory = Memory(
        has_memory=True,
        memory_types={MemoryType.VECTOR_DATABASE},
        memory_scopes={MemoryScope.LONG_TERM},
        retrieval_strategies={RetrievalStrategy.SEMANTIC_SEARCH},
        shared_across_agents=True
    )

    # Tools for agents
    tools = ToolUse(
        has_tools=True,
        external_tools={ExternalToolsType.DATABASE, ExternalToolsType.API_CALL},
        choice_reasoning="Uses database for historical data and APIs for external services"
    )

    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.TEXT}
    )

    genai_model = GenAIModel(
        model_name="Claude-3",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )

    # Create multiple agents
    orchestrator = AIAgent(
        agent_role=AgentRoleType.ORCHESTRATOR,
        reasoning_capabilities={ReasoningCapabilitiesType.REACT},
        memory=memory,
        tools=tools,
        genai_model=genai_model,
        multiple_instances=False
    )

    planner = AIAgent(
        agent_role=AgentRoleType.PLANNER,
        reasoning_capabilities={ReasoningCapabilitiesType.CHAIN_OF_THOUGHT},
        memory=memory,
        tools=tools,
        genai_model=genai_model,
        multiple_instances=False
    )

    orchestration = OrchestrationPattern(
        collaboration_mechanism=set(),
        collaboration_structure={CollaborationStructureType.HIERARCHICAL},
        collaboration_strategy=set()
    )

    context_engineering = ContextEngineeringTechniques(
        tool_use=tools,
        memory=memory,
        prompt_engineering_details="RAG with semantic search"
    )

    agent_architecture = AgentArchitecture(
        agents=[orchestrator, planner],
        orchestration_pattern=orchestration,
        autonomy_level={AutonomyLevel.EXPERT_IN_LOOP},
        shared_memory=True
    )

    outcomes = ReportedOutcomes()

    system = AISystem(
        agent_architecture=agent_architecture,
        context_engineering=context_engineering,
        application_domains={DomainType.SIMULATION},
        application_domains_reasoning="Reasoning",
        paradigm=ParadigmType.AGENTIC_AI,
        paradigm_reasoning="Multi-agent with ReAct and dynamic tool use",
        validation_methods={ValidationMethod.SIMULATION},
        reported_outcomes=outcomes
    )

    # Assertions
    assert len(system.agent_architecture.agents) == 2
    assert system.agent_architecture.shared_memory is True
    assert system.agent_architecture.orchestration_pattern is not None
    assert system.context_engineering.memory.has_memory is True


def test_validation_single_agent_cannot_have_orchestration():
    """Test that single-agent systems cannot have orchestration patterns."""

    tool_use = ToolUse(has_tools=False, external_tools=set())
    memory = Memory(has_memory=False, memory_types=set(), memory_scopes=set(), retrieval_strategies=set())

    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.TEXT}
    )

    genai_model = GenAIModel(
        model_name="GPT-4",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )

    agent = AIAgent(
        agent_role=AgentRoleType.MONOLITHIC,
        reasoning_capabilities={ReasoningCapabilitiesType.RULE_BASED},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model
    )

    orchestration = OrchestrationPattern(
        collaboration_mechanism=set(),
        collaboration_structure={CollaborationStructureType.CENTRALIZED},
        collaboration_strategy=set()
    )

    # Should raise ValidationError
    with pytest.raises(ValidationError, match="Single-agent system should not have orchestration pattern"):
        AgentArchitecture(
            agents=[agent],
            orchestration_pattern=orchestration,
            autonomy_level={AutonomyLevel.FIXED_WORKFLOW},
            shared_memory=False
        )


def test_agent_must_have_reasoning_capability():
    """Test that agents must have at least one reasoning capability."""

    tool_use = ToolUse(has_tools=False, external_tools=set())
    memory = Memory(has_memory=False, memory_types=set(), memory_scopes=set(), retrieval_strategies=set())

    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.TEXT}
    )

    genai_model = GenAIModel(
        model_name="GPT-4",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )

    # Should raise ValidationError for empty reasoning capabilities
    with pytest.raises(ValidationError, match="Agent must have at least one reasoning capability"):
        AIAgent(
            agent_role=AgentRoleType.MONOLITHIC,
            reasoning_capabilities=set(),  # Empty set
            memory=memory,
            tools=tool_use,
            genai_model=genai_model
        )