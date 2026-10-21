# CPW Transmission Line Theory

## Introduction to the transmission-line model

A CPW is a *distributed* structure. A voltage or current disturbance does not appear everywhere along it at once; it travels at a finite speed. A lumped circuit model ignores this travel time, which is a good approximation only when the circuit is much smaller than the wavelength. A 6 GHz CPW resonator on silicon is about 5 mm long, a quarter of the guided wavelength, so the travel time matters and the line must be treated as distributed.

When the cross-section and materials are uniform along the line and the dominant mode is quasi-TEM (see [CPW Fundamentals](cpw_fundamentals.md)), the three-dimensional field problem reduces to a one-dimensional **transmission-line model**. This model captures propagation, reflection, and power flow while keeping the finite travel time.

Let $z$ be the position along the line, increasing from source toward load, and $t$ be time. The line voltage $V(z,t)$ is the potential of the center conductor relative to the grounds at position $z$. The line current $I(z,t)$ is the current on the center conductor in the $+z$ direction; an equal and opposite return current flows on the grounds.

## Distributed circuit parameters

A short segment of line, of length $dz$, is modeled by a series impedance and a shunt admittance built from four parameters per unit length:

| Parameter | Physical origin | SI units |
|---|---|---|
| $R'$ | Series resistance of the signal and return paths (conductor loss) | Ω/m |
| $L'$ | Series inductance: magnetic-field energy, plus kinetic inductance in superconductors | H/m |
| $G'$ | Shunt conductance: dielectric loss and leakage | S/m |
| $C'$ | Shunt capacitance between signal and grounds: electric-field energy | F/m |

![Equivalent circuit of a transmission-line segment](figures/rlgc_segment.png)

*Figure 1. Equivalent circuit of a segment of length $dz$. A long line is a cascade of many such segments in the limit $dz \to 0$.*

The prime marks a quantity per unit length; it is not a derivative. $L'$ and $C'$ describe energy *storage* (magnetic and electric); $R'$ and $G'$ describe energy *dissipation*.

For an ideal lossless line, $R' = G' = 0$. Real lines are lossy, and their parameters can depend on frequency. Skin and proximity effects redistribute current in normal metals; in superconductors, the surface impedance and kinetic inductance depend on frequency, temperature, and film quality. For a low-loss dielectric, shunt loss is often written as

$$
G' \approx \omega C' \tan\delta ,
$$

where $\tan\delta$ is the dielectric loss tangent. In a CPW, the field occupies several dielectric regions (substrate, vacuum, thin surface layers), so the effective $\tan\delta$ is a participation-weighted average of each region's loss tangent, not a property of the substrate alone.

## Telegrapher's equations

Apply Kirchhoff's laws to the segment in Figure 1. The voltage drop across the series elements is

$$
V(z,t) - V(z+dz,t) = R'\,dz\,I(z,t) + L'\,dz\,\frac{\partial I(z,t)}{\partial t},
$$

and the current lost through the shunt elements is $G'\,dz\,V + C'\,dz\,\partial V/\partial t$. Dividing by $dz$ and letting $dz \to 0$ gives the **telegrapher's equations**:

$$
\frac{\partial V}{\partial z} = -R' I - L' \frac{\partial I}{\partial t},
\qquad
\frac{\partial I}{\partial z} = -G' V - C' \frac{\partial V}{\partial t}.
$$

The minus signs mean that voltage and current both decrease along the direction of propagation: the series elements drop voltage and the shunt elements draw current away.

For sinusoidal signals, use phasors with the engineering convention

$$
v(z,t) = \mathrm{Re}\{V(z)\,e^{j\omega t}\},
\qquad
i(z,t) = \mathrm{Re}\{I(z)\,e^{j\omega t}\},
$$

where $\omega = 2\pi f$. A time derivative becomes multiplication by $j\omega$, so

$$
\frac{dV}{dz} = -(R' + j\omega L')\,I \equiv -Z' I,
\qquad
\frac{dI}{dz} = -(G' + j\omega C')\,V \equiv -Y' V,
$$

with series impedance per length $Z' = R' + j\omega L'$ and shunt admittance per length $Y' = G' + j\omega C'$. Differentiating one equation and substituting the other gives decoupled wave equations:

$$
\frac{d^2 V}{dz^2} = \gamma^2 V,
\qquad
\frac{d^2 I}{dz^2} = \gamma^2 I,
\qquad
\gamma = \sqrt{(R' + j\omega L')(G' + j\omega C')} = \alpha + j\beta .
$$

$\gamma$ is the **propagation constant**. Its real part $\alpha$ is the attenuation constant (Np/m) and its imaginary part $\beta$ is the phase constant (rad/m). The root is chosen with $\alpha \ge 0$ so that a forward wave decays rather than grows in a passive line.

## Characteristic impedance

The general solution is a superposition of forward and backward waves:

$$
V(z) = V^+ e^{-\gamma z} + V^- e^{+\gamma z},
\qquad
I(z) = \frac{1}{Z_0}\left(V^+ e^{-\gamma z} - V^- e^{+\gamma z}\right).
$$

Substituting the forward wave into $dV/dz = -Z' I$ gives the ratio of voltage to current in a single traveling wave, the **characteristic impedance**:

$$
Z_0 \equiv \frac{V^+}{I^+} = \frac{Z'}{\gamma} = \sqrt{\frac{R' + j\omega L'}{G' + j\omega C'}} .
$$

The backward wave has the opposite sign of current ($I^- = -V^-/Z_0$) because it carries power in the $-z$ direction. $Z_0$ is not a resistance that dissipates power. It is the impedance a wave "sees" as it travels, and the impedance an infinitely long (or perfectly terminated) line presents at its input. For a lossless line,

$$
Z_0 = \sqrt{\frac{L'}{C'}} ,
$$

which is real. $Z_0$ measures the balance between magnetic and electric energy storage: increasing $L'$ (for example, through kinetic inductance) raises $Z_0$; increasing $C'$ (a wider center strip or narrower gaps) lowers it. For a CPW, $L'$ and $C'$ are set by the cross-section; closed-form conformal-mapping expressions are given in [CPW Fundamentals](cpw_fundamentals.md#quasi-static-design-equations).

## Propagation constant and wave velocity

For a forward wave $e^{-\gamma z} = e^{-\alpha z}e^{-j\beta z}$, the amplitude decays as $e^{-\alpha z}$ and the phase advances by $\beta$ per unit length. The phase velocity and guided wavelength are

$$
v_\mathrm{p} = \frac{\omega}{\beta},
\qquad
\lambda = \frac{2\pi}{\beta}.
$$

For a lossless line, $\gamma = j\omega\sqrt{L'C'}$, so

$$
\alpha = 0,
\qquad
\beta = \omega\sqrt{L'C'},
\qquad
v_\mathrm{p} = \frac{1}{\sqrt{L'C'}} .
$$

The phase velocity is independent of frequency, so the line is dispersion-free and the group velocity equals the phase velocity. With frequency-dependent $L'$, $C'$, or significant loss, the two velocities differ.

For a nonmagnetic quasi-TEM CPW with negligible kinetic inductance,

$$
v_\mathrm{p} = \frac{c}{\sqrt{\varepsilon_\mathrm{eff}}},
\qquad
\varepsilon_\mathrm{eff} = c^2 L' C' ,
$$

where $c = 1/\sqrt{\mu_0\varepsilon_0}$. When kinetic inductance is significant, write $L' = L_m' + L_k'$ (magnetic plus kinetic). The phase velocity is still $1/\sqrt{L'C'}$, but it is now lower than $c/\sqrt{\varepsilon_\mathrm{eff}}$ by a factor $\sqrt{1 - \alpha_k}$, where $\alpha_k = L_k'/L'$ is the kinetic-inductance fraction. In that case $c^2 L'C'$ is an effective index squared and no longer a purely dielectric quantity.

**Summary for the reference geometry** ($w = 10$ µm, $s = 6$ µm on silicon, from the worked example in [CPW Fundamentals](cpw_fundamentals.md)): $L' \approx 424$ nH/m, $C' \approx 163$ pF/m, $Z_0 \approx 51$ Ω, and $v_\mathrm{p} \approx 0.40\,c$.

## Terminated lines: reflection and input impedance

A line of characteristic impedance $Z_0$ terminated in a load $Z_L$ at $z = 0$ must satisfy $V(0)/I(0) = Z_L$. A single forward wave cannot satisfy this unless $Z_L = Z_0$, so the load generates a reflected wave. The **reflection coefficient** at the load is

$$
\Gamma_L = \frac{V^-}{V^+} = \frac{Z_L - Z_0}{Z_L + Z_0}.
$$

Three limits are important:

| Termination | $\Gamma_L$ | Behavior at the load |
|---|---|---|
| Matched, $Z_L = Z_0$ | 0 | No reflection; all power absorbed |
| Short circuit, $Z_L = 0$ | −1 | Voltage node, current antinode |
| Open circuit, $Z_L \to \infty$ | +1 | Voltage antinode, current node |

The incident and reflected waves interfere to form a **standing wave**. On a lossless line the voltage magnitude at distance $d$ from the load is $|V(d)| = |V^+|\,|1 + \Gamma_L e^{-2j\beta d}|$. This repeats every half wavelength, with maxima and minima a quarter wavelength apart.

![Standing-wave voltage for several terminations](figures/standing_waves.png)

*Figure 2. Voltage magnitude along a lossless line for several terminations. A short forces a voltage node at the load; one quarter wavelength away the voltage is maximal, so the short looks like an open circuit there.*

Seen from a distance $\ell$ in front of the load, the line plus load presents an **input impedance**

$$
Z_\mathrm{in}(\ell) = Z_0\,\frac{Z_L + Z_0\tanh\gamma\ell}{Z_0 + Z_L\tanh\gamma\ell}
\;\xrightarrow{\ \text{lossless}\ }\;
Z_0\,\frac{Z_L + jZ_0\tan\beta\ell}{Z_0 + jZ_L\tan\beta\ell}.
$$

For short- and open-circuited sections ("stubs") of a lossless line, this reduces to

$$
Z_\mathrm{in}^\mathrm{short} = jZ_0\tan\beta\ell,
\qquad
Z_\mathrm{in}^\mathrm{open} = -jZ_0\cot\beta\ell .
$$

![Input reactance of open and shorted stubs](figures/stub_input_impedance.png)

*Figure 3. Input reactance of lossless shorted and open stubs. A shorted stub behaves like an inductor when short ($\ell < \lambda/4$) and its reactance diverges at $\ell = \lambda/4$. An open stub behaves like a capacitor when short and has a series-resonance zero at $\ell = \lambda/4$.*

The pole of $Z_\mathrm{in}^\mathrm{short}$ at $\beta\ell = \pi/2$ is the key result for this project. A quarter-wavelength section shorted at one end presents an open circuit at the other end. Near that frequency it behaves exactly like a parallel *LC* circuit. This is the **quarter-wave resonator**, analyzed in [Quarter-Wave Resonators](quarter_wave_resonators.md). Two related tools follow from the same equation:

- **Quarter-wave transformer.** For $\beta\ell = \pi/2$, $Z_\mathrm{in} = Z_0^2/Z_L$. A quarter-wave section with $Z_0 = \sqrt{Z_1 Z_2}$ matches two impedances at one frequency.
- **Short stubs as lumped elements.** A shorted stub with $\beta\ell \ll 1$ is an inductor, $L \approx L'\ell$. An open stub is a capacitor, $C \approx C'\ell$. This is how compact on-chip reactances are often made.

## Loss mechanisms

For a low-loss line ($R' \ll \omega L'$ and $G' \ll \omega C'$), expanding $\gamma$ to first order gives

$$
\alpha \approx \underbrace{\frac{R'}{2Z_0}}_{\alpha_c} + \underbrace{\frac{G' Z_0}{2}}_{\alpha_d},
\qquad
Z_0 = \sqrt{L'/C'} ,
$$

with conductor and dielectric contributions $\alpha_c$ and $\alpha_d$. For resonators it is more natural to express loss as a quality factor. A resonator built from a low-loss line, with no other loss channels, has

$$
Q = \frac{\beta}{2\alpha},
\qquad\text{and for dielectric loss alone,}\qquad
Q_d = \frac{1}{\tan\delta}.
$$

With $\tan\delta = 10^{-6}$, a typical value for the participation-weighted loss of a good silicon CPW at low power, $Q_d = 10^6$. This connection between distributed attenuation and resonator $Q$ is what makes CPW resonators sensitive probes of material loss.

Physical contributions to loss include:

- **Conductor loss.** Joule heating in normal metals. In superconductors, loss comes from the real part of the surface impedance, set by thermal or non-equilibrium quasiparticles, vortices, and film defects. Superconductivity does not imply zero microwave loss.
- **Dielectric loss.** Absorption in the substrate and, typically dominant in superconducting devices, in amorphous surface and interface layers that host two-level-system (TLS) defects. TLS loss decreases at high microwave power and higher temperature.
- **Radiation and mode conversion.** Bends, discontinuities, finite grounds, and package cavities can radiate or excite slotline and box modes. The two-conductor RLGC model does not capture these. They can be lumped into an effective loss term but often need full-wave analysis.
- **Other mechanisms.** Substrate conduction, trapped magnetic flux, lossy seams in the package, and infrared or cosmic-ray-generated quasiparticles.

## Practical design interpretation

The RLGC parameters summarize how a given cross-section stores and dissipates energy. Geometry (center width, gap, thickness, ground extent) sets $L'$ and $C'$ through the field distribution, and with it $Z_0$ and $v_\mathrm{p}$. Materials set $R'$ (through the surface impedance), $G'$ (through the participation-weighted loss tangents), and the kinetic part of $L'$. These quantities are coupled: changing the geometry moves both electric and magnetic fields, so no single dimension controls impedance or loss independently.

Analytical RLGC models are best for uniform sections and for identifying trends. They become inaccurate for strongly non-uniform structures, dispersive materials, finite grounds and package boundaries, thick conductors with shaped edges, and situations with radiation or mode conversion. Full-wave simulation is the right tool for these cases and for realistic launches, couplers, bends, and packages. Simulations should be checked for mesh and boundary convergence. They use superconducting and dielectric material models that must themselves be validated against measurement.

## References

1. D. M. Pozar, *Microwave Engineering*, 4th ed. (John Wiley & Sons, 2011), Chapters 2 (transmission-line theory) and 3 (transmission lines and waveguides). [Wiley publisher page](https://www.wiley.com/en-us/Microwave+Engineering%2C+4th+Edition-p-9780470631553)
2. R. N. Simons, *Coplanar Waveguide Circuits, Components, and Systems* (John Wiley & Sons, 2001). [https://doi.org/10.1002/0471224758](https://doi.org/10.1002/0471224758)
3. G. Ghione and C. U. Naldi, "Coplanar waveguides for MMIC applications: effect of upper shielding, conductor backing, finite-extent ground planes, and line-to-line coupling," *IEEE Transactions on Microwave Theory and Techniques* **35**, 260–267 (1987). [https://doi.org/10.1109/TMTT.1987.1133637](https://doi.org/10.1109/TMTT.1987.1133637)
4. J. Gao, *The Physics of Superconducting Microwave Resonators*, Ph.D. thesis, California Institute of Technology (2008). [https://doi.org/10.7907/RAT0-VM75](https://doi.org/10.7907/RAT0-VM75)
5. W. Woods et al., "Determining interface dielectric losses in superconducting coplanar-waveguide resonators," *Physical Review Applied* **12**, 014012 (2019). [https://doi.org/10.1103/PhysRevApplied.12.014012](https://doi.org/10.1103/PhysRevApplied.12.014012)
