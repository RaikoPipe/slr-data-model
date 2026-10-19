from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class ComparatorType(DescriptiveEnum):
    """Type of comparator used in evaluation per §3.6."""
    HUMAN_PLANNER = "human-planner", "Humans doing the task without the system, incl. the manual pre-LLM process"
    CONVENTIONAL_METHOD = "conventional-method", "Non-AI algorithm or tool (OR solver, heuristic, commercial software)"
    PRIOR_AI_ML = "prior-AI-ML", "Another AI/ML or LLM method, incl. prompting baselines such as plain CoT"
    NONE = "none", "No comparator used"


class StudyDesignType(DescriptiveEnum):
    """Evaluation setting(s) per §3.6 (multi-valued; who ran the evaluation is coded in independent_evaluation)."""
    BENCHMARK = "benchmark", "Set of test items (public or author-built) scored against expected answers"
    SINGLE_CASE = "single-case", "One case (one company, line or network) worked through"
    MULTI_CASE = "multi-case", "Two or more distinct cases worked through"
    USER_STUDY = "user-study", (
        "Structured protocol (tasks, questionnaire or interviews) with participants other than the authors"
    )
    QUASI_EXPERIMENTAL = "quasi-experimental", "Controlled comparison of conditions or groups on the same tasks"
    FIELD_DEPLOYMENT = "field-deployment", "System in operational use, outcomes observed in practice"


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
        description="Type(s) of comparator: an alternative method applied to the same task and cases as the paper's "
        "method. Not comparators: swapping the LLM backbone, ablations of the method's own components, and "
        "comparison against ground truth or observed data. Code 'none' if only these occur."
        + make_type_annotations(ComparatorType)
    )
    comparator_reasoning: str = reasoning_field()
    reported_metrics: list[ReportedMetric] = Field(
        description="All quantitative metric values with units, context, and page reference. Empty list only if truly absent (explain in reported_metrics_reasoning)."
    )
    reported_metrics_reasoning: str = reasoning_field(
        description="Reasoning for reported_metrics; state NR with the search performed if no quantitative values are reported. "
    )
    study_design: list[StudyDesignType] = Field(
        min_length=1,
        description="All evaluation settings used for the paper's own method, pick all applicable."
        + make_type_annotations(StudyDesignType)
    )
    study_design_reasoning: str = reasoning_field()
    independent_evaluation: bool = Field(
        description="True only if the evaluation was run or judged by people other than the authors and their "
        "project partners (e.g., third-party testers, external experts scoring blind). Partner employees testing "
        "the system under the authors' protocol do not count."
    )
    independent_evaluation_reasoning: str = reasoning_field()
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
