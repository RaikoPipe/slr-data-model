from typing import Optional

from pydantic import BaseModel, Field

from .annotation_helper import make_type_annotations, reasoning_field
from .descriptive_enum import DescriptiveEnum


class FormalizationLevel(DescriptiveEnum):
    """Formalization level of the optimization tradition per §3.5."""
    MATURE_MILP = "mature-MILP", "Mature MILP-based optimization tradition"
    MID_MATURITY_RL_METAHEURISTIC = "mid-maturity-RL-metaheuristic", "Mid-maturity RL or metaheuristic optimization"
    LOW_FORMALIZATION = "low-formalization", "Low-formalization optimization approach"
    NONE = "none", "No optimization tradition present"


class ORSubstrate(BaseModel):
    """OR/optimization substrate characteristics."""
    optimization_tradition_present: bool = Field(
        description="Whether an underlying optimization/OR tradition is present."
    )
    optimization_tradition_present_reasoning: str = reasoning_field()
    formalization_level: FormalizationLevel = Field(
        description="Formalization level of the optimization tradition." + make_type_annotations(FormalizationLevel)
    )
    formalization_level_reasoning: str = reasoning_field()
    solver_type: Optional[str] = Field(
        default=None,
        description="Exact solver name as reported (e.g., Gurobi, COPT, CPLEX). NR if absent."
    )
    solver_type_reasoning: str = reasoning_field()
    optimization_description: Optional[str] = Field(
        default=None,
        description="Free-text description of what is formulated and optimized as reported: decision variables, objective function, constraints."
    )