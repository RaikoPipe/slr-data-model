# SLR Data Model

Pydantic data models for the extraction schema of the SLR on **LLM-based decision support for the strategic planning horizon in manufacturing and logistics** (v5.0 extractor instructions).

## Overview

This package provides the structured-JSON schema for the extraction pipeline: raw LLM output is validated against these models before human review; schema-invalid outputs are flagged and re-extracted.

### Field groups (one `StudyExtraction` per study)

- **Bibliographic metadata** (imported from search-stage records; R1 spot-checks 10%): DOI, title, authors, affiliations, country, year, venue, venue type, language, funding
- **Study characterization** (descriptive, LLM pre-fill, R1 verifies 100%; validation status is interpretive): research type (Wieringa et al. 2006 facet), validation status, sector, RQs
- **Strategic planning scope**: subdomain, planning tasks (§5 vocabulary), SCP-matrix process, VDI 5200 phase, stated horizon, reviewer-judged and author-claimed horizon tier, system-configuring decision, theoretical framework
- **LLM/AI intervention**: models, family, open-weight status, size, deployment, modality, fine-tuning, prompting techniques, agentic architecture, workflow patterns, agent capabilities, integrations
- **OR/optimization substrate**: tradition, ordinal formalization level, optimization paradigm, LLM role relative to the optimizer, solver
- **Evaluation and outcomes**: study design, FEDS evaluation paradigm (artificial/naturalistic), dataset, comparator, structured reported metrics (with page/section reference), sample size, LLM-specific evaluation properties (repeated runs, LLM-as-judge, efficiency metrics, statistical testing), limitations
- **Retrieval traceability** (§3.7): source (Scopus / WoS / OpenAlex / snowballing), anchor paper(s)
- **Gap indicators** (interpretive, LLM-extracted, R1 + R2 verify 100%): HITL pattern, automation stage and decision autonomy, domain knowledge formalization (with KG model / construction / usage and encoded standards), evaluation framework
- **Quality appraisal** (§3.9): Q1–Q4 scored `Yes` / `Partially` / `No`; LLM reproducibility block (model version, prompts, decoding parameters, code, data, run date; own tier, not in the low-quality flag); study-type category (A/B/C) derived from validation status; low-quality flag (≥ 2 × `No`) auto-computed; no composite score
- **Extraction metadata** (§7/§8): per-field provenance tags (M / H / L-V / L-C / D), per-verifier verdicts (blind R1 + R2 for interpretive fields), derived `verified_by`, original LLM values (`llm_raw`)

### Tiers

The tier of a field is implied by its group; only the reproducibility tier cuts across a group and is listed explicitly (`REPRODUCIBILITY_FIELDS`). Agreement is pooled per tier.

| Tier | Groups / fields | Scored in pilot? |
|---|---|---|
| Bibliographic metadata | `bibliographic_metadata` | No (§9: not piloted) |
| Descriptive | `study_characterization` (except `validation_status`), `strategic_planning_scope` (except `system_configuring_decision`), `llm_intervention`, `or_substrate`, `evaluation_and_outcomes`, `retrieval_traceability` | Yes |
| Interpretive | `validation_status`, `system_configuring_decision`, `gap_indicators`, `quality_appraisal` Q1–Q4 | Yes |
| Reproducibility | `quality_appraisal`: `model_version_reported`, `prompts_disclosed`, `decoding_params_reported`, `code_available`, `data_available`, `run_date_reported` | Yes, pooled separately |

Every extracted value field has a sibling `<field>_reasoning` column (§4: justification + evidence locator; interpretive fields add a verbatim anchor). Existing `*_rationale` fields serve the same role. Blocks of closely related flags share one reasoning column (`agent_capabilities_reasoning`, `llm_evaluation_properties_reasoning`, `kg_reasoning`, `reproducibility_reasoning`).

Not reported is always the sentinel `NR` (`from slr_data_model import NR`): free-text fields default to `NR` and normalise `None`, `""`, `"n/a"` to it; free-text lists use the empty list; interpretive yes/no fields use `YesNoUnclear` (`Y` / `N` / `unclear`).

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
    StudyExtraction, BibliographicMetadata, VenueType,
    StudyCharacterization, ResearchType, ValidationStatusType,
    StrategicPlanningScope, SubdomainType, PlanningTaskType, PlanningHorizonTier, TheoreticalFrameworkType,
    SCPProcess, VDI5200Phase, YesNoUnclear,
    LLMIntervention, ModelFamilyType, OpenWeightType, DeploymentType, ModalityType, FineTuningType,
    PromptingTechnique, AgenticArchitectureType, WorkflowPattern, AgentMemory, IntegrationType,
    ORSubstrate, FormalizationLevel, OptimizationParadigm, LLMORRole,
    EvaluationAndOutcomes, EvaluationParadigm, EfficiencyReporting, ReportedMetric, ComparatorType, StudyDesignType,
    GapIndicators, HITLType, AutomationStage, DecisionAutonomy,
    RetrievalTraceability, RetrievalSource,
    QualityAppraisal, AppraisalAnswer, PromptDisclosure, DataAvailability,
    ExtractionMetaData, ProvenanceTag, ReviewerRole, VerificationStatus, FieldVerdict,
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
        self_authored_flag=False,
    ),
    study_characterization=StudyCharacterization(
        research_type=ResearchType.VALIDATION_RESEARCH,
        research_type_rationale="New method evaluated on 12 lab cases (p. 2, §1).",
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
        scp_process=[SCPProcess.PRODUCTION],
        scp_process_reasoning="Plant layout decision (p. 3).",
        vdi5200_phase=[VDI5200Phase.CONCEPT_PLANNING],
        vdi5200_phase_reasoning="Layout variants = concept planning (p. 3, §2).",
        time_horizon_explicitly_stated=YesNoUnclear.YES,
        time_horizon_explicitly_stated_reasoning="p. 3: '5-year horizon'.",
        stated_horizon_value="5 years",
        planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC],
        planning_horizon_rationale="p. 3: '5-year horizon'.",
        authors_claimed_tier=[PlanningHorizonTier.STRATEGIC],
        authors_claimed_tier_reasoning="p. 1: 'strategic factory planning'.",
        system_configuring_decision=True,
        system_configuring_decision_reasoning="p. 3: 'selects machines and sets capacities'.",
        system_configuring_decision_stated=True,
        system_configuring_decision_stated_reasoning="p. 3, §2.",
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
        theoretical_framework_cited_reasoning="p. 2, §2.1.",
    ),
    llm_intervention=LLMIntervention(
        intervention_description="LLM agent elicits requirements and generates layout alternatives; solver evaluates material flow.",
        models=["GPT-4o"],
        models_rationale="No other LLMs discussed.",
        model_family=[ModelFamilyType.GPT],
        model_family_reasoning="p. 5.",
        open_weight=OpenWeightType.NO,
        open_weight_rationale="GPT-4o is proprietary.",
        deployment=DeploymentType.API,
        deployment_reasoning="OpenAI API (p. 5).",
        modality=ModalityType.TEXT,
        modality_reasoning="Layouts passed as JSON (p. 4).",
        fine_tuning=[FineTuningType.NONE],
        fine_tuning_reasoning="p. 5, §3.2.",
        prompting_techniques=[PromptingTechnique.FEW_SHOT, PromptingTechnique.REACT],
        prompting_techniques_reasoning="Appendix B.",
        agentic_architecture=AgenticArchitectureType.SINGLE_AGENT,
        agentic_architecture_reasoning="p. 4, Fig. 2.",
        workflow_patterns=[WorkflowPattern.NONE],
        workflow_patterns_reasoning="Single ReAct loop (p. 4).",
        agent_memory=AgentMemory.SHORT_TERM,
        planning_reflection=False,
        tool_use=True,
        agent_capabilities_reasoning="Agent calls the solver tool at run time (p. 4).",
        integrations=[IntegrationType.SOLVER],
        integrations_reasoning="p. 4, Fig. 2.",
    ),
    or_substrate=ORSubstrate(
        optimization_tradition_present=True,
        optimization_tradition_present_reasoning="p. 5, §3.3.",
        formalization_level=FormalizationLevel.HIGH,
        formalization_level_reasoning="p. 5, Eq. 1-4.",
        optimization_paradigm=[OptimizationParadigm.MILP_LP],
        optimization_paradigm_reasoning="p. 5, Eq. 1-4.",
        llm_or_role=[LLMORRole.SOLVER_ORCHESTRATOR],
        llm_or_role_reasoning="Agent calls Gurobi as a tool (p. 4).",
        solver_type="Gurobi",
        solver_type_reasoning="p. 6.",
    ),
    evaluation_and_outcomes=EvaluationAndOutcomes(
        study_design=[StudyDesignType.TEST_SET],
        study_design_reasoning="p. 8, §5.",
        evaluation_paradigm=EvaluationParadigm.ARTIFICIAL,
        evaluation_paradigm_reasoning="Lab cases only (p. 8).",
        dataset_or_benchmark_reasoning="NR: no named dataset (searched 'dataset', 'benchmark').",
        comparator=[ComparatorType.HUMAN_PLANNER],
        comparator_reasoning="p. 8, Table 3.",
        reported_metrics=[ReportedMetric(
            metric="planning time reduction",
            value="35",
            unit="%",
            context="vs. human planner baseline across 12 cases",
            page_section_reference="p. 8, Table 3",
        )],
        reported_metrics_reasoning="p. 8, Table 3.",
        independent_evaluation=YesNoUnclear.NO,
        independent_evaluation_reasoning="Authors ran all tests (p. 8).",
        sample_size="12 test cases",
        sample_size_reasoning="p. 8, §5.",
        repeated_runs="NR",
        llm_as_judge=False,
        efficiency_metrics_reported=EfficiencyReporting.YES,
        statistical_testing=False,
        llm_evaluation_properties_reasoning="Run time reported (Table 3); runs per case not stated.",
        reported_limitations=["Single LLM evaluated."],
        reported_limitations_reasoning="p. 10, §6.",
    ),
    retrieval_traceability=RetrievalTraceability(
        source=RetrievalSource.SCOPUS,
        source_reasoning="Scopus search export.",
    ),
    gap_indicators=GapIndicators(
        hitl_pattern_present=True,
        hitl_pattern_present_reasoning="p. 4: 'the planner approves each layout'.",
        hitl_type=[HITLType.APPROVAL_GATE],
        hitl_type_reasoning="p. 4: 'the planner approves each layout'.",
        domain_knowledge_formalization_present=False,
        domain_knowledge_formalization_present_reasoning="No ontology/KG/standards encoding found (full-text search).",
        evaluation_framework_used=False,
        evaluation_framework_used_reasoning="Ad-hoc metrics only (p. 8).",
        automation_stage=[AutomationStage.INFORMATION_ANALYSIS, AutomationStage.DECISION_SELECTION],
        automation_stage_reasoning="Generates and ranks layout variants (p. 4).",
        decision_autonomy=DecisionAutonomy.L2_RECOMMENDATION,
        decision_autonomy_reasoning="p. 4: 'the planner selects the final layout'.",
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
        model_version_reported=True,
        prompts_disclosed=PromptDisclosure.FULL,
        decoding_params_reported=True,
        code_available=False,
        data_available=DataAvailability.NONE,
        run_date_reported=False,
        reproducibility_reasoning="'gpt-4o-2024-08-06', temperature 0 (Appendix B); no repository link.",
    ),
    extraction_metadata=ExtractionMetaData(
        provenance={"strategic_planning_scope.subdomain": ProvenanceTag.LLM_VERIFIED},
        verification={"strategic_planning_scope.subdomain": [
            FieldVerdict(reviewer=ReviewerRole.R1, status=VerificationStatus.VERIFIED),
        ]},
    ),
)

print(record.study_type_category)  # StudyTypeCategory.A, derived from validation_status
print(record.consistency_flags)    # [] - soft warnings for reviewers
print(record.model_dump_json(indent=2))
```

### JSON Schema for the LLM Pipeline

```python
from slr_data_model import StudyExtraction

schema = StudyExtraction.model_json_schema()  # use for structured-output validation (§7); excludes derived fields
```

For strict structured-output modes that reject defaults (e.g. OpenAI `strict: true`), use `strict_json_schema()`: every property is required and no defaults remain. Cross-field rules are not expressible in JSON Schema; validate the LLM output with `StudyExtraction.model_validate_json(...)` and feed the `ValidationError` text back to the LLM as a repair prompt.

## Key Components

- **`StudyExtraction`** — top-level record; composes all field groups plus `extraction_metadata`
- **`BibliographicMetadata`** — §3.1; imported, no `_reasoning` columns; `VenueType` per Scimago quartile (current-year lookup) (`journal-q1` … `journal-q4`, `conference-proceedings`, `tier-1-preprint`, `grey-literature`)
- **`StudyCharacterization`** — §3.2; `research_type` (Wieringa et al. 2006: validation/evaluation research, solution proposal, philosophical/opinion/experience paper), `validation_status` (maturity axis) with rationale fields
- **`StrategicPlanningScope`** — §3.3; subdomains (closed inclusion gate), planning tasks (§5 vocabulary, `TASK_SUBDOMAINS` mapping), SCP-matrix process, VDI 5200 phase, stated horizon, reviewer-judged and author-claimed tiers, system-configuring decision, theoretical frameworks
- **`LLMIntervention`** — §3.4; models, families, open-weight, size, deployment, modality, fine-tuning (multi), prompting techniques, agentic architecture + workflow patterns (Anthropic 2024), memory / reflection / tool use, integrations
- **`ORSubstrate`** — §3.5; optimization tradition, ordinal formalization level, optimization paradigm (incl. MCDM, simulation-optimization, stochastic/robust), LLM role relative to the optimizer, solver
- **`EvaluationAndOutcomes`** — §3.6; study design, FEDS paradigm, LLM-specific evaluation properties; `ReportedMetric` requires value, unit, context, and page/section reference per numeric metric
- **`RetrievalTraceability`** — §3.7; `anchor_papers` required iff source is `snowballing`
- **`GapIndicators`** — §3.8; type enums and their `_reasoning` enforced conditional on `*_present` flags via validators; automation stage and decision autonomy (Parasuraman et al. 2000); KG detail fields
- **`QualityAppraisal`** — §3.9; Q1–Q4 (`AppraisalAnswer`) each with `_reasoning` and a documented MMAT/Hevner mapping; reproducibility block (TRIPOD-LLM; own tier, `REPRODUCIBILITY_FIELDS`, not in the low-quality flag); computed `low_quality_flag`. `StudyExtraction.study_type_category` (A/B/C) is computed from `validation_status` via `CATEGORY_BY_VALIDATION_STATUS`
- **`ExtractionMetaData`** — §7/§8; per-field provenance (`M`/`H`/`L-V`/`L-C`/`D`), `FieldVerdict` list per field (reviewer, status `Y`/`corrected`/`unverifiable`, own value + reasoning), computed `verified_by` (e.g. `R1;R2`), `llm_raw` originals

Free-text conventions: `*_reasoning` / `*_rationale` (justification + evidence locator for the sibling value, §4), `*_description` (elaboration of what the paper reports), `*_other_specification` (required detail when an enum `other` value is used).

## Validation Rules

- Gap indicator type fields (and their `_reasoning`) required iff the corresponding `*_present` flag is true; `kg_*` fields required iff `domain_knowledge_type` includes `ontology` or `knowledge-graph`; `standards_encoded` non-empty iff it includes `standards-encoding`
- Every `other` value requires its `*_other_specification` / `other_*_specification` field, which must be null otherwise
- `QualityAppraisal.low_quality_flag` auto-computed (`No` on ≥ 2 items); study-type category derived, not coded
- `none` / `NA` values are mutually exclusive with other values in every multi-select; multi-selects that make no sense empty (`subdomain`, `planning_task_type`, `integrations`, `comparator`, `theoretical_framework_cited`, …) need at least one value; duplicates are dropped
- `model_family` non-empty iff `models` is non-empty
- `study_design` is `["none"]` iff `validation_status` is `framework-only` or `conceptual`; `evaluation_paradigm` is `NA` iff `study_design` is `none`
- `formalization_level` is `none` and `optimization_paradigm` empty iff `optimization_tradition_present` is false; `llm_or_role` is `none` if it is false
- `vdi5200_phase` is `NA` iff `factory-planning` is not in `subdomain`
- `extraction_metadata` keys must be field paths of `StudyExtraction` (typos are rejected)
- Soft checks (reviewers may override) are reported in the computed `StudyExtraction.consistency_flags`, e.g. `open_weight = Y` with only GPT/Claude/Gemini, a `solver` integration without optimization, metrics on a `prototype`, planning tasks outside the coded subdomains (`TASK_SUBDOMAINS`)
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
│   ├── common.py                   # NR sentinel, YesNoUnclear, shared cross-field rules
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

- Python >= 3.9
- Pydantic >= 2.0.0

## Version

Current version: 0.10.2 (`StudyExtraction.schema_version`)

### 0.10.2 — consensus review of the pilot rules

No vocabulary or type changes; rules are tagged `(0.10.2)` in the field descriptions.

- **Clarified definitions:** Q1 counts details in a cited publication the paper explicitly defers to, and does not count confidential company data of a naturalistic case as missing; `system_configuring_decision_stated` includes selecting network members (suppliers, partners); `evaluation_paradigm` naturalistic rests on real operational data or real users of the organisation's own system, so researcher execution and expert-constructed auxiliary inputs no longer make an episode artificial; Q2 applies the criterion of the category derived from `validation_status` only, with Yes/Partially/No anchors for category A

### 0.10.1 — rule revision after the extraction pilot

No vocabulary or type changes. Values of the clarified fields coded under 0.10.0 may need re-checking; each rule is tagged `(pilot 0.10.1)` in its field description.

- **Added:** reproducibility tier: the six reproducibility items of `QualityAppraisal` are exported as `REPRODUCIBILITY_FIELDS` so the agreement tool pools them separately from the interpretive Q1–Q4.
- **Clarified definitions** (fields below the §9 gate in the pilot): `authors_claimed_tier` label must refer to the supported planning decision; `system_configuring_decision_stated` needs a design/configure/select/locate statement; `models` includes alternative LLMs run in the evaluation and `open_weight` judges the named variant; `optimization_tradition_present` excludes LLM self-refinement loops and includes MCDM ranking, with matching `formalization_level` anchors; `evaluation_paradigm` naturalistic needs real users, problem and system together; `decision_autonomy` rates the real-world decision and requires selection for 2; anchors for Q1, Q3 and Q4; `prompts_disclosed` and `decoding_params_reported` boundary cases
- **Enforced:** reasoning fields must contain a letter or digit, so placeholder reasoning ('...') fails validation and is re-extracted (§4). Records with empty reasoning no longer validate.
- **Changed:** provenance tag `H` allows AI assistance for evidence location, verification and phrasing (disclosed per reviewer)

### 0.10.0 — revision after the R1/R2 triage

Records coded under 0.9.0 need re-coding of the three retyped fields and of `llm_or_role` where it conflicts.

- **Type changes:** `repeated_runs` is free text so the count can be tied to its case (D015); `data_available` is `DataAvailability` full/partial/none (D025); `efficiency_metrics_reported` is `EfficiencyReporting` yes/partially/no (D153)
- **Enforced:** `llm_or_role` must be `none` when `optimization_tradition_present` is false (was a soft flag; D075/D079)
- **Clarified definitions:** `authors_claimed_tier` only on explicit tier labels (D035, D060, D140); `vdi5200_phase` only with `factory-planning` (D034); real-company-data cases are `evaluation-research` (D001); `models` excludes preliminary-test models (D065); `approval-gate` requires active correction (D086); `decision-selection` requires the system to rank (D092); `rubric` requires an explicit scoring scale (D052); `database-SQL` only for LLM-generated SQL, `simulation-platform` only for an external platform (D111); `parallelization` also at system level (D110)

### 0.9.0 — revision after the v0.8.0 review

Records coded under 0.8.0 need re-coding of the changed fields (protocol deviation; log it). Sources for each change are cited in the code comments and enum docstrings.

- **Fixes (A1–A10):** `study_design = none` for conceptual papers; enforced `formalization_level`/`optimization_tradition_present` link; generic `other`-specification rule; non-empty and de-duplicated multi-selects; soft `consistency_flags`; shared `NR` sentinel and `YesNoUnclear`; validated metadata keys; tests import the package (`pythonpath = ["src"]`), Python ≥ 3.9; `strict_json_schema()`
- **Renamed / removed:** `ResearchType` values replaced by the Wieringa et al. (2006) facet; `StudyDesignType.BENCHMARK` → `test-set`; `FormalizationLevel` values → `high`/`medium`/`low`/`none`; `validation_method` removed; `IntegrationType.KG` removed (derived as `kg_integrated`); planning tasks `site-selection` → `facility-location`, `distribution-network-planning` + `logistics-network-planning` → `logistics-distribution-network-planning`; `fine_tuning` is now a list; `time_horizon_explicitly_stated` and `independent_evaluation` are `YesNoUnclear`
- **Added (B1–B9):** see the field groups above

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.