from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Set

from .descriptive_enum import DescriptiveEnum
from .context_engineering import ContextEngineering
from .ai_system_types import (
    ParadigmType, ExternalToolsType, AgentRoleType,
    AgentCollaborationType, OrganizationalStructureType, ModalityType
)
from .validation import ValidationMethodType, ReportedOutcomes
from .domain import DomainType
from .annotation_helper import make_type_annotations

class ToolUse(BaseModel):
    """External tools and integrations available to the agent."""
    # tool_use_description: str = Field(description="Description of the function and purpose of tool use as reported in the paper.")

    has_tools: bool = Field(
        description="Whether the agent uses any external tools beyond the base LLM."
    )
    external_tools: List[ExternalToolsType] = Field(
        description="Types of external tools utilized. Empty set if no tools." + make_type_annotations(ExternalToolsType)
    )
    # choice_reasoning: Optional[str] = Field(
    #     default=None,
    #     description="Explanation of which tools are used and why, if applicable."
    # )

class FinetuningDatasetType(DescriptiveEnum):
    """Source and type of data used for model fine-tuning."""
    HUMAN_ANNOTATED = "human-annotated", "Datasets labeled or curated by human annotators for specific tasks."
    LLM_GENERATED = "llm-generated", "Datasets created by other large language models to augment training data."
    REAL_WORLD = "real-world", "Data collected from real-world applications and user interactions."
    SYNTHETIC = "synthetic", "Artificially generated data designed to simulate specific scenarios or tasks."


class MultiAgentCoordinationStrategy(BaseModel):
    """Multi-agent coordination patterns and collaboration strategies, if present."""
    multi_agent_coordination_strategy_description: str = Field(description="Short description of multi agent coordination strategy.")

    task_alignment: AgentCollaborationType = Field(
        description="How agents align individual or shared objectives." + make_type_annotations(AgentCollaborationType)
    )
    organizational_structure: OrganizationalStructureType = Field(
        description="Organizational structure of agent interactions." + make_type_annotations(OrganizationalStructureType)
    )

class GenAIModel(BaseModel):
    """Specification of the generative AI model used in the system."""
    model_name: str = Field(
        description="Name or identifier of the base generative AI model (e.g., 'GPT-4', 'Claude-3', 'Llama-2')."
    )
    supported_modalities: List[ModalityType] = Field(
        default_factory=List,
        description="Input/output modalities the model supports (text, image, audio, video)." + make_type_annotations(ModalityType)
    )

    finetuning_datasets: List[FinetuningDatasetType] = Field(
        description="Types of datasets used for fine-tuning. Empty if model is not fine-tuned." + make_type_annotations(FinetuningDatasetType)
    )

    finetuning_dataset_description: Optional[str] = Field(description="Description of the dataset used for fine-tuning, if applicable.")


class TriggerType(DescriptiveEnum):
    """How the AI system is triggered."""
    HUMAN_TRIGGERED = "human-initiated", "System assists, but requires human triggering"
    EVENT_TRIGGERED = "system-initiated", "AI system is triggered in response to events without human input"

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
    description: Optional[str] = Field(description="Description of the agent's purpose and functionality as reported in the paper.")

    role: AgentRoleType = Field(
        description="Specialized role of this agent (orchestrator, coder, planner, etc.)." + make_type_annotations(AgentRoleType)
    )
    context_engineering: ContextEngineering = Field(
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
    # prompt_engineering_details: Optional[str] = Field(
    #     default=None,
    #     description="Description of prompt engineering approaches used (system prompts, few-shot examples, etc.)."
    # )



class HumanOversightType(DescriptiveEnum):
    """Types of human oversight mechanisms integrated into the system."""

    PRE_ACTION_VALIDATION = "pre-action-validation", "Humans acts as approval gate for AI outputs prior to critical actions."
    REAL_TIME_MONITORING = "real-time-monitoring", "Humans monitor AI decisions and actions and intervenes if necessary during operation."
    RISK_BASED_ESCALATION = "risk-based-escalation", "System escalates problem to human/reverts to human control on uncertainty or errors."
    POST_ACTION_REVIEW = "post-action-review", "AI decides and acts independently, with only human review and possibly feedback after the fact."

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
    human_oversight_mechanism: List[HumanOversightType] = Field(
        description="Types of human oversight mechanisms integrated into the system." + make_type_annotations(HumanOversightType)
    )
    interaction_modalities: List[ModalityType] = Field(
        description="Modalities through which humans interact with the AI system." + make_type_annotations(InteractionModalityType)
    )
    feedback_and_learning_methods: List[FeedbackAndLearningType] = Field(
        description="Methods for incorporating human feedback into system learning and adaptation." + make_type_annotations(FeedbackAndLearningType)
    )

class TaskExecutionType(DescriptiveEnum):
    """How a task is processed by the AI system."""
    SINGLE_STEP = "single-step", "One-shot generation, no iteration"
    PLANNING_GRAPH = "planning-graph", "Graph-based planning with predefined state transitions"
    MULTI_AGENT_COLLABORATION = "multi-agent-collaboration", "Multiple agents working together on subtasks"
    # DECOMPOSITION = "dynamic-decomposition", "Breaking down tasks into subtasks dynamically, often seen in collaborative multi-agent systems"
    # iterative_refinement = "iterative-refinement", "ReAct loops, CoT with backtracking"

class OrchestrationPattern(BaseModel):
    """Orchestration pattern for LLM-based AI systems."""
    orchestration_pattern_description: str = Field(description="Description of the orchestration pattern as reported in the paper.")
    orchestration_pattern: TaskExecutionType = Field(
        description="How AI agents are orchestrated."
    )
    multi_agent_coordination_strategy: Optional[MultiAgentCoordinationStrategy] = Field(
        default=None,
        description="Collaboration mechanisms for multi-agent systems."
    )

    @field_validator('multi_agent_coordination_strategy')
    def validate_orchestration(cls, v, info):
        agents = info.data.get('agents', [])
        if len(agents) <= 1 and v == "multi-agent-collaboration":
            raise ValueError("Single-agent system cannot have multi-agent collaboration orchestration pattern")
        if info.data.get('orchestration_pattern') == "multi-agent-collaboration":
            raise ValueError("Multi-agent system with multi-agent collaboration must specify coordination strategy")

        return v


class SystemArchitecture(BaseModel):
    """Overall architecture of the LLM-based system."""
    agents: List[AIAgent] = Field(
        description="List of LLM-based agents in the system. Single-agent systems have one element."
    )
    orchestration_pattern: Optional[OrchestrationPattern] = Field(
        description="Orchestration pattern of the AI system."
    )

    trigger: TriggerType = Field(
        description="Mechanism that initiates system."  + make_type_annotations(TriggerType)
    )

    human_integration: Optional[HumanIntegration] = Field(
        description="Human integration aspects of the system, if applicable."
    )

    # shared_memory: bool = Field(
    #     default=False,
    #     description="Whether agents share memory/knowledge with each other."
    # )

    @field_validator("agents")
    def empty_list(cls, v, info):
        if not v:
            raise ValueError("System must have at least one agent")
        return v


class AISystem(BaseModel):
    """Complete AI system specification extracted from a paper."""

    # domain application
    # application_domain_reasoning: str = Field(
    #     description="Explanation of the chosen application domain."
    # )
    application_domain: DomainType = Field(
        description='Primary field of application targeted by the paper.' + make_type_annotations(DomainType)
    )


    # Paradigm classification
    # paradigm_reasoning: str = Field(
    #     description="Justification for paradigm classification."
    # )
    paradigm: ParadigmType = Field(
        description="Overall system paradigm classification." + make_type_annotations(ParadigmType)
    )


    # System architecture
    system_architecture: SystemArchitecture = Field(
        description="Architecture of the LLM-based System."
    )

    # Validation and outcomes
    validation_methods: List[ValidationMethodType] = Field(
        description="Methods used to validate system performance." + make_type_annotations(ValidationMethodType)
    )
    reported_outcomes: ReportedOutcomes = Field(
        description="Performance outcomes and limitations."
    )