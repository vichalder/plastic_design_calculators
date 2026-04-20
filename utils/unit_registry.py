"""Shared pint UnitRegistry singleton for all plastic design notebooks."""
import pint

ureg = pint.UnitRegistry()
ureg.setup_matplotlib()  # enables pint-aware matplotlib axis labels
Q_ = ureg.Quantity


def to_base_si(quantity):
    """Convert a pint Quantity to SI base units (m, Pa, N, s, K).

    Args:
        quantity (pint.Quantity): Any dimensioned quantity.

    Returns:
        pint.Quantity: Same value expressed in SI base units.
    """
    return quantity.to_base_units()


def strip_units(quantity):
    """Extract the SI-base magnitude of a pint Quantity for use in scipy/numpy operations.

    Args:
        quantity (pint.Quantity): Dimensioned value.

    Returns:
        float | numpy.ndarray: Raw numerical magnitude in SI base units.
    """
    return to_base_si(quantity).magnitude


def reattach_units(magnitude, unit_str):
    """Wrap a raw magnitude (returned from scipy/numpy) back into a pint Quantity.

    Args:
        magnitude (float | numpy.ndarray): Raw numerical result.
        unit_str (str): Target pint-compatible unit string (e.g. 'Pa', 'N*m').

    Returns:
        pint.Quantity: Dimensioned quantity.
    """
    return Q_(magnitude, unit_str)
