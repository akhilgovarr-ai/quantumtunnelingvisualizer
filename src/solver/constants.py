"""
Physical constants and unit conversion helpers for the solver.

Two modes are supported:
- dimensionless: hbar = 1, m = 1 (used for numerical validation and tests)
- physical: real units in SI-derived quantities, converted internally to
  atomic-like units consistent with the dimensionless grid
"""

# Physical constants (SI)
HBAR_SI = 1.054571817e-34            # J*s
ELECTRON_MASS_SI = 9.1093837015e-31  # kg
EV_TO_JOULE = 1.602176634e-19        # J per eV

# Dimensionless mode defaults
HBAR_DIMENSIONLESS = 1.0
MASS_DIMENSIONLESS = 1.0

def electron_preset():
    """Return parameters for a physical-units electron simulation."""
    return {
        "mass": ELECTRON_MASS_SI,
        "hbar": HBAR_SI,
    }