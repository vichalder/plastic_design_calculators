# Glossary — Design of Plastic Products (Exam Tools)

Every symbol, term, and abbreviation used in E01–E05.

---

## General Mechanics

| Term | Symbol | Unit | Definition |
|------|--------|------|------------|
| Stress | σ | Pa (MPa) | Force per unit area. Tensile stress is positive; compressive stress is negative. |
| Strain | ε | — | Dimensionless deformation: ε = ΔL / L₀. Reported as a fraction or %. |
| Tensile modulus | E | Pa (MPa) | Stiffness in tension: σ = E · ε. Use this (not flexural modulus) for thermal and press-fit calculations. |
| Flexural modulus | E_flex | Pa (MPa) | Stiffness in bending. Used in snap-fit if labelled as "secant modulus" on a datasheet. |
| Secant modulus | E_s | Pa (MPa) | Slope of the stress–strain curve from the origin to the operating strain point. Accounts for nonlinearity at large strains. Always use E_s in snap-fit force calculations. |
| Yield stress | σ_yield | Pa (MPa) | Stress at which permanent deformation begins. Design limit for thermal stress and press-fit initial pressure. |
| Yield strain | ε_yield | — | Strain at yield point: ε_yield = σ_yield / E. Used to set the allowable snap-fit strain. |
| Poisson's ratio | ν | — | Ratio of lateral contraction to axial elongation (0 ≤ ν ≤ 0.5). Used in the Lamé press-fit formula. Typical polymer values: 0.35–0.45. |
| Safety factor | SF | — | SF = limiting value / computed value. SF > 1 means the design passes. |
| Cross-sectional area | A_cross | m² | For a circular rod: A = π d² / 4. |

---

## E01 — Viscoelasticity

### Core concepts

**Viscoelasticity** — Polymer behaviour that combines elastic (spring-like, instantaneous) and viscous (flow-like, time-dependent) responses. Unlike metals, a plastic part under constant load continues to deform over time (creep) and its stiffness decreases.

**Creep** — Progressive increase in strain under constant stress. Relevant for long-term structural applications (press-fits, press-loaded snap-fits, pipe clips).

**Stress relaxation** — Progressive decrease in stress under constant strain. Relevant for seals, press-fits, and clamped joints.

### Creep compliance

| Symbol | Unit | Definition |
|--------|------|------------|
| J(t) | 1/Pa | Creep compliance at time t: how much strain you get per unit stress. J(t) = ε(t) / σ. |
| J₀ | 1/Pa | Instantaneous compliance = 1/E₀ (inverse of the elastic modulus at t → 0). |
| A | 1/(Pa·s^n) | Creep coefficient — controls the magnitude of time-dependent deformation. |
| n | — | Creep exponent — controls the rate of creep (0 < n < 1 for polymers; n = 0 means no creep). |

**Power-law formula:** J(t) = J₀ + A · t^n, where t is in **seconds**.

### Boltzmann Superposition Principle (BSP)

**BSP** — A linearity assumption: the total strain at time t is the sum of strain contributions from every past load increment, each acting independently since it was applied.

$$\varepsilon(t) = \sum_i \Delta\sigma_i \cdot J(t - t_i)$$

| Symbol | Unit | Definition |
|--------|------|------------|
| Δσᵢ | Pa | Stress increment applied at time tᵢ (can be positive or negative). |
| tᵢ | s | Time at which stress increment i was applied. |
| t − tᵢ | s | Elapsed time since step i — the argument passed to J(). |

**Causality rule** — The most common exam error. A load step at tᵢ contributes zero strain for any evaluation time t < tᵢ. The material cannot respond before the load arrives.

### Time–Temperature Superposition (TTS) and WLF

**TTS** — Elevated temperature accelerates polymer chain mobility, making the material creep faster. A period at high temperature is equivalent to a much longer period at the reference temperature.

**WLF equation** (Williams-Landel-Ferry):

$$\log(a_T) = \frac{-C_1 (T - T_\text{ref})}{C_2 + (T - T_\text{ref})}$$

| Symbol | Unit | Definition |
|--------|------|------------|
| a_T | — | WLF shift factor: ratio of relaxation time at T to relaxation time at T_ref. a_T < 1 when T > T_ref (chains move faster). |
| C₁, C₂ | — | WLF material constants. Obtained by fitting shift-factor data. |
| T_ref | °C | Reference temperature for which the creep/relaxation master curve was measured. |
| α_T | — | Shift-factor table value at temperature T (used in the PP_SHIFT_FACTORS lookup). Numerically larger at lower temperatures. |
| α_ref | — | Shift-factor value at T_ref (same table). |

**Reduced / effective time:**

$$t_\text{eff} = \Delta t \cdot \frac{\alpha_\text{ref}}{\alpha_T}$$

The ratio α_ref / α_T > 1 when T > T_ref, meaning real time Δt at the elevated temperature is equivalent to more time at the reference. For a multi-temperature history, sum the contributions: t_eff = Σ Δtᵢ · (α_ref / α_Tᵢ).

**PP_SHIFT_FACTORS** — Pre-computed table of α values for PP at discrete temperatures. If the test temperature is in the table, use the table ratio directly (more accurate than WLF). WLF formula is a fallback for temperatures not in the table.

---

## E02 — Snap-Fit

### Geometry

| Symbol | Unit | Definition |
|--------|------|------------|
| h | m (mm) | Beam thickness at the root (where it joins the wall). The critical cross-section. |
| b | m (mm) | Beam width (perpendicular to bending). |
| L | m (mm) | Effective beam length from root to tip. |
| Y | m (mm) | Required deflection = undercut height. The tip must deflect by Y to pass the retention feature. |
| Q | — | Wall compliance factor. Q = 1 for a rigid wall (default). Q > 1 if the wall itself is flexible and contributes to deflection, which reduces root strain. |

**Y/L ratio** — Beam slenderness check. Classical Euler–Bernoulli beam theory (which the snap-fit formula uses) is valid only when Y/L ≤ 0.20. Above this the beam undergoes geometric nonlinearity.

### Strain

**Root strain (ε_max)** — Maximum fibre strain at the root cross-section when the beam is deflected by Y:

$$\varepsilon_\text{max} = \frac{1.5 \cdot h \cdot Y}{L^2 \cdot Q}$$

**Allowable strain (ε_allow)** — The strain the material can sustain repeatedly without fatigue cracking:

$$\varepsilon_\text{allow} = 0.6 \times \varepsilon_\text{yield}$$

The factor 0.6 accounts for cyclic fatigue reduction. A single-assembly snap-fit can use ε_yield directly. A repeated-assembly snap-fit must use the 0.6 reduction.

**Strain margin** — ε_allow − ε_max. Positive = safe.

### Forces

**Deflection force (Fd)** — Force required to hold the beam at deflection Y:

$$F_d = \frac{b \cdot h^2 \cdot E_s \cdot \varepsilon_\text{max}}{6 \cdot L}$$

E_s is the **secant modulus** at the operating strain — not the initial slope of the stress–strain curve.

**Assembly force (Fa)** — Force to push the mating part past the snap-fit during assembly:

$$F_a = F_d \cdot \frac{\mu + \tan\alpha}{1 - \mu \tan\alpha}$$

**Disassembly force (Fdis)** — Force to separate the assembled joint:

$$F_\text{dis} = F_d \cdot \frac{\mu + \tan\beta}{1 - \mu \tan\beta}$$

| Symbol | Unit | Definition |
|--------|------|------------|
| μ | — | Coefficient of static friction between the snap-fit material and the mating surface (e.g. POM/steel = 0.20). |
| α | ° | Lead-in angle — the angle of the ramp the mating part rides up during assembly. Smaller α → easier to assemble. |
| β | ° | Return (retention) angle — the angle of the shoulder the mating part must overcome during disassembly. Larger β → harder to remove. |
| β_lock | ° | Locking angle: β_lock = arctan(1/μ). At β ≥ β_lock the denominator of the Fdis formula reaches zero — the joint becomes **inseparable** (permanent snap-fit). For POM (μ=0.20): β_lock = 78.7°. |

---

## E03 — Press-Fit

### Geometry and interference

| Symbol | Unit | Definition |
|--------|------|------------|
| δ | m (mm) | **Diametral** interference = D_shaft − D_bore (the total diameter difference, not the radius). |
| D₁ | m (mm) | Bore (shaft) diameter — the inner diameter of the hub after assembly = shaft outer diameter. |
| D₂ | m (mm) | Hub outer diameter. Must be > D₁. |
| δ/D₁ | % | Relative interference. Design limit for unfilled POM: ≤ 3%; glass-filled POM: ≤ 1%. |
| L | m (mm) | Engagement length — axial overlap between hub and shaft. |

**Lamé equations** — Thick-wall cylinder equations relating internal pressure to hoop and radial stress in an elastic cylinder. Used here to relate diametral interference to contact pressure.

**Geometry factor (A):**

$$A = \frac{(D_2/D_1)^2 + 1}{(D_2/D_1)^2 - 1}$$

A > 1 always. A → 1 for a very thick hub (D₂ ≫ D₁); A → ∞ for a thin-walled hub (D₂ → D₁). Swapping D₁ and D₂ gives A < 1, which is wrong — always put outer diameter in the numerator.

### Time-dependent behaviour

**Relaxation modulus Er(t)** — The apparent modulus of a polymer under constant strain, decreasing over time as the polymer relaxes. Given as a 6-point table at standard times (0.01 h to 10 000 h). Interpolated on a **log-log scale** because both time and modulus span decades.

**Log-log interpolation** — `np.interp(log₁₀(t), log₁₀(times_h), log₁₀(Er_Pa))`, then exponentiate the result. More accurate than linear interpolation for modulus data.

**Modulus retention** — Er(t_service) / Er(t=0), expressed as %. Indicates how much stiffness the material retains after relaxation.

**Contact pressure (p(t)):**

$$p(t) = \frac{\delta}{D_1} \cdot \frac{E_r(t)}{A + \nu}$$

As Er decreases with time, p decreases proportionally — the joint loosens.

**Torque capacity (Mt(t)):**

$$M_t(t) = \frac{\pi}{2} \cdot D_1^2 \cdot L \cdot p(t) \cdot \mu$$

Always evaluate torque at **end-of-life** Er (not assembly Er) to find the minimum torque the joint will ever transmit.

---

## E04 — Thermal Expansion

| Symbol | Unit | Definition |
|--------|------|------------|
| α (or CTE) | 1/°C | Coefficient of thermal expansion — fractional length change per degree. Polymers: 50–150 μm/(m·°C). Steel: ~12 μm/(m·°C). |
| ΔT | °C | Temperature change. Positive = heating; negative = cooling. |
| ΔL_free | m (mm) | Free (unconstrained) thermal expansion: ΔL = L · α · ΔT. |
| σ_thermal | Pa (MPa) | Stress in a fully constrained part: σ = E · α · ΔT. Compressive when ΔT > 0 (expansion is prevented). |
| δ_gap | m (mm) | Available clearance gap between the part and its constraint. If δ_gap ≥ ΔL_free, no stress develops. |
| F_constraint | N | Force the constraint exerts on the part when the gap is smaller than the free expansion: F = E · A_cross · (α·ΔT − δ_gap/L). Clamped to zero when gap absorbs all expansion. |
| ΔT_crit | °C | Temperature rise that would bring σ_thermal to yield: ΔT_crit = σ_yield / (E · α). Useful upper bound — exceeding it causes permanent deformation. |

**Differential thermal expansion** — When two materials with different CTEs are bonded or press-fitted, heating causes one to expand more than the other, generating internal stress. For a polymer hub on a steel shaft: the hub expands more (α_polymer > α_steel), which relieves the interference. Effective interference at ΔT: δ_eff = δ₀ − (α_polymer − α_steel) · D₁ · ΔT.

---

## E05 — Material Selection & DFM

### 5-Step Selection Method

| Step | Action |
|------|--------|
| 1 | **Establish demands** — list all operational requirements (temperature, load, environment, regulations). |
| 2 | **Translate to thresholds** — convert each demand into a measurable material property and a numerical limit. |
| 3 | **Qualitative filters** — eliminate materials failing thickness-independent criteria (e.g. FDA approval, chemical resistance). |
| 4 | **Quantitative filters** — eliminate materials failing measurable thresholds (HDT, modulus, impact). |
| 5 | **Final selection** — from the survivors choose the most cost-effective candidate. |

**Boolean AND filter** — All constraints must be satisfied simultaneously (AND logic). A material failing any single criterion is eliminated regardless of how well it performs on others. Using OR logic is the most common exam error.

### Material property terms

| Term | Column | Unit | Definition |
|------|--------|------|------------|
| HDT | HDT_C | °C | Heat Deflection Temperature — temperature at which a standard bar deflects 0.25 mm under a fixed load. Indicates the upper service temperature. HDT ≠ maximum continuous service temperature; apply a safety margin (typically 10–20°C). |
| Tensile modulus | tensile_modulus_MPa | MPa | Stiffness in tension. Use this column (in MPa) when setting E thresholds in E05. |
| Notched Izod | notched_izod_kJ_m2 | kJ/m² | Standard impact test with a notch to concentrate stress. Measures toughness / crack resistance. Higher = more impact resistant. |
| Elongation at yield | elongation_yield_pct | % | Strain at yield point. Important for snap-fits (living hinges need > 20–30%). |
| FDA approval | FDA_approved | bool | Whether the material is approved for food contact. Mandatory filter when the part contacts food or drink. |

### DFM terms

**DFM** (Design for Manufacture) — Design rules that ensure the part can be injection-moulded without defects, warpage, or sink marks.

**Amorphous polymer** — Disordered molecular structure. Examples: PC, ABS, PMMA, PS. Properties: transparent, low shrinkage (0.4–0.8%), lower warpage risk, wider moulding window.

**Semi-crystalline polymer** — Partially ordered molecular structure. Examples: PP, PE, POM, PA66, PEEK. Properties: opaque, higher shrinkage (1.2–2.5%), higher warpage risk, sharper melt transition.

| DFM Parameter | Amorphous | Semi-crystalline |
|---------------|-----------|-----------------|
| Shrinkage | 0.4–0.8% | 1.2–2.5% |
| Warpage risk | LOW | MODERATE–HIGH |
| Draft angle | 0.5–3.0° | 1.0–3.0° (more critical) |
| Rib thickness | ≤ 60% of wall | ≤ 60% of wall |
| Wall variation | ≤ 10% | ≤ 10% |

**Draft angle** — Taper applied to vertical walls so the part releases from the mould without drag marks. Insufficient draft causes ejection damage and surface defects. More critical for semi-crystalline materials because they grip the mould during crystallisation.

**Shrinkage** — Volume reduction as the melt cools and solidifies. The mould cavity is made slightly larger to compensate. Anisotropic shrinkage (different in flow vs cross-flow directions) causes **warpage** in flat parts.

**Rib thickness rule** — A rib thicker than ~60% of the adjacent wall causes a sink mark on the opposite surface. The cooling rate differential creates a depression.

**Wall uniformity rule** — Wall thickness should not vary by more than ~10% between adjacent sections. Abrupt transitions cause differential cooling, internal stress, and warpage.

**Warpage** — Out-of-plane distortion in injection-moulded parts caused by differential shrinkage. More severe in semi-crystalline materials. Mitigated by uniform wall thickness, balanced gate location, and higher mould temperature.

---

## Shared Symbols Quick-Reference

| Symbol | Context | Meaning |
|--------|---------|---------|
| ε | E01, E02 | Strain (dimensionless) |
| σ | E01, E03, E04 | Stress [Pa] |
| E | E02, E03, E04 | Modulus [Pa] |
| μ | E02, E03 | Friction coefficient |
| α | E01 | Shift factor (TTS) |
| α | E04 | CTE [1/°C] |
| A | E01 | Creep coefficient |
| A | E03 | Lamé geometry factor |
| δ | E03 | Diametral interference [m] |
| δ_gap | E04 | Expansion clearance gap [m] |
| ν | E03 | Poisson's ratio |
| D₁ | E03 | Bore / shaft diameter [m] |
| D₂ | E03 | Hub outer diameter [m] |
| L | E02, E03, E04 | Length / engagement length [m] |
| h | E02 | Beam root thickness [m] |
| b | E02 | Beam width [m] |
| Y | E02 | Required beam deflection [m] |
| t | E01, E03 | Time [s or h — check context] |
| T | E01, E04 | Temperature [°C] |
| J(t) | E01 | Creep compliance [1/Pa] |
| Er(t) | E03 | Relaxation modulus [Pa] |
| p(t) | E03 | Contact pressure [Pa] |
| Mt | E03 | Torque capacity [N·m] |
| ΔT | E04 | Temperature change [°C] |
| CTE | E04 | Coefficient of thermal expansion [1/°C] |
