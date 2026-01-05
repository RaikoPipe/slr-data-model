#!/usr/bin/env python3
"""
Simple verification script to test the AI System model without pytest.
This can be run directly with: python test/verify_model.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from slr_data_model import (
        AISystem,
        SystemArchitecture,
        AIAgent,
        GenAIModel,
        ModelCapabilities,
        ToolUse,
        AutonomyLevel,
        Memory,
        MemoryType,
        MemoryScope,
        RetrievalStrategy,
        ParadigmType,
        AgentRoleType,
        ReasoningCapabilitiesType,
        CapabilityAcquisitionType,
        ModalityType,
        ExternalToolsType,
        ValidationMethod,
        ReportedOutcomes,
        DomainType,
    )

    print("✓ All imports successful!")

    # Create a simple AI system
    print("\nCreating a simple code generation AI agent...")

    memory = Memory(
        has_memory=False,
        memory_types=set(),
        memory_scopes=set(),
        retrieval_strategies=set(),
        shared_across_agents=False
    )
    print("✓ Memory created")

    tool_use = ToolUse(
        has_tools=True,
        external_tools={ExternalToolsType.FUNCTION_CALLING, ExternalToolsType.API_CALL},
        choice_reasoning="Agent uses function calling for code execution and API calls for documentation lookup"
    )
    print("✓ Tool configuration created")

    model_capabilities = ModelCapabilities(
        capability_acquisition_methods={CapabilityAcquisitionType.PROMPT_ENGINEERING},
        supported_modalities={ModalityType.Conversational}
    )
    print("✓ Model capabilities created")

    genai_model = GenAIModel(
        model_name="GPT-4",
        model_capabilities=model_capabilities,
        finetuning_datasets=set()
    )
    print("✓ GenAI model created")

    agent = AIAgent(
        agent_role=AgentRoleType.CODER,
        reasoning_capabilities={ReasoningCapabilitiesType.ITERATIVE_REASONING, ReasoningCapabilitiesType.CHAIN_OF_THOUGHT},
        memory=memory,
        tools=tool_use,
        genai_model=genai_model,
        multiple_instances=False
    )
    print("✓ AI agent created")

    agent_architecture = SystemArchitecture(
        agents=[agent],
        orchestration_pattern=None,
        autonomy_level={AutonomyLevel.SEMI_AUTONOMOUS},
        shared_memory=False
    )
    print("✓ Agent architecture created")

    reported_outcomes = ReportedOutcomes(
        decision_quality_improvement="Code quality improved by 30% compared to baseline",
        response_time_impact="Average response time: 5 seconds",
        reliability_metrics="95% success rate on benchmark tasks",
        failure_modes={"syntax errors on complex nested structures", "struggles with ambiguous requirements"},
        limitations={"limited to Python and JavaScript", "requires clear specifications"}
    )
    print("✓ Reported outcomes created")

    domain = DomainType.SIMULATION
    print("✓ Domain created")

    ai_system = AISystem(
        application_domains={domain},
        application_domains_reasoning="General-purpose code generation across software development tasks",
        paradigm=ParadigmType.AGENTIC_AI,
        paradigm_reasoning="Uses ReAct reasoning with autonomous tool use and iterative problem-solving",
        agent_architecture=agent_architecture,
        validation_methods={ValidationMethod.BENCHMARK, ValidationMethod.CASE_STUDY},
        reported_outcomes=reported_outcomes
    )
    print("✓ Complete AI system created")

    # Verify key properties
    print("\nVerifying system properties...")
    assert ai_system.paradigm == ParadigmType.AGENTIC_AI
    print(f"  - Paradigm: {ai_system.paradigm.value}")

    assert len(ai_system.system_architecture.agents) == 1
    print(f"  - Number of agents: {len(ai_system.system_architecture.agents)}")

    assert ai_system.system_architecture.agents[0].agent_role == AgentRoleType.CODER
    print(f"  - Agent role: {ai_system.system_architecture.agents[0].agent_role.value}")

    assert ReasoningCapabilitiesType.ITERATIVE_REASONING in ai_system.system_architecture.agents[0].prompt_engineering_techniques
    print(f"  - Reasoning capabilities: {[r.value for r in ai_system.system_architecture.agents[0].prompt_engineering_techniques]}")

    # Test serialization
    print("\nTesting serialization...")
    system_dict = ai_system.model_dump()
    print("✓ Serialized to dictionary")

    json_str = ai_system.model_dump_json(indent=2)
    print("✓ Serialized to JSON")

    recreated_system = AISystem.model_validate(system_dict)
    print("✓ Deserialized from dictionary")

    assert recreated_system.paradigm == ai_system.paradigm
    print("✓ Deserialized system matches original")

    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    print("\nThe AI System model is working correctly.")
    print("Install pytest to run the full test suite:")
    print("  pip install -r requirements.txt")
    print("  pytest test/test_ai_system.py -v")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure pydantic is installed:")
    print("  pip install pydantic")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
