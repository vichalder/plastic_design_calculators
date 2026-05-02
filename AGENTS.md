# AGENTS.md — Plastic Design Calculators

## Project Purpose

This repository is a suite of production-ready Jupyter Notebooks for parametric plastic part design. It covers six engineering domains: viscoelastic creep, living hinges, snap-fits, press-fits, mould design, and material selection. The physics are deliberately viscoelastic — static linear-elastic approximations are prohibited. Every calculation must honour the time- and temperature-dependence of polymer materials.

Intended users: plastic design engineers, materials scientists, and mechanical engineers working on polymer components.

The master architectural specification is [implementation_plan.md](implementation_plan.md). Read it before generating or modifying notebooks. It contains the governing equations, boundary conditions, and all domain-specific formulas.

---

## Repository Layout

```
plastic_design_calculators/
├── 01_viscoelasticity_creep.ipynb   # Creep / stress relaxation (Boltzmann + WLF)
├── 02_living_hinge.ipynb            # Living hinge fatigue life (Coffin-Manson / Basquin)
├── 03_snap_fit.ipynb                # Cantilever snap-fit forces and strain
├── 04_press_fit.ipynb               # Interference fit torque decay (Lamé + E_r(t))
├── 05_mould_design.ipynb            # DFM checks: shrinkage, draft, wall thickness
├── 06_material_selection.ipynb      # 5-step multi-constraint material filtering
├── implementation_plan.md           # Master spec — governing equations, patterns, constraints
├── requirements.txt                 # Python dependencies
└── utils/
    ├── __init__.py                  # Re-exports all public symbols
    ├── unit_registry.py             # Shared pint UnitRegistry singleton
    └── material_db.py               # All material property tables (SI unless noted)
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running Notebooks

```bash
jupyter lab
```

Open any `.ipynb` file and run all cells top-to-bottom. Each notebook is self-contained and accepts user parameters in Part 2.

---

## Tech Stack

| Library | Purpose |
|---|---|
| numpy ≥ 1.21 | Vectorised arrays, log-space time series, matrix ops |
| scipy ≥ 1.7 | Boltzmann integrals, root-finding (`brentq`), interpolation |
| sympy ≥ 1.9 | Symbolic derivation of equations before numerical evaluation |
| pint ≥ 0.18 | Dimensional analysis — every physical variable must carry units |
| matplotlib ≥ 3.4 | Publication-quality plots on logarithmic time axes |
| pandas ≥ 1.3 | Boolean masking of `MATERIAL_DB` in notebook 06 |
| seaborn ≥ 0.11 | Optional statistical overlays |

---

## Mandatory 5-Part Notebook Architecture

Every notebook must follow this exact sequence. Deviations are not permitted.

### Part 1 — Theory and Governing Equations
- Markdown cells only
- LaTeX equations for all governing physics
- Explicit statement of boundary conditions and model assumptions

### Part 2 — Variable Definitions and Unit Handling
- Import `ureg`, `Q_` from `utils`
- Declare every input parameter as a `pint.Quantity`
- Group variables by type: geometry, material properties, environmental conditions

### Part 3 — Computation Engine
- Define modular Python functions with full docstrings (see conventions below)
- Use `sympy` to display equations symbolically before numerical substitution
- Use `numpy`/`scipy` for vectorised computation — no Python `for` loops over large arrays
- Strip units before passing to `scipy`, reattach immediately after (see utils API below)

### Part 4 — Data Visualisation
- Log-scale time axis for all temporal phenomena
- Unit-aware axis labels via pint-matplotlib integration
- Parametric sweeps and sensitivity analyses
- Colour coding: green = safe, orange = warning, red = fail; annotate design points and thresholds

### Part 5 — Design Rule Validation
- Check computed results against design limits and safety factors
- Output a structured PASS/FAIL block in this exact format:

```
═══════════════════════════════════════════════════════════
  DESIGN RULE VALIDATION — [DOMAIN]
═══════════════════════════════════════════════════════════
  [Criterion 1]:
    Computed: <value with units>
    Limit:    <threshold with units>
    Result:   PASS / FAIL
  ...
═══════════════════════════════════════════════════════════
  ✓ OVERALL: DESIGN PASSES all criteria.   (or FAILS)
═══════════════════════════════════════════════════════════
```

---

## utils Module API

Import at the top of every notebook:

```python
from utils import ureg, Q_, to_base_si, strip_units, reattach_units
from utils import material_db
```

### unit_registry.py

| Symbol | Type | Description |
|---|---|---|
| `ureg` | `pint.UnitRegistry` | Shared singleton — never instantiate a second `UnitRegistry` |
| `Q_` | `ureg.Quantity` | Quantity constructor shorthand |
| `to_base_si(q)` | `Quantity → Quantity` | Converts any Quantity to SI base units (m, Pa, N, s, K) |
| `strip_units(q)` | `Quantity → float/ndarray` | Returns SI magnitude only — use before scipy/numpy calls |
| `reattach_units(mag, unit_str)` | `(float, str) → Quantity` | Wraps a raw magnitude back into a Quantity |

Usage pattern for scipy calls:

```python
# Wrap input
E = Q_(2.3e9, 'Pa')
L = Q_(50, 'mm')

# Strip before scipy
E_si = strip_units(E)           # 2.3e9 (float, Pa)
L_si = strip_units(L)           # 0.05  (float, m)

result_raw = scipy_function(E_si, L_si)

# Reattach after scipy
result = reattach_units(result_raw, 'N')
```

Note: `ureg.setup_matplotlib()` is called in `unit_registry.py` — pint-aware axis labels work automatically when you pass Quantities to matplotlib.

---

## material_db.py — Data Structures

All values are in SI unless the key name states otherwise (e.g. `HDT_C` is Celsius, `times_h` is hours).

### `WLF_CONSTANTS`
Williams-Landel-Ferry parameters for time-temperature superposition.

```python
WLF_CONSTANTS = {
    "PC_145": {"C1": 22.87, "C2": 78.09, "T_ref": 145.0, "description": "..."},
    "PP_23":  {"C1": 8.86,  "C2": 101.6, "T_ref": 23.0,  "description": "..."},
}
```

Equation: `log(a_T) = -C1*(T - T_ref) / (C2 + (T - T_ref))`

### `PP_SHIFT_FACTORS`
Pre-computed shift factors for PP at 23 °C reference: `{temperature_°C: alpha_T}`

### `CREEP_COMPLIANCE`
Power-law: `J(t) = J0 + A * t^n` [1/Pa]

```python
CREEP_COMPLIANCE = {
    "PP": {"J0": 1/1_300e6, "A": 2.5e-12, "n": 0.25, "description": "..."},
    ...
}
```

Keys: `"PP"`, `"POM"`, `"PC"`, `"PA66"`, `"PEEK"`

### `RELAXATION_MODULUS`
6-point `(times_h, Er_Pa)` table for interpolation, plus `poisson`.

```python
RELAXATION_MODULUS = {
    "POM_unfilled": {
        "times_h": [0.01, 1, 10, 100, 1000, 10000],
        "Er_Pa":   [3.1e9, 2.4e9, 2.0e9, 1.6e9, 1.2e9, 0.9e9],
        "poisson": 0.38,
        "description": "...",
    },
    ...
}
```

Keys: `"POM_unfilled"`, `"POM_GF30"`, `"PP"`, `"PC"`

### `FATIGUE_COEFFICIENTS`
Coffin-Manson / Basquin: `εa = (σ'f/E)*(2Nf)^b + ε'f*(2Nf)^c`

```python
FATIGUE_COEFFICIENTS = {
    "PP_Hostalen": {
        "sigma_f_prime_Pa": 35e6,
        "E_Pa": 1_300e6,
        "b": -0.10,
        "epsilon_f_prime": 0.45,
        "c": -0.55,
        "description": "...",
    },
    ...
}
```

### `FRICTION_COEFFICIENTS`
Static friction, polymer-on-steel: `{"PP_steel": 0.30, ...}`

### `SHRINKAGE_RATES`
Volumetric shrinkage (dimensionless): `{"PP": 0.015, ...}`

### `MATERIAL_DB`
List of dicts used by `06_material_selection.ipynb`. Required fields:

| Key | Type | Unit |
|---|---|---|
| `name` | `str` | — |
| `flexural_modulus_MPa` | `float` | MPa |
| `tensile_modulus_MPa` | `float` | MPa |
| `HDT_C` | `float` | °C |
| `notched_izod_kJ_m2` | `float` | kJ/m² |
| `elongation_yield_pct` | `float` | % |
| `FDA_approved` | `bool` | — |

---

## Code Conventions

### Function template

```python
def function_name(param1, param2, **kwargs):
    """One-line summary.

    Args:
        param1 (pint.Quantity): Description [Pa].
        param2 (float): Description [m].
        **kwargs: Reserved for future extensions.

    Returns:
        pint.Quantity: Description [N].
    """
    # inline comments must cite the physical phenomenon
    pass
```

- All internal computation in SI base units
- User inputs wrapped in `Q_()` in Part 2; never bare floats for physical quantities
- `**kwargs` in every public function for extensibility
- No bare `for` loops over large arrays — use `numpy` vectorised operations
- `scipy.optimize.brentq` for nonlinear root-finding
- `sympy` display of governing equations before numerical substitution

### Notebook naming

Follow the existing prefix pattern: `NN_short_description.ipynb` where `NN` is a zero-padded integer.

---

## Existing Notebooks Summary

| File | Domain | Key Algorithms |
|---|---|---|
| [01_viscoelasticity_creep.ipynb](01_viscoelasticity_creep.ipynb) | Creep & stress relaxation | Boltzmann Superposition Principle, WLF time-temperature superposition, effective reduced time |
| [02_living_hinge.ipynb](02_living_hinge.ipynb) | Living hinge fatigue | Coffin-Manson / Basquin strain-life, geometric optimisation (L=πR), thickness scaling |
| [03_snap_fit.ipynb](03_snap_fit.ipynb) | Cantilever snap-fit | Beam root strain `ε = 1.5·t·Y/L²·Q`, assembly/retention forces, friction geometry |
| [04_press_fit.ipynb](04_press_fit.ipynb) | Interference fit | Modified Lamé thick-wall equations, `E_r(t)` interpolation, torque decay over service life |
| [05_mould_design.ipynb](05_mould_design.ipynb) | Mould DFM | Shrinkage compensation (pvT), draft angle validation, wall uniformity, gate positioning |
| [06_material_selection.ipynb](06_material_selection.ipynb) | Material selection | Boolean pandas filtering of `MATERIAL_DB`, constraint satisfaction matrix |

---

## How to Add a New Notebook

1. Read [implementation_plan.md](implementation_plan.md) — the domain-specific blueprint section for your topic.
2. Name the file `NN_short_description.ipynb` following the existing sequence.
3. Implement all five parts in order (Theory → Variables → Computation → Visualisation → Validation).
4. Import `ureg`, `Q_`, `strip_units`, `reattach_units` from `utils` in Part 2.
5. Pull material constants from `utils.material_db` — do not hardcode property values in the notebook.
6. Define every governing equation with `sympy` and display it in LaTeX before numerical use.
7. Use `numpy.logspace` for time arrays spanning multiple decades.
8. Log-scale the time axis in all temporal plots.
9. Part 5 must output the structured PASS/FAIL block (see architecture section above).
10. Test by running all cells top-to-bottom in a clean kernel.

---

## How to Add a New Material

Edit [utils/material_db.py](utils/material_db.py). Add entries to whichever dicts apply to the material. Not every dict needs an entry — only add data you have from a verified datasheet.

### `MATERIAL_DB` (required for material selection notebook)

```python
{"name": "PEI",
 "flexural_modulus_MPa": 3300,
 "tensile_modulus_MPa": 3000,
 "HDT_C": 200,
 "notched_izod_kJ_m2": 55,
 "elongation_yield_pct": 7,
 "FDA_approved": False},
```

All modulus values in MPa (the column name carries the unit). `HDT_C` in °C. `elongation_yield_pct` as a percentage (e.g. `7` means 7 %).

### `CREEP_COMPLIANCE` (for creep notebook)

```python
"PEI": {
    "J0": 1 / 3_000e6,   # instantaneous compliance = 1/E_instant [1/Pa]
    "A": 5.0e-13,          # creep coefficient [1/(Pa·s^n)]
    "n": 0.18,             # creep exponent [dimensionless]
    "description": "PEI, 23°C",
},
```

### `RELAXATION_MODULUS` (for press-fit notebook)

Provide exactly 6 time points spanning 0.01 h to 10 000 h:

```python
"PEI": {
    "times_h": [0.01, 1, 10, 100, 1000, 10000],
    "Er_Pa":   [3.2e9, 2.7e9, 2.3e9, 1.9e9, 1.5e9, 1.1e9],
    "poisson": 0.36,
    "description": "PEI",
},
```

### `FATIGUE_COEFFICIENTS` (for living hinge / snap-fit fatigue)

```python
"PEI": {
    "sigma_f_prime_Pa": 90e6,      # fatigue strength coefficient [Pa]
    "E_Pa": 3_000e6,               # elastic modulus [Pa]
    "b": -0.09,                    # Basquin exponent [dimensionless, negative]
    "epsilon_f_prime": 0.25,       # fatigue ductility coefficient [dimensionless]
    "c": -0.60,                    # Coffin-Manson exponent [dimensionless, negative]
    "description": "PEI, cyclic loading",
},
```

### `WLF_CONSTANTS` (for time-temperature superposition)

```python
"PEI_200": {
    "C1": 17.5,
    "C2": 90.0,
    "T_ref": 200.0,    # reference temperature [°C]
    "description": "PEI, Tref=200°C",
},
```

### `SHRINKAGE_RATES`

```python
"PEI": 0.005,   # volumetric shrinkage, dimensionless (e.g. 0.005 = 0.5%)
```

### `FRICTION_COEFFICIENTS`

Key format: `"<POLYMER>_steel"` for polymer-on-steel, or `"<POLYMER1>_<POLYMER2>"` for polymer-on-polymer.

```python
"PEI_steel": 0.38,
```

### Checklist before committing a new material

- [ ] Property values sourced from a vendor datasheet or peer-reviewed reference
- [ ] All moduli in Pa (CREEP_COMPLIANCE, RELAXATION_MODULUS, FATIGUE_COEFFICIENTS) — note that `MATERIAL_DB` moduli are intentionally in MPa
- [ ] `description` field populated with grade name and test conditions (temperature, moisture state)
- [ ] Run affected notebooks top-to-bottom to confirm no KeyError or unit mismatch

---

## What NOT to Do

- **Never use a bare float for a physical quantity** — always wrap in `Q_()`.
- **Never instantiate a second `pint.UnitRegistry`** — import the singleton `ureg` from `utils`.
- **Never hardcode material property numbers inside a notebook** — pull from `material_db`.
- **Never use a static Young's modulus for long-term loading** — use `RELAXATION_MODULUS` with time interpolation.
- **Never skip Part 1 or Part 5** — theory and validation are mandatory, not optional.
- **Never use a Python `for` loop over a large time or geometry array** — use `numpy` vectorisation.
- **Never invent a new notebook architecture** — follow the 5-part structure exactly as specified in [implementation_plan.md](implementation_plan.md).
