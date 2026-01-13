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

class ReportedOutcomes(BaseModel):
    """Performance outcomes and limitations reported in the paper."""
    decision_quality_improvement: str = Field(
        description="Reported improvements in decision quality or accuracy against traditional methods are ablation of context engineering techniques."
    )
    response_time_impact: str = Field(
        description="Impact on response time or processing speed."
    )
    reliability_metrics: str = Field(
        description="System reliability, uptime, or error rate metrics."
    )
    failure_modes: list[str] = Field(
        description="Identified failure modes or error conditions."
    )
    limitations: list[str] = Field(
        description="Acknowledged limitations of the approach."
    )
