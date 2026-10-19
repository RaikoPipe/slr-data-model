from functools import cache
from typing import Literal, get_args

from pydantic import BaseModel, Field, computed_field, model_validator

from .bibliographic import BibliographicMetadata
from .study_characterization import StudyCharacterization, ValidationStatusType
from .strategic_planning import StrategicPlanningScope, TASK_SUBDOMAINS
from .llm_intervention import LLMIntervention, IntegrationType, OpenWeightType, PROPRIETARY_FAMILIES
from .or_substrate import ORSubstrate, LLMORRole
from .evaluation import EvaluationAndOutcomes, StudyDesignType
from .gap_indicators import GapIndicators, KG_TYPES
from .quality_appraisal import QualityAppraisal, StudyTypeCategory, CATEGORY_BY_VALIDATION_STATUS
from .retrieval import RetrievalTraceability
from .provenance import ExtractionMetaData
from .common import NR, YesNoUnclear

# Protocol caveat in the v0.8.0 review: vocabulary changes after extraction has started are protocol deviations.
# Every record carries the schema version it was coded under, so affected fields can be found and re-coded.
SCHEMA_VERSION = "0.9.0"

NON_EVALUATED = frozenset({ValidationStatusType.FRAMEWORK_ONLY, ValidationStatusType.CONCEPTUAL})


@cache
def field_paths(model: type[BaseModel] = None, prefix: str = "") -> frozenset[str]:
    """A8: all dotted field paths of StudyExtraction (e.g. 'strategic_planning_scope.subdomain'), for metadata keys."""
    model = model or StudyExtraction
    paths = set()
    for name, info in model.model_fields.items():
        if name == "extraction_metadata":
            continue
        path = prefix + name
        paths.add(path)
        for sub in (info.annotation, *get_args(info.annotation)):
            if isinstance(sub, type) and issubclass(sub, BaseModel):
                paths |= field_paths(sub, path + ".")
    return frozenset(paths)


class StudyExtraction(BaseModel):
    """Top-level study extraction record aligned with the v5.0 extractor instructions.

    Composes all field groups into a single study-level record. Cross-group rules (A10: stated here so the
    LLM sees them in the JSON schema): evaluation_and_outcomes.study_design is ['none'] iff
    study_characterization.validation_status is framework-only or conceptual. Soft checks are reported in
    consistency_flags and do not reject the record.
    """
    schema_version: Literal[SCHEMA_VERSION] = Field(
        default=SCHEMA_VERSION,
        description="Schema version the record was coded under. Set automatically, do not supply."
    )
    study_id: str = Field(
        description="Unique identifier for the study within the review (e.g., OSF record ID)."
    )
    bibliographic_metadata: BibliographicMetadata = Field(
        description="Bibliographic metadata (imported from search-stage records, R1 spot-checks 10%; not LLM-extracted)."
    )
    study_characterization: StudyCharacterization = Field(
        description="Study characterization (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    strategic_planning_scope: StrategicPlanningScope = Field(
        description="Strategic planning scope (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    llm_intervention: LLMIntervention = Field(
        description="LLM/AI intervention details (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    or_substrate: ORSubstrate = Field(
        description="OR/optimization substrate (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    evaluation_and_outcomes: EvaluationAndOutcomes = Field(
        description="Evaluation and outcomes (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    retrieval_traceability: RetrievalTraceability = Field(
        description="Retrieval traceability (descriptive: LLM pre-fill, R1 verifies 100%)."
    )
    gap_indicators: GapIndicators = Field(
        description="Gap indicators (interpretive: LLM-extracted, R1 + R2 each verify 100%, blind)."
    )
    quality_appraisal: QualityAppraisal = Field(
        description="Quality appraisal (interpretive: LLM-extracted, R1 + R2 each verify 100%, blind)."
    )
    extraction_metadata: ExtractionMetaData = Field(
        description="Provenance and verification metadata (§7, §8)."
    )

    @model_validator(mode="after")
    def validate_cross_group(self):
        """A1: no-evaluation design iff framework-only/conceptual. A8: metadata keys must be real field paths."""
        no_evaluation = StudyDesignType.NONE in self.evaluation_and_outcomes.study_design
        if no_evaluation != (self.study_characterization.validation_status in NON_EVALUATED):
            raise ValueError("study_design must be ['none'] iff validation_status is framework-only or conceptual")
        meta = self.extraction_metadata
        unknown = sorted(set().union(meta.provenance, meta.verification, meta.llm_raw) - field_paths())
        if unknown:
            raise ValueError(f"extraction_metadata keys are not field paths of StudyExtraction: {unknown}")
        return self

    @computed_field(description="B8: KG integration, derived from domain_knowledge_type. Auto-computed, do not supply.")
    @property
    def kg_integrated(self) -> bool:
        return bool(KG_TYPES.intersection(self.gap_indicators.domain_knowledge_type or []))

    @computed_field(description="A6: soft cross-group consistency warnings for reviewers. Auto-computed, do not supply.")
    @property
    def consistency_flags(self) -> list[str]:
        llm, opt = self.llm_intervention, self.or_substrate
        scope, ev = self.strategic_planning_scope, self.evaluation_and_outcomes
        flags = []
        if llm.open_weight == OpenWeightType.YES and llm.model_family and set(llm.model_family) <= PROPRIETARY_FAMILIES:
            flags.append("open_weight is 'Y' but all model families are usually proprietary (GPT/Claude/Gemini)")
        if IntegrationType.SOLVER in llm.integrations and not opt.optimization_tradition_present:
            flags.append("integrations includes 'solver' but optimization_tradition_present is false")
        if (LLMORRole.NONE in opt.llm_or_role) == opt.optimization_tradition_present:
            flags.append("llm_or_role should be 'none' iff optimization_tradition_present is false")
        if ev.reported_metrics and self.study_characterization.validation_status == ValidationStatusType.PROTOTYPE:
            flags.append("reported_metrics present but validation_status 'prototype' is defined as 'without defined metrics'")
        if scope.time_horizon_explicitly_stated == YesNoUnclear.NO and scope.stated_horizon_value != NR:
            flags.append("stated_horizon_value given but time_horizon_explicitly_stated is 'N'")
        for task in scope.planning_task_type:
            if not TASK_SUBDOMAINS[task].intersection(scope.subdomain):
                flags.append(f"planning task '{task.value}' maps to none of the coded subdomains (Appendix A)")
        return flags

    @computed_field(description="§3.9 study-type category, derived from validation status. Auto-computed, do not supply.")
    @property
    def study_type_category(self) -> StudyTypeCategory:
        return CATEGORY_BY_VALIDATION_STATUS[self.study_characterization.validation_status]


def strict_json_schema(model: type[BaseModel] = StudyExtraction) -> dict:
    """A10: JSON schema variant for strict structured-output modes (e.g. OpenAI strict), which reject defaults.

    Every property becomes required and defaults are dropped; fields that default to None are already
    nullable, the others (NR strings, empty lists) must then be emitted explicitly. Computed fields and
    validators are not part of the schema: validate the LLM output with `model.model_validate_json` and feed
    the ValidationError text back to the LLM as a repair prompt.
    """
    schema = model.model_json_schema()

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("properties"), dict):
                for prop in node["properties"].values():
                    prop.pop("default", None)
                node["required"] = list(node["properties"])
                node["additionalProperties"] = False
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)
    return schema
