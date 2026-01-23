def unsafe_divide(a: float, b: float) -> float:
    # Intentionally unsafe (kept for contrast)
    return a / b


def safe_divide(a: float, b: float):
    """
    Supposed to be safe, but currently crashes on division by zero.

    BUG: It delegates to unsafe_divide without checking b == 0.
    """
    return unsafe_divide(a, b)


# Repeated block (very similar) to stress patch precision.
def safe_divide_verbose(a: float, b: float):
    """
    This helper already behaves safely (do not break it).
    """
    if b == 0:
        return None
    return a / b

