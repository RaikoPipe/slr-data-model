"""Tests for the v5.0 extraction schema data model."""
import pytest
from pydantic import ValidationError

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
    NR,
    YesNoUnclear,
    SCPProcess,
    VDI5200Phase,
    PromptingTechnique,
    WorkflowPattern,
    AgentMemory,
    DeploymentType,
    ModalityType,
    OptimizationParadigm,
    LLMORRole,
    EvaluationParadigm,
    KGModel,
    KGConstruction,
    KGUsage,
    AutomationStage,
    DecisionAutonomy,
    PromptDisclosure,
    strict_json_schema,
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
        research_type=ResearchType.VALIDATION_RESEARCH,
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
        scp_process=[SCPProcess.PRODUCTION],
        vdi5200_phase=[VDI5200Phase.CONCEPT_PLANNING],
        time_horizon_explicitly_stated=YesNoUnclear.YES,
        stated_horizon_value="5 years",
        planning_horizon_tiers=[PlanningHorizonTier.STRATEGIC],
        authors_claimed_tier=[PlanningHorizonTier.STRATEGIC],
        planning_horizon_rationale="Paper states a 5-year planning horizon.",
        system_configuring_decision=True,
        system_configuring_decision_stated=True,
        system_configuring_decision_description="Determines workshop layout and machine capacities.",
        theoretical_framework_cited=[TheoreticalFrameworkType.VDI_5200],
        planning_task_type_reasoning=R,
        scp_process_reasoning=R,
        vdi5200_phase_reasoning=R,
        authors_claimed_tier_reasoning=R,
        time_horizon_explicitly_stated_reasoning=R,
        system_configuring_decision_reasoning=R,
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
        deployment=DeploymentType.API,
        modality=ModalityType.TEXT,
        fine_tuning=[FineTuningType.NONE],
        prompting_techniques=[PromptingTechnique.FEW_SHOT, PromptingTechnique.REACT],
        agentic_architecture=AgenticArchitectureType.SINGLE_AGENT,
        workflow_patterns=[WorkflowPattern.NONE],
        agent_memory=AgentMemory.SHORT_TERM,
        planning_reflection=False,
        tool_use=True,
        integrations=[IntegrationType.SOLVER],
        models_rationale="No other LLMs discussed.",
        model_family_reasoning=R,
        open_weight_rationale=R,
        deployment_reasoning=R,
        modality_reasoning=R,
        fine_tuning_reasoning=R,
        prompting_techniques_reasoning=R,
        agentic_architecture_reasoning=R,
        workflow_patterns_reasoning=R,
        agent_capabilities_reasoning=R,
        integrations_reasoning=R,
    )
    defaults.update(overrides)
    return LLMIntervention(**defaults)


def make_or_substrate(**overrides):
    defaults = dict(
        optimization_tradition_present=True,
        formalization_level=FormalizationLevel.HIGH,
        optimization_paradigm=[OptimizationParadigm.MILP_LP],
        llm_or_role=[LLMORRole.SOLVER_ORCHESTRATOR],
        solver_type="Gurobi",
        optimization_description="MILP minimizing material flow distance over layout alternatives.",
        optimization_tradition_present_reasoning=R,
        formalization_level_reasoning=R,
        optimization_paradigm_reasoning=R,
        llm_or_role_reasoning=R,
        solver_type_reasoning=R,
    )
    defaults.update(overrides)
    return ORSubstrate(**defaults)


def make_evaluation(**overrides):
    defaults = dict(
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
        study_design=[StudyDesignType.TEST_SET],
        evaluation_paradigm=EvaluationParadigm.ARTIFICIAL,
        independent_evaluation=YesNoUnclear.NO,
        repeated_runs=3,
        llm_as_judge=False,
        efficiency_metrics_reported=True,
        statistical_testing=False,
        llm_evaluation_properties_reasoning=R,
        sample_size="12 test cases",
        reported_limitations=["Single LLM evaluated; results may not generalize to other models."],
        outcome_summary="LLM-assisted planning reduced time by 12-15% with equal layout quality.",
        evaluation_paradigm_reasoning=R,
        dataset_or_benchmark_reasoning=R,
        comparator_reasoning=R,
        reported_metrics_reasoning=R,
        study_design_reasoning=R,
        independent_evaluation_reasoning=R,
        sample_size_reasoning=R,
        reported_limitations_reasoning=R,
    )
    defaults.update(overrides)
    return EvaluationAndOutcomes(**defaults)


def make_gap_indicators(**overrides):
    defaults = dict(
        hitl_pattern_present=True,
        hitl_type=[HITLType.APPROVAL_GATE],
        hitl_description="Planner approves generated layout before solver runs.",
        domain_knowledge_formalization_present=True,
        domain_knowledge_type=[DomainKnowledgeType.STANDARDS_ENCODING],
        domain_knowledge_description="VDI 5200 phase model encoded as structured prompts.",
        standards_encoded=["VDI 5200"],
        automation_stage=[AutomationStage.INFORMATION_ANALYSIS, AutomationStage.DECISION_SELECTION],
        automation_stage_reasoning=R,
        decision_autonomy=DecisionAutonomy.L2_RECOMMENDATION,
        decision_autonomy_reasoning=R,
        evaluation_framework_used=True,
        evaluation_framework_type=[EvaluationFrameworkType.BENCHMARK],
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
        model_version_reported=True,
        prompts_disclosed=PromptDisclosure.FULL,
        decoding_params_reported=True,
        code_available=False,
        data_available=False,
        run_date_reported=False,
        reproducibility_reasoning=R,
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


def make_conceptual_study(status=ValidationStatusType.FRAMEWORK_ONLY, **overrides):
    """A1: category-C study without any evaluation of its own method."""
    return make_study_extraction(
        study_characterization=make_characterization(
            research_type=ResearchType.SOLUTION_PROPOSAL, validation_status=status
        ),
        evaluation_and_outcomes=make_evaluation(
            study_design=[StudyDesignType.NONE],
            evaluation_paradigm=EvaluationParadigm.NA,
            comparator=[ComparatorType.NONE],
            reported_metrics=[],
            repeated_runs="NR",
            efficiency_metrics_reported=False,
        ),
        **overrides,
    )


class TestStudyExtraction:
    def test_complete_record_valid(self):
        record = make_study_extraction()
        assert record.study_id == "S001"
        assert record.bibliographic_metadata.venue_type == VenueType.JOURNAL_Q1
        assert record.strategic_planning_scope.planning_horizon_tiers == [PlanningHorizonTier.STRATEGIC]
        assert record.llm_intervention.models == ["GPT-4o"]
        assert record.or_substrate.solver_type == "Gurobi"
        assert record.evaluation_and_outcomes.reported_metrics[0].page_section_reference == "p. 8, Table 3"
        assert record.gap_indicators.hitl_type == [HITLType.APPROVAL_GATE]

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
        record = make_study_extraction(
            study_characterization=make_characterization(validation_status=ValidationStatusType.PROTOTYPE)
        )
        assert record.study_type_category == StudyTypeCategory.B
        for status in (ValidationStatusType.FRAMEWORK_ONLY, ValidationStatusType.CONCEPTUAL):
            record = make_conceptual_study(status)
            assert record.study_type_category == StudyTypeCategory.C
        dumped = make_study_extraction().model_dump(mode="json")
        assert dumped["study_type_category"] == "A"
        assert dumped["quality_appraisal"]["low_quality_flag"] is False

    def test_derived_fields_not_in_llm_schema(self):
        schema = StudyExtraction.model_json_schema()
        assert "study_type_category" not in schema["properties"]
        assert "low_quality_flag" not in schema["$defs"]["QualityAppraisal"]["properties"]
        assert "consistency_flags" not in schema["properties"] and "kg_integrated" not in schema["properties"]

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
            standards_encoded=[],
        ).domain_knowledge_type is None

    def test_integrations_none_exclusive(self):
        with pytest.raises(ValidationError, match="'none' cannot be combined"):
            make_llm_intervention(integrations=[IntegrationType.SOLVER, IntegrationType.NONE])

    def test_gap_indicator_types_multi_select(self):
        gi = make_gap_indicators(
            hitl_type=[HITLType.APPROVAL_GATE, HITLType.WHAT_IF_INTERFACE],
            evaluation_framework_type=[EvaluationFrameworkType.CUSTOM_TEST_SET, EvaluationFrameworkType.RUBRIC],
        )
        assert len(gi.hitl_type) == 2 and len(gi.evaluation_framework_type) == 2
        with pytest.raises(ValidationError, match="hitl_type is required"):
            make_gap_indicators(hitl_type=[])

    def test_study_design_multi_select(self):
        ev = make_evaluation(study_design=[StudyDesignType.MULTI_CASE, StudyDesignType.USER_STUDY])
        assert len(ev.study_design) == 2
        with pytest.raises(ValidationError):
            make_evaluation(study_design=[])

    def test_system_configuring_decision_drives_strategic_tier(self):
        tactical = [PlanningHorizonTier.TACTICAL]
        with pytest.raises(ValidationError, match="iff system_configuring_decision"):
            make_strategic_scope(system_configuring_decision=False, system_configuring_decision_stated=False)
        with pytest.raises(ValidationError, match="iff system_configuring_decision"):
            make_strategic_scope(planning_horizon_tiers=tactical)
        with pytest.raises(ValidationError, match="requires system_configuring_decision"):
            make_strategic_scope(system_configuring_decision=False, planning_horizon_tiers=tactical)
        assert not make_strategic_scope(
            system_configuring_decision=False, system_configuring_decision_stated=False, planning_horizon_tiers=tactical
        ).system_configuring_decision

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
        bib = make_bibliographic(funding_description=None, funding_source=None)
        assert bib.funding_source == NR
        assert bib.funding_description is None


class TestV090Rules:
    """Rules added in schema 0.9.0 (v0.8.0 review items A1-A10, B1-B9)."""

    def test_schema_version_recorded(self):
        assert make_study_extraction().schema_version == "0.9.0"

    def test_a1_conceptual_paper_encodable(self):
        assert make_conceptual_study().evaluation_and_outcomes.study_design == [StudyDesignType.NONE]
        with pytest.raises(ValidationError, match="iff validation_status is framework-only"):
            make_study_extraction(evaluation_and_outcomes=make_conceptual_study().evaluation_and_outcomes)
        with pytest.raises(ValidationError, match="iff validation_status is framework-only"):
            make_study_extraction(study_characterization=make_characterization(
                validation_status=ValidationStatusType.CONCEPTUAL))
        with pytest.raises(ValidationError, match="'none' cannot be combined"):
            make_evaluation(study_design=[StudyDesignType.NONE, StudyDesignType.SINGLE_CASE])
        with pytest.raises(ValidationError, match="evaluation_paradigm must be 'NA'"):
            make_evaluation(evaluation_paradigm=EvaluationParadigm.NA)

    def test_a2_formalization_none_iff_no_optimization(self):
        with pytest.raises(ValidationError, match="formalization_level must be 'none'"):
            make_or_substrate(formalization_level=FormalizationLevel.NONE)
        with pytest.raises(ValidationError, match="formalization_level must be 'none'"):
            make_or_substrate(optimization_tradition_present=False, optimization_paradigm=[])
        with pytest.raises(ValidationError, match="optimization_paradigm must be null"):
            make_or_substrate(optimization_tradition_present=False, formalization_level=FormalizationLevel.NONE)
        assert make_or_substrate(
            optimization_tradition_present=False, formalization_level=FormalizationLevel.NONE,
            optimization_paradigm=[], llm_or_role=[LLMORRole.NONE], solver_type=None,
        ).solver_type == NR

    def test_a3_other_requires_specification_everywhere(self):
        cases = [
            (make_strategic_scope, "planning_task_type", [PlanningTaskType.OTHER], "other_planning_task_specification"),
            (make_llm_intervention, "model_family", [ModelFamilyType.OTHER], "other_model_family_specification"),
            (make_llm_intervention, "fine_tuning", [FineTuningType.OTHER], "other_fine_tuning_specification"),
            (make_llm_intervention, "prompting_techniques", [PromptingTechnique.OTHER], "other_prompting_technique_specification"),
            (make_gap_indicators, "hitl_type", [HITLType.OTHER], "hitl_type_other_specification"),
            (make_gap_indicators, "evaluation_framework_type", [EvaluationFrameworkType.OTHER], "evaluation_framework_type_other_specification"),
            (make_or_substrate, "optimization_paradigm", [OptimizationParadigm.OTHER], "other_optimization_paradigm_specification"),
        ]
        for factory, field, value, spec in cases:
            with pytest.raises(ValidationError, match=f"{spec} is required"):
                factory(**{field: value})
            assert getattr(factory(**{field: value, spec: "x"}), spec) == "x"
            with pytest.raises(ValidationError, match=f"{spec} must be null"):
                factory(**{spec: "stray"})

    def test_a4_empty_lists_rejected(self):
        for factory, field in (
            (make_strategic_scope, "subdomain"),
            (make_strategic_scope, "planning_task_type"),
            (make_strategic_scope, "theoretical_framework_cited"),
            (make_llm_intervention, "integrations"),
            (make_evaluation, "comparator"),
        ):
            with pytest.raises(ValidationError, match=field):
                factory(**{field: []})
        with pytest.raises(ValidationError, match="model_family is required"):
            make_llm_intervention(model_family=[])
        with pytest.raises(ValidationError, match="model_family must be null"):
            make_llm_intervention(models=[])

    def test_a5_duplicates_dropped_in_order(self):
        scope = make_strategic_scope(planning_task_type=[
            PlanningTaskType.MATERIAL_FLOW_DESIGN, PlanningTaskType.FACTORY_LAYOUT_PLANNING,
            PlanningTaskType.MATERIAL_FLOW_DESIGN,
        ])
        assert scope.planning_task_type == [PlanningTaskType.MATERIAL_FLOW_DESIGN, PlanningTaskType.FACTORY_LAYOUT_PLANNING]

    def test_a6_consistency_flags_are_soft(self):
        assert make_study_extraction().consistency_flags == []
        record = make_study_extraction(
            study_characterization=make_characterization(validation_status=ValidationStatusType.PROTOTYPE),
            llm_intervention=make_llm_intervention(open_weight=OpenWeightType.YES),
            or_substrate=make_or_substrate(
                optimization_tradition_present=False, formalization_level=FormalizationLevel.NONE,
                optimization_paradigm=[],
            ),
        )
        flags = " | ".join(record.consistency_flags)
        assert "open_weight" in flags and "'solver'" in flags and "llm_or_role" in flags and "prototype" in flags
        mismatch = make_study_extraction(strategic_planning_scope=make_strategic_scope(
            planning_task_type=[PlanningTaskType.GPN_CONFIGURATION]))
        assert any("GPN-configuration" in f for f in mismatch.consistency_flags)

    def test_a7_not_reported_sentinel(self):
        ev = make_evaluation(sample_size="n/a", dataset_or_benchmark=None, reported_limitations=["NR"], repeated_runs="NR")
        assert ev.sample_size == NR and ev.dataset_or_benchmark == NR
        assert ev.reported_limitations == [] and ev.repeated_runs == NR
        with pytest.raises(ValidationError):
            make_evaluation(repeated_runs=0)
        assert make_evaluation(independent_evaluation=YesNoUnclear.UNCLEAR).independent_evaluation == YesNoUnclear.UNCLEAR

    def test_a8_metadata_keys_validated(self):
        bad = ExtractionMetaData(provenance={"strategic_planing_scope.subdomain": ProvenanceTag.LLM_VERIFIED})
        with pytest.raises(ValidationError, match="strategic_planing_scope.subdomain"):
            make_study_extraction(extraction_metadata=bad)
        nested = ExtractionMetaData(llm_raw={"evaluation_and_outcomes.reported_metrics.value": "x"})
        assert make_study_extraction(extraction_metadata=nested)

    def test_a10_strict_schema(self):
        schema = strict_json_schema()
        nodes = [schema, *schema["$defs"].values()]
        for node in nodes:
            if "properties" in node:
                assert set(node["required"]) == set(node["properties"])
                assert node["additionalProperties"] is False
                assert not any("default" in prop for prop in node["properties"].values())

    def test_b4_vdi_phase_na_iff_not_factory_planning(self):
        with pytest.raises(ValidationError, match="vdi5200_phase must be 'NA'"):
            make_strategic_scope(vdi5200_phase=[VDI5200Phase.NA])
        with pytest.raises(ValidationError, match="vdi5200_phase must be 'NA'"):
            make_strategic_scope(subdomain=[SubdomainType.SITE_SELECTION],
                                 planning_task_type=[PlanningTaskType.FACILITY_LOCATION])
        with pytest.raises(ValidationError, match="'NA' cannot be combined"):
            make_strategic_scope(scp_process=[SCPProcess.NA, SCPProcess.PRODUCTION])

    def test_b8_kg_details_required_iff_kg(self):
        kg = [DomainKnowledgeType.KNOWLEDGE_GRAPH]
        with pytest.raises(ValidationError, match="kg_model is required"):
            make_gap_indicators(domain_knowledge_type=kg, standards_encoded=[])
        gi = make_gap_indicators(
            domain_knowledge_type=kg, standards_encoded=[], kg_model=KGModel.RDF_OWL,
            kg_construction=KGConstruction.HYBRID, kg_usage=[KGUsage.RETRIEVAL], kg_reasoning=R,
        )
        assert make_study_extraction(gap_indicators=gi).kg_integrated is True
        assert make_study_extraction().kg_integrated is False
        with pytest.raises(ValidationError, match="standards_encoded is required"):
            make_gap_indicators(standards_encoded=[])
