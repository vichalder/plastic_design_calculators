Here is a cheat sheet of the core formulas and concepts required to solve the exam questions, categorized by topic:

### 1. General Injection Molding & Part Design Rules
*   **Viscosity and Melt Flow:** Polymer melts are non-Newtonian, shear-thinning fluids. Their viscosity drops significantly as both **temperature increases** and **shear rate increases**, making the material easier to flow and fill a mold. 
*   **Uniform Wall Thickness:** Wall thickness should always be kept as **uniform as possible** throughout the part. Uneven thickness leads to differential shrinkage, which causes internal voids, sink marks, and warpage.
*   **Gate Location:** Gates should be located at the **thickest wall section**. This allows the melt to flow from thick to thin areas, maintaining packing pressure to compensate for shrinkage and reducing pressure loss.
*   **Stress Concentrations:** **Sharp inner corners must be avoided** because they create high localized stress concentrations. Always use an appropriately large corner radius (fillet) to distribute stress.
*   **Cooling Time:** If the cooling time is set **too short**, the material will not be solid enough to withstand the mechanical force of ejection, leading to prominent **ejector pin marks** or part deformation.

### 2. Snap-Fit Design
Snap-fits act as cantilever beams and are primarily designed based on allowable strain limits. 
*   **Strain ($\epsilon$):** $\epsilon = \frac{3 \cdot Y \cdot h_0}{2 \cdot L^2}$
*   **Deflection ($Y$):** $Y = \frac{2 \cdot L^2 \cdot \epsilon}{3 \cdot h_0}$
*   **Beam Length ($L$):** $L = \sqrt{\frac{3 \cdot Y \cdot h_0}{2 \cdot \epsilon}}$
*   **Beam Thickness ($h_0$):** $h_0 = \frac{2 \cdot L^2 \cdot \epsilon}{3 \cdot Y}$
*   **Repeated Use:** If a snap joint is required to be engaged and disengaged more than once, the beam should be designed to **60% of the recommended strain limit** (remaining strictly in the linear elastic region) to prevent permanent plastic deformation and fatigue.

### 3. Press-Fit Assembly (Shaft & Hub)
Press-fits rely on the interference (U) between a slightly larger shaft and a slightly smaller hub (hole).
*   **Specific Joint Pressure ($p$):** For a metal shaft and a plastic hub, the contact pressure is calculated as $p = \frac{U}{D_1} \cdot E_{r(t)} \cdot \frac{1}{A + \nu}$. 
*   **Geometry Factor ($A$):** $A = \frac{(D_2/D_1)^2 + 1}{(D_2/D_1)^2 - 1}$, where $D_1$ is the inner hub diameter (shaft diameter) and $D_2$ is the outer hub diameter. Poisson's ratio ($\nu$) for plastics is generally $\approx 0.4$.
*   **Maximum Transmissible Axial Force ($F_{max}$):** $F_{max} = \pi \cdot D_1 \cdot L \cdot p \cdot \mu_0$.
*   **Maximum Transmissible Torque ($M_{t\_max}$):** $M_{t\_max} = \pi \cdot \frac{D_1^2}{2} \cdot L \cdot p \cdot \mu_0$.
*   **Relaxation Modulus ($E_R$):** The material's stiffness drops over time under a constant load. For long-term press-fit capabilities (like 1 year/10,000 hours), you must use the time-dependent relaxation modulus ($E_{r(t)}$), which is significantly lower than the short-term modulus.

### 4. Viscoelasticity & Creep
Polymers change their behavior over time and temperature. 
*   **Secant Modulus:** Used to approximate the stress-to-strain relationship at a specific point on the non-linear stress-strain curve: $E_{sec} = \frac{\Delta\sigma}{\Delta\epsilon}$.
*   **Creep Compliance ($J$):** The ratio of time-dependent strain to applied stress. $J(t) = 1 / E(t)$. To convert from $\text{MPa}^{-1}$ to $\text{Pa}^{-1}$, you must divide by $10^6$.
*   **Time-Temperature Superposition (WLF Equation):** High temperatures accelerate viscoelastic behavior. The shift factor ($a_T$) allows you to equate a short time at a high temperature to a long time at a low reference temperature: $\log a_T = -\frac{8.86(T - T_{ref})}{101.6 + T - T_{ref}}$. The effective time is $t_{ref} = t \cdot \frac{\alpha_{T2}}{\alpha_{T1}}$.
*   **Boltzmann Superposition Principle (BSP):** Assumes the effects of individual sequential loads are cumulative. 
    $\epsilon(t) = \sigma_1 \cdot J(t) + (\sigma_2 - \sigma_1) \cdot J(t - t_1) + \dots$
*   **Viscoelastic Recovery:** When a load is removed ($\sigma$ drops to 0), the polymer gradually recovers. Giving the material more time with zero stress decreases the final residual strain.

### 5. Shrinkage & pvT Curves
Volumetric shrinkage is evaluated using pvT (pressure-volume-Temperature) diagrams.
*   **Volumetric Shrinkage ($S_v$):** The relative change in specific volume between the melt state (at gate freeze temperature) and the solid state (at room temperature). $S_v = \frac{v_{melt} - v_{solid}}{v_{melt}}$.
*   **Linear Shrinkage ($S_L$):** Isotropic linear shrinkage is derived from volumetric shrinkage via the equation $S_L = 1 - (1 - S_V)^{1/3}$. A quick approximation is that linear shrinkage is exactly **one-third** of the volumetric shrinkage ($S_L \approx S_V / 3$).

### 6. Integral (Living) Hinges
Living hinges require a very thin, highly oriented section of plastic to survive millions of flexes.
*   **Strain on the Outer Fibers ($\epsilon_b$):** $\epsilon_b = \frac{h}{2} \cdot (\frac{\alpha}{L} - \frac{\alpha+\beta}{L})$.
*   **Thickness Rules:** Increasing the thickness ($h$) of a living hinge drastically **increases the strain** on the outer fibers during bending, which causes premature failure. Ideal hinge thickness is typically very thin, between $0.2 \text{ mm}$ and $0.35 \text{ mm}$.