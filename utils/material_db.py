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
    "ABS": {
        "C1": 14.3,
        "C2": 52.5,
        "T_ref": 100.0,
        "description": "ABS, Tref=Tg=100°C",
    },
    "PA66_dry": {
        "C1": 15.0,
        "C2": 45.0,
        "T_ref": 50.0,
        "description": "PA66 dry, Tref=Tg=50°C",
    },
    "PEEK": {
        "C1": 14.5,
        "C2": 50.2,
        "T_ref": 143.0,
        "description": "PEEK, Tref=Tg=143°C",
    },
    "PPS": {
        "C1": 16.2,
        "C2": 53.1,
        "T_ref": 90.0,
        "description": "PPS, Tref=Tg=90°C",
    },
    "PVC": {
        "C1": 18.5,
        "C2": 45.8,
        "T_ref": 80.0,
        "description": "Rigid PVC, Tref=Tg=80°C",
    },
    "POM": {
        "C1": 17.4,
        "C2": 51.6,
        "T_ref": -60.0,
        "description": "POM, Tref=Tg=-60°C",
    },
    "PE_HD": {
        "C1": 6.0,
        "C2": 150.0,
        "T_ref": 190.0,
        "description": "PE-HD melt, Tref=190°C",
    },
    "PE_LD": {
        "C1": 8.5,
        "C2": 174.0,
        "T_ref": 190.0,
        "description": "PE-LD melt, Tref=190°C",
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
    "ABS": {
        "J0": 4.25e-10,
        "A": 5.0e-11,
        "n": 0.27,
        "description": "ABS, 23°C",
    },
    "PPS_GF40": {
        "J0": 7.2e-11,
        "A": 1.0e-11,
        "n": 0.13,
        "description": "PPS 40% glass-filled, 23°C",
    },
    "PVC": {
        "J0": 3.25e-10,
        "A": 4.0e-11,
        "n": 0.22,
        "description": "Rigid PVC, 23°C",
    },
    "PE_HD": {
        "J0": 1.1e-9,
        "A": 0.018e-9,
        "n": 0.06,
        "description": "PE-HD, 23°C",
    },
    "PE_LD": {
        "J0": 5.0e-9,
        "A": 0.080e-9,
        "n": 0.13,
        "description": "PE-LD, 23°C",
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
    "ABS": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [2.3e9, 2.1e9, 1.95e9, 1.8e9, 1.65e9, 1.5e9],
        "poisson": 0.35,
        "description": "ABS",
    },
    "PA66_dry": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [3.2e9, 2.8e9, 2.5e9, 2.2e9, 1.9e9, 1.6e9],
        "poisson": 0.40,
        "description": "PA66 dry",
    },
    "PEEK": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [4.0e9, 3.9e9, 3.85e9, 3.75e9, 3.65e9, 3.5e9],
        "poisson": 0.38,
        "description": "PEEK",
    },
    "PPS_unfilled": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [3.4e9, 3.3e9, 3.15e9, 3.0e9, 2.85e9, 2.7e9],
        "poisson": 0.37,
        "description": "PPS unfilled",
    },
    "PVC": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [3.3e9, 2.9e9, 2.75e9, 2.6e9, 2.4e9, 2.2e9],
        "poisson": 0.38,
        "description": "Rigid PVC",
    },
    "PE_HD": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [8.0e8, 7.0e8, 6.0e8, 5.0e8, 4.0e8, 3.0e8],
        "poisson": 0.40,
        "description": "PE-HD",
    },
    "PE_LD": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [2.0e8, 1.5e8, 1.3e8, 1.1e8, 9.0e7, 7.0e7],
        "poisson": 0.45,
        "description": "PE-LD",
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
    "POM": {
        "sigma_f_prime_Pa": 90e6,
        "E_Pa": 2_800e6,
        "b": -0.06,
        "epsilon_f_prime": 0.20,
        "c": -0.55,
        "description": "POM (Delrin 100)",
    },
    "PC": {
        "sigma_f_prime_Pa": 100e6,
        "E_Pa": 2_300e6,
        "b": -0.07,
        "epsilon_f_prime": 0.50,
        "c": -0.60,
        "description": "Polycarbonate",
    },
    "ABS": {
        "sigma_f_prime_Pa": 60e6,
        "E_Pa": 2_000e6,
        "b": -0.10,
        "epsilon_f_prime": 0.15,
        "c": -0.55,
        "description": "ABS",
    },
    "PEEK": {
        "sigma_f_prime_Pa": 145e6,
        "E_Pa": 3_700e6,
        "b": -0.05,
        "epsilon_f_prime": 0.28,
        "c": -0.60,
        "description": "PEEK",
    },
    "PPS_GF40": {
        "sigma_f_prime_Pa": 180e6,
        "E_Pa": 14_500e6,
        "b": -0.10,
        "epsilon_f_prime": 0.02,
        "c": -0.60,
        "description": "PPS 40% glass-filled",
    },
    "PVC": {
        "sigma_f_prime_Pa": 70e6,
        "E_Pa": 3_000e6,
        "b": -0.11,
        "epsilon_f_prime": 0.10,
        "c": -0.65,
        "description": "Rigid PVC",
    },
    "PE_HD": {
        "sigma_f_prime_Pa": 55e6,
        "E_Pa": 1_000e6,
        "b": -0.10,
        "epsilon_f_prime": 0.65,
        "c": -0.60,
        "description": "PE-HD",
    },
    "PE_LD": {
        "sigma_f_prime_Pa": 25e6,
        "E_Pa": 300e6,
        "b": -0.12,
        "epsilon_f_prime": 1.5,
        "c": -0.70,
        "description": "PE-LD",
    },
}

# ---------------------------------------------------------------------------
# Friction coefficients (static, polymer-on-steel unless noted)
# ---------------------------------------------------------------------------
FRICTION_COEFFICIENTS = {
    "PP_steel": 0.30,
    "PP_copolymer_steel": 0.30,
    "PE_steel": 0.25,
    "PE_LD_steel": 0.40,
    "PA66_steel": 0.28,
    "POM_steel": 0.20,
    "PC_steel": 0.35,
    "ABS_steel": 0.40,
    "PEEK_steel": 0.35,
    "PPS_steel": 0.45,
    "PVC_steel": 0.55,
}

# ---------------------------------------------------------------------------
# Moulding shrinkage rates (volumetric, dimensionless)
# ---------------------------------------------------------------------------
SHRINKAGE_RATES = {
    "PP":     0.015,
    "PP_copolymer": 0.018,
    "PE_HD":  0.020,
    "PE_LD":  0.025,
    "PA66":   0.012,
    "POM":    0.020,
    "PC":     0.006,
    "ABS":    0.006,
    "PEEK":   0.004,
    "PPS":    0.007,
    "PVC":    0.003,
    "PA66_GF30": 0.006,
}

# ---------------------------------------------------------------------------
# Thermal expansion coefficients [m/(m·°C)] = [1/°C]
# Linear CTE at 23°C unless noted
# ---------------------------------------------------------------------------
THERMAL_EXPANSION = {
    "PVC": {
        "CTE": 70e-6,   # linear CTE [1/°C]
        "description": "Rigid PVC (uPVC), 23°C",
    },
    "PP": {
        "CTE": 90e-6,
        "description": "PP homopolymer, 23°C, Borealis datasheet",
    },
    "POM": {
        "CTE": 110e-6,
        "description": "POM (Delrin 100), 23°C, DuPont datasheet",
    },
    "PC": {
        "CTE": 65e-6,
        "description": "Polycarbonate, 23°C",
    },
    "PA66": {
        "CTE": 80e-6,
        "description": "PA66 dry, 23°C",
    },
    "ABS": {
        "CTE": 90e-6,
        "description": "ABS, 23°C",
    },
    "PA66_GF30": {
        "CTE": 25e-6,
        "description": "PA66 30% glass-filled, longitudinal, 23°C",
    },
    "PEEK_GF30": {
        "CTE": 22e-6,
        "description": "PEEK 30% glass-filled, longitudinal, 23°C",
    },
    "PPS": {
        "CTE": 55e-6,
        "description": "PPS unfilled, 23°C",
    },
    "PE_LD": {
        "CTE": 160e-6,
        "description": "PE-LD, 23°C",
    },
    "PE_HD": {
        "CTE": 150e-6,
        "description": "PE-HD, 23°C",
    },
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
    {"name": "Rigid PVC",        "flexural_modulus_MPa": 3000, "tensile_modulus_MPa": 3000, "HDT_C":  70, "notched_izod_kJ_m2":   5, "elongation_yield_pct":  3, "FDA_approved": False},
]
