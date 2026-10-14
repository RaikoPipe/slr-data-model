from typing import Optional

from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class ResearchType(DescriptiveEnum):
    """Coarse research type classification per §3.2."""
    EMPIRICAL = "empirical", "Empirical study with primary data collection"
    CONCEPTUAL = "conceptual", "Conceptual or vision paper"
    DESIGN_SCIENCE = "design-science", "Design-science research with artifact creation"


class ValidationStatusType(DescriptiveEnum):
    """Validation status of the proposed system per §3.2 (interpretive; fixes the §3.9 study-type category)."""
    IMPLEMENTED_VALIDATED = "implemented-validated", (
        "Working system + evaluation under a defined protocol with defined metrics "
        "(benchmark, case study with quantitative metrics, user study)"
    )
    PROTOTYPE = "prototype", (
        "Working system demonstrated on illustrative case(s) or a single walkthrough without defined metrics"
    )
    FRAMEWORK_ONLY = "framework-only", "Architecture described, no implementation"
    CONCEPTUAL = "conceptual", "Position or vision paper"


class StudyCharacterization(BaseModel):
    """Study characterization fields (LLM pre-fill; R1 verifies 100%; validation status is interpretive, R1 + R2 verify)."""
    research_type: ResearchType = Field(
        description="Coarse research type classification." + make_type_annotations(ResearchType)
    )
    research_type_rationale: str = reasoning_field(
        description="Reasoning for research_type, citing the paper's stated methodology. "
    )
    validation_status: ValidationStatusType = Field(
        description="Validation status of the proposed system. Decision rules: prototype + controlled evaluation "
        "-> implemented-validated; prototype on a single walkthrough without defined metrics -> prototype."
        + make_type_annotations(ValidationStatusType)
    )
    validation_status_rationale: str = reasoning_field(
        interpretive=True,
        description="Reasoning for validation_status: what evaluation was or was not present. "
        "Also serves as the rationale for the derived §3.9 study-type category. ",
    )
    industry_sector: Optional[str] = Field(
        default=None,
        description="Industry sector as reported. NR if absent."
    )
    industry_sector_reasoning: str = reasoning_field()
    case_study_domain: Optional[str] = Field(
        default=None,
        description="Case study domain as reported. NR if absent."
    )
    case_study_domain_reasoning: str = reasoning_field()
    stated_research_questions: Optional[str] = Field(
        default=None,
        description="Verbatim or close paraphrase of the paper's RQs. NR if none stated."
    )
    stated_research_questions_reasoning: str = reasoning_field()
