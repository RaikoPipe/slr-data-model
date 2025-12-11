from enum import Enum
from typing import Optional, Set

from pydantic import BaseModel, Field


class ValidationMethod(str, Enum):
    SIMULATION = "simulation"
    CASE_STUDY = "case study"
    BENCHMARK = "benchmark"
    FIELD_DEPLOYMENT = "field deployment"
    NONE = "none"

class ReportedOutcomes(BaseModel):
    """Performance outcomes and limitations reported in the paper."""
    decision_quality_improvement: Optional[str] = Field(
        default=None,
        description="Reported improvements in decision quality or accuracy."
    )
    response_time_impact: Optional[str] = Field(
        default=None,
        description="Impact on response time or processing speed."
    )
    reliability_metrics: Optional[str] = Field(
        default=None,
        description="System reliability, uptime, or error rate metrics."
    )
    failure_modes: Set[str] = Field(
        default_factory=set,
        description="Identified failure modes or error conditions."
    )
    limitations: Set[str] = Field(
        default_factory=set,
        description="Acknowledged limitations of the approach."
    )
