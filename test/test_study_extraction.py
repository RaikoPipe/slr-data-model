"""Tests for the v3.0 extraction schema data model."""
import pytest
from pydantic import ValidationError

from src.slr_data_model import (
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
    DomainKnowledgeType,
    EvaluationFrameworkType,
    QualityAppraisal,
    ExtractionMetaData,
    ProvenanceTag,
    VerificationStatus,
)


def make_bibliographic(**overrides):
    defaults = dict(
        doi="10.1000/example.2024",
        title="LLM-Based Factory Layout Planning",
        authors=["A. Author", "B. Researcher"],
        affiliations=["TU Example, Germany"],
        country="Germany",
        year=2024,
        venue="Production Engineering",
        venue_type=VenueType.JOURNAL_Q1,
        language="English",
        funding_source="NR",
        self_authored_flag=False,
    )
    defaults.update(overrides)
    return BibliographicMetadata(**defaults)


def make_characterization(**overrides):
    defaults = dict(
        research_type=ResearchType.DESIGN_SCIENCE,
        research_type_rationale="Artifact creation with iterative evaluation.",
        validation_status=ValidationStatusType.IMPLEMENTED_VALIDATED,
        validation_status_rationale="Working system evaluated on benchmark with quantitative metrics.",
        industry_sector="automotive",
        case_study_domain="factory layout redesign",
        stated_research_questions="RQ1: How can LLMs support layout planning?",
    )
    defaults.update(overrides)
    return StudyCharacterization(**defaults)


def make_strategic_scope(**overrides):
    defaults = dict(
        subdomain=[SubdomainType.FACTORY_PLANNING],
        subdomain_mapping_rationale="Task mapped per Appendix A decision tree.",
        planning_task_type=[PlanningTaskType.FACTORY_LAYOUT_PLANNING, PlanningTaskType.CAPACITY_DIMENSIONING],
        time_horizon_explicitly_stated=True,
        planning_horizon_tier=PlanningHorizonTier.STRATEGIC,
        planning_horizon_rationale="Paper states a 5-year planning horizon.",
        system_configuring_decision_stated=True,
        system_configuring_decision_description="Determines workshop layout and machine capacities.",
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
    )
    defaults.update(overrides)
    return StrategicPlanningScope(**defaults)


def make_llm_intervention(**overrides):
    defaults = dict(
        intervention_description="LLM agent elicits requirements and generates layout alternatives; solver evaluates material flow.",
        models=["GPT-4o"],
        model_family=[ModelFamilyType.GPT],
        open_weight=OpenWeightType.NO,
        fine_tuning=FineTuningType.PROMPT_ENGINEERING_ONLY,
        architectural_pattern=[ArchitecturalPatternType.LLM_SOLVER],
        agentic_architecture=AgenticArchitectureType.SINGLE_AGENT,
        integrations=[IntegrationType.SOLVER],
    )
    defaults.update(overrides)
    return LLMIntervention(**defaults)


def make_or_substrate(**overrides):
    defaults = dict(
        optimization_tradition_present=True,
        formalization_level=FormalizationLevel.MATURE_MILP,
        solver_type="Gurobi",
        optimization_description="MILP minimizing material flow distance over layout alternatives.",
    )
    defaults.update(overrides)
    return ORSubstrate(**defaults)


def make_evaluation(**overrides):
    defaults = dict(
        validation_method=["benchmark comparison"],
        dataset_or_benchmark="12 layout cases from VDI 5200 companion examples",
        comparator=[ComparatorType.HUMAN_PLANNER],
        reported_metrics=[
            ReportedMetric(
                metric="planning time reduction",
                value="35",
                unit="%",
                context="vs. human planner baseline across 12 cases",
                page_section_reference="p. 8, Table 3",
            )
        ],
        study_design=StudyDesignType.BENCHMARK,
        sample_size="12 test cases",
        reported_limitations=["Single LLM evaluated; results may not generalize to other models."],
        outcome_summary="LLM-assisted planning reduced time by 12-15% with equal layout quality.",
    )
    defaults.update(overrides)
    return EvaluationAndOutcomes(**defaults)


def make_gap_indicators(**overrides):
    defaults = dict(
        hitl_pattern_present=True,
        hitl_type=HITLType.APPROVAL_GATE,
        hitl_description="Planner approves generated layout before solver runs.",
        domain_knowledge_formalization_present=True,
        domain_knowledge_type=DomainKnowledgeType.STANDARDS_ENCODING,
        domain_knowledge_description="VDI 5200 phase model encoded as structured prompts.",
        evaluation_framework_used=True,
        evaluation_framework_type=EvaluationFrameworkType.BENCHMARK,
    )
    defaults.update(overrides)
    return GapIndicators(**defaults)


def make_quality_appraisal(**overrides):
    defaults = dict(
        methodological_transparency=3,
        methodological_transparency_rationale="Prompts, model version, and evaluation protocol fully reported.",
        empirical_grounding=3,
        empirical_grounding_rationale="Implemented system with quantitative benchmark evaluation.",
        venue_tier_dimension=3,
        venue_tier_rationale="Q1 journal (Scimago 2024).",
    )
    defaults.update(overrides)
    return QualityAppraisal(**defaults)


def make_study_extraction(**overrides):
    defaults = dict(
        study_id="S001",
        bibliographic_metadata=make_bibliographic(),
        study_characterization=make_characterization(),
        strategic_planning_scope=make_strategic_scope(),
        llm_intervention=make_llm_intervention(),
        or_substrate=make_or_substrate(),
        evaluation_and_outcomes=make_evaluation(),
        gap_indicators=make_gap_indicators(),
        quality_appraisal=make_quality_appraisal(),
        extraction_metadata=ExtractionMetaData(
            provenance={
                "bibliographic_metadata.title": ProvenanceTag.LLM_VERIFIED,
                "quality_appraisal.composite_score": ProvenanceTag.DUAL,
            },
            verification={
                "strategic_planning_scope.planning_horizon_tier": VerificationStatus.VERIFIED,
            },
            llm_raw={
                "strategic_planning_scope.planning_horizon_tier": "tactical",
            },
            notes={
                "strategic_planning_scope.subdomain": "Spans tactical and strategic tasks; strategic task explicitly addressed (§6).",
            },
        ),
    )
    defaults.update(overrides)
    return StudyExtraction(**defaults)


class TestStudyExtraction:
    def test_complete_record_valid(self):
        record = make_study_extraction()
        assert record.study_id == "S001"
        assert record.bibliographic_metadata.venue_type == VenueType.JOURNAL_Q1
        assert record.strategic_planning_scope.planning_horizon_tier == PlanningHorizonTier.STRATEGIC
        assert record.llm_intervention.models == ["GPT-4o"]
        assert record.or_substrate.solver_type == "Gurobi"
        assert record.evaluation_and_outcomes.reported_metrics[0].page_section_reference == "p. 8, Table 3"
        assert record.gap_indicators.hitl_type == HITLType.APPROVAL_GATE

    def test_json_roundtrip(self):
        record = make_study_extraction()
        json_str = record.model_dump_json()
        recreated = StudyExtraction.model_validate_json(json_str)
        assert recreated == record

    def test_quality_appraisal_composite_computed(self):
        qa = make_quality_appraisal()
        assert qa.composite_score == 9
        assert qa.needs_dual_verification is False

    def test_quality_appraisal_bounds_enforced(self):
        with pytest.raises(ValidationError):
            make_quality_appraisal(methodological_transparency=0)
        with pytest.raises(ValidationError):
            make_quality_appraisal(venue_tier_dimension=4)

    def test_quality_appraisal_dual_verification_threshold(self):
        qa = make_quality_appraisal(
            methodological_transparency=1,
            empirical_grounding=2,
            venue_tier_dimension=1,
        )
        assert qa.composite_score == 4
        assert qa.needs_dual_verification is True

    def test_gap_indicators_type_required_when_present(self):
        with pytest.raises(ValidationError, match="hitl_type is required"):
            make_gap_indicators(hitl_type=None)

    def test_gap_indicators_type_forbidden_when_absent(self):
        with pytest.raises(ValidationError, match="must be null"):
            make_gap_indicators(hitl_pattern_present=False, hitl_type=HITLType.APPROVAL_GATE)

    def test_gap_indicators_domain_knowledge_conditional(self):
        with pytest.raises(ValidationError, match="domain_knowledge_type is required"):
            make_gap_indicators(domain_knowledge_type=None)
        assert make_gap_indicators(
            domain_knowledge_formalization_present=False,
            domain_knowledge_type=None,
        ).domain_knowledge_type is None

    def test_integrations_none_exclusive(self):
        with pytest.raises(ValidationError, match="'none' cannot be combined"):
            make_llm_intervention(integrations=[IntegrationType.SOLVER, IntegrationType.NONE])

    def test_architectural_pattern_list_valid(self):
        # §5 pattern vocabulary has no 'none' member; multi-pattern selection is allowed.
        intervention = make_llm_intervention(
            architectural_pattern=[
                ArchitecturalPatternType.RAG,
                ArchitecturalPatternType.LLM_SOLVER,
            ]
        )
        assert len(intervention.architectural_pattern) == 2

    def test_model_family_multiple_valid(self):
        # model_family has no 'none' member; multiple families for multiple models.
        intervention = make_llm_intervention(
            models=["GPT-4o", "Llama 3.1 70B"],
            model_family=[ModelFamilyType.GPT, ModelFamilyType.LLAMA],
        )
        assert len(intervention.model_family) == 2

    def test_llm_intervention_mixed_open_weight_allows_rationale(self):
        intervention = make_llm_intervention(
            models=["GPT-4o", "Llama 3.1 70B"],
            model_family=[ModelFamilyType.GPT, ModelFamilyType.LLAMA],
            open_weight=OpenWeightType.MIXED,
            open_weight_rationale="GPT-4o proprietary for extraction; Llama 70B open-weight for generation.",
        )
        assert intervention.open_weight == OpenWeightType.MIXED

    def test_reported_metric_with_range_and_conditionals(self):
        metric = ReportedMetric(
            metric="cost reduction",
            value="8-15% (10% when demand variance < 20%)",
            unit=None,
            context="compared to conventional network design across 3 scenarios",
            page_section_reference="p. 12, §5.2",
        )
        assert "8-15%" in metric.value

    def test_schema_generation(self):
        schema = StudyExtraction.model_json_schema()
        assert "StudyExtraction" in schema.get("$defs", {}) or "StudyExtraction" in str(schema)
        props = schema["properties"]
        assert "bibliographic_metadata" in props
        assert "gap_indicators" in props
        assert "extraction_metadata" in props
        # retrieval traceability omitted
        assert "retrieval_traceability" not in props

    def test_extraction_metadata_maps(self):
        meta = ExtractionMetaData(
            provenance={"evaluation_and_outcomes.sample_size": ProvenanceTag.LLM_CORRECTED},
            verification={"evaluation_and_outcomes.sample_size": VerificationStatus.CORRECTED},
            llm_raw={"evaluation_and_outcomes.sample_size": "N=10"},
            notes={"evaluation_and_outcomes.sample_size": "Paper reports 12 cases; LLM said 10."},
        )
        assert meta.provenance["evaluation_and_outcomes.sample_size"] == ProvenanceTag.LLM_CORRECTED
        assert meta.llm_raw["evaluation_and_outcomes.sample_size"] == "N=10"

    def test_strategic_scope_other_task_specification(self):
        scope = make_strategic_scope(
            planning_task_type=[PlanningTaskType.OTHER],
            other_planning_task_specification="Generation of investment decision memos",
        )
        assert scope.other_planning_task_specification == "Generation of investment decision memos"

    def test_bibliographic_defaults_optional_fields(self):
        bib = make_bibliographic(funding_description=None)
        assert bib.funding_source == "NR"
        assert bib.funding_description is None