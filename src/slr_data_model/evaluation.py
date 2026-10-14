from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class ComparatorType(DescriptiveEnum):
    """Type of comparator used in evaluation per §3.6."""
    HUMAN_PLANNER = "human-planner", "Comparison against human planner"
    CONVENTIONAL_METHOD = "conventional-method", "Comparison against conventional non-AI method"
    PRIOR_AI_ML = "prior-AI-ML", "Comparison against prior AI/ML approach"
    NONE = "none", "No comparator used"


class StudyDesignType(DescriptiveEnum):
    """Study design classification for evaluation per §3.6."""
    DEVELOPER_REPORTED = "developer-reported", "Results reported by the system developer"
    SINGLE_CASE = "single-case", "Single case study evaluation"
    BENCHMARK = "benchmark", "Benchmark-based evaluation"
    USER_STUDY = "user-study", "User study evaluation"
    QUASI_EXPERIMENTAL = "quasi-experimental", "Quasi-experimental design"


class ReportedMetric(BaseModel):
    """A single quantitative metric as reported, with provenance (§2: log page/section for every numeric metric)."""
    metric: str = Field(
        description="Name of the metric as reported (e.g., 'solution quality gap', 'planning time')."
    )
    value: str = Field(
        description="Reported value as a string; capture ranges as both endpoints and conditional values with their conditions (§6), e.g., '12-15%', '0.82 (baseline), 0.91 (with RAG)'."
    )
    unit: Optional[str] = Field(
        default=None,
        description="Unit of the value as reported (e.g., '%', 'seconds', 'count'). NR if unitless."
    )
    context: str = Field(
        description="Free-text context: what the value measures and under which conditions."
    )
    page_section_reference: str = Field(
        description="Page and/or section reference in the source where the value is reported (§2: log for every numeric metric)."
    )


class EvaluationAndOutcomes(BaseModel):
    """Evaluation methods and reported outcomes."""
    validation_method: list[str] = Field(
        description="Validation method(s) as reported (e.g., benchmark comparison, user study, ablation). NR if absent."
    )
    validation_method_reasoning: str = reasoning_field()
    dataset_or_benchmark: Optional[str] = Field(
        default=None,
        description="Dataset or benchmark name and size as reported. NR if absent."
    )
    dataset_or_benchmark_reasoning: str = reasoning_field()
    comparator: list[ComparatorType] = Field(
        description="Type(s) of comparator used." + make_type_annotations(ComparatorType)
    )
    comparator_reasoning: str = reasoning_field()
    reported_metrics: list[ReportedMetric] = Field(
        description="All quantitative metric values with units, context, and page reference. Empty list only if truly absent (explain in reported_metrics_reasoning)."
    )
    reported_metrics_reasoning: str = reasoning_field(
        description="Reasoning for reported_metrics; state NR with the search performed if no quantitative values are reported. "
    )
    study_design: StudyDesignType = Field(
        description="Study design classification." + make_type_annotations(StudyDesignType)
    )
    study_design_reasoning: str = reasoning_field()
    sample_size: Optional[str] = Field(
        default=None,
        description="Number of test cases, users, or records as reported. NR if absent."
    )
    sample_size_reasoning: str = reasoning_field()
    reported_limitations: list[str] = Field(
        description="1-3 sentence paraphrase of author-stated limitations. NR if absent."
    )
    reported_limitations_reasoning: str = reasoning_field()
    outcome_summary: Optional[str] = Field(
        default=None,
        description="Free-text narrative summary of the main results beyond isolated metrics, as reported."
    )

    @model_validator(mode="after")
    def validate_exclusive_none(self):
        """'none' is mutually exclusive with other comparator values."""
        if len(self.comparator) > 1 and ComparatorType.NONE in self.comparator:
            raise ValueError("comparator: 'none' cannot be combined with other values")
        return self
