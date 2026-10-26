from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations, reasoning_field
from .common import NR, ReportedStr
from .descriptive_enum import DescriptiveEnum


class ResearchType(DescriptiveEnum):
    """Research-type facet per §3.2 (v0.9.0, B1).

    Source: Wieringa, Maiden, Mead & Rolland (2006), "Requirements engineering paper classification and
    evaluation criteria", Requirements Engineering 11(1); adopted as the research-type facet for mapping studies
    by Petersen et al. (2008, EASE) and Petersen, Vakkalanka & Kuzniarz (2015, IST 64). Replaces the v0.8.0
    empirical / conceptual / design-science triple, whose 'conceptual' overlapped ValidationStatusType.
    Maturity stays on validation_status; this facet records what kind of contribution the paper makes.
    """
    VALIDATION_RESEARCH = "validation-research", (
        "Novel technique evaluated in the lab / artificial setting (experiments, simulations, benchmarks, "
        "prototype on test cases), not yet used in practice"
    )
    EVALUATION_RESEARCH = "evaluation-research", (
        "Technique evaluated in practice (naturalistic setting: real organisation, real users, real data in "
        "operational use), incl. industrial case studies; a case built on real company data counts as one (D001)"
    )
    SOLUTION_PROPOSAL = "solution-proposal", (
        "Novel or significantly extended technique, argued for with a small example or none; no thorough evaluation"
    )
    PHILOSOPHICAL_PAPER = "philosophical-paper", "New way of looking at the field: taxonomy, conceptual framework, research agenda"
    OPINION_PAPER = "opinion-paper", "Personal opinion on what is good or bad, not grounded in related work or method"
    EXPERIENCE_PAPER = "experience-paper", "Practitioner's account of what was done in practice and how it went"


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
        description="Research type of the paper's contribution (Wieringa et al. 2006 facet). Lab/benchmark "
        "evaluation -> validation-research; evaluation in operational practice or on a case built on real company data "
        "(industrial case study) -> evaluation-research."
        + make_type_annotations(ResearchType)
    )
    research_type_rationale: str = reasoning_field(
        description="Reasoning for research_type, citing the paper's stated methodology. "
    )
    validation_status: ValidationStatusType = Field(
        description="Validation status of the proposed system. Decision rules: prototype + controlled evaluation "
        "-> implemented-validated; prototype on a single walkthrough without defined metrics -> prototype. "
        "framework-only/conceptual iff evaluation_and_outcomes.study_design is ['none']."
        + make_type_annotations(ValidationStatusType)
    )
    validation_status_rationale: str = reasoning_field(
        interpretive=True,
        description="Reasoning for validation_status: what evaluation was or was not present. "
        "Also serves as the rationale for the derived §3.9 study-type category. ",
    )
    industry_sector: ReportedStr = Field(
        default=NR,
        description="Industry sector as reported. NR if absent."
    )
    industry_sector_reasoning: str = reasoning_field()
    case_study_domain: ReportedStr = Field(
        default=NR,
        description="Case study domain as reported. NR if absent."
    )
    case_study_domain_reasoning: str = reasoning_field()
    stated_research_questions: ReportedStr = Field(
        default=NR,
        description="Verbatim or close paraphrase of the paper's RQs. NR if none stated."
    )
    stated_research_questions_reasoning: str = reasoning_field()
