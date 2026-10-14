from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class ModelFamilyType(DescriptiveEnum):
    """Model family classification per §3.4."""
    GPT = "GPT", "OpenAI GPT family"
    CLAUDE = "Claude", "Anthropic Claude family"
    GEMINI = "Gemini", "Google Gemini family"
    LLAMA = "Llama", "Meta Llama family"
    MISTRAL = "Mistral", "Mistral AI family"
    QWEN = "Qwen", "Alibaba Qwen family"
    DEEPSEEK = "DeepSeek", "DeepSeek family"
    OTHER = "other", "Other model family (specify)"


class OpenWeightType(DescriptiveEnum):
    """Whether the model weights are openly available per §3.4."""
    YES = "Y", "Open-weight model (Llama, Mistral, Qwen, DeepSeek, ...)"
    NO = "N", "Proprietary model (GPT, Claude, Gemini, ...)"
    MIXED = "mixed", "System uses both open-weight and proprietary models"


class FineTuningType(DescriptiveEnum):
    """Fine-tuning method applied per §3.4."""
    NONE = "none", "No fine-tuning applied"
    PROMPT_ENGINEERING_ONLY = "prompt-engineering-only", "Prompt engineering only, no weight updates"
    LORA = "LoRA", "Low-Rank Adaptation fine-tuning"
    FULL_FINE_TUNING = "full-fine-tuning", "Full model fine-tuning"
    OTHER = "other", "Other fine-tuning method (specify)"


class ArchitecturalPatternType(DescriptiveEnum):
    """Top-level architectural pattern classification (§5)."""
    RAG = "RAG", "Retrieval-augmented generation"
    MULTI_AGENT = "multi-agent", "Multi-agent system"
    LLM_SOLVER = "LLM+solver", "LLM combined with mathematical solver"
    LLM_DIGITAL_TWIN = "LLM+digital-twin", "LLM integrated with digital twin"
    SINGLE_AGENT_PIPELINE = "single-agent-pipeline", "Single agent pipeline"
    OTHER = "other", "Other architectural pattern (specify)"


class AgenticArchitectureType(DescriptiveEnum):
    """Agentic architecture classification per §3.4."""
    SINGLE_AGENT = "single-agent", "Single agent system"
    MULTI_AGENT = "multi-agent", "Multi-agent system"
    SUPERVISOR_AGENT = "supervisor-agent", "Supervisor-agent hierarchy"
    PIPELINE = "pipeline", "Sequential pipeline of agents"
    NONE = "none", "No agentic architecture"


class IntegrationType(DescriptiveEnum):
    """Integration types for the LLM system per §3.4 (list all applicable)."""
    RAG = "RAG", "Retrieval-augmented generation integration"
    KG = "KG", "Knowledge graph integration"
    SOLVER = "solver", "Mathematical solver integration"
    DIGITAL_TWIN = "digital-twin", "Digital twin integration"
    SIMULATION_PLATFORM = "simulation-platform", "Simulation platform integration"
    NONE = "none", "No external integration"


class LLMIntervention(BaseModel):
    """LLM/AI intervention details (LLM pre-fill; R1 verifies 100% against source text)."""
    intervention_description: str = Field(
        description="Free-text description of the role the LLM/agent system plays in the planning task: inputs, outputs, and decision support function as reported."
    )
    models: list[str] = Field(
        description="Exact name(s) + version (e.g., 'GPT-4o', 'Llama 3.1 70B') of only those LLMs deployed and evaluated "
        "with the paper's own method. Do not list models that are merely discussed, cited or used outside the method "
        "(e.g., related work, external baselines); record those in models_rationale."
    )
    models_rationale: str = reasoning_field(
        description="Reasoning for models; list other LLMs discussed in the paper but not deployed and evaluated "
        "with the paper's method, and in what role they appear (e.g., related work, baseline). "
    )
    model_usage_context: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of which model is used for what, when multiple models are reported."
    )
    model_family: list[ModelFamilyType] = Field(
        description="Model family classification(s) of the models listed in 'models'." + make_type_annotations(ModelFamilyType)
    )
    model_family_reasoning: str = reasoning_field()
    other_model_family_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the model family if 'other' was selected."
    )
    open_weight: OpenWeightType = Field(
        description="Whether the weights of the models listed in 'models' are openly available." + make_type_annotations(OpenWeightType)
    )
    open_weight_rationale: str = reasoning_field(
        description="Reasoning for open_weight; when 'mixed', state which models are open-weight and which proprietary. "
    )
    fine_tuning: FineTuningType = Field(
        description="Fine-tuning method applied." + make_type_annotations(FineTuningType)
    )
    fine_tuning_reasoning: str = reasoning_field()
    fine_tuning_description: Optional[str] = Field(
        default=None,
        description="Free-text details of fine-tuning data and procedure as reported, if applicable."
    )
    other_fine_tuning_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the fine-tuning method if 'other' was selected."
    )
    architectural_pattern: list[ArchitecturalPatternType] = Field(
        description="Top-level architectural pattern(s)." + make_type_annotations(ArchitecturalPatternType)
    )
    other_architectural_pattern_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the pattern if 'other' was selected."
    )
    architectural_pattern_reasoning: str = reasoning_field()
    agentic_architecture: AgenticArchitectureType = Field(
        description="Agentic architecture classification." + make_type_annotations(AgenticArchitectureType)
    )
    agentic_architecture_reasoning: str = reasoning_field()
    integrations: list[IntegrationType] = Field(
        description="All integration types applicable to the system." + make_type_annotations(IntegrationType)
    )
    integrations_reasoning: str = reasoning_field()

    @model_validator(mode="after")
    def validate_exclusive_none(self):
        """'none' is mutually exclusive with other integration values."""
        if len(self.integrations) > 1 and IntegrationType.NONE in self.integrations:
            raise ValueError("integrations: 'none' cannot be combined with other values")
        return self