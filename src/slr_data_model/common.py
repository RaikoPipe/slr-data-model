"""Shared types and cross-field rules used by all field groups (v0.9.0)."""
from typing import Annotated, Literal, TypeVar

from pydantic import AfterValidator, BeforeValidator

from .descriptive_enum import DescriptiveEnum

T = TypeVar("T")

# A7 (v0.8.0 review): one shared 'not reported' sentinel instead of a mix of None, "NR" strings and ["NR"]
# list items, so the analysis can test `value == NR` instead of string-matching. Also used by the §6 '?'
# convention: uncertainty goes into the sibling _reasoning column, absence of a value is NR.
NR = "NR"
NotReported = Literal["NR"]
_NR_SPELLINGS = {"", "NR", "N/A", "NOT REPORTED", "NONE REPORTED"}


def _to_nr(value):
    if value is None or (isinstance(value, str) and value.strip().upper() in _NR_SPELLINGS):
        return NR
    return value


# Free-text value as reported; None and common NR spellings are normalised to NR.
ReportedStr = Annotated[str, BeforeValidator(_to_nr)]

# A5 (v0.8.0 review): duplicate enum values in multi-selects are dropped (first occurrence wins, order kept
# for JSON). Plain `set[...]` would lose the coder's order and does not round-trip as a JSON array.
UniqueList = Annotated[list[T], AfterValidator(lambda values: list(dict.fromkeys(values)))]

# Free-text lists (e.g. limitations): NR items are dropped, so 'not reported' is always the empty list.
ReportedList = Annotated[list[str], AfterValidator(lambda values: [v for v in values if _to_nr(v) != NR])]


class YesNoUnclear(DescriptiveEnum):
    """A7 (v0.8.0 review): third state for interpretive booleans, so coders are not forced to guess (§6 '?')."""
    YES = "Y", "Clearly stated or clearly the case in the source"
    NO = "N", "Clearly not the case, or searched for and not found"
    UNCLEAR = "unclear", "Source is ambiguous; explain in the sibling _reasoning column"


def _selected(values, value) -> bool:
    if isinstance(values, (list, tuple, set)):
        return value in values
    return values == value


def exclusive(model, field: str, value: DescriptiveEnum) -> None:
    """`value` (e.g. 'none', 'NA') cannot be combined with other values of the multi-select `field`."""
    values = getattr(model, field) or []
    if value in values and len(values) > 1:
        raise ValueError(f"{field}: '{value.value}' cannot be combined with other values")


def require_spec_iff(model, field: str, value: DescriptiveEnum, spec_field: str) -> None:
    """A3 (v0.8.0 review): free-text `spec_field` is required iff `value` (usually 'other') is selected in `field`."""
    selected = _selected(getattr(model, field) or [], value)
    filled = bool((getattr(model, spec_field) or "").strip())
    if selected and not filled:
        raise ValueError(f"{spec_field} is required when '{value.value}' is selected in {field}")
    if filled and not selected:
        raise ValueError(f"{spec_field} must be null unless '{value.value}' is selected in {field}")


def require_iff(model, field: str, condition: bool, reason: str) -> None:
    """`field` must be set (non-null, non-empty) iff `condition` holds."""
    set_ = getattr(model, field) not in (None, [])
    if condition and not set_:
        raise ValueError(f"{field} is required when {reason}")
    if not condition and set_:
        raise ValueError(f"{field} must be null unless {reason}")
