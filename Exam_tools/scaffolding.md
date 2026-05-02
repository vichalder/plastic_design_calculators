To effectively prepare for your Design of Plastic Products exam, you can leverage the following Jupyter Notebook structure. This framework is designed to handle the multi-layered analysis required for the core topics identified in your past exam summaries.

### At a Glance: Jupyter Notebook Scaffolding

| Exam Category         | Key Formula/Logic                                                                           | Critical Constraint/Data                                                |
| :-------------------- | :------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------- |
| **Viscoelasticity**   | $\\epsilon = \\sigma \\cdot J(t)$ (Creep) or $\\sigma = \\epsilon \\cdot E(t)$ (Relaxation) | Use **Shift Factor ($\\alpha\_T$)** to map high-temp data to ref-temp.  |
| **Snap-Fits**         | $\\epsilon = \\frac{3 \\cdot Y \\cdot h}{2 \\cdot L^2 \\cdot K}$                            | $K=1$ for straight beams. Unfilled POM max $\\epsilon \\approx 6%$.     |
| **Press-Fits**        | $p = \\frac{U}{D} \\cdot E\_{r(t)} \\cdot \\frac{1}{A + \\nu}$                              | Unfilled POM relative interference $U \\le 3%$ ($1%$ for glass-filled). |
| **Thermal Expansion** | $\\Delta l = L \\cdot \\alpha \\cdot \\Delta T$                                             | Prevented expansion causes force $F = E \\cdot \\epsilon \\cdot A$.     |

-----

### Module 1: Viscoelasticity & Superposition Principle

This module handles time-dependent behavior, specifically the **Boltzmann Superposition Principle** for varying load/temperature histories.

  * **Linear Interpolation (Log-Log Scale):** Most plastic data is linear on a log-log plot. Use this for $J(t)$ or $E(t)$ when specific times aren't in your tables.
  * **Time-Temperature Superposition:**
      * **Master Formula:** $t\_{effective} = \\Delta t\_n \\cdot \\frac{\\alpha\_{ref}}{\\alpha\_{T\_n}}$.
      * **Shift Factor ($\\alpha\_T$):** Typically provided via the WLF equation or a material-specific log table.
  * **Implementation Tip:** Create a function to convert "real-world" time steps into "effective time" at your calculation reference temperature (often 23°C or 58°C) before summing them to find the final compliance $J$.

### Module 2: Snap-Fit Mechanical Design

Designed for cantilever beams (both straight and tapered) and circular sections.

  * **The Straight Beam Logic:**
      * **Max Strain:** $\\epsilon = \\frac{3 \\cdot Y \\cdot h}{2 \\cdot L^2}$.
      * **Deflection Force ($F\_d$):** $F\_d = \\frac{B \\cdot h^2 \\cdot E\_s \\cdot \\epsilon}{6 \\cdot L}$ (using Secant Modulus $E\_s$).
  * **The Assembly Dynamics:**
      * **Assembly Force ($F\_a$):** $F\_a = F\_d \\cdot \\frac{\\mu + \\tan\\alpha}{1 - \\mu \\cdot \\tan\\alpha}$.
      * **Disassembly Force:** Substitute assembly angle $\\alpha$ with the retaining angle $\\beta$.
      * **Friction ($\\mu$):** POM-on-plastic typically ranges from 0.20 (low) to 0.30 (high).

### Module 3: Press-Fit & Torque Transmission

This module evaluates the specific joint pressure ($p$) required to transmit torque over a product's lifetime.

  * **Torque Formula:** $M\_{t,max} = \\pi \\cdot \\frac{D\_1^2}{2} \\cdot L \\cdot p \\cdot \\mu$.
  * **Specific Pressure ($p$):** Requires the **Relaxation Modulus** $E\_{r(t)}$ at the end of service life (e.g., 1,000h).
  * **Geometric Factor ($A$):** $A = \\frac{(D\_2/D\_1)^2 + 1}{(D\_2/D\_1)^2 - 1}$.
  * **Critical Decision Point:** If $M\_{t,max}$ is insufficient, you must either increase friction $\\mu$ (via surface treatment), use a stiffer (glass-filled) material, or increase the hub diameter $D\_2$.

### Module 4: General Design Rules & DFM

For written questions on manufacturing, reference these standardized rules:

  * **Uniformity:** Maintain uniform wall thickness to prevent warpage and sink marks.
  * **Draft Angles:** $1.5^\\circ - 3^\\circ$ for amorphous plastics; $0.5^\\circ - 3^\\circ$ for semi-crystalline.
  * **Material Selection:** Follow the **5-Step Method**:
    1.  **Establish Demands** (Operational environment).
    2.  **Translate Demands** (Convert to material properties like HDT).
    3.  **Categorize** (Qualitative, Thickness-independent, Thickness-dependent).
    4.  **Eliminate** candidates failing Category 1 & 2.
    5.  **Final Selection** based on cost-effective thickness for Category 3.

**Would you like me to generate the specific Python code blocks for one of these modules, such as the Press-Fit torque calculator?**
