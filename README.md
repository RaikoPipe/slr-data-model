# SLR Data Model

Pydantic data models for the extraction schema of the SLR on **LLM-based decision support for the strategic planning horizon in manufacturing and logistics** (v5.0 extractor instructions).

## Overview

This package provides the structured-JSON schema for the extraction pipeline: raw LLM output is validated against these models before human review; schema-invalid outputs are flagged and re-extracted.

### Field groups (one `StudyExtraction` per study)

- **Bibliographic metadata** (imported from search-stage records; R1 spot-checks 10%): DOI, title, authors, affiliations, country, year, venue, venue type, language, funding
- **Study characterization** (descriptive, LLM pre-fill, R1 verifies 100%; validation status is interpretive): research type, validation status, sector, RQs
- **Strategic planning scope**: subdomain, planning tasks (§5 vocabulary), horizon tier, system-configuring decision, theoretical framework
- **LLM/AI intervention**: models, family, open-weight status, fine-tuning, architectural pattern, agentic architecture, integrations
- **OR/optimization substrate**: tradition, formalization level, solver
- **Evaluation and outcomes**: validation method, dataset, comparator, structured reported metrics (with page/section reference), study design, sample size, limitations
- **Retrieval traceability** (§3.7): source (Scopus / WoS / OpenAlex / snowballing), anchor paper(s)
- **Gap indicators** (interpretive, LLM-extracted, R1 + R2 verify 100%): HITL pattern, domain knowledge formalization, evaluation framework
- **Quality appraisal** (§3.9): Q1–Q4 scored `Yes` / `Partially` / `No`; study-type category (A/B/C) derived from validation status; low-quality flag (≥ 2 × `No`) auto-computed; no composite score
- **Extraction metadata** (§7/§8): per-field provenance tags (M / H / L-V / L-C / D), per-verifier verdicts (blind R1 + R2 for interpretive fields), derived `verified_by`, original LLM values (`llm_raw`)

Every extracted value field has a sibling `<field>_reasoning` column (§4: justification + evidence locator; interpretive fields add a verbatim anchor). Existing `*_rationale` fields serve the same role.

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
    RetrievalTraceability,
    RetrievalSource,
    QualityAppraisal,
    AppraisalAnswer,
    ExtractionMetaData,
    ProvenanceTag,
    ReviewerRole,
    VerificationStatus,
    FieldVerdict,
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
        research_type_rationale="Artifact built and evaluated (p. 2, §1).",
        validation_status=ValidationStatusType.IMPLEMENTED_VALIDATED,
        validation_status_rationale="Benchmark on 12 cases with defined metrics (p. 8): 'we evaluate on 12 cases'.",
        industry_sector="automotive",
        industry_sector_reasoning="p. 1, abstract.",
        case_study_domain="factory layout redesign",
        case_study_domain_reasoning="p. 6, §4.",
        stated_research_questions="RQ1: How can LLMs support layout planning?",
        stated_research_questions_reasoning="p. 2, §1.",
    ),
    strategic_planning_scope=StrategicPlanningScope(
        subdomain=[SubdomainType.FACTORY_PLANNING],
        subdomain_mapping_rationale="Stated explicitly (p. 1).",
        planning_task_type=[PlanningTaskType.FACTORY_LAYOUT_PLANNING],
        planning_task_type_reasoning="p. 3, §2.",
        time_horizon_explicitly_stated=True,
        time_horizon_explicitly_stated_reasoning="p. 3: '5-year horizon'.",
        planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC],
        planning_horizon_rationale="p. 3: '5-year horizon'.",
        system_configuring_decision_stated=True,
        system_configuring_decision_stated_reasoning="p. 3, §2.",
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
        theoretical_framework_cited_reasoning="p. 2, §2.1.",
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
        models_rationale="No other LLMs discussed.",
        model_family_reasoning="p. 5.",
        open_weight_rationale="GPT-4o is proprietary.",
        fine_tuning_reasoning="p. 5, §3.2.",
        architectural_pattern_reasoning="p. 4, Fig. 2.",
        agentic_architecture_reasoning="p. 4, Fig. 2.",
        integrations_reasoning="p. 4, Fig. 2.",
    ),
    or_substrate=ORSubstrate(
        optimization_tradition_present=True,
        formalization_level=FormalizationLevel.MATURE_MILP,
        solver_type="Gurobi",
        optimization_tradition_present_reasoning="p. 5, §3.3.",
        formalization_level_reasoning="p. 5, Eq. 1-4.",
        solver_type_reasoning="p. 6.",
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
        validation_method_reasoning="p. 8, §5.",
        dataset_or_benchmark_reasoning="NR: no named dataset (searched 'dataset', 'benchmark').",
        comparator_reasoning="p. 8, Table 3.",
        reported_metrics_reasoning="p. 8, Table 3.",
        study_design_reasoning="p. 8, §5.",
        sample_size_reasoning="p. 8, §5.",
        reported_limitations_reasoning="p. 10, §6.",
    ),
    retrieval_traceability=RetrievalTraceability(
        source=RetrievalSource.SCOPUS,
        source_reasoning="Scopus search export.",
    ),
    gap_indicators=GapIndicators(
        hitl_pattern_present=True,
        hitl_pattern_present_reasoning="p. 4: 'the planner approves each layout'.",
        hitl_type=HITLType.APPROVAL_GATE,
        hitl_type_reasoning="p. 4: 'the planner approves each layout'.",
        domain_knowledge_formalization_present=False,
        domain_knowledge_formalization_present_reasoning="No ontology/KG/standards encoding found (full-text search).",
        evaluation_framework_used=False,
        evaluation_framework_used_reasoning="Ad-hoc metrics only (p. 8).",
    ),
    quality_appraisal=QualityAppraisal(
        q1_methodological_transparency=AppraisalAnswer.YES,
        q1_methodological_transparency_reasoning="Prompts, model version, and protocol fully reported (Appendix B).",
        q2_empirical_or_demonstration_grounding=AppraisalAnswer.YES,
        q2_empirical_or_demonstration_grounding_reasoning="Category A: metrics, comparator, sample size reported (p. 8).",
        q3_validity_and_limitation_discussion=AppraisalAnswer.PARTIALLY,
        q3_validity_and_limitation_discussion_reasoning="Scalability discussed, external validity not (p. 10).",
        q4_positioning_against_prior_work=AppraisalAnswer.YES,
        q4_positioning_against_prior_work_reasoning="Comparison table vs. prior work (p. 3).",
    ),
    extraction_metadata=ExtractionMetaData(
        provenance={"strategic_planning_scope.subdomain": ProvenanceTag.LLM_VERIFIED},
        verification={"strategic_planning_scope.subdomain": [
            FieldVerdict(reviewer=ReviewerRole.R1, status=VerificationStatus.VERIFIED),
        ]},
    ),
)

print(record.study_type_category)  # StudyTypeCategory.A, derived from validation_status
print(record.model_dump_json(indent=2))
```

### JSON Schema for the LLM Pipeline

```python
from slr_data_model import StudyExtraction

schema = StudyExtraction.model_json_schema()  # use for structured-output validation (§7); excludes derived fields
```

## Key Components

- **`StudyExtraction`** — top-level record; composes all field groups plus `extraction_metadata`
- **`BibliographicMetadata`** — §3.1; imported, no `_reasoning` columns; `VenueType` per Scimago quartile (current-year lookup) (`journal-q1` … `journal-q4`, `conference-proceedings`, `tier-1-preprint`, `grey-literature`)
- **`StudyCharacterization`** — §3.2; `research_type`, `validation_status` with rationale fields
- **`StrategicPlanningScope`** — §3.3; subdomains, planning tasks (§5 vocabulary), horizon tier, system-configuring decision, theoretical frameworks — each with free-text rationale/specification fields
- **`LLMIntervention`** — §3.4; flat intervention description with models, families, open-weight, fine-tuning, patterns, integrations
- **`ORSubstrate`** — §3.5; optimization tradition, formalization level, solver
- **`EvaluationAndOutcomes`** — §3.6; `ReportedMetric` requires value, unit, context, and page/section reference per numeric metric
- **`RetrievalTraceability`** — §3.7; `anchor_papers` required iff source is `snowballing`
- **`GapIndicators`** — §3.8; type enums and their `_reasoning` enforced conditional on `*_present` flags via validators
- **`QualityAppraisal`** — §3.9; Q1–Q4 (`AppraisalAnswer`) each with `_reasoning`; computed `low_quality_flag`. `StudyExtraction.study_type_category` (A/B/C) is computed from `validation_status` via `CATEGORY_BY_VALIDATION_STATUS`
- **`ExtractionMetaData`** — §7/§8; per-field provenance (`M`/`H`/`L-V`/`L-C`/`D`), `FieldVerdict` list per field (reviewer, status `Y`/`corrected`/`unverifiable`, own value + reasoning), computed `verified_by` (e.g. `R1;R2`), `llm_raw` originals

Free-text conventions: `*_reasoning` / `*_rationale` (justification + evidence locator for the sibling value, §4), `*_description` (elaboration of what the paper reports), `*_other_specification` (required detail when an enum `other` value is used).

## Validation Rules

- Gap indicator type fields (and their `_reasoning`) required iff the corresponding `*_present` flag is true
- `QualityAppraisal.low_quality_flag` auto-computed (`No` on ≥ 2 items); study-type category derived, not coded
- `integrations` / `comparator` / `theoretical_framework_cited`: `none` mutually exclusive; `planning_horizon_tiers`: `NA` exclusive
- `FieldVerdict.corrected_value` required iff status is `corrected`
- `ReportedMetric.page_section_reference` mandatory for every numeric metric (§2)

## Project Structure

```
slr-data-model/
├── src/slr_data_model/
│   ├── __init__.py                 # Package exports
│   ├── bibliographic.py            # Bibliographic metadata (imported)
│   ├── study_characterization.py   # Descriptive: study characterization
│   ├── strategic_planning.py       # Descriptive: strategic planning scope
│   ├── llm_intervention.py         # Descriptive: LLM/AI intervention
│   ├── or_substrate.py             # Descriptive: OR/optimization substrate
│   ├── evaluation.py               # Descriptive: evaluation and outcomes
│   ├── retrieval.py                # Retrieval traceability
│   ├── gap_indicators.py           # Interpretive: gap indicators
│   ├── quality_appraisal.py        # Interpretive: quality appraisal checklist
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

Current version: 0.7.0

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.