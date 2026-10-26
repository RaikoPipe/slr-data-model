from pydantic import BaseModel, Field, computed_field

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum
from .study_characterization import ValidationStatusType


class StudyTypeCategory(DescriptiveEnum):
    """Study-type category per §3.9 step 1; derived from validation status, never coded independently."""
    # B1 (v0.8.0 review): category A was described as "Empirical: primary data collection" although it is mapped
    # from implemented-validated, a design-science state; renamed. Research type is coded separately (Wieringa et al. 2006).
    A = "A", "Implemented system with defined evaluation protocol"
    B = "B", "Prototype / design science: implemented system on illustrative cases without controlled evaluation"
    C = "C", "Conceptual / framework: no implementation or empirical evaluation"


CATEGORY_BY_VALIDATION_STATUS = {
    ValidationStatusType.IMPLEMENTED_VALIDATED: StudyTypeCategory.A,
    ValidationStatusType.PROTOTYPE: StudyTypeCategory.B,
    ValidationStatusType.FRAMEWORK_ONLY: StudyTypeCategory.C,
    ValidationStatusType.CONCEPTUAL: StudyTypeCategory.C,
}


class AppraisalAnswer(DescriptiveEnum):
    """Score for a §3.9 appraisal item."""
    YES = "Yes", "Criterion fully met"
    PARTIALLY = "Partially", "Criterion partly met"
    NO = "No", "Criterion not met"


class PromptDisclosure(DescriptiveEnum):
    """How completely the prompts are disclosed (B3)."""
    FULL = "full", "All prompts/templates given verbatim (in paper, appendix or repository)"
    PARTIAL = "partial", "Some prompts, excerpts or a paraphrase of the prompt structure"
    NONE = "none", "Prompts not disclosed"


class DataAvailability(DescriptiveEnum):
    """How completely the evaluation data/test cases are available (v0.10.0, D025); ordinal like PromptDisclosure."""
    FULL = "full", "All evaluation data/test cases publicly available (in paper, appendix or repository)"
    PARTIAL = "partial", "Some of the data, a sample, excerpts, or available on request only"
    NONE = "none", "Data not available"


REPRODUCIBILITY_FIELDS = (
    "model_version_reported",
    "prompts_disclosed",
    "decoding_params_reported",
    "code_available",
    "data_available",
    "run_date_reported",
)
"""Reproducibility tier: the only tier not implied by its field group, so it is listed here."""


def _item(question: str):
    return Field(description=question + make_type_annotations(AppraisalAnswer))


class QualityAppraisal(BaseModel):
    """Quality appraisal checklist per §3.9 step 2 (informed by MMAT and Hevner et al.; interpretive, R1 + R2 verify).

    Item-level traceability (B3; MMAT 2018 = Hong et al., Education for Information 34(4); Hevner = Hevner, March,
    Park & Ram (2004), "Design Science in Information Systems Research", MIS Quarterly 28(1), guidelines G1-G7):
    - Q1 transparency: Hevner G7 (communication of research) + G5 (research rigor); MMAT screening S1/S2.
    - Q2 grounding: Hevner G3 (design evaluation); MMAT 4.3 (appropriate measurements), 4.5 (appropriate
      statistical analysis) for category A.
    - Q3 limitations: Hevner G5 (research rigor); no direct MMAT 2018 item (closest: 3.4/4.4, bias/confounders).
    - Q4 positioning: Hevner G4 (research contributions) + G2 (problem relevance); no direct MMAT 2018 item.

    The reproducibility block below is not appraisal-scored and does not enter low_quality_flag; it records
    LLM-specific reporting items as synthesis variables (B3). It forms its own tier (REPRODUCIBILITY_FIELDS),
    so inter-rater agreement is pooled separately from the interpretive Q1-Q4. Source: TRIPOD-LLM, Gallifant et al. (2025), "The TRIPOD-LLM
    reporting guideline for studies using large language models", Nature Medicine 31; its methods and
    open-science items (model version, prompts, decoding parameters, output variability, code/data availability,
    date of use) carry over from the clinical setting.

    No composite score. Never used for exclusion; the low-quality flag drives the sensitivity analysis.
    The study-type category (step 1) is derived on StudyExtraction from validation status.
    """
    q1_methodological_transparency: AppraisalAnswer = _item(
        "Q1: Is the method (study design, system architecture, or framework logic) described in enough detail "
        "for independent replication? Yes: architecture, all prompts, models, knowledge/data sources and key parameters "
        "are available (paper, appendix or repository). Partially: architecture described but at least one of these is "
        "missing. No: high-level description only (pilot 0.10.1)."
    )
    q1_methodological_transparency_reasoning: str = reasoning_field(interpretive=True)
    q2_empirical_or_demonstration_grounding: AppraisalAnswer = _item(
        "Q2, read by study-type category (derived from validation_status): "
        "A: are metrics defined and results reported with context (sample size, variance, comparator)? "
        "B: is the artifact demonstrated on a case that exercises its core claims? "
        "C: is the argumentation internally consistent and traceable?"
    )
    q2_empirical_or_demonstration_grounding_reasoning: str = reasoning_field(interpretive=True)
    q3_validity_and_limitation_discussion: AppraisalAnswer = _item(
        "Q3: Are the boundaries of the contribution explicitly discussed (failure modes, scalability, "
        "external validity, domain assumptions)? Yes: discusses both scope or failure modes and threats to the validity "
        "of the evaluation itself (sample, setting, bias). Partially: only one of these, or only future work. No: "
        "neither (pilot 0.10.1)."
    )
    q3_validity_and_limitation_discussion_reasoning: str = reasoning_field(interpretive=True)
    q4_positioning_against_prior_work: AppraisalAnswer = _item(
        "Q4: Is the contribution compared against existing solutions with explicit differentiation? Yes: explicit "
        "differentiation from named prior solutions, conceptually per solution or empirically against one. Partially: "
        "a related-work review plus a gap claim ('no study has...'). No: comparison only with the manual status quo, the "
        "authors' own work, or none. An empirical comparison only with a generic prompting baseline (plain CoT, "
        "zero-shot) does not make it Yes (pilot 0.10.1)."
    )
    q4_positioning_against_prior_work_reasoning: str = reasoning_field(interpretive=True)

    model_version_reported: bool = Field(
        description="True if the exact model version/snapshot is reported for every model (e.g., 'gpt-4o-2024-08-06', "
        "'Llama 3.1 70B Instruct'); False for e.g. 'ChatGPT' or 'GPT-4' without date/snapshot."
    )
    prompts_disclosed: PromptDisclosure = Field(
        description="How completely the prompts are disclosed. A stated public repository containing the prompts counts "
        "as 'full'; a described prompt assembly (e.g., 'Q&A pairs are appended to the query') is 'partial'; 'none' only if "
        "nothing about prompt content or structure is given (pilot 0.10.1)." + make_type_annotations(PromptDisclosure)
    )
    decoding_params_reported: bool = Field(
        description="True if at least one decoding parameter (temperature, top-p, max tokens, seed) is reported with its "
        "value; 'default parameters' without values is False (pilot 0.10.1)."
    )
    code_available: bool = Field(
        description="True if source code of the method is publicly available (link given and stated as available)."
    )
    data_available: DataAvailability = Field(
        description="How completely the evaluation data/test cases are available." + make_type_annotations(DataAvailability)
    )
    run_date_reported: bool = Field(
        description="True if the date or period in which the models were queried is reported."
    )
    reproducibility_reasoning: str = reasoning_field(
        description="Reasoning for the six reproducibility items, with locators (appendix, repository link). "
    )

    @computed_field(description="Y if the source scores 'No' on >= 2 items. Auto-computed, do not supply.")
    @property
    def low_quality_flag(self) -> bool:
        items = (
            self.q1_methodological_transparency,
            self.q2_empirical_or_demonstration_grounding,
            self.q3_validity_and_limitation_discussion,
            self.q4_positioning_against_prior_work,
        )
        return sum(item == AppraisalAnswer.NO for item in items) >= 2
