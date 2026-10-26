from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .common import NR, ReportedStr, UniqueList, exclusive, require_iff, require_spec_iff
from .descriptive_enum import DescriptiveEnum


class ModelFamilyType(DescriptiveEnum):
    """Model family classification per §3.4.

    v0.9.0 (B9): added Phi, Gemma, GLM, ERNIE, Command and Falcon, which occur in the manufacturing/logistics
    LLM literature but had to be coded 'other' under v0.8.0. Mistral-derived models (Mixtral, Ministral) are 'Mistral'.
    """
    GPT = "GPT", "OpenAI GPT family (incl. o-series and ChatGPT)"
    CLAUDE = "Claude", "Anthropic Claude family"
    GEMINI = "Gemini", "Google Gemini family (proprietary)"
    GEMMA = "Gemma", "Google Gemma family (open-weight)"
    LLAMA = "Llama", "Meta Llama family"
    MISTRAL = "Mistral", "Mistral AI family, incl. Mixtral and other Mistral-derived models"
    QWEN = "Qwen", "Alibaba Qwen family"
    DEEPSEEK = "DeepSeek", "DeepSeek family"
    PHI = "Phi", "Microsoft Phi family"
    GLM = "GLM", "Zhipu AI / THUDM GLM family, incl. ChatGLM"
    ERNIE = "ERNIE", "Baidu ERNIE family"
    COMMAND = "Command", "Cohere Command family"
    FALCON = "Falcon", "TII Falcon family"
    OTHER = "other", "Other model family (specify)"


# A6 (v0.8.0 review): families whose models are (almost) only available as proprietary APIs; used for the soft
# open_weight consistency flag. Soft, not a hard rule, because e.g. OpenAI's gpt-oss is open-weight.
PROPRIETARY_FAMILIES = frozenset({ModelFamilyType.GPT, ModelFamilyType.CLAUDE, ModelFamilyType.GEMINI})


class OpenWeightType(DescriptiveEnum):
    """Whether the model weights are openly available per §3.4."""
    YES = "Y", "Open-weight model (Llama, Mistral, Qwen, DeepSeek, ...)"
    NO = "N", "Proprietary model (GPT, Claude, Gemini, ...)"
    MIXED = "mixed", "System uses both open-weight and proprietary models"
    NR = "NR", "Not reported: model not named precisely enough to decide (B9)"


class DeploymentType(DescriptiveEnum):
    """Where the model runs (B9). Relevant to the industrial data-confidentiality barrier argued in many papers."""
    API = "API", "Hosted model accessed via a provider API or chat interface"
    LOCAL = "local-on-prem", "Model runs locally or on the organisation's own (on-prem/private-cloud) infrastructure"
    MIXED = "mixed", "Both API and local models used"
    NR = "NR", "Not reported"


class ModalityType(DescriptiveEnum):
    """Input modality of the LLM (B9): layouts, CAD drawings and maps matter in factory and network planning."""
    TEXT = "text", "Text (incl. code, tables or JSON serialised as text)"
    VISION_LANGUAGE = "vision-language", "Images plus text (e.g., layout drawings, screenshots, photos)"
    MULTIMODAL = "multimodal", "Other or further modalities (e.g., CAD/3D, audio, sensor streams)"


class FineTuningType(DescriptiveEnum):
    """Fine-tuning method(s) applied per §3.4 (weight updates only; prompting is coded in prompting_techniques).

    v0.9.0 (B9) sources: LoRA (Hu et al., ICLR 2022), QLoRA (Dettmers et al., NeurIPS 2023), adapters (Houlsby
    et al., ICML 2019), prefix tuning (Li & Liang, ACL 2021), RLHF (Ouyang et al., NeurIPS 2022), DPO (Rafailov
    et al., NeurIPS 2023), continued/domain-adaptive pre-training (Gururangan et al., ACL 2020), knowledge
    distillation (Hinton, Vinyals & Dean 2015). Instruction tuning / SFT (Wei et al., ICLR 2022) is the usual
    objective of full-fine-tuning, LoRA and PEFT-other and is not coded separately.
    """
    NONE = "none", "No weight updates (prompting, in-context examples, RAG only)"
    FULL_FINE_TUNING = "full-fine-tuning", "All weights updated (supervised / instruction fine-tuning)"
    LORA = "LoRA", "Low-Rank Adaptation, incl. QLoRA and other LoRA variants"
    PEFT_OTHER = "PEFT-other", "Other parameter-efficient fine-tuning (adapters, prefix/prompt tuning, IA3)"
    PREFERENCE_OPTIMIZATION = "preference-optimization", "Preference optimisation (RLHF, DPO, ORPO, KTO, ...)"
    CONTINUED_PRETRAINING = "continued-pretraining", "Continued / domain-adaptive pre-training on domain corpora"
    DISTILLATION = "distillation", "Knowledge distillation from a larger teacher model"
    OTHER = "other", "Other fine-tuning method (specify)"


class PromptingTechnique(DescriptiveEnum):
    """Prompting technique(s) of the paper's method (B6; v0.8.0 excluded prompting from fine_tuning but coded it nowhere).

    Sources: Schulhoff et al. (2024), "The Prompt Report: A Systematic Survey of Prompting Techniques",
    arXiv:2406.06608; zero-shot (Kojima et al., NeurIPS 2022), few-shot / in-context (Brown et al., NeurIPS 2020),
    chain-of-thought (Wei et al., NeurIPS 2022), self-consistency (Wang et al., ICLR 2023), ReAct (Yao et al., ICLR 2023).
    """
    ZERO_SHOT = "zero-shot", "Instructions only, no worked examples"
    FEW_SHOT = "few-shot", "In-context examples of input/output pairs"
    CHAIN_OF_THOUGHT = "CoT", "Model is asked for intermediate reasoning steps"
    SELF_CONSISTENCY = "self-consistency", "Several sampled outputs aggregated (e.g., majority vote)"
    REACT = "ReAct", "Interleaved reasoning and tool actions"
    STRUCTURED_OUTPUT = "structured-output", "Output constrained to a schema or grammar (JSON schema, function calling)"
    OTHER = "other", "Other technique (e.g., tree-of-thoughts, role prompting) (specify)"
    NR = "NR", "Prompting not described"


class AgenticArchitectureType(DescriptiveEnum):
    """Agentic architecture classification per §3.4 (outermost control structure)."""
    SINGLE_AGENT = "single-agent", "One agent that loops over reasoning/tool use (e.g., ReAct)"
    MULTI_AGENT = "multi-agent", "Several peer agents interacting without a controlling agent"
    SUPERVISOR_AGENT = "supervisor-agent", "A supervisor agent routes work to sub-agents (hierarchy)"
    PIPELINE = "pipeline", (
        "Fixed, developer-defined sequence of several specialised LLM roles (incl. evaluator/repair loops), "
        "even if the authors call them 'agents'; detail the pattern(s) in workflow_patterns"
    )
    NONE = "none", "LLM used as a single function (e.g., translator, generator) inside conventional software"


class WorkflowPattern(DescriptiveEnum):
    """Workflow patterns inside the method (B6).

    Source: Schluntz & Zhang (Anthropic, Dec 2024), "Building effective agents", which names these five
    workflow patterns and contrasts them with autonomous agents. supervisor-agent ~ orchestrator-workers;
    v0.8.0 'evaluator/repair loops' ~ evaluator-optimizer.
    """
    PROMPT_CHAINING = "prompt-chaining", "Fixed sequence of LLM calls, each processing the previous output"
    ROUTING = "routing", "An LLM call classifies the input and sends it to a specialised follow-up"
    PARALLELIZATION = "parallelization", (
        "Independent LLM calls or agents run in parallel (sectioning or voting) and are aggregated; also at the "
        "level of the whole system, not only within a single chain (D110)"
    )
    ORCHESTRATOR_WORKERS = "orchestrator-workers", "A central LLM breaks the task down at run time and delegates to workers"
    EVALUATOR_OPTIMIZER = "evaluator-optimizer", "One LLM generates, another evaluates and feeds back, in a loop"
    NONE = "none", "None of these patterns (single call or single autonomous agent)"


class AgentMemory(DescriptiveEnum):
    """Memory of the LLM system beyond one context window (B6).

    Source: Sumers, Yao, Narasimhan & Griffiths (2024), "Cognitive Architectures for Language Agents" (CoALA), TMLR.
    """
    NONE = "none", "No memory beyond the current prompt"
    SHORT_TERM = "short-term", "Working memory within one task/session (conversation history, scratchpad)"
    LONG_TERM = "long-term", "Persistent memory across tasks/sessions (episodic store, learned experience)"


class IntegrationType(DescriptiveEnum):
    """Integration types for the LLM system per §3.4 (list all applicable).

    v0.9.0: 'KG' removed; knowledge graphs are coded once in gap_indicators.domain_knowledge_type and the
    KG integration is derived from it (StudyExtraction.kg_integrated; B8). Added code-execution, database-SQL,
    enterprise-system, CAD-GIS and web-search-API (B9).
    """
    RAG = "RAG", "Retrieval-augmented generation over a document/vector store"
    SOLVER = "solver", "Mathematical optimization/OR solver (MILP, CP, heuristics), incl. tools wrapping one"
    ML_MODEL = "ML-model", "Non-LLM predictive or explanatory ML model (regression, GNN, SHAP, forecasting)"
    DIGITAL_TWIN = "digital-twin", "Digital twin integration"
    SIMULATION_PLATFORM = "simulation-platform", (
        "External simulation platform the LLM system calls (e.g., AnyLogic, Plant Simulation); not a system that "
        "is itself the simulation (D111)"
    )
    CODE_EXECUTION = "code-execution", "Generated code is executed (Python interpreter, sandbox)"
    DATABASE_SQL = "database-SQL", (
        "LLM generates SQL (or similar) queries itself; calling predefined queries does not count"
    )
    ENTERPRISE_SYSTEM = "enterprise-system", "Enterprise system (ERP, MES, PLM, WMS, APS)"
    CAD_GIS = "CAD-GIS", "CAD/layout tool or GIS / map service"
    WEB_SEARCH_API = "web-search-API", "Web search or other external web API"
    NONE = "none", "No external integration"


class LLMIntervention(BaseModel):
    """LLM/AI intervention details (LLM pre-fill; R1 verifies 100% against source text)."""
    intervention_description: str = Field(
        description="Free-text description of the role the LLM/agent system plays in the planning task: inputs, outputs, and decision support function as reported."
    )
    models: list[str] = Field(
        description="Exact name(s) + version (e.g., 'GPT-4o', 'Llama 3.1 70B') of only those LLMs deployed and evaluated "
        "with the paper's own method. If the version is not given, write e.g. 'ChatGPT (unspecified version)'. "
        "Do not list models that are merely discussed, cited or used outside the method "
        "(e.g., related work, external baselines) or only in preliminary tests/model selection; record those in "
        "models_rationale (D065)."
    )
    models_rationale: str = reasoning_field(
        description="Reasoning for models; list other LLMs discussed in the paper but not deployed and evaluated "
        "with the paper's method, and in what role they appear (e.g., related work, baseline, preliminary test). "
    )
    model_usage_context: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of which model is used for what, when multiple models are reported."
    )
    model_family: UniqueList[ModelFamilyType] = Field(
        description="Model family classification(s) of the models listed in 'models'; non-empty iff models is non-empty."
        + make_type_annotations(ModelFamilyType)
    )
    model_family_reasoning: str = reasoning_field()
    other_model_family_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the model family. Required if 'other' was selected, otherwise null."
    )
    open_weight: OpenWeightType = Field(
        description="Whether the weights of the models listed in 'models' are openly available." + make_type_annotations(OpenWeightType)
    )
    open_weight_rationale: str = reasoning_field(
        description="Reasoning for open_weight; when 'mixed', state which models are open-weight and which proprietary. "
    )
    model_size: ReportedStr = Field(
        default=NR,
        description="Parameter count(s) as reported (e.g., '70B', '8B; 70B'). NR if not reported (B9)."
    )
    deployment: DeploymentType = Field(
        description="Where the model(s) run." + make_type_annotations(DeploymentType)
    )
    deployment_reasoning: str = reasoning_field()
    modality: ModalityType = Field(
        description="Input modality the LLM receives in the paper's method." + make_type_annotations(ModalityType)
    )
    modality_reasoning: str = reasoning_field()
    fine_tuning: UniqueList[FineTuningType] = Field(
        min_length=1,
        description="Fine-tuning method(s) applied, pick all applicable; 'none' is exclusive."
        + make_type_annotations(FineTuningType)
    )
    fine_tuning_reasoning: str = reasoning_field()
    fine_tuning_description: Optional[str] = Field(
        default=None,
        description="Free-text details of fine-tuning data and procedure as reported, if applicable."
    )
    other_fine_tuning_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the fine-tuning method. Required if 'other' was selected, otherwise null."
    )
    prompting_techniques: UniqueList[PromptingTechnique] = Field(
        min_length=1,
        description="Prompting technique(s) used by the paper's method, pick all applicable; 'NR' (exclusive) if "
        "prompting is not described." + make_type_annotations(PromptingTechnique)
    )
    prompting_techniques_reasoning: str = reasoning_field()
    other_prompting_technique_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the prompting technique. Required if 'other' was selected, otherwise null."
    )
    agentic_architecture: AgenticArchitectureType = Field(
        description="Agentic architecture of the paper's own method. An 'agent' is an LLM component that decides "
        "its next action or tool call at run time; a step whose position in the flow is fixed by the developer is "
        "not an agent, whatever the authors call it. If several apply, code the outermost control structure."
        + make_type_annotations(AgenticArchitectureType)
    )
    agentic_architecture_reasoning: str = reasoning_field()
    workflow_patterns: UniqueList[WorkflowPattern] = Field(
        min_length=1,
        description="All workflow patterns used inside the method, at any level of nesting; 'none' is exclusive."
        + make_type_annotations(WorkflowPattern)
    )
    workflow_patterns_reasoning: str = reasoning_field()
    agent_memory: AgentMemory = Field(
        description="Memory of the LLM system beyond one prompt." + make_type_annotations(AgentMemory)
    )
    planning_reflection: bool = Field(
        description="True if an LLM component explicitly plans, self-critiques or reflects on its own output before "
        "the next step (e.g., plan-and-execute, Reflexion; Shinn et al., NeurIPS 2023)."
    )
    tool_use: bool = Field(
        description="True if an LLM component itself decides to call tools/functions at run time (Schick et al., "
        "'Toolformer', NeurIPS 2023); developer-fixed calls to external components are coded only in integrations."
    )
    agent_capabilities_reasoning: str = reasoning_field(
        description="Reasoning for agent_memory, planning_reflection and tool_use. "
    )
    integrations: UniqueList[IntegrationType] = Field(
        min_length=1,
        description="All external (non-LLM) components the LLM system calls or retrieves from, pick all applicable; "
        "'none' is exclusive. Code only components of the paper's own method, not future work. Knowledge graphs "
        "are coded in gap_indicators.domain_knowledge_type, not here." + make_type_annotations(IntegrationType)
    )
    integrations_reasoning: str = reasoning_field()

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Exclusive none values, 'other' specifications, and model_family non-empty iff models non-empty (A4)."""
        exclusive(self, "integrations", IntegrationType.NONE)
        exclusive(self, "fine_tuning", FineTuningType.NONE)
        exclusive(self, "workflow_patterns", WorkflowPattern.NONE)
        exclusive(self, "prompting_techniques", PromptingTechnique.NR)
        require_iff(self, "model_family", bool(self.models), "models is non-empty")
        require_spec_iff(self, "model_family", ModelFamilyType.OTHER, "other_model_family_specification")
        require_spec_iff(self, "fine_tuning", FineTuningType.OTHER, "other_fine_tuning_specification")
        require_spec_iff(self, "prompting_techniques", PromptingTechnique.OTHER, "other_prompting_technique_specification")
        return self
