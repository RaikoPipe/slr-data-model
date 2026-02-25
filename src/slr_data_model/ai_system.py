from pydantic import BaseModel, Field, field_validator
from typing import Optional
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
    external_tools: list[ExternalToolsType] = Field(
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

    finetuning_datasets: list[FinetuningDatasetType] = Field(
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
        description="Specific role of this agent in the system." + make_type_annotations(AgentRoleType)
    )
    specialized_role: str = Field(
        description="Precise role type classification. Format answer like this: 'information_extractor'."
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
    human_oversight_mechanism: list[HumanOversightType] = Field(
        description="Types of human oversight mechanisms integrated into the system." + make_type_annotations(HumanOversightType)
    )
    interaction_modalities: list[ModalityType] = Field(
        description="Modalities through which humans interact with the AI system." + make_type_annotations(InteractionModalityType)
    )
    feedback_and_learning_methods: list[FeedbackAndLearningType] = Field(
        description="Methods for incorporating human feedback into system learning and adaptation." + make_type_annotations(FeedbackAndLearningType)
    )

class OrchestrationPatternType(DescriptiveEnum):
    """How LLM agents are orchestrated in the system.."""
    SINGLE_STEP = "single-step", "One-shot generation, no orchestration."
    ORCHESTRATION_GRAPH = "orchestration-graph", "Agents are orchestrated through a rule-based graph"
    MULTI_AGENT_COLLABORATION = "multi-agent-collaboration", "Multiple agents working together to solve a task"
    REACT = "re-act", "Agents use Reasoning+Acting pattern in an iterative loop, usually integrating Chain of Thought and Tool Use"

class Orchestration(BaseModel):
    """Orchestration pattern for LLM-based AI systems."""
    orchestration_pattern_description: str = Field(description="Description of the orchestration patterns as reported in the paper.")
    orchestration_pattern: list[OrchestrationPatternType] = Field(
        description="How AI agents are orchestrated."
    )
    multi_agent_coordination_strategy: Optional[MultiAgentCoordinationStrategy] = Field(
        default=None,
        description="Collaboration mechanisms for multi-agent systems. State one if orchestration pattern is multi-agent collaboration."
    )

    @field_validator('multi_agent_coordination_strategy')
    def validate_orchestration(cls, v, info):
        agents = info.data.get('agents', [])
        if len(agents) <= 1 and v == "multi-agent-collaboration":
            raise ValueError("Single-agent system cannot have multi-agent collaboration orchestration pattern")
        if info.data.get('orchestration_pattern') == "multi-agent-collaboration":
            raise ValueError("Multi-agent system with multi-agent collaboration must specify coordination strategy")

        return v

class CPSIntegrationType(DescriptiveEnum):
    CYBER_PHYSICAL_SYSTEM = "CYBER-PHYSICAL-SYSTEM", "System integrates with cyber physical systems."
    DIGITAL_TWIN = "DIGITAL-TWIN", "System integrates with digital twin systems."
    IOT = "IOT", "System integrates with iot systems."

class SystemArchitecture(BaseModel):
    """Overall architecture of the LLM-based system."""
    agents: list[AIAgent] = Field(
        min_length=1,
        description="List of LLM-based agents in the system. Single-agent systems have one element. Required field.",

    )
    orchestration: Orchestration = Field(
        description="Orchestration of the AI agent(s)."
    )

    trigger: TriggerType = Field(
        description="Mechanism that initiates system."  + make_type_annotations(TriggerType)
    )

    human_integration: HumanIntegration = Field(
        description="Human integration aspects of the system."
    )

    integration_with_cps: CPSIntegrationType = Field(
        description="Type of external system integration."
    )

    @field_validator("agents", mode="before")
    def empty_list(cls, v, info, ):
        if not v:
            raise ValueError("System must have at least one agent")
        return v

class ResearchMaturityType(DescriptiveEnum):
    CONCEPTUAL = "conceptual", "Framework or architecture proposal only"
    PROTOTYPE = "prototype", "Working implementation, lab evaluation"
    PILOT = "pilot", "Limited real-world deployment"
    PRODUCTION = "production", "Full operational deployment"

class ResearchMethodologyType(DescriptiveEnum):
    """Research methodology employed in the study."""
    DESIGN_SCIENCE = "design-science", "Artifact creation with iterative evaluation cycles"
    CASE_STUDY = "case-study", "In-depth analysis of specific implementation instances"
    EXPERIMENT = "experiment", "Controlled experimental comparison with baselines"
    ACTION_RESEARCH = "action-research", "Collaborative intervention in real organizational setting"
    SIMULATION_STUDY = "simulation-study", "Evaluation using simulated environments or synthetic data"
    PROOF_OF_CONCEPT = "proof-of-concept", "Feasibility demonstration without rigorous evaluation"
    MIXED_METHODS = "mixed-methods", "Combination of qualitative and quantitative approaches"

class EvaluationMetricType(DescriptiveEnum):
    CLASSIFICATION = "classification", "Classification metrics are used, such as: accuracy, precision, recall, F1, AUC"
    GENERATION_QUALITY = "generation-quality", "Generation quality metrics are used, such as: ROUGE (L/1/2), BLEU, BERTScore, METEOR, cosine similarity"
    COMPUTATIONAL_EFFICIENCY = "computational-efficiency", "Computational efficiency metrics were tested such as: response time, latency, inference time, processing time."
    RETRIEVAL_QUALITY = "retrieval-quality", "Information retrieval metric such as: MRR, NDCG, Hit Rate"
    OPERATIONAL_KPI = "operational-kpi", "Domain specific metrics were tested"
    HUMAN_EVALUATION = "human-evaluation", "Human evaluation metrics were tested, such as Likert Scales, User Satisfaction Scores, Expert ratings"
    TASK_COMPLETION = "task-completion", "Task success was measures, which are typically binary, such as: success rate, detection rate, pass rate"
    REGRESSION = "regression", "Regression metrics were tested, such as: MSE, MAE, RMSE, MAPE"

class IndustryParadigmType(DescriptiveEnum):
    INDUSTRY_4 = "industry-4.0", "Industry 4.0"
    INDUSTRY_5 = "industry-5.0", "Industry 5.0"
    NOT_SPECIFIED = "not-specified", "Not specified"

class ScalabilityAssessmentType(DescriptiveEnum):
    """Dimensions of scalability assessed or acknowledged as limitations in the study."""
    DOMAIN_GENERALIZATION = "domain-generalization", "Transfer to other industrial domains, equipment types, or manufacturing processes beyond the validated scope."
    DATA_SCALABILITY = "data-scalability", "Ability to handle larger datasets, broader knowledge bases, or increased number of fault types and entity classes."
    COMPUTATIONAL_SCALABILITY = "computational-scalability", "Inference latency, hardware resource demands, or constraints on edge versus cloud deployment."
    ORGANIZATIONAL_SCALABILITY = "organizational-scalability", "Multi-site, multi-plant, or enterprise-wide deployment across organizational boundaries."
    AGENT_SCALABILITY = "agent-scalability", "Performance under increasing number of agents, concurrent tasks, or orchestration complexity."
    NOT_ASSESSED = "not-assessed", "Scalability not discussed or evaluated in the study."


class AISystem(BaseModel):
    """Complete AI system specification extracted from a paper."""

    # domain application


    # System architecture
    system_architecture: SystemArchitecture = Field(
        description="Architecture of the LLM-based System."
    )

    # meta
    application_domain: DomainType = Field(
        description='Primary field of application targeted by the paper.' + make_type_annotations(DomainType)
    )

    application_domain_description: str = Field(
        description="Short description of the addressed field by the paper."
    )

    industry_paradigm: IndustryParadigmType = Field(
        description="Industry paradigm addressed by the paper."
    )

    problem_description : str = Field(
        description="Short summary of the research problem and motivation of the paper"
    )

    proposed_solution : str = Field(
        description="Short overview about the proposed solution to solve the research problem"
    )

    research_maturity: ResearchMaturityType = Field(
        description="Maturity level of the research"
    )

    research_methodology: ResearchMethodologyType = Field(
        description="Primary research methodology employed." + make_type_annotations(ResearchMethodologyType)
    )

    research_methodology_description: str = Field(
        description="Short description of the conducted research methodology"
    )

    # Validation, results, limitations
    validation_methods: list[ValidationMethodType] = Field(
        description="Methods used to validate system performance." + make_type_annotations(ValidationMethodType)
    )
    baseline_methods: list[str] = Field(
        description="What the system was compared against."
    )
    evaluation_metric_categories: list[EvaluationMetricType] = Field(
        description="Metric categories used in evaluation."
    )
    reported_outcomes: ReportedOutcomes = Field(
        description="Performance outcomes and limitations."
    )
    identified_research_gaps: list[str] = Field(
        description="Explicit future work / gaps stated by authors."
    )
    scalability_assessment: ScalabilityAssessmentType = Field(
        description="Scalability assessment of system performance."
    )
