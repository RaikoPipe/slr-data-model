from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List, Optional, Set
from .memory import Memory
from .ai_system_types import (
    ParadigmType, ExternalToolsType, CapabilityAcquisitionType,
    ReasoningCapabilitiesType, AgentRoleType, CollaborationStrategyType,
    CollaborationMechanismType, CollaborationStructureType, ModalityType
)
from .validation import ValidationMethod, ReportedOutcomes
from .domain import DomainType

class GenerativeAIParadigm(BaseModel):
    """Classification of the system's AI paradigm based on autonomy and capabilities."""
    reasoning: str = Field(
        description="Justification for the paradigm classification based on observed system characteristics."
    )
    paradigm_type: ParadigmType = Field(
        description="The identified paradigm: generative-ai (simple generation), ai-agent (fixed workflows), or agentic-ai (autonomous reasoning)."
    )

class ToolUse(BaseModel):
    """External tools and integrations available to the agent."""
    has_tools: bool = Field(
        description="Whether the agent uses any external tools beyond the base LLM."
    )
    external_tools: Set[ExternalToolsType] = Field(
        default_factory=set,
        description="Types of external tools utilized. Empty set if no tools."
    )
    choice_reasoning: Optional[str] = Field(
        default=None,
        description="Explanation of which tools are used and why, if applicable."
    )

class FinetuningDataset(str, Enum):
    """Source and type of data used for model fine-tuning."""
    HUMAN_ANNOTATED = "human-annotated"
    LLM_GENERATED = "llm-generated"
    REAL_WORLD = "real-world"
    SYNTHETIC = "synthetic"

class ModelCapabilities(BaseModel):
    """Capabilities and characteristics of the underlying generative AI model."""
    capability_acquisition_methods: Set[CapabilityAcquisitionType] = Field(
        default_factory=set,
        description="Methods used to acquire task-specific capabilities (fine-tuning, prompt-engineering, or both)."
    )
    supported_modalities: Set[ModalityType] = Field(
        default_factory=set,
        description="Input/output modalities the model supports (text, image, audio, video)."
    )

class OrchestrationPattern(BaseModel):
    """Multi-agent coordination patterns and strategies."""
    collaboration_mechanism: Set[CollaborationMechanismType] = Field(
        default_factory=set,
        description="How agents align objectives: cooperation, competition, or coopetition."
    )
    collaboration_structure: Set[CollaborationStructureType] = Field(
        default_factory=set,
        description="Organizational structure: centralized, distributed, or hierarchical."
    )
    collaboration_strategy: Set[CollaborationStrategyType] = Field(
        default_factory=set,
        description="Strategy for task allocation: rule-based, role-based, or model-based."
    )

class GenAIModel(BaseModel):
    """Specification of the generative AI model used in the system."""
    model_name: str = Field(
        description="Name or identifier of the base generative AI model (e.g., 'GPT-4', 'Claude-3', 'Llama-2')."
    )
    model_capabilities: ModelCapabilities = Field(
        description="Capabilities and modalities supported by the model."
    )
    finetuning_datasets: Set[FinetuningDataset] = Field(
        default_factory=set,
        description="Types of datasets used for fine-tuning. Empty if model is not fine-tuned."
    )

class AutonomyLevel(str, Enum):
    """Level of autonomy in agent decision-making and operation."""
    FIXED_WORKFLOW = "fixed-workflow"  # Predefined steps, no adaptation
    SEMI_AUTONOMOUS = "semi-autonomous"  # Some dynamic decisions within constraints
    FULLY_AUTONOMOUS = "fully-autonomous"  # Independent decision-making without human intervention
    EXPERT_IN_LOOP = "expert-in-loop"  # Human expert validates/guides decisions

class ContextEngineeringTechniques(BaseModel):
    """Context engineering methods used to provide information and capabilities to the LLM."""
    tool_use: ToolUse = Field(
        description="External tools and APIs available to the agent."
    )
    memory: Memory = Field(
        description="Memory systems for storing and retrieving information."
    )
    prompt_engineering_details: Optional[str] = Field(
        default=None,
        description="Description of prompt engineering approaches used (system prompts, few-shot examples, etc.)."
    )

class AIAgent(BaseModel):
    """Individual agent within the system with specific role and capabilities."""
    agent_role: AgentRoleType = Field(
        description="Specialized role of this agent (orchestrator, coder, planner, etc.)."
    )
    reasoning_capabilities: Set[ReasoningCapabilitiesType] = Field(
        description="Reasoning approaches used (rule-based, ReAct, chain-of-thought, etc.)."
    )
    memory: Memory = Field(
        description="Memory configuration for this agent."
    )
    tools: ToolUse = Field(
        description="External tools available to this agent."
    )
    genai_model: GenAIModel = Field(
        description="The underlying generative AI model powering this agent."
    )
    multiple_instances: bool = Field(
        default=False,
        description="Whether multiple instances of this agent type exist (e.g., multiple worker agents)."
    )

    @field_validator('reasoning_capabilities')
    def validate_reasoning(cls, v):
        if not v:
            raise ValueError("Agent must have at least one reasoning capability")
        return v

class AgentArchitecture(BaseModel):
    """Overall architecture of the agent system."""
    agents: List[AIAgent] = Field(
        description="List of agents in the system. Single-agent systems have one element."
    )
    orchestration_pattern: Optional[OrchestrationPattern] = Field(
        default=None,
        description="Coordination pattern for multi-agent systems. None for single-agent systems."
    )
    autonomy_level: Set[AutonomyLevel] = Field(
        description="Level(s) of autonomy exhibited by the system."
    )
    shared_memory: bool = Field(
        default=False,
        description="Whether agents share memory/knowledge with each other."
    )

    @field_validator('orchestration_pattern')
    def validate_orchestration(cls, v, info):
        agents = info.data.get('agents', [])
        if len(agents) > 1 and v is None:
            raise ValueError("Multi-agent system must specify orchestration pattern")
        if len(agents) == 1 and v is not None:
            raise ValueError("Single-agent system should not have orchestration pattern")
        return v

class AISystem(BaseModel):
    """Complete AI system specification extracted from a paper."""

    # domain application
    application_domains: Set[DomainType] = Field(
        default_factory=set,
        description="Specific application domains and phases targeted by the system."
    )
    application_domains_reasoning: str = Field(
        description="Explanation of the chosen application domains."
    )

    # Paradigm classification
    paradigm: ParadigmType = Field(
        description="Overall system paradigm classification."
    )
    paradigm_reasoning: str = Field(
        description="Justification for paradigm classification."
    )

    # System architecture
    agent_architecture: AgentArchitecture = Field(
        description="Agent architecture and coordination patterns."
    )

    # Context engineering (RQ2)
    context_engineering: ContextEngineeringTechniques = Field(
        description="Context engineering techniques employed."
    )

    # Validation and outcomes (RQ3)
    validation_methods: Set[ValidationMethod] = Field(
        default_factory=set,
        description="Methods used to validate system performance."
    )
    reported_outcomes: ReportedOutcomes = Field(
        description="Performance outcomes and limitations."
    )