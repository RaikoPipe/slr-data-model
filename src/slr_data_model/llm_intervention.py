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
    """Fine-tuning method applied per §3.4 (weight updates only; prompting techniques are not coded here)."""
    NONE = "none", "No weight updates (prompting, in-context examples, RAG only)"
    LORA = "LoRA", "Low-Rank Adaptation fine-tuning"
    FULL_FINE_TUNING = "full-fine-tuning", "Full model fine-tuning"
    OTHER = "other", "Other fine-tuning method (specify)"


class AgenticArchitectureType(DescriptiveEnum):
    """Agentic architecture classification per §3.4."""
    SINGLE_AGENT = "single-agent", "One agent that loops over reasoning/tool use (e.g., ReAct)"
    MULTI_AGENT = "multi-agent", "Several peer agents interacting without a controlling agent"
    SUPERVISOR_AGENT = "supervisor-agent", "A supervisor agent routes work to sub-agents (hierarchy)"
    PIPELINE = "pipeline", (
        "Fixed, developer-defined sequence of several specialised LLM roles (incl. evaluator/repair loops), "
        "even if the authors call them 'agents'"
    )
    NONE = "none", "LLM used as a single function (e.g., translator, generator) inside conventional software"


class IntegrationType(DescriptiveEnum):
    """Integration types for the LLM system per §3.4 (list all applicable)."""
    RAG = "RAG", "Retrieval-augmented generation integration"
    KG = "KG", "Knowledge graph integration"
    SOLVER = "solver", "Mathematical optimization/OR solver (MILP, CP, heuristics), incl. tools wrapping one"
    ML_MODEL = "ML-model", "Non-LLM predictive or explanatory ML model (regression, GNN, SHAP, forecasting)"
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
    agentic_architecture: AgenticArchitectureType = Field(
        description="Agentic architecture of the paper's own method. An 'agent' is an LLM component that decides "
        "its next action or tool call at run time; a step whose position in the flow is fixed by the developer is "
        "not an agent, whatever the authors call it. If several apply, code the outermost control structure."
        + make_type_annotations(AgenticArchitectureType)
    )
    agentic_architecture_reasoning: str = reasoning_field()
    integrations: list[IntegrationType] = Field(
        description="All external (non-LLM) components the LLM system calls or retrieves from, pick all applicable. "
        "Code only components of the paper's own method, not future work." + make_type_annotations(IntegrationType)
    )
    integrations_reasoning: str = reasoning_field()

    @model_validator(mode="after")
    def validate_exclusive_none(self):
        """'none' is mutually exclusive with other integration values."""
        if len(self.integrations) > 1 and IntegrationType.NONE in self.integrations:
            raise ValueError("integrations: 'none' cannot be combined with other values")
        return self