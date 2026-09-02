from typing import Optional

from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations
from .descriptive_enum import DescriptiveEnum


class ResearchType(DescriptiveEnum):
    """Coarse research type classification per §3.2."""
    EMPIRICAL = "empirical", "Empirical study with primary data collection"
    CONCEPTUAL = "conceptual", "Conceptual or vision paper"
    DESIGN_SCIENCE = "design-science", "Design-science research with artifact creation"


class ValidationStatusType(DescriptiveEnum):
    """Validation status of the proposed system per §3.2."""
    IMPLEMENTED_VALIDATED = "implemented-validated", "Working system + quantitative evaluation"
    PROTOTYPE = "prototype", "Working system, limited or no evaluation"
    FRAMEWORK_ONLY = "framework-only", "Architecture described, no implementation"
    CONCEPTUAL = "conceptual", "Position or vision paper"


class StudyCharacterization(BaseModel):
    """Study characterization fields (LLM pre-fill; R1 verifies 100% against source text)."""
    research_type: ResearchType = Field(
        description="Coarse research type classification." + make_type_annotations(ResearchType)
    )
    research_type_rationale: Optional[str] = Field(
        default=None,
        description="Free-text justification for the research type classification, citing the paper's stated methodology."
    )
    validation_status: ValidationStatusType = Field(
        description="Validation status of the proposed system." + make_type_annotations(ValidationStatusType)
    )
    validation_status_rationale: Optional[str] = Field(
        default=None,
        description="Free-text justification: what evaluation was or was not present, to support the validation-status judgment."
    )
    industry_sector: Optional[str] = Field(
        default=None,
        description="Industry sector as reported. NR if absent."
    )
    case_study_domain: Optional[str] = Field(
        default=None,
        description="Case study domain as reported. NR if absent."
    )
    stated_research_questions: Optional[str] = Field(
        default=None,
        description="Verbatim or close paraphrase of the paper's RQs. NR if none stated."
    )