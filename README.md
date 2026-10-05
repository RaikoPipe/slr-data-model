# SLR Data Model

Pydantic data models for the extraction schema of the SLR on **LLM-based decision support for the strategic planning horizon in manufacturing and logistics** (v3.0 extractor instructions).

## Overview

This package provides the structured-JSON schema for the extraction pipeline: raw LLM output is validated against these models before human review; schema-invalid outputs are flagged and re-extracted.

### Field groups (one `StudyExtraction` per study)

- **Bibliographic metadata** (Tier 1, LLM-extracted; R1 spot-checks 10%): DOI, title, authors, affiliations, country, year, venue, venue type, language, funding
- **Study characterization** (Tier 2, LLM pre-fill, R1 verifies 100%): research type, validation status, sector, RQs
- **Strategic planning scope**: subdomain, planning tasks (§5 vocabulary), horizon tier, system-configuring decision, theoretical framework
- **LLM/AI intervention**: models, family, open-weight status, fine-tuning, architectural pattern, agentic architecture, integrations
- **OR/optimization substrate**: tradition, formalization level, solver
- **Evaluation and outcomes**: validation method, dataset, comparator, structured reported metrics (with page/section reference), study design, sample size, limitations
- **Gap indicators** (Tier 3, interpretive, dual-verified): HITL pattern, domain knowledge formalization, evaluation framework
- **Quality appraisal** (§3.9): three dimensions scored 1–3, composite 3–9 auto-computed; scores ≤ 4 flagged for dual verification
- **Extraction metadata** (§7/§8): per-field provenance tags (H / L-V / L-C / D), verification status, original LLM values (`llm_raw`), notes

Retrieval traceability is intentionally omitted from the schema.

## Installation

```bash
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Example

```python
from slr_data_model import (
    StudyExtraction,
    BibliographicMetadata,
    VenueType,
    StudyCharacterization,
    ResearchType,
    ValidationStatusType,
    StrategicPlanningScope,
    SubdomainType,
    PlanningTaskType,
    PlanningHorizonTier,
    TheoreticalFrameworkType,
    LLMIntervention,
    ModelFamilyType,
    OpenWeightType,
    FineTuningType,
    ArchitecturalPatternType,
    AgenticArchitectureType,
    IntegrationType,
    ORSubstrate,
    FormalizationLevel,
    EvaluationAndOutcomes,
    ReportedMetric,
    ComparatorType,
    StudyDesignType,
    GapIndicators,
    HITLType,
    QualityAppraisal,
    ExtractionMetaData,
    ProvenanceTag,
)

record = StudyExtraction(
    study_id="S001",
    bibliographic_metadata=BibliographicMetadata(
        doi="10.1000/example.2024",
        title="LLM-Based Factory Layout Planning",
        authors=["A. Author"],
        affiliations=["TU Example"],
        country="Germany",
        year=2024,
        venue="Production Engineering",
        venue_type=VenueType.JOURNAL_Q1,
        language="English",
        funding_source="NR",
        self_authored_flag=False,
    ),
    study_characterization=StudyCharacterization(
        research_type=ResearchType.DESIGN_SCIENCE,
        validation_status=ValidationStatusType.IMPLEMENTED_VALIDATED,
        industry_sector="automotive",
        case_study_domain="factory layout redesign",
        stated_research_questions="RQ1: How can LLMs support layout planning?",
    ),
    strategic_planning_scope=StrategicPlanningScope(
        subdomain=[SubdomainType.FACTORY_PLANNING],
        planning_task_type=[PlanningTaskType.FACTORY_LAYOUT_PLANNING],
        time_horizon_explicitly_stated=True,
        planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC],
        system_configuring_decision_stated=True,
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
    ),
    llm_intervention=LLMIntervention(
        intervention_description="LLM agent elicits requirements and generates layout alternatives; solver evaluates material flow.",
        models=["GPT-4o"],
        model_family=[ModelFamilyType.GPT],
        open_weight=OpenWeightType.NO,
        fine_tuning=FineTuningType.PROMPT_ENGINEERING_ONLY,
        architectural_pattern=[ArchitecturalPatternType.LLM_SOLVER],
        agentic_architecture=AgenticArchitectureType.SINGLE_AGENT,
        integrations=[IntegrationType.SOLVER],
    ),
    or_substrate=ORSubstrate(
        optimization_tradition_present=True,
        formalization_level=FormalizationLevel.MATURE_MILP,
        solver_type="Gurobi",
    ),
    evaluation_and_outcomes=EvaluationAndOutcomes(
        validation_method=["benchmark comparison"],
        comparator=[ComparatorType.HUMAN_PLANNER],
        reported_metrics=[ReportedMetric(
            metric="planning time reduction",
            value="35",
            unit="%",
            context="vs. human planner baseline across 12 cases",
            page_section_reference="p. 8, Table 3",
        )],
        study_design=StudyDesignType.BENCHMARK,
        sample_size="12 test cases",
        reported_limitations=["Single LLM evaluated."],
    ),
    gap_indicators=GapIndicators(
        hitl_pattern_present=True,
        hitl_type=HITLType.APPROVAL_GATE,
        domain_knowledge_formalization_present=False,
        evaluation_framework_used=False,
    ),
    quality_appraisal=QualityAppraisal(
        methodological_transparency=3,
        methodological_transparency_rationale="Prompts, model version, and protocol fully reported.",
        empirical_grounding=3,
        empirical_grounding_rationale="Implemented system with quantitative evaluation.",
        venue_tier_dimension=3,
        venue_tier_rationale="Q1 journal (Scimago 2024).",
    ),
    extraction_metadata=ExtractionMetaData(
        provenance={"strategic_planning_scope.subdomain": ProvenanceTag.LLM_VERIFIED},
        verification={"strategic_planning_scope.subdomain": "verified"},
        notes={"strategic_planning_scope.subdomain": "Mapped via Appendix A."},
    ),
)

print(record.model_dump_json(indent=2))
```

### JSON Schema for the LLM Pipeline

```python
from slr_data_model import StudyExtraction

schema = StudyExtraction.model_json_schema()  # use for structured-output validation (§7)
```

## Key Components

- **`StudyExtraction`** — top-level record; composes all field groups plus `extraction_metadata`
- **`BibliographicMetadata`** — §3.1; `VenueType` per Scimago quartile (`journal-q1` … `journal-q4`, `conference-proceedings`, `tier-1-preprint`, `grey-literature`)
- **`StudyCharacterization`** — §3.2; `research_type`, `validation_status` with rationale fields
- **`StrategicPlanningScope`** — §3.3; subdomains, planning tasks (§5 vocabulary), horizon tier, system-configuring decision, theoretical frameworks — each with free-text rationale/specification fields
- **`LLMIntervention`** — §3.4; flat intervention description with models, families, open-weight, fine-tuning, patterns, integrations
- **`ORSubstrate`** — §3.5; optimization tradition, formalization level, solver
- **`EvaluationAndOutcomes`** — §3.6; `ReportedMetric` requires value, unit, context, and page/section reference per numeric metric
- **`GapIndicators`** — §3.8; type enums enforced conditional on `*_present` flags via validators
- **`QualityAppraisal`** — §3.9; three dimensions (1–3) with mandatory rationales; `composite_score` (3–9) computed by validator; `needs_dual_verification` property (≤ 4)
- **`ExtractionMetaData`** — §7/§8; per-field provenance (`H`/`L-V`/`L-C`/`D`), verification status, `llm_raw` originals, notes

Free-text conventions: `*_description` (elaboration of what the paper reports), `*_rationale` (justification for a judgment), `*_other_specification` (required detail when an enum `other` value is used).

## Validation Rules

- Gap indicator type fields required iff the corresponding `*_present` flag is true
- `QualityAppraisal.composite_score` auto-computed as the sum of the three dimensions (bounds 3–9)
- `integrations` / `model_family`: `none` mutually exclusive with other values
- `ReportedMetric.page_section_reference` mandatory for every numeric metric (§2)

## Project Structure

```
slr-data-model/
├── src/slr_data_model/
│   ├── __init__.py                 # Package exports
│   ├── bibliographic.py            # Tier 1: bibliographic metadata
│   ├── study_characterization.py   # Tier 2: study characterization
│   ├── strategic_planning.py       # Tier 2: strategic planning scope
│   ├── llm_intervention.py         # Tier 2: LLM/AI intervention
│   ├── or_substrate.py             # Tier 2: OR/optimization substrate
│   ├── evaluation.py               # Tier 2: evaluation and outcomes
│   ├── gap_indicators.py           # Tier 3: gap indicators
│   ├── quality_appraisal.py        # Tier 3: quality appraisal rubric
│   ├── provenance.py               # §7/§8 provenance and verification
│   ├── study_extraction.py         # Top-level StudyExtraction record
│   ├── descriptive_enum.py         # Base enumeration with descriptions
│   └── annotation_helper.py        # Helper for enum type annotations
├── test/                           # Test files
├── pyproject.toml                  # Project configuration
└── README.md                       # This file
```

## Development

### Running Tests

```bash
pytest
```

## Requirements

- Python >= 3.8
- Pydantic >= 2.0.0

## Version

Current version: 0.4.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.