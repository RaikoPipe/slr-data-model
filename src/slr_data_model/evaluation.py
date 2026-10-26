from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .common import NR, ReportedList, ReportedStr, UniqueList, YesNoUnclear, exclusive
from .descriptive_enum import DescriptiveEnum


class ComparatorType(DescriptiveEnum):
    """Type of comparator used in evaluation per §3.6."""
    HUMAN_PLANNER = "human-planner", "Humans doing the task without the system, incl. the manual pre-LLM process"
    CONVENTIONAL_METHOD = "conventional-method", "Non-AI algorithm or tool (OR solver, heuristic, commercial software)"
    PRIOR_AI_ML = "prior-AI-ML", "Another AI/ML or LLM method, incl. prompting baselines such as plain CoT"
    NONE = "none", "No comparator used"


class StudyDesignType(DescriptiveEnum):
    """Evaluation setting(s) per §3.6 (multi-valued; who ran the evaluation is coded in independent_evaluation).

    v0.9.0: 'benchmark' renamed 'test-set' (B2) so that 'benchmark' only means a reused public benchmark
    (gap_indicators.evaluation_framework_type); 'none' added for framework-only/conceptual papers (A1).
    """
    TEST_SET = "test-set", "Set of test items (public or author-built) scored against expected answers"
    SINGLE_CASE = "single-case", "One case (one company, line or network) worked through"
    MULTI_CASE = "multi-case", "Two or more distinct cases worked through"
    USER_STUDY = "user-study", (
        "Structured protocol (tasks, questionnaire or interviews) with participants other than the authors"
    )
    QUASI_EXPERIMENTAL = "quasi-experimental", "Controlled comparison of conditions or groups on the same tasks"
    FIELD_DEPLOYMENT = "field-deployment", "System in operational use, outcomes observed in practice"
    NONE = "none", "No evaluation of the paper's own method (framework-only or conceptual papers only)"


class EvaluationParadigm(DescriptiveEnum):
    """Evaluation paradigm per FEDS (B2).

    Source: Venable, Pries-Heje & Baskerville (2016), "FEDS: a Framework for Evaluation in Design Science
    Research", European Journal of Information Systems 25(1). Artificial = lab, simulation, test set,
    illustrative or invented case; naturalistic = real users, real problem, real organisation/system.
    """
    ARTIFICIAL = "artificial", "All evaluation episodes are artificial"
    NATURALISTIC = "naturalistic", "All evaluation episodes are naturalistic"
    BOTH = "both", "Both artificial and naturalistic episodes"
    NA = "NA", "No evaluation (study_design is 'none')"


class EfficiencyReporting(DescriptiveEnum):
    """How completely cost, latency/run time or token usage of the LLM system is reported (v0.10.0, D153)."""
    YES = "yes", "Reported quantitatively for the evaluated configurations"
    PARTIALLY = "partially", "Reported only for some cases/configurations, or only qualitatively (e.g., 'a few minutes')"
    NO = "no", "Not reported"


class ReportedMetric(BaseModel):
    """A single quantitative metric as reported, with provenance (§2: log page/section for every numeric metric)."""
    metric: str = Field(
        description="Name of the metric as reported (e.g., 'solution quality gap', 'planning time')."
    )
    value: str = Field(
        description="Reported value as a string; capture ranges as both endpoints and conditional values with their conditions (§6), e.g., '12-15%', '0.82 (baseline), 0.91 (with RAG)'."
    )
    unit: ReportedStr = Field(
        default=NR,
        description="Unit of the value as reported (e.g., '%', 'seconds', 'count'). NR if unitless."
    )
    context: str = Field(
        description="Free-text context: what the value measures and under which conditions."
    )
    page_section_reference: str = Field(
        description="Page and/or section reference in the source where the value is reported (§2: log for every numeric metric)."
    )


class EvaluationAndOutcomes(BaseModel):
    """Evaluation methods and reported outcomes.

    v0.9.0 (B2): free-text validation_method removed; it re-coded what study_design, evaluation_paradigm,
    gap_indicators.evaluation_framework_type and dataset_or_benchmark already record.
    """
    study_design: UniqueList[StudyDesignType] = Field(
        min_length=1,
        description="All evaluation settings used for the paper's own method, pick all applicable. 'none' "
        "(exclusive) iff validation_status is framework-only or conceptual."
        + make_type_annotations(StudyDesignType)
    )
    study_design_reasoning: str = reasoning_field()
    evaluation_paradigm: EvaluationParadigm = Field(
        description="Artificial vs. naturalistic evaluation (FEDS); 'NA' iff study_design is 'none'. An episode is "
        "naturalistic only with real users, a real problem and a real system or organisation together; synthetic or "
        "mock-up data, or researcher-run or lab sessions, make it artificial. 'both' needs at least one episode of each "
        "kind (pilot 0.10.1)."
        + make_type_annotations(EvaluationParadigm)
    )
    evaluation_paradigm_reasoning: str = reasoning_field()
    dataset_or_benchmark: ReportedStr = Field(
        default=NR,
        description="Dataset or benchmark name and size as reported. NR if absent."
    )
    dataset_or_benchmark_reasoning: str = reasoning_field()
    comparator: UniqueList[ComparatorType] = Field(
        min_length=1,
        description="Type(s) of comparator: an alternative method applied to the same task and cases as the paper's "
        "method. Not comparators: swapping the LLM backbone, ablations of the method's own components, and "
        "comparison against ground truth or observed data. Code 'none' (exclusive) if only these occur."
        + make_type_annotations(ComparatorType)
    )
    comparator_reasoning: str = reasoning_field()
    reported_metrics: list[ReportedMetric] = Field(
        description="All quantitative metric values with units, context, and page reference. Empty list only if truly absent (explain in reported_metrics_reasoning)."
    )
    reported_metrics_reasoning: str = reasoning_field(
        description="Reasoning for reported_metrics; state NR with the search performed if no quantitative values are reported. "
    )
    independent_evaluation: YesNoUnclear = Field(
        description="Y only if the evaluation was run or judged by people other than the authors and their "
        "project partners (e.g., third-party testers, external experts scoring blind). Partner employees testing "
        "the system under the authors' protocol do not count." + make_type_annotations(YesNoUnclear)
    )
    independent_evaluation_reasoning: str = reasoning_field()
    sample_size: ReportedStr = Field(
        default=NR,
        description="Number of test cases, users, or records as reported. NR if absent."
    )
    sample_size_reasoning: str = reasoning_field()
    # B2 LLM-specific evaluation properties. Sources: run-to-run non-determinism (Ouyang et al., "An Empirical
    # Study of the Non-determinism of ChatGPT in Code Generation", ACM TOSEM 2025; TRIPOD-LLM, Gallifant et al.,
    # Nat Med 2025, on output variability); LLM-as-judge (Zheng et al., "Judging LLM-as-a-Judge with MT-Bench
    # and Chatbot Arena", NeurIPS 2023); efficiency as an evaluation dimension (Liang et al., "Holistic
    # Evaluation of Language Models", TMLR 2023); significance testing (Dror et al., "The Hitchhiker's Guide to
    # Testing Statistical Significance in NLP", ACL 2018).
    repeated_runs: ReportedStr = Field(
        description="Number of repeated runs per test item/case used to capture LLM output variability, tied to "
        "the case it refers to when it differs (e.g., '10 for Case A, 11 for Case B'); '1' if explicitly a single "
        "run. NR if not reported. Free text since v0.10.0 (D015)."
    )
    llm_as_judge: bool = Field(
        description="True if an LLM scores or judges the outputs of the paper's method."
    )
    efficiency_metrics_reported: EfficiencyReporting = Field(
        description="Whether cost, latency/run time, or token usage of the LLM system is reported."
        + make_type_annotations(EfficiencyReporting)
    )
    statistical_testing: bool = Field(
        description="True if a statistical significance test or confidence interval is reported for a comparison."
    )
    llm_evaluation_properties_reasoning: str = reasoning_field(
        description="Reasoning for repeated_runs, llm_as_judge, efficiency_metrics_reported and statistical_testing. "
    )
    reported_limitations: ReportedList = Field(
        description="1-3 sentence paraphrase of author-stated limitations. Empty list if none are stated (= NR)."
    )
    reported_limitations_reasoning: str = reasoning_field()
    outcome_summary: Optional[str] = Field(
        default=None,
        description="Free-text narrative summary of the main results beyond isolated metrics, as reported."
    )

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Exclusive none values; evaluation_paradigm 'NA' iff study_design 'none'."""
        exclusive(self, "comparator", ComparatorType.NONE)
        exclusive(self, "study_design", StudyDesignType.NONE)
        if (StudyDesignType.NONE in self.study_design) != (self.evaluation_paradigm == EvaluationParadigm.NA):
            raise ValueError("evaluation_paradigm must be 'NA' iff study_design is 'none'")
        return self
