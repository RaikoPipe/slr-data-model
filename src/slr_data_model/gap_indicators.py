from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class HITLType(DescriptiveEnum):
    """Types of human-in-the-loop patterns per §3.8."""
    APPROVAL_GATE = "approval-gate", "Human approval gate before action execution"
    WHAT_IF_INTERFACE = "what-if-interface", "What-if or scenario analysis interface for human exploration"
    ESCALATION_PROTOCOL = "escalation-protocol", "Escalation protocol to human on uncertainty"
    OTHER = "other", "Other HITL pattern (specify)"


class DomainKnowledgeType(DescriptiveEnum):
    """Types of domain knowledge formalization per §3.8."""
    ONTOLOGY = "ontology", "Formal ontology for domain knowledge"
    KNOWLEDGE_GRAPH = "knowledge-graph", "Knowledge graph representation"
    STANDARDS_ENCODING = "standards-encoding", "Encoding of domain standards (e.g., VDI, ISO)"
    OTHER = "other", "Other domain knowledge formalization (specify)"


class EvaluationFrameworkType(DescriptiveEnum):
    """Types of evaluation frameworks per §3.8."""
    BENCHMARK = "benchmark", "Standardized benchmark for evaluation"
    RUBRIC = "rubric", "Evaluation rubric or scoring guide"
    DOMAIN_SPECIFIC_METRIC = "domain-specific-metric", "Domain-specific evaluation metric"
    OTHER = "other", "Other evaluation framework (specify)"


class GapIndicators(BaseModel):
    """Gap indicator fields (LLM; interpretive; R1 + R2 verify 100%)."""
    hitl_pattern_present: bool = Field(
        description="Whether a human-in-the-loop pattern is present."
    )
    hitl_pattern_present_reasoning: str = reasoning_field(interpretive=True)
    hitl_type: Optional[HITLType] = Field(
        default=None,
        description="Type of HITL pattern, required if hitl_pattern_present is true." + make_type_annotations(HITLType)
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
        description="Free-text specification if hitl_type is 'other'."
    )
    domain_knowledge_formalization_present: bool = Field(
        description="Whether domain knowledge formalization is present."
    )
    domain_knowledge_formalization_present_reasoning: str = reasoning_field(interpretive=True)
    domain_knowledge_type: Optional[DomainKnowledgeType] = Field(
        default=None,
        description="Type of domain knowledge formalization, required if domain_knowledge_formalization_present is true."
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
        description="Free-text specification if domain_knowledge_type is 'other'."
    )
    evaluation_framework_used: bool = Field(
        description="Whether an evaluation framework is used."
    )
    evaluation_framework_used_reasoning: str = reasoning_field(interpretive=True)
    evaluation_framework_type: Optional[EvaluationFrameworkType] = Field(
        default=None,
        description="Type of evaluation framework, required if evaluation_framework_used is true."
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
        description="Free-text specification if evaluation_framework_type is 'other'."
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
                set_ = getattr(self, field_name) is not None
                if getattr(self, flag) and not set_:
                    raise ValueError(f"{field_name} is required when {flag} is true")
                if not getattr(self, flag) and set_:
                    raise ValueError(f"{field_name} must be null when {flag} is false")
        return self
