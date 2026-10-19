from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class HITLType(DescriptiveEnum):
    """Types of human-in-the-loop patterns per §3.8."""
    APPROVAL_GATE = "approval-gate", (
        "Workflow-initiated: a human must check and accept or repair output before the workflow proceeds"
    )
    WHAT_IF_INTERFACE = "what-if-interface", "Human-initiated: human poses scenarios or changes inputs to explore outcomes"
    ESCALATION_PROTOCOL = "escalation-protocol", (
        "System-initiated: the system detects uncertainty, failure or missing information and asks the human"
    )
    ITERATIVE_FEEDBACK = "iterative-feedback", (
        "Human judges each iteration's output and gives guidance that steers the next iteration"
    )
    HUMAN_OVERRIDE = "human-override", "Human edits or vetoes the agents' intermediate decisions or plans"
    OTHER = "other", "Other HITL pattern (specify)"


class DomainKnowledgeType(DescriptiveEnum):
    """Types of domain knowledge formalization per §3.8."""
    ONTOLOGY = "ontology", "Formal ontology for domain knowledge"
    KNOWLEDGE_GRAPH = "knowledge-graph", "Knowledge graph representation"
    STANDARDS_ENCODING = "standards-encoding", "Encoding of domain standards (e.g., VDI, ISO)"
    STRUCTURED_SCHEMA = "structured-schema", "Metamodel or schema (e.g., JSON) for domain entities and constraints"
    RELATIONAL_DATABASE = "relational-database", "Relational database or taxonomy of domain entities and attributes"
    CODE_TEMPLATE = "code-template", "Code or model template encoding domain structure (e.g., simulation blueprint)"
    MATHEMATICAL_MODEL = "mathematical-model", "Optimization or simulation model encoding domain structure and rules"
    OTHER = "other", "Other domain knowledge formalization (specify)"


class EvaluationFrameworkType(DescriptiveEnum):
    """Types of evaluation frameworks per §3.8."""
    BENCHMARK = "benchmark", "Public, standardised benchmark reused from prior work"
    CUSTOM_TEST_SET = "custom-test-set", "Test items or cases built by the authors for this paper"
    EXPERT_GROUND_TRUTH = "expert-ground-truth", "Outputs compared with expert or practitioner decisions"
    RUBRIC = "rubric", "Graded scoring scale or criteria (incl. Likert ratings, ordinal suitability levels)"
    DOMAIN_SPECIFIC_METRIC = "domain-specific-metric", (
        "Metric defined by the planning domain (e.g., throughput, space utilisation, cost); not generic accuracy/F1"
    )
    OTHER = "other", "Other evaluation framework (specify)"


class GapIndicators(BaseModel):
    """Gap indicator fields (LLM; interpretive; R1 + R2 verify 100%)."""
    hitl_pattern_present: bool = Field(
        description="True if a human acts on intermediate or final LLM output inside the method's workflow "
        "(reviews, approves, edits, answers a system request, steers exploration). Only issuing the initial "
        "query or reading the final answer does not count."
    )
    hitl_pattern_present_reasoning: str = reasoning_field(interpretive=True)
    hitl_type: Optional[list[HITLType]] = Field(
        default=None,
        description="All HITL patterns present, required if hitl_pattern_present is true. Classify by who "
        "triggers the human step (workflow, human, system) and when." + make_type_annotations(HITLType)
    )
    hitl_type_reasoning: Optional[str] = reasoning_field(
        interpretive=True, default=None, description="Required if hitl_type is set, otherwise null. "
    )
    hitl_description: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of how the HITL pattern operates in the system, as reported."
    )
    hitl_type_other_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification if 'other' is in hitl_type."
    )
    domain_knowledge_formalization_present: bool = Field(
        description="True if domain knowledge is encoded in an explicit, reusable, machine-readable structure "
        "that the system uses. Free-text prompts, few-shot examples or unstructured RAG corpora alone do not count."
    )
    domain_knowledge_formalization_present_reasoning: str = reasoning_field(interpretive=True)
    domain_knowledge_type: Optional[list[DomainKnowledgeType]] = Field(
        default=None,
        description="All types of domain knowledge formalization present, required if domain_knowledge_formalization_present is true."
        + make_type_annotations(DomainKnowledgeType)
    )
    domain_knowledge_type_reasoning: Optional[str] = reasoning_field(
        interpretive=True, default=None, description="Required if domain_knowledge_type is set, otherwise null. "
    )
    domain_knowledge_description: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of what domain knowledge is formalized and how, as reported."
    )
    domain_knowledge_type_other_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification if 'other' is in domain_knowledge_type."
    )
    evaluation_framework_used: bool = Field(
        description="True if the paper describes an explicit, repeatable evaluation protocol: defined test items "
        "or cases, defined metrics or scoring criteria, and a stated procedure. A single walkthrough, anecdotes, "
        "or metrics without a stated procedure do not count."
    )
    evaluation_framework_used_reasoning: str = reasoning_field(interpretive=True)
    evaluation_framework_type: Optional[list[EvaluationFrameworkType]] = Field(
        default=None,
        description="All framework elements used, required if evaluation_framework_used is true. Code both the "
        "test instrument (benchmark, custom test set, expert ground truth) and the scoring (rubric, "
        "domain-specific metric)."
        + make_type_annotations(EvaluationFrameworkType)
    )
    evaluation_framework_type_reasoning: Optional[str] = reasoning_field(
        interpretive=True, default=None, description="Required if evaluation_framework_type is set, otherwise null. "
    )
    evaluation_framework_description: Optional[str] = Field(
        default=None,
        description="Free-text elaboration of the evaluation framework and its application, as reported."
    )
    evaluation_framework_type_other_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification if 'other' is in evaluation_framework_type."
    )

    @model_validator(mode="after")
    def validate_conditional_types(self):
        """Type fields and their reasoning are required iff the corresponding flag is true."""
        for flag, type_field in (
            ("hitl_pattern_present", "hitl_type"),
            ("domain_knowledge_formalization_present", "domain_knowledge_type"),
            ("evaluation_framework_used", "evaluation_framework_type"),
        ):
            for field_name in (type_field, f"{type_field}_reasoning"):
                set_ = getattr(self, field_name) not in (None, [])
                if getattr(self, flag) and not set_:
                    raise ValueError(f"{field_name} is required when {flag} is true")
                if not getattr(self, flag) and set_:
                    raise ValueError(f"{field_name} must be null when {flag} is false")
        return self
