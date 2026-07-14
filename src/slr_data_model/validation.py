from typing import Optional
from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class ValidationMethodType(DescriptiveEnum):
    SIMULATION = "simulation", "Validation through simulated environments or scenarios."
    CASE_STUDY = "case study", "In-depth analysis of specific instances or applications."
    BENCHMARK = "benchmark", "Comparison against established benchmarks or datasets."
    FIELD_DEPLOYMENT = "field deployment", "Real-world deployment and observation of system performance."
    NONE = "none", "No validation method reported."


class StudyDesignType(DescriptiveEnum):
    """Study design classification for evaluation."""
    DEVELOPER_REPORTED = "developer-reported", "Results reported by the system developer"
    SINGLE_CASE = "single-case", "Single case study evaluation"
    BENCHMARK = "benchmark", "Benchmark-based evaluation"
    USER_STUDY = "user-study", "User study evaluation"
    QUASI_EXPERIMENTAL = "quasi-experimental", "Quasi-experimental design"


class ComparatorType(DescriptiveEnum):
    """Type of comparator used in evaluation."""
    HUMAN_PLANNER = "human-planner", "Comparison against human planner"
    CONVENTIONAL_METHOD = "conventional-method", "Comparison against conventional non-AI method"
    PRIOR_AI_ML = "prior-AI-ML", "Comparison against prior AI/ML approach"
    NONE = "none", "No comparator used"


class FailureAttributionType(DescriptiveEnum):
    CONTEXT_INSUFFICIENCY = "context-insufficiency", "Missing or incomplete context"
    CONTEXT_FORMATTING = "context-formatting", "Poorly structured context"
    MODEL_CAPABILITY = "model-capability", "LLM reasoning or generation error"
    TOOL_FAILURE = "tool-failure", "External tool or API failure"
    UNATTRIBUTED = "unattributed", "Failure mode not analyzed"


class EvaluationAndOutcomes(BaseModel):
    """Evaluation methods and reported outcomes aligned with the OSF prereg."""
    validation_method: list[ValidationMethodType] = Field(
        description="Methods used to validate system performance." + make_type_annotations(ValidationMethodType)
    )
    dataset_or_benchmark: Optional[str] = Field(
        default=None,
        description="Dataset or benchmark name and size as reported. NR if absent."
    )
    comparator: list[ComparatorType] = Field(
        description="Type(s) of comparator used." + make_type_annotations(ComparatorType)
    )
    reported_metrics: list[str] = Field(
        description="All quantitative metric values with units, context, and page reference. NR if absent."
    )
    study_design: StudyDesignType = Field(
        description="Study design classification." + make_type_annotations(StudyDesignType)
    )
    sample_size: Optional[str] = Field(
        default=None,
        description="Number of test cases, users, or records as reported. NR if absent."
    )
    reported_limitations: list[str] = Field(
        description="1-3 sentence paraphrase of author-stated limitations."
    )


class ReportedOutcomes(BaseModel):
    """Performance outcomes and limitations reported in the paper.

    Retained for backward compatibility with detailed outcome categorization.
    """
    decision_quality_improvement: list[str] = Field(
        description="Reported improvements in decision quality or accuracy against traditional methods are ablation of context engineering techniques."
    )
    response_time_impact: list[str] = Field(
        description="Impacts on response time or processing speed."
    )
    reliability_metrics: list[str] = Field(
        description="System reliability, uptime, or error rate metrics."
    )
    failure_attribution: list[FailureAttributionType] = Field(...)
    ce_technique_effectiveness: dict[str, str] = Field(
        description="Mapping of CE technique to reported effectiveness"
    )
    failure_modes: list[str] = Field(
        description="Identified failure modes or error conditions."
    )
    limitations: list[str] = Field(
        description="Acknowledged limitations of the approach."
    )
