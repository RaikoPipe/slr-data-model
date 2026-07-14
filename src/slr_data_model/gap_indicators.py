from typing import Optional
from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class HITLType(DescriptiveEnum):
    """Types of human-in-the-loop patterns."""
    APPROVAL_GATE = "approval-gate", "Human approval gate before action execution"
    WHAT_IF_INTERFACE = "what-if-interface", "What-if or scenario analysis interface for human exploration"
    ESCALATION_PROTOCOL = "escalation-protocol", "Escalation protocol to human on uncertainty"
    OTHER = "other", "Other HITL pattern"


class DomainKnowledgeType(DescriptiveEnum):
    """Types of domain knowledge formalization."""
    ONTOLOGY = "ontology", "Formal ontology for domain knowledge"
    KNOWLEDGE_GRAPH = "knowledge-graph", "Knowledge graph representation"
    STANDARDS_ENCODING = "standards-encoding", "Encoding of domain standards (e.g., VDI, ISO)"
    OTHER = "other", "Other domain knowledge formalization"


class EvaluationFrameworkType(DescriptiveEnum):
    """Types of evaluation frameworks."""
    BENCHMARK = "benchmark", "Standardized benchmark for evaluation"
    RUBRIC = "rubric", "Evaluation rubric or scoring guide"
    DOMAIN_SPECIFIC_METRIC = "domain-specific-metric", "Domain-specific evaluation metric"
    OTHER = "other", "Other evaluation framework"


class GapIndicators(BaseModel):
    """Gap indicator fields for RQ3 analysis."""
    hitl_pattern_present: bool = Field(
        description="Whether a human-in-the-loop pattern is present."
    )
    hitl_type: Optional[HITLType] = Field(
        default=None,
        description="Type of HITL pattern, if present." + make_type_annotations(HITLType)
    )
    domain_knowledge_formalization_present: bool = Field(
        description="Whether domain knowledge formalization is present."
    )
    domain_knowledge_type: Optional[DomainKnowledgeType] = Field(
        default=None,
        description="Type of domain knowledge formalization, if present." + make_type_annotations(DomainKnowledgeType)
    )
    evaluation_framework_used: bool = Field(
        description="Whether an evaluation framework is used."
    )
    evaluation_framework_type: Optional[EvaluationFrameworkType] = Field(
        default=None,
        description="Type of evaluation framework, if used." + make_type_annotations(EvaluationFrameworkType)
    )
