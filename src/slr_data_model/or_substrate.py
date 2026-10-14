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
        description="True only if the proposed method itself formulates or solves an optimization/OR problem "
        "(e.g., a MILP, a metaheuristic or RL search, a solver call, or an LLM-generated model that is then "
        "solved). False if optimization appears only in the introduction, related work, or background, or "
        "only as a baseline the method is compared against; note such mentions in the reasoning."
    )
    optimization_tradition_present_reasoning: str = reasoning_field()
    formalization_level: FormalizationLevel = Field(
        description="Formalization level of the optimization the proposed method itself performs; 'none' iff "
        "optimization_tradition_present is false." + make_type_annotations(FormalizationLevel)
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