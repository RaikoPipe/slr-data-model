from pydantic import BaseModel, Field, computed_field

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum
from .study_characterization import ValidationStatusType


class StudyTypeCategory(DescriptiveEnum):
    """Study-type category per §3.9 step 1; derived from validation status, never coded independently."""
    A = "A", "Empirical: primary data collection with a defined evaluation protocol"
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


def _item(question: str):
    return Field(description=question + make_type_annotations(AppraisalAnswer))


class QualityAppraisal(BaseModel):
    """Quality appraisal checklist per §3.9 step 2 (informed by MMAT and Hevner et al.; interpretive, R1 + R2 verify).

    No composite score. Never used for exclusion; the low-quality flag drives the sensitivity analysis.
    The study-type category (step 1) is derived on StudyExtraction from validation status.
    """
    q1_methodological_transparency: AppraisalAnswer = _item(
        "Q1: Is the method (study design, system architecture, or framework logic) described in enough detail "
        "for independent replication?"
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
        "external validity, domain assumptions)?"
    )
    q3_validity_and_limitation_discussion_reasoning: str = reasoning_field(interpretive=True)
    q4_positioning_against_prior_work: AppraisalAnswer = _item(
        "Q4: Is the contribution compared against existing solutions with explicit differentiation?"
    )
    q4_positioning_against_prior_work_reasoning: str = reasoning_field(interpretive=True)

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
