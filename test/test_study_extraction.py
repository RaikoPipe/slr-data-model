"""Tests for the v5.0 extraction schema data model."""
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
    AppraisalAnswer,
    StudyTypeCategory,
    RetrievalTraceability,
    RetrievalSource,
    ExtractionMetaData,
    ProvenanceTag,
    ReviewerRole,
    VerificationStatus,
    FieldVerdict,
)

R = "p. 3, §2"  # placeholder reasoning + locator


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
        industry_sector_reasoning=R,
        case_study_domain_reasoning=R,
        stated_research_questions_reasoning=R,
    )
    defaults.update(overrides)
    return StudyCharacterization(**defaults)


def make_strategic_scope(**overrides):
    defaults = dict(
        subdomain=[SubdomainType.FACTORY_PLANNING],
        subdomain_mapping_rationale="Task mapped per Appendix A decision tree.",
        planning_task_type=[PlanningTaskType.FACTORY_LAYOUT_PLANNING, PlanningTaskType.CAPACITY_DIMENSIONING],
        time_horizon_explicitly_stated=True,
        planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC],
        planning_horizon_rationale="Paper states a 5-year planning horizon.",
        system_configuring_decision_stated=True,
        system_configuring_decision_description="Determines workshop layout and machine capacities.",
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
        planning_task_type_reasoning=R,
        time_horizon_explicitly_stated_reasoning=R,
        system_configuring_decision_stated_reasoning=R,
        theoretical_framework_cited_reasoning=R,
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
        models_rationale="No other LLMs discussed.",
        model_family_reasoning=R,
        open_weight_rationale=R,
        fine_tuning_reasoning=R,
        architectural_pattern_reasoning=R,
        agentic_architecture_reasoning=R,
        integrations_reasoning=R,
    )
    defaults.update(overrides)
    return LLMIntervention(**defaults)


def make_or_substrate(**overrides):
    defaults = dict(
        optimization_tradition_present=True,
        formalization_level=FormalizationLevel.MATURE_MILP,
        solver_type="Gurobi",
        optimization_description="MILP minimizing material flow distance over layout alternatives.",
        optimization_tradition_present_reasoning=R,
        formalization_level_reasoning=R,
        solver_type_reasoning=R,
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
        validation_method_reasoning=R,
        dataset_or_benchmark_reasoning=R,
        comparator_reasoning=R,
        reported_metrics_reasoning=R,
        study_design_reasoning=R,
        sample_size_reasoning=R,
        reported_limitations_reasoning=R,
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
        hitl_pattern_present_reasoning=R,
        hitl_type_reasoning=R,
        domain_knowledge_formalization_present_reasoning=R,
        domain_knowledge_type_reasoning=R,
        evaluation_framework_used_reasoning=R,
        evaluation_framework_type_reasoning=R,
    )
    defaults.update(overrides)
    return GapIndicators(**defaults)


def make_quality_appraisal(**overrides):
    defaults = dict(
        q1_methodological_transparency=AppraisalAnswer.YES,
        q1_methodological_transparency_reasoning="Prompts, model version, and evaluation protocol fully reported.",
        q2_empirical_or_demonstration_grounding=AppraisalAnswer.YES,
        q2_empirical_or_demonstration_grounding_reasoning="Metrics defined, comparator and sample size reported.",
        q3_validity_and_limitation_discussion=AppraisalAnswer.PARTIALLY,
        q3_validity_and_limitation_discussion_reasoning="Scalability discussed, external validity not.",
        q4_positioning_against_prior_work=AppraisalAnswer.YES,
        q4_positioning_against_prior_work_reasoning="Explicit comparison table vs. prior work.",
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
        retrieval_traceability=RetrievalTraceability(source=RetrievalSource.SCOPUS, source_reasoning="Scopus record ID 123."),
        gap_indicators=make_gap_indicators(),
        quality_appraisal=make_quality_appraisal(),
        extraction_metadata=ExtractionMetaData(
            provenance={
                "bibliographic_metadata.title": ProvenanceTag.METADATA,
                "quality_appraisal.q1_methodological_transparency": ProvenanceTag.LLM_VERIFIED,
            },
            verification={
                "quality_appraisal.q1_methodological_transparency": [
                    FieldVerdict(reviewer=ReviewerRole.R1, status=VerificationStatus.VERIFIED),
                    FieldVerdict(reviewer=ReviewerRole.R2, status=VerificationStatus.VERIFIED),
                ],
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
        assert record.strategic_planning_scope.planning_horizon_tiers == [PlanningHorizonTier.STRATEGIC]
        assert record.llm_intervention.models == ["GPT-4o"]
        assert record.or_substrate.solver_type == "Gurobi"
        assert record.evaluation_and_outcomes.reported_metrics[0].page_section_reference == "p. 8, Table 3"
        assert record.gap_indicators.hitl_type == HITLType.APPROVAL_GATE

    def test_json_roundtrip(self):
        record = make_study_extraction()
        json_str = record.model_dump_json()
        recreated = StudyExtraction.model_validate_json(json_str)
        assert recreated == record

    def test_quality_appraisal_low_quality_flag(self):
        assert make_quality_appraisal().low_quality_flag is False
        no = AppraisalAnswer.NO
        assert make_quality_appraisal(q1_methodological_transparency=no).low_quality_flag is False
        assert make_quality_appraisal(
            q1_methodological_transparency=no, q4_positioning_against_prior_work=no
        ).low_quality_flag is True

    def test_study_type_category_derived_from_validation_status(self):
        assert make_study_extraction().study_type_category == StudyTypeCategory.A
        for status, category in (
            (ValidationStatusType.PROTOTYPE, StudyTypeCategory.B),
            (ValidationStatusType.FRAMEWORK_ONLY, StudyTypeCategory.C),
            (ValidationStatusType.CONCEPTUAL, StudyTypeCategory.C),
        ):
            record = make_study_extraction(study_characterization=make_characterization(validation_status=status))
            assert record.study_type_category == category
        dumped = make_study_extraction().model_dump(mode="json")
        assert dumped["study_type_category"] == "A"
        assert dumped["quality_appraisal"]["low_quality_flag"] is False

    def test_derived_fields_not_in_llm_schema(self):
        schema = StudyExtraction.model_json_schema()
        assert "study_type_category" not in schema["properties"]
        assert "low_quality_flag" not in schema["$defs"]["QualityAppraisal"]["properties"]

    def test_reasoning_fields_required(self):
        with pytest.raises(ValidationError, match="industry_sector_reasoning"):
            make_characterization(industry_sector_reasoning=None)
        with pytest.raises(ValidationError, match="q2_empirical_or_demonstration_grounding_reasoning"):
            make_quality_appraisal(q2_empirical_or_demonstration_grounding_reasoning=None)

    def test_gap_indicators_type_reasoning_conditional(self):
        with pytest.raises(ValidationError, match="hitl_type_reasoning is required"):
            make_gap_indicators(hitl_type_reasoning=None)
        with pytest.raises(ValidationError, match="hitl_type_reasoning must be null"):
            make_gap_indicators(hitl_pattern_present=False, hitl_type=None)

    def test_retrieval_traceability_anchor_papers(self):
        snowball = RetrievalSource.SNOWBALLING
        assert RetrievalTraceability(
            source=snowball, source_reasoning=R, anchor_papers=["10.1000/anchor"]
        ).anchor_papers == ["10.1000/anchor"]
        with pytest.raises(ValidationError, match="anchor_papers is required"):
            RetrievalTraceability(source=snowball, source_reasoning=R)
        with pytest.raises(ValidationError, match="anchor_papers must be empty"):
            RetrievalTraceability(source=RetrievalSource.WOS, source_reasoning=R, anchor_papers=["x"])

    def test_comparator_none_exclusive(self):
        with pytest.raises(ValidationError, match="'none' cannot be combined"):
            make_evaluation(comparator=[ComparatorType.NONE, ComparatorType.HUMAN_PLANNER])

    def test_gap_indicators_type_required_when_present(self):
        with pytest.raises(ValidationError, match="hitl_type is required"):
            make_gap_indicators(hitl_type=None)

    def test_gap_indicators_type_forbidden_when_absent(self):
        with pytest.raises(ValidationError, match="must be null"):
            make_gap_indicators(hitl_pattern_present=False, hitl_type_reasoning=None)

    def test_gap_indicators_domain_knowledge_conditional(self):
        with pytest.raises(ValidationError, match="domain_knowledge_type is required"):
            make_gap_indicators(domain_knowledge_type=None)
        assert make_gap_indicators(
            domain_knowledge_formalization_present=False,
            domain_knowledge_type=None,
            domain_knowledge_type_reasoning=None,
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
        assert "retrieval_traceability" in props

    def test_extraction_metadata_maps(self):
        field = "evaluation_and_outcomes.sample_size"
        meta = ExtractionMetaData(
            provenance={field: ProvenanceTag.LLM_CORRECTED},
            verification={field: [FieldVerdict(
                reviewer=ReviewerRole.R1,
                status=VerificationStatus.CORRECTED,
                corrected_value="12 test cases",
                reasoning="Paper reports 12 cases (p. 8); LLM said 10.",
            )]},
            llm_raw={field: "N=10"},
        )
        assert meta.provenance[field] == ProvenanceTag.LLM_CORRECTED
        assert meta.llm_raw[field] == "N=10"
        assert meta.verified_by == {field: "R1"}
        assert make_study_extraction().extraction_metadata.verified_by == {
            "quality_appraisal.q1_methodological_transparency": "R1;R2"
        }

    def test_field_verdict_corrected_value_conditional(self):
        with pytest.raises(ValidationError, match="corrected_value is required"):
            FieldVerdict(reviewer=ReviewerRole.R2, status=VerificationStatus.CORRECTED)
        with pytest.raises(ValidationError, match="corrected_value must be null"):
            FieldVerdict(reviewer=ReviewerRole.R2, status=VerificationStatus.VERIFIED, corrected_value="x")

    def test_strategic_scope_other_task_specification(self):
        scope = make_strategic_scope(
            planning_task_type=[PlanningTaskType.OTHER],
            other_planning_task_specification="Generation of investment decision memos",
        )
        assert scope.other_planning_task_specification == "Generation of investment decision memos"

    def test_strategic_scope_horizon_tiers(self):
        scope = make_strategic_scope(
            planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC, PlanningHorizonTier.TACTICAL]
        )
        assert scope.planning_horizon_tiers == [PlanningHorizonTier.STRATEGIC, PlanningHorizonTier.TACTICAL]
        with pytest.raises(ValidationError, match="'NA' cannot be combined"):
            make_strategic_scope(planning_horizon_tiers=[PlanningHorizonTier.NA, PlanningHorizonTier.STRATEGIC])
        with pytest.raises(ValidationError):
            make_strategic_scope(planning_horizon_tiers=[])

    def test_strategic_scope_framework_conditional_fields(self):
        none = TheoreticalFrameworkType.NONE
        other = TheoreticalFrameworkType.OTHER
        assert make_strategic_scope(
            theoretical_framework_cited=[none],
            theoretical_framework_rationale="No planning framework referenced.",
        ).theoretical_framework_rationale
        assert make_strategic_scope(
            theoretical_framework_cited=[other],
            other_theoretical_framework_specification="Resource-Based View (Barney 1991)",
        ).other_theoretical_framework_specification
        with pytest.raises(ValidationError, match="theoretical_framework_rationale is required"):
            make_strategic_scope(theoretical_framework_cited=[none])
        with pytest.raises(ValidationError, match="other_theoretical_framework_specification is required"):
            make_strategic_scope(theoretical_framework_cited=[other])
        with pytest.raises(ValidationError, match="must be null"):
            make_strategic_scope(theoretical_framework_rationale="stray")
        with pytest.raises(ValidationError, match="'none' cannot be combined"):
            make_strategic_scope(
                theoretical_framework_cited=[none, TheoreticalFrameworkType.VDI_5200],
                theoretical_framework_rationale="x",
            )

    def test_bibliographic_defaults_optional_fields(self):
        bib = make_bibliographic(funding_description=None)
        assert bib.funding_source == "NR"
        assert bib.funding_description is None