from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List, Optional, Set

from . import DescriptiveEnum
from .memory import Memory
from .ai_system_types import (
    ParadigmType, ExternalToolsType, CapabilityAcquisitionType,
    ReasoningCapabilitiesType, AgentRoleType, CollaborationStrategyType,
    CollaborationMechanismType, CollaborationStructureType, ModalityType
)
from .validation import ValidationMethodType, ReportedOutcomes
from .domain import DomainType
from .annotation_helper import make_type_annotations

class ToolUse(BaseModel):
    """External tools and integrations available to the agent."""
    tool_use_description: str = Field(description="Description of the function and purpose of tool use as reported in the paper.")

    has_tools: bool = Field(
        description="Whether the agent uses any external tools beyond the base LLM."
    )
    external_tools: Set[ExternalToolsType] = Field(
        default_factory=set,
        description="Types of external tools utilized. Empty set if no tools." + make_type_annotations(ExternalToolsType)
    )
    choice_reasoning: Optional[str] = Field(
        default=None,
        description="Explanation of which tools are used and why, if applicable."
    )

class FinetuningDatasetType(DescriptiveEnum):
    """Source and type of data used for model fine-tuning."""
    HUMAN_ANNOTATED = "human-annotated", "Datasets labeled or curated by human annotators for specific tasks."
    LLM_GENERATED = "llm-generated", "Datasets created by other large language models to augment training data."
    REAL_WORLD = "real-world", "Data collected from real-world applications and user interactions."
    SYNTHETIC = "synthetic", "Artificially generated data designed to simulate specific scenarios or tasks."

class ModelCapabilities(BaseModel):
    """Capabilities and characteristics of the underlying generative AI model."""
    model_capabilities_description: str = Field(description="Description of the model's capabilities as reported in the paper.")

    capability_acquisition_methods: Set[CapabilityAcquisitionType] = Field(
        default_factory=set,
        description="Methods used to acquire task-specific capabilities (fine-tuning, prompt-engineering, or both)." + make_type_annotations(CapabilityAcquisitionType)
    )
    supported_modalities: Set[ModalityType] = Field(
        default_factory=set,
        description="Input/output modalities the model supports (text, image, audio, video)." + make_type_annotations(ModalityType)
    )

class OrchestrationPattern(BaseModel):
    """Multi-agent coordination patterns and strategies."""
    orchestration_pattern_description: str = Field(description="Description of the orchestration pattern as reported in the paper.")

    collaboration_mechanism: CollaborationMechanismType = Field(
        description="How agents align individual or shared objectives." + make_type_annotations(CollaborationMechanismType)
    )
    collaboration_structure: CollaborationStructureType = Field(
        description="Organizational structure of agent interactions." + make_type_annotations(CollaborationStructureType)
    )
    collaboration_strategy: CollaborationStrategyType = Field(
        description="Strategy for task allocation" + make_type_annotations(CollaborationStrategyType)
    )

class GenAIModel(BaseModel):
    """Specification of the generative AI model used in the system."""
    model_name: str = Field(
        description="Name or identifier of the base generative AI model (e.g., 'GPT-4', 'Claude-3', 'Llama-2')."
    )
    model_capabilities: ModelCapabilities = Field(
        description="Capabilities and modalities supported by the model."
    )
    finetuning_dataset_description: str = Field(description="Description of the dataset used for fine-tuning.")

    finetuning_datasets: Set[FinetuningDatasetType] = Field(
        default_factory=set,
        description="Types of datasets used for fine-tuning. Empty if model is not fine-tuned." + make_type_annotations(FinetuningDatasetType)
    )


class AutonomyLevelType(DescriptiveEnum):
    """Level of autonomy in agent decision-making and operation."""
    HUMAN_INITIATED = "human-initiated", "System assists, but requires human triggering"
    SEMI_AUTONOMOUS = "semi-autonomous", "System proposes, human approves before action."
    FULLY_AUTONOMOUS = "fully-autonomous", "System acts independently, human notified post-action."

# class ContextEngineeringTechniques(BaseModel):
#     """Context engineering methods used to provide information and capabilities to the LLM."""
#     tool_use: ToolUse = Field(
#         description="External tools and APIs available to the agent."
#     )
#     memory: Memory = Field(
#         description="Memory systems for storing and retrieving information."
#     )
#     prompt_engineering_details: Optional[str] = Field(
#         default=None,
#         description="Description of prompt engineering approaches used (system prompts, few-shot examples, etc.)."
#     )

class AIAgent(BaseModel):
    """Individual agent within the system with specific role and capabilities."""
    agent_description: Optional[str] = Field(description="Description of the agent's purpose and functionality as reported in the paper.")

    agent_role: AgentRoleType = Field(
        description="Specialized role of this agent (orchestrator, coder, planner, etc.)." + make_type_annotations(AgentRoleType)
    )
    reasoning_capabilities: Set[ReasoningCapabilitiesType] = Field(
        description="Reasoning approaches used (rule-based, ReAct, chain-of-thought, etc.). State at least one."+ make_type_annotations(ReasoningCapabilitiesType)
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
    generated_workers: bool = Field(
        default=False,
        description="Whether multiple instances of this agent are spawned dynamically by the system."
    )
    prompt_engineering_details: Optional[str] = Field(
        default=None,
        description="Description of prompt engineering approaches used (system prompts, few-shot examples, etc.)."
    )

    @field_validator('reasoning_capabilities')
    def validate_reasoning(cls, v):
        if not v:
            raise ValueError("Agent must have at least one reasoning capability")
        return v

class HumanOversightType(DescriptiveEnum):
    """Types of human oversight mechanisms integrated into the system."""

    PRE_ACTION_VALIDATION = "pre-action-validation", "Humans acts as approval gate for AI outputs prior to critical actions."
    REAL_TIME_MONITORING = "real-time-monitoring", "Humans monitor AI decisions and actions and intervenes if necessary during operation."
    RISK_BASED_ESCALATION = "risk-based-escalation", "System escalates problem to human/reverts to human control on uncertainty or errors."
    POST_ACTION_REVIEW = "post-action-review", "Humans provide post hoc feedback on AI decision and/or action to improve future performance."

class InteractionModalityType(DescriptiveEnum):
    """Modalities through which humans interact with the AI system."""
    CONVERSATIONAL_TEXT = "conversational-text", "Textual interfaces for conversation-based interaction."
    CONVERSATIONAL_VOICE = "voice", "Speech-based interaction."
    FORM_TEXT = "form-text", "Structured text forms for input/output."
    DASHBOARD_GUI = "dashboard-gui", "Graphical user interfaces with visual dashboards and context-sensitive controls."

class FeedbackAndLearningType(DescriptiveEnum):
    """Methods for incorporating human feedback into system learning and adaptation."""
    CORRECTIVE_FEEDBACK = "corrective-feedback", "Humans provide corrections to AI outputs to guide learning."
    PREFERENCE_ALIGNMENT = "preference-alignment", "System learns user preferences over time."
    ACTIVE_LEARNING = "active-learning", "System actively solicits human input on uncertain cases to improve performance."
    CONTINUOUS_IMPROVEMENT = "continuous-improvement", "Ongoing human feedback loops for iterative system enhancement."

class HumanIntegration(BaseModel):
    """Human integration aspects of the LLM-based system."""
    human_integration_description: str = Field(description="Overall description of human integration aspects as reported in the paper.")
    human_oversight_mechanism: Set[str] = Field(
        default_factory=set,
        description="Types of human oversight mechanisms integrated into the system." + make_type_annotations(HumanOversightType)
    )
    interaction_modalities: Set[ModalityType] = Field(
        default_factory=set,
        description="Modalities through which humans interact with the AI system." + make_type_annotations(InteractionModalityType)
    )
    feedback_and_learning_methods: Set[FeedbackAndLearningType] = Field(
        default_factory=set,
        description="Methods for incorporating human feedback into system learning and adaptation." + make_type_annotations(FeedbackAndLearningType)
    )

class SystemArchitecture(BaseModel):
    """Overall architecture of the LLM-based system."""
    agents: List[AIAgent] = Field(
        description="List of LLM-based agents in the system. Single-agent systems have one element."
    )
    orchestration_pattern: Optional[OrchestrationPattern] = Field(
        default=None,
        description="Coordination pattern for multi-agent systems. Only define when agent architecture is comprised of multiple agents."
    )
    autonomy_level: AutonomyLevelType = Field(
        description="Level(s) of autonomy exhibited by the system."  + make_type_annotations(AutonomyLevelType)
    )
    human_integration: Optional[HumanIntegration] = Field(
        default=None,
        description="Human integration aspects of the system, if applicable."
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
    application_domain: DomainType = Field(
        description='Primary field of application targeted by the paper.' + make_type_annotations(DomainType)
    )
    application_domains_reasoning: str = Field(
        description="Explanation of the chosen application domains."
    )

    # Paradigm classification
    paradigm: ParadigmType = Field(
        description="Overall system paradigm classification."  + make_type_annotations(ParadigmType)
    )
    paradigm_reasoning: str = Field(
        description="Justification for paradigm classification."
    )

    # System architecture
    system_architecture: SystemArchitecture = Field(
        description="Architecture of the LLM-based System."
    )

    # Validation and outcomes
    validation_methods: Set[ValidationMethodType] = Field(
        default_factory=set,
        description="Methods used to validate system performance." + make_type_annotations(ValidationMethodType)
    )
    reported_outcomes: ReportedOutcomes = Field(
        description="Performance outcomes and limitations."
    )