from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .common import NR, ReportedStr, UniqueList, exclusive, require_iff, require_spec_iff
from .descriptive_enum import DescriptiveEnum


class FormalizationLevel(DescriptiveEnum):
    """Ordinal formalization level of the method's own optimization per §3.5 (kept for the H-tests).

    v0.9.0 (B5): v0.8.0 mixed paradigm and maturity ('mid-maturity-RL-metaheuristic'); the paradigm is now coded
    in optimization_paradigm and this field only grades how formally the problem is stated and solved.
    """
    HIGH = "high", "Explicit mathematical program (variables, objective, constraints) solved exactly or to a bound"
    MEDIUM = "medium", (
        "Explicit objective and constraints, solved by approximate search or scoring (metaheuristic, RL, "
        "simulation-optimization, MCDM)"
    )
    LOW = "low", "Objective/criteria named informally; no formal model"
    NONE = "none", "No optimization tradition present"


class OptimizationParadigm(DescriptiveEnum):
    """Optimization paradigm(s) of the method's own optimization (B5).

    Adds the paradigms common in site, technology and network selection that v0.8.0 lacked: MCDM (AHP: Saaty,
    The Analytic Hierarchy Process, 1980; TOPSIS: Hwang & Yoon, Multiple Attribute Decision Making, 1981),
    simulation-based optimization (Fu, INFORMS J. Computing 14(3), 2002) and stochastic/robust programs.
    """
    MILP_LP = "MILP-LP", "Linear or mixed-integer linear program"
    NLP = "NLP", "Nonlinear (incl. MINLP, quadratic) program"
    CP = "CP", "Constraint programming / SAT"
    STOCHASTIC_ROBUST = "stochastic-robust", "Stochastic, robust or chance-constrained program"
    METAHEURISTIC = "metaheuristic", "Metaheuristic or constructive heuristic (GA, SA, tabu, ...)"
    RL = "RL", "Reinforcement learning"
    MCDM = "MCDM", "Multi-criteria decision making (AHP, TOPSIS, PROMETHEE, ...)"
    SIMULATION_OPTIMIZATION = "simulation-optimization", "Optimization over a simulation model"
    OTHER = "other", "Other paradigm (specify)"


class LLMORRole(DescriptiveEnum):
    """Role of the LLM relative to the optimizer (B5), the main question of the LLM-for-OR literature.

    Roles are synthesised from the LLM4OR surveys (Wang & Li: automatic modeling / auxiliary optimization /
    direct solving; Xiu et al.: model formulation, designers, solution verification; Zhang et al. 2025:
    modeling, stand-alone optimizer, high-level algorithm generation; Liu et al.: LLMaO / LLMaD) plus exemplar
    systems. solver-orchestrator and result-interpreter are top-level categories in none of these surveys;
    they are added because they are common in planning decision support. Further exemplars: NL4Opt
    (Ramamonjison et al., NeurIPS 2022 competition), OptiMUS (AhmadiTeshnizi, Gao & Udell, ICML 2024),
    FunSearch (Romera-Paredes et al., Nature 2024), EoH (Liu et al., ICML 2024).
    """
    # Wang & Li (automatic modeling); Xiu et al. (model formulation); Zhang et al. 2025 (modeling)
    FORMULATOR = "formulator", "Translates natural language into an optimization model or solver code"
    # Liu et al. (LLMaO); Zhang et al. 2025 (stand-alone optimizer); OPRO (Yang et al., ICLR 2024)
    DIRECT_OPTIMIZER = "direct-optimizer", "LLM itself proposes and iteratively improves solutions (OPRO-style)"
    # Liu et al. (LLMaD); Zhang et al. 2025 (high-level algorithm generation); Xiu et al. (designers)
    HEURISTIC_DESIGNER = "heuristic-designer", "LLM designs or evolves algorithms/heuristics that are then run"
    # OR-Toolformer; partly Wang & Li (auxiliary optimization). Not a top-level category in any survey.
    SOLVER_ORCHESTRATOR = "solver-orchestrator", "LLM calls a solver as a tool and handles inputs/outputs"
    # OptiGuide (Li et al. 2023, arXiv:2307.03875). Not a top-level category in any survey.
    RESULT_INTERPRETER = "result-interpreter", "LLM explains solutions or answers what-if questions on them (OptiGuide-style)"
    # Xiu et al. (solution verification)
    VERIFIER = "verifier", "LLM checks models or solutions for errors, feasibility or plausibility"
    NONE = "none", "No optimizer in the method, or the LLM does not interact with it"


class ORSubstrate(BaseModel):
    """OR/optimization substrate characteristics."""
    optimization_tradition_present: bool = Field(
        description="True only if the proposed method itself formulates or solves an optimization/OR problem "
        "(e.g., a MILP, a metaheuristic or RL search, an MCDM ranking, a solver call, or an LLM-generated model "
        "that is then solved). False if optimization appears only in the introduction, related work, or "
        "background, or only as a baseline the method is compared against; note such mentions in the reasoning. An LLM proposing and "
        "refining solutions through its own reasoning (generate-evaluate, reflection or OPRO-style loops) is not "
        "optimization. Ranking alternatives against explicit, weighted criteria computed by the method (MCDM) is, even if "
        "an LLM sets the weights or the authors call the tool exploratory (pilot 0.10.1)."
    )
    optimization_tradition_present_reasoning: str = reasoning_field()
    formalization_level: FormalizationLevel = Field(
        description="Formalization level of the optimization the proposed method itself performs; 'none' iff "
        "optimization_tradition_present is false. 'high' also when the mathematical program is only cited, not printed; "
        "'medium' when explicit criteria or an objective are scored or searched by an algorithm (MCDM, metaheuristic, RL, "
        "simulation-optimization); 'low' when optimization is present but its objective is only informal (pilot 0.10.1)."
        + make_type_annotations(FormalizationLevel)
    )
    formalization_level_reasoning: str = reasoning_field()
    optimization_paradigm: UniqueList[OptimizationParadigm] = Field(
        default_factory=list,
        description="All optimization paradigms the method itself uses; non-empty iff "
        "optimization_tradition_present is true." + make_type_annotations(OptimizationParadigm)
    )
    optimization_paradigm_reasoning: str = reasoning_field()
    other_optimization_paradigm_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the paradigm. Required if 'other' was selected, otherwise null."
    )
    llm_or_role: UniqueList[LLMORRole] = Field(
        min_length=1,
        description="All roles the LLM plays relative to the optimizer, pick all applicable; 'none' (exclusive) if "
        "there is no optimizer or the LLM does not interact with it; must be 'none' if optimization_tradition_present "
        "is false (D075/D079)." + make_type_annotations(LLMORRole)
    )
    llm_or_role_reasoning: str = reasoning_field()
    solver_type: ReportedStr = Field(
        default=NR,
        description="Exact solver name as reported (e.g., Gurobi, COPT, CPLEX). NR if absent."
    )
    solver_type_reasoning: str = reasoning_field()
    optimization_description: Optional[str] = Field(
        default=None,
        description="Free-text description of what is formulated and optimized as reported: decision variables, objective function, constraints."
    )

    @model_validator(mode="after")
    def validate_optimization_present(self):
        """A2 (v0.8.0 review): formalization_level 'none' and an empty paradigm list iff no optimization is present;
        llm_or_role 'none' if no optimization is present (v0.10.0, D075/D079: was only a soft flag)."""
        present = self.optimization_tradition_present
        if present == (self.formalization_level == FormalizationLevel.NONE):
            raise ValueError("formalization_level must be 'none' iff optimization_tradition_present is false")
        require_iff(self, "optimization_paradigm", present, "optimization_tradition_present is true")
        require_spec_iff(self, "optimization_paradigm", OptimizationParadigm.OTHER, "other_optimization_paradigm_specification")
        exclusive(self, "llm_or_role", LLMORRole.NONE)
        if not present and self.llm_or_role != [LLMORRole.NONE]:
            raise ValueError("llm_or_role must be 'none' when optimization_tradition_present is false")
        return self
