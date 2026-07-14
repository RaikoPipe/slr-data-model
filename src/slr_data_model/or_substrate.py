from typing import Optional
from pydantic import BaseModel, Field
from .descriptive_enum import DescriptiveEnum
from .annotation_helper import make_type_annotations


class FormalizationLevel(DescriptiveEnum):
    """Formalization level of the optimization tradition."""
    MATURE_MILP = "mature-MILP", "Mature MILP-based optimization tradition"
    MID_MATURITY_RL_METAHEURISTIC = "mid-maturity-RL-metaheuristic", "Mid-maturity RL or metaheuristic optimization"
    LOW_FORMALIZATION = "low-formalization", "Low-formalization optimization approach"
    NONE = "none", "No optimization tradition present"


class ORSubstrate(BaseModel):
    """OR/optimization substrate characteristics."""
    optimization_tradition_present: bool = Field(
        description="Whether an underlying optimization tradition is present."
    )
    formalization_level: FormalizationLevel = Field(
        description="Formalization level of the optimization tradition." + make_type_annotations(FormalizationLevel)
    )
    solver_type: Optional[str] = Field(
        default=None,
        description="Exact solver name as reported (e.g., Gurobi, COPT, CPLEX). NR if absent."
    )
