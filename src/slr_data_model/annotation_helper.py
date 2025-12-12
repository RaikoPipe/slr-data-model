def make_type_annotations(enum) -> str:
    """Generate a description string listing all enum values and their descriptions."""
    return '\n\n' + '\n'.join(f"- {e.value}: {e.description}" for e in enum)