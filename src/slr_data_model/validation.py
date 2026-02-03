from enum import Enum
from typing import Optional, Set

from pydantic import BaseModel, Field

from . import DescriptiveEnum


class ValidationMethodType(DescriptiveEnum):
    SIMULATION = "simulation", "Validation through simulated environments or scenarios."
    CASE_STUDY = "case study", "In-depth analysis of specific instances or applications."
    BENCHMARK = "benchmark", "Comparison against established benchmarks or datasets."
    FIELD_DEPLOYMENT = "field deployment", "Real-world deployment and observation of system performance."
    NONE = "none", "No validation method reported."

class FailureAttributionType(DescriptiveEnum):
    CONTEXT_INSUFFICIENCY = "context-insufficiency", "Missing or incomplete context"
    CONTEXT_FORMATTING = "context-formatting", "Poorly structured context"
    MODEL_CAPABILITY = "model-capability", "LLM reasoning or generation error"
    TOOL_FAILURE = "tool-failure", "External tool or API failure"
    UNATTRIBUTED = "unattributed", "Failure mode not analyzed"

class ReportedOutcomes(BaseModel):
    """Performance outcomes and limitations reported in the paper."""
    decision_quality_improvement: list[str] = Field(
        description="Reported improvements in decision quality or accuracy against traditional methods are ablation of context engineering techniques."
    )
    response_time_impact: list[str] = Field(
        description="Impacts on response time or processing speed."
    )
    reliability_metrics: list[str] = Field(
        description="System reliability, uptime, or error rate metrics."
    )
    failure_attribution: list[FailureAttributionType] = Field(...)
    ce_technique_effectiveness: dict[str, str] = Field(
        description="Mapping of CE technique to reported effectiveness"
    )
    failure_modes: list[str] = Field(
        description="Identified failure modes or error conditions."
    )
    limitations: list[str] = Field(
        description="Acknowledged limitations of the approach."
    )
