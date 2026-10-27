from pydantic import Field


def make_type_annotations(enum) -> str:
    """Generate a description string listing all enum values and their descriptions."""
    return '\n\n Types: ' + '\n'.join(f"- {e.value}: {e.description}" for e in enum)


def reasoning_field(interpretive: bool = False, **kwargs):
    """`<field>_reasoning` column per §4: justification + evidence locator for the sibling value field."""
    description = "Justification + evidence locator (page/section)"
    if interpretive:
        description += " + short verbatim anchor from the source"
    description += (
        ". Note uncertainty ('?' per §6), contradictions, and verifier corrections/flags here."
    )
    # pilot 0.10.1: placeholder reasoning ('...') failed §4 but passed validation; requiring a letter or digit rejects it
    # (so the LLM retries) while short locators like 'p. 3, §2' stay valid
    return Field(description=kwargs.pop("description", "") + description, pattern=r"\w", **kwargs)
