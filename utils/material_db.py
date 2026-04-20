"""Polymer material property database for plastic design calculators.

All moduli are in Pa, temperatures in °C, times in seconds unless noted.
Sources: Basf Ultramid, DuPont Delrin, CAMPUS Plastics, Borealis PP datasheets.
"""

# ---------------------------------------------------------------------------
# WLF constants  {material_key: {"C1": ..., "C2": ..., "T_ref": °C}}
# ---------------------------------------------------------------------------
WLF_CONSTANTS = {
    "PC_145": {
        "C1": 22.87,
        "C2": 78.09,
        "T_ref": 145.0,
        "description": "Polycarbonate, Tref=145°C",
    },
    "PP_23": {
        "C1": 8.86,
        "C2": 101.6,
        "T_ref": 23.0,
        "description": "Polypropylene, Tref=23°C",
    },
}

# ---------------------------------------------------------------------------
# Time-Temperature shift factors for PP @ 23°C reference
# {temperature_°C: alpha_T}
# ---------------------------------------------------------------------------
PP_SHIFT_FACTORS = {
    23: 45306.05,
    40: 80.84544,
    60: 0.674462,
}

# ---------------------------------------------------------------------------
# Creep compliance power-law parameters  J(t) = J0 + A * t^n  [1/Pa]
# J0: instantaneous compliance, A: coefficient, n: exponent
# ---------------------------------------------------------------------------
CREEP_COMPLIANCE = {
    "PP": {
        "J0": 1 / 1_300e6,   # 1/E_instant [1/Pa]
        "A": 2.5e-12,
        "n": 0.25,
        "description": "PP homopolymer, 23°C",
    },
    "POM": {
        "J0": 1 / 2_800e6,
        "A": 8.0e-13,
        "n": 0.22,
        "description": "POM (Delrin 100), 23°C",
    },
    "PC": {
        "J0": 1 / 2_300e6,
        "A": 6.0e-13,
        "n": 0.20,
        "description": "Polycarbonate, 23°C",
    },
    "PA66": {
        "J0": 1 / 3_000e6,
        "A": 9.0e-13,
        "n": 0.28,
        "description": "PA66 dry, 23°C",
    },
    "PEEK": {
        "J0": 1 / 3_700e6,
        "A": 2.0e-13,
        "n": 0.15,
        "description": "PEEK, 23°C",
    },
}

# ---------------------------------------------------------------------------
# Relaxation modulus E_r(t) at discrete times [Pa]
# Provided as (time_hours, modulus_Pa) pairs for interpolation
# ---------------------------------------------------------------------------
RELAXATION_MODULUS = {
    "POM_unfilled": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [3.1e9, 2.4e9, 2.0e9, 1.6e9, 1.2e9, 0.9e9],
        "poisson": 0.38,
        "description": "POM unfilled",
    },
    "POM_GF30": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [8.5e9, 7.2e9, 6.5e9, 6.0e9, 5.0e9, 4.5e9],
        "poisson": 0.35,
        "description": "POM 30% glass-filled",
    },
    "PP": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [1.8e9, 1.4e9, 1.1e9, 0.85e9, 0.65e9, 0.50e9],
        "poisson": 0.42,
        "description": "PP homopolymer",
    },
    "PC": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [2.5e9, 2.1e9, 1.9e9, 1.6e9, 1.3e9, 1.0e9],
        "poisson": 0.37,
        "description": "Polycarbonate",
    },
}

# ---------------------------------------------------------------------------
# Fatigue coefficients for Coffin-Manson / Basquin combined model
# εa = (σ'f/E)*(2Nf)^b + ε'f*(2Nf)^c
# ---------------------------------------------------------------------------
FATIGUE_COEFFICIENTS = {
    "PP_Hostalen": {
        "sigma_f_prime_Pa": 35e6,
        "E_Pa": 1_300e6,
        "b": -0.10,
        "epsilon_f_prime": 0.45,
        "c": -0.55,
        "description": "PP Hostalen PPR 1042, living hinge fatigue",
    },
    "PA66_GF30": {
        "sigma_f_prime_Pa": 120e6,
        "E_Pa": 8_500e6,
        "b": -0.09,
        "epsilon_f_prime": 0.15,
        "c": -0.60,
        "description": "PA66 GF30, snap-fit cyclic loading",
    },
}

# ---------------------------------------------------------------------------
# Friction coefficients (static, polymer-on-steel unless noted)
# ---------------------------------------------------------------------------
FRICTION_COEFFICIENTS = {
    "PP_steel": 0.30,
    "PE_steel": 0.25,
    "PA66_steel": 0.28,
    "POM_steel": 0.20,
    "PC_steel": 0.35,
    "ABS_steel": 0.40,
}

# ---------------------------------------------------------------------------
# Moulding shrinkage rates (volumetric, dimensionless)
# ---------------------------------------------------------------------------
SHRINKAGE_RATES = {
    "PP":     0.015,
    "PE_HD":  0.020,
    "PA66":   0.012,
    "POM":    0.020,
    "PC":     0.006,
    "ABS":    0.006,
    "PEEK":   0.004,
    "PA66_GF30": 0.006,
}

# ---------------------------------------------------------------------------
# Material selection database — used by 06_material_selection.ipynb
# Property keys: flexural_modulus_MPa, tensile_modulus_MPa, HDT_C,
#                notched_izod_kJ_m2, elongation_yield_pct, FDA_approved
# ---------------------------------------------------------------------------
MATERIAL_DB = [
    {"name": "PP homopolymer",   "flexural_modulus_MPa": 1300, "tensile_modulus_MPa": 1300, "HDT_C":  90, "notched_izod_kJ_m2":  30, "elongation_yield_pct": 10, "FDA_approved": True},
    {"name": "PP copolymer",     "flexural_modulus_MPa":  900, "tensile_modulus_MPa":  900, "HDT_C":  80, "notched_izod_kJ_m2":  50, "elongation_yield_pct": 20, "FDA_approved": True},
    {"name": "PE-HD",            "flexural_modulus_MPa":  900, "tensile_modulus_MPa":  800, "HDT_C":  80, "notched_izod_kJ_m2":  60, "elongation_yield_pct": 20, "FDA_approved": True},
    {"name": "PE-LD",            "flexural_modulus_MPa":  200, "tensile_modulus_MPa":  200, "HDT_C":  45, "notched_izod_kJ_m2": 100, "elongation_yield_pct": 30, "FDA_approved": True},
    {"name": "POM (Delrin)",     "flexural_modulus_MPa": 2600, "tensile_modulus_MPa": 2800, "HDT_C": 110, "notched_izod_kJ_m2":  65, "elongation_yield_pct": 15, "FDA_approved": False},
    {"name": "PC",               "flexural_modulus_MPa": 2300, "tensile_modulus_MPa": 2300, "HDT_C": 130, "notched_izod_kJ_m2":  70, "elongation_yield_pct":  6, "FDA_approved": True},
    {"name": "ABS",              "flexural_modulus_MPa": 2200, "tensile_modulus_MPa": 2000, "HDT_C":  95, "notched_izod_kJ_m2":  20, "elongation_yield_pct":  5, "FDA_approved": False},
    {"name": "PA66 dry",         "flexural_modulus_MPa": 2800, "tensile_modulus_MPa": 3000, "HDT_C": 200, "notched_izod_kJ_m2":  50, "elongation_yield_pct":  5, "FDA_approved": True},
    {"name": "PA66-GF30",        "flexural_modulus_MPa": 7500, "tensile_modulus_MPa": 8500, "HDT_C": 240, "notched_izod_kJ_m2":  80, "elongation_yield_pct":  3, "FDA_approved": True},
    {"name": "PEEK",             "flexural_modulus_MPa": 4100, "tensile_modulus_MPa": 3700, "HDT_C": 260, "notched_izod_kJ_m2":  50, "elongation_yield_pct": 30, "FDA_approved": False},
    {"name": "PEEK-GF30",        "flexural_modulus_MPa": 9500, "tensile_modulus_MPa":10000, "HDT_C": 280, "notched_izod_kJ_m2":  40, "elongation_yield_pct":  2, "FDA_approved": False},
    {"name": "PPS",              "flexural_modulus_MPa": 3800, "tensile_modulus_MPa": 3700, "HDT_C": 260, "notched_izod_kJ_m2":  25, "elongation_yield_pct":  2, "FDA_approved": False},
]
