from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .annotation_helper import make_type_annotations, reasoning_field
from .common import ReportedStr, UniqueList, YesNoUnclear, exclusive, require_spec_iff
from .descriptive_enum import DescriptiveEnum


class SubdomainType(DescriptiveEnum):
    """Strategic planning subdomains scoped by the review per §3.3.

    Closed vocabulary on purpose (no 'other'): it doubles as the inclusion gate. A study that fits none of these
    is out of scope and must be rejected at screening, not coded at extraction (v0.8.0 review, B4).
    """
    FACTORY_PLANNING = "factory-planning", "Factory planning per VDI 5200"
    SC_NETWORK_DESIGN = "SC-network-design", "Supply chain network design"
    LOGISTICS_DISTRIBUTION_NETWORK_DESIGN = "logistics-distribution-network-design", "Strategic logistics and distribution network design"
    TECHNOLOGY_SELECTION = "technology-selection", "Technology selection and investment appraisal"
    SITE_SELECTION = "site-selection", "Site selection and facility location"
    GPN_DESIGN = "GPN-design", "Global production network design"


class PlanningTaskType(DescriptiveEnum):
    """Controlled vocabulary for specific planning tasks (§5).

    v0.9.0 (B4): the task 'site-selection' was merged into 'facility-location' (it duplicated the subdomain), and
    'distribution-network-planning' + 'logistics-network-planning' were merged into
    'logistics-distribution-network-planning'. New strategic tasks follow the long-term row of the Supply Chain
    Planning Matrix (Rohde, Meyr & Wagner 2000; Fleischmann, Meyr & Wagner in Stadtler, Kilger & Meyr (eds.),
    Supply Chain Management and Advanced Planning, Springer 2015): sourcing strategy, production-system design,
    capacity footprint, plus resilience and reverse/circular network design.
    """
    REQUIREMENTS_ELICITATION = "requirements-elicitation", "Elicitation of planning requirements"
    LASTENHEFT_GENERATION = "Lastenheft-generation", "Generation of requirements specification (Lastenheft)"
    FACTORY_LAYOUT_PLANNING = "factory-layout-planning", "Factory or facility layout planning"
    CAPACITY_DIMENSIONING = "capacity-dimensioning", "Dimensioning of resources/capacity within one site (machines, staff, area)"
    MATERIAL_FLOW_DESIGN = "material-flow-design", "Material flow design and optimization"
    PRODUCTION_SYSTEM_CONCEPT_DESIGN = "production-system-concept-design", (
        "Concept design of the production system or line (organisation form, process chain, automation level)"
    )
    WAREHOUSE_INTRALOGISTICS_DESIGN = "warehouse-intralogistics-system-design", (
        "Design of warehouse or intralogistics systems (storage, picking, conveying technology)"
    )
    SIMULATION_MODELING = "simulation-modeling", "Simulation modeling for planning"
    SC_NETWORK_CONFIGURATION = "SC-network-configuration", (
        "Multi-echelon supply chain network configuration across suppliers, plants and distribution"
    )
    LOGISTICS_DISTRIBUTION_NETWORK_PLANNING = "logistics-distribution-network-planning", (
        "Design of the downstream logistics/distribution network (warehouses, hubs, transport links)"
    )
    REVERSE_CIRCULAR_NETWORK_DESIGN = "reverse-circular-network-design", (
        "Design of reverse-logistics, remanufacturing or circular-economy networks"
    )
    SUPPLIER_SOURCING_STRATEGY = "supplier-sourcing-network-strategy", (
        "Supplier selection and sourcing-network strategy (single/multi-sourcing, supplier base)"
    )
    FACILITY_LOCATION = "facility-location", "Facility location / site selection"
    CAPACITY_STRATEGY_FOOTPRINT = "capacity-strategy-footprint", (
        "Capacity strategy and production footprint across sites (how much capacity where)"
    )
    GPN_CONFIGURATION = "GPN-configuration", "Global production network configuration"
    MAKE_OR_BUY = "make-or-buy", "Make-or-buy decision"
    TECHNOLOGY_SCOUTING = "technology-scouting", "Technology scouting and identification"
    INVESTMENT_APPRAISAL = "investment-appraisal", "Investment appraisal and evaluation"
    RESILIENCE_RISK_SCENARIO_PLANNING = "resilience-risk-scenario-planning", (
        "Resilience and risk scenario planning for network or system configuration"
    )
    NORM_COMPLIANCE = "norm-compliance", "Norm and standards compliance checking"
    TENDER_EVALUATION = "tender-evaluation", "Tender and bid evaluation"
    OTHER = "other", "Other planning task not covered by standard categories (specify)"


_ANY = frozenset(SubdomainType)
_FP, _SC, _LD = SubdomainType.FACTORY_PLANNING, SubdomainType.SC_NETWORK_DESIGN, SubdomainType.LOGISTICS_DISTRIBUTION_NETWORK_DESIGN
_TS, _SS, _GPN = SubdomainType.TECHNOLOGY_SELECTION, SubdomainType.SITE_SELECTION, SubdomainType.GPN_DESIGN

# B4 (v0.8.0 review): task -> admissible subdomains (Appendix A), checked as a soft consistency flag on
# StudyExtraction. ponytail: drafted from the task definitions above, not copied from protocol Appendix A;
# reconcile with Appendix A before relying on the flag.
TASK_SUBDOMAINS: dict[PlanningTaskType, frozenset[SubdomainType]] = {
    PlanningTaskType.REQUIREMENTS_ELICITATION: _ANY,
    PlanningTaskType.LASTENHEFT_GENERATION: frozenset({_FP, _TS}),
    PlanningTaskType.FACTORY_LAYOUT_PLANNING: frozenset({_FP}),
    PlanningTaskType.CAPACITY_DIMENSIONING: frozenset({_FP, _GPN}),
    PlanningTaskType.MATERIAL_FLOW_DESIGN: frozenset({_FP}),
    PlanningTaskType.PRODUCTION_SYSTEM_CONCEPT_DESIGN: frozenset({_FP}),
    PlanningTaskType.WAREHOUSE_INTRALOGISTICS_DESIGN: frozenset({_FP, _LD}),
    PlanningTaskType.SIMULATION_MODELING: _ANY,
    PlanningTaskType.SC_NETWORK_CONFIGURATION: frozenset({_SC, _GPN}),
    PlanningTaskType.LOGISTICS_DISTRIBUTION_NETWORK_PLANNING: frozenset({_LD, _SC}),
    PlanningTaskType.REVERSE_CIRCULAR_NETWORK_DESIGN: frozenset({_SC, _LD}),
    PlanningTaskType.SUPPLIER_SOURCING_STRATEGY: frozenset({_SC, _GPN}),
    PlanningTaskType.FACILITY_LOCATION: frozenset({_SS, _SC, _LD, _GPN}),
    PlanningTaskType.CAPACITY_STRATEGY_FOOTPRINT: frozenset({_GPN, _SC}),
    PlanningTaskType.GPN_CONFIGURATION: frozenset({_GPN}),
    PlanningTaskType.MAKE_OR_BUY: frozenset({_GPN, _SC, _TS}),
    PlanningTaskType.TECHNOLOGY_SCOUTING: frozenset({_TS}),
    PlanningTaskType.INVESTMENT_APPRAISAL: frozenset({_TS, _SS, _FP}),
    PlanningTaskType.RESILIENCE_RISK_SCENARIO_PLANNING: frozenset({_SC, _GPN, _LD}),
    PlanningTaskType.NORM_COMPLIANCE: _ANY,
    PlanningTaskType.TENDER_EVALUATION: frozenset({_TS, _FP}),
    PlanningTaskType.OTHER: _ANY,
}


class PlanningHorizonTier(DescriptiveEnum):
    """Planning horizon tiers addressed per §3.3 (multi-valued; NA is exclusive)."""
    NA = "NA", "No planning horizon addressed"
    STRATEGIC = "Strategic", "Strategic planning horizon (system configuration: what exists); set iff system_configuring_decision"
    TACTICAL = "Tactical", "Tactical planning horizon (mid-term allocation of existing resources)"
    OPERATIONAL = "Operational", "Operational planning horizon (short-term scheduling and control)"


class TheoreticalFrameworkType(DescriptiveEnum):
    """Theoretical frameworks cited for strategic planning scope per §3.3."""
    VDI_5200 = "VDI-5200", "VDI 5200 factory planning guideline"
    SC_PLANNING_MATRIX = "SC-Planning-Matrix", "Supply Chain Planning Matrix (Fleischmann, Meyr, Wagner)"
    LANZA_ET_AL_2019 = "Lanza-et-al-2019", "Global production network design (Lanza et al., CIRP Annals 2019)"
    WIENDAHL_NYHUIS = "Wiendahl-Nyhuis", "Wiendahl-Nyhuis factory planning framework"
    MELO_NICKEL_SALDANHA_DA_GAMA_2009 = "Melo-Nickel-Saldanha-da-Gama-2009", "Strategic logistics/distribution network design framework (Melo, Nickel, Saldanha-da-Gama 2009)"
    OTHER = "other", (
        "Another planning-domain framework or reference model (e.g., Systematic Layout Planning) that structures "
        "the paper's planning scope (specify)"
    )
    NONE = "none", "No planning-domain framework used to structure the scope"


class SCPProcess(DescriptiveEnum):
    """Process dimension of the Supply Chain Planning Matrix (B4).

    Source: Rohde, Meyr & Wagner (2000), "Die Supply Chain Planning Matrix", PPS Management 5(1); Fleischmann,
    Meyr & Wagner, "Advanced Planning", in Stadtler, Kilger & Meyr (eds.), Supply Chain Management and Advanced
    Planning, Springer 2015. The matrix crosses this process axis with the long/mid/short-term horizon axis,
    which is coded separately in planning_horizon_tiers.
    """
    PROCUREMENT = "procurement", "Procurement / sourcing (suppliers, materials)"
    PRODUCTION = "production", "Production (plants, lines, capacities)"
    DISTRIBUTION = "distribution", "Distribution (warehouses, transport, network to customers)"
    SALES = "sales", "Sales (demand, markets, customer allocation)"
    NA = "NA", "No SCP process addressed (e.g., pure technology selection)"


class VDI5200Phase(DescriptiveEnum):
    """Factory planning phases per VDI 5200 Part 1 (2011), "Fabrikplanung - Planungsvorgehen" (B4).

    Locates *where in the planning process* the LLM is used. 'NA' iff the study is not factory planning.
    """
    SETTING_OBJECTIVES = "1-setting-of-objectives", "Phase 1: Zielfestlegung (setting of objectives)"
    PROJECT_BASIS = "2-project-basis", "Phase 2: Grundlagenermittlung (establishment of the project basis)"
    CONCEPT_PLANNING = "3-concept-planning", "Phase 3: Konzeptplanung (concept planning: structure, dimensioning, layout variants)"
    DETAILED_PLANNING = "4-detailed-planning", "Phase 4: Detailplanung (detailed planning)"
    REALIZATION_PREPARATION = "5-preparation-for-realization", "Phase 5: Realisierungsvorbereitung (preparation for realization, tenders)"
    REALIZATION_SUPERVISION = "6-realization-supervision", "Phase 6: Realisierungsueberwachung (realization supervision)"
    RAMP_UP_SUPPORT = "7-ramp-up-support", "Phase 7: Hochlaufbetreuung (ramp-up support)"
    NA = "NA", "Not a factory planning study"


class StrategicPlanningScope(BaseModel):
    """Strategic planning scope (LLM pre-fill; R1 verifies 100% against source text)."""
    subdomain: UniqueList[SubdomainType] = Field(
        min_length=1,
        description="Strategic planning subdomain(s) addressed. If not stated explicitly, map by task description using Appendix A."
        + make_type_annotations(SubdomainType)
    )
    subdomain_mapping_rationale: str = reasoning_field(
        description="Reasoning for subdomain: how tasks were mapped per Appendix A; document tactical/strategic boundary cases (§6). "
    )
    planning_task_type: UniqueList[PlanningTaskType] = Field(
        min_length=1,
        description="Specific planning task(s) the paper's method performs, pick all applicable. Add 'other' next to "
        "listed values only if a core task of the method is not covered by them; do not add it for side aspects. "
        "Each task's subdomain (Appendix A) should appear in subdomain."
        + make_type_annotations(PlanningTaskType)
    )
    other_planning_task_specification: Optional[str] = Field(
        default=None,
        description="Free-text specification of the planning task. Required if 'other' was selected, otherwise null."
    )
    planning_task_type_reasoning: str = reasoning_field()
    scp_process: UniqueList[SCPProcess] = Field(
        min_length=1,
        description="Process(es) of the Supply Chain Planning Matrix the decision concerns, pick all applicable; "
        "'NA' (exclusive) if none applies." + make_type_annotations(SCPProcess)
    )
    scp_process_reasoning: str = reasoning_field()
    vdi5200_phase: UniqueList[VDI5200Phase] = Field(
        min_length=1,
        description="VDI 5200 factory planning phase(s) the method supports, pick all applicable. Applies only when "
        "'factory-planning' is among the subdomains; 'NA' (exclusive) iff it is not (D034)." + make_type_annotations(VDI5200Phase)
    )
    vdi5200_phase_reasoning: str = reasoning_field()
    time_horizon_explicitly_stated: YesNoUnclear = Field(
        description="Whether the paper explicitly states a time horizon (e.g., '5 years')."
        + make_type_annotations(YesNoUnclear)
    )
    time_horizon_explicitly_stated_reasoning: str = reasoning_field()
    stated_horizon_value: ReportedStr = Field(
        description="The horizon as stated by the authors, verbatim (e.g., '5 years', '2025-2035'). NR if none stated."
    )
    planning_horizon_tiers: UniqueList[PlanningHorizonTier] = Field(
        min_length=1,
        description="Reviewer-judged planning horizon tiers for which the paper's method produces or supports a "
        "decision, pick all applicable; tiers only mentioned as context do not count. 'NA' only if no tier is "
        "addressed. Strategic is selected iff system_configuring_decision is true."
        + make_type_annotations(PlanningHorizonTier)
    )
    planning_horizon_rationale: str = reasoning_field(
        description="Reasoning for planning_horizon_tiers; quote the paper's horizon statement(s) per tier. "
    )
    authors_claimed_tier: UniqueList[PlanningHorizonTier] = Field(
        min_length=1,
        description="Tier(s) the authors themselves claim to address (e.g., 'strategic planning'), regardless of "
        "the reviewer judgement in planning_horizon_tiers. Code a tier only if the paper explicitly uses its label "
        "('strategic', 'tactical', 'operational'); otherwise 'NA', never inferred from the task (D035, D060, D140). Compared with "
        "planning_horizon_tiers in the analysis ('claimed strategic, actually tactical')."
        + make_type_annotations(PlanningHorizonTier)
    )
    authors_claimed_tier_reasoning: str = reasoning_field(
        description="Verbatim quote of the authors' tier claim with locator, or 'no claim found'. "
    )
    system_configuring_decision: bool = Field(
        description="True if a decision the method supports determines what exists in the system (sites, lines, "
        "equipment, network links created or removed; capacities set), as opposed to how existing resources are "
        "used. Judged from the decision itself, regardless of the authors' wording."
    )
    system_configuring_decision_reasoning: str = reasoning_field(interpretive=True)
    system_configuring_decision_stated: bool = Field(
        description="True only if the authors themselves frame the decision as configuring or designing the system "
        "(what exists); a verbatim quote is required in the reasoning. Default False if no such statement exists. "
        "Can only be true if system_configuring_decision is true."
    )
    system_configuring_decision_stated_reasoning: str = reasoning_field(
        description="Verbatim quote of the authors' framing with locator, or 'no statement found'. "
    )
    system_configuring_decision_description: Optional[str] = Field(
        default=None,
        description="Free-text description, if system_configuring_decision is true, of what the decision determines (entities created, capacities set, locations chosen), as reported."
    )
    theoretical_framework_cited: UniqueList[TheoreticalFrameworkType] = Field(
        min_length=1,
        description="Planning-domain framework(s) the paper uses to structure its planning scope. General methods "
        "(MCDM, game theory, V&V principles, prompting techniques) and frameworks only cited as background do "
        "not count; then code 'none'." + make_type_annotations(TheoreticalFrameworkType)
    )
    theoretical_framework_cited_reasoning: str = reasoning_field()
    theoretical_framework_rationale: Optional[str] = Field(
        default=None,
        description="Free-text reasoning why no theoretical framework applies. Required if 'none' was selected, otherwise null."
    )
    other_theoretical_framework_specification: Optional[str] = Field(
        default=None,
        description="Free-text name and citation of the specific framework(s) utilized, not restricted to a controlled vocabulary. Required if 'other' was selected, otherwise null."
    )

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        """Exclusive NA/none values and conditionally required free-text fields."""
        exclusive(self, "planning_horizon_tiers", PlanningHorizonTier.NA)
        exclusive(self, "authors_claimed_tier", PlanningHorizonTier.NA)
        exclusive(self, "scp_process", SCPProcess.NA)
        exclusive(self, "vdi5200_phase", VDI5200Phase.NA)
        exclusive(self, "theoretical_framework_cited", TheoreticalFrameworkType.NONE)
        if self.system_configuring_decision != (PlanningHorizonTier.STRATEGIC in self.planning_horizon_tiers):
            raise ValueError("planning_horizon_tiers must include 'Strategic' iff system_configuring_decision is true")
        if self.system_configuring_decision_stated and not self.system_configuring_decision:
            raise ValueError("system_configuring_decision_stated requires system_configuring_decision")
        if (SubdomainType.FACTORY_PLANNING in self.subdomain) == (VDI5200Phase.NA in self.vdi5200_phase):
            raise ValueError("vdi5200_phase must be 'NA' iff 'factory-planning' is not in subdomain")
        require_spec_iff(self, "planning_task_type", PlanningTaskType.OTHER, "other_planning_task_specification")
        require_spec_iff(self, "theoretical_framework_cited", TheoreticalFrameworkType.NONE, "theoretical_framework_rationale")
        require_spec_iff(self, "theoretical_framework_cited", TheoreticalFrameworkType.OTHER, "other_theoretical_framework_specification")
        return self
