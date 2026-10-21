# Quarter-Wave CPW Resonators

## Operating Principle

A quarter-wave ($\lambda/4$) resonator is a section of CPW that is **short-circuited to ground at one end** and **open-circuited at the other**. A wave launched along the line reflects from both ends: the short reflects voltage with $\Gamma = -1$, and the open reflects it with $\Gamma = +1$. At certain frequencies the round-trip phase makes the reflections add constructively, and energy builds up in a standing wave. Those frequencies are the resonances.

The boundary conditions fix the shape of the standing wave:

- At the **shorted end**, the voltage must vanish: a voltage node and a current antinode. The magnetic field, and the inductive energy, is largest here.
- At the **open end**, the current must vanish: a voltage antinode and a current node. The electric field, and the capacitive energy, is largest here.

The shortest line that fits both conditions is one quarter of a wavelength long. This is half the length of a $\lambda/2$ resonator at the same frequency, which is one reason quarter-wave resonators are popular for frequency-multiplexed readout, where many resonators share one chip.

![Hanger-coupled quarter-wave CPW resonator](figures/qw_hanger_layout.png)

*Figure 1. Schematic top view of a quarter-wave CPW resonator in the hanger configuration (gold = metal, white = exposed substrate). The open end runs parallel to a feedline over a coupling length $\ell_c$, where the high voltage gives capacitive coupling. The line is meandered to save area and terminates by merging its center conductor into the ground plane.*

In circuit-QED hardware [6], quarter-wave resonators serve as qubit readout resonators, Purcell filters, and quantum buses. A qubit is usually coupled near the open end (strong electric field) for capacitive coupling, or near the shorted end (strong current) for inductive coupling.

## Resonance Conditions

The transmission-line result in [Transmission Line Theory](transmission_line_theory.md#terminated-lines-reflection-and-input-impedance) gives the input impedance of a lossless shorted line of length $\ell$ seen from its open end:

$$
Z_\mathrm{in} = jZ_0\tan\beta\ell .
$$

Resonance occurs where $Z_\mathrm{in}$ diverges, i.e. where the shorted line looks like an open circuit and can sustain a voltage at the open end with no current flowing into it:

$$
\beta\ell = (2n - 1)\,\frac{\pi}{2},
\qquad n = 1, 2, 3, \ldots
\qquad\Longleftrightarrow\qquad
\ell = (2n - 1)\,\frac{\lambda_n}{4}.
$$

The voltage and current profiles of mode $n$, measuring $z$ from the open end, are

$$
V_n(z) \propto \cos\!\left(\frac{(2n-1)\pi z}{2\ell}\right),
\qquad
I_n(z) \propto \sin\!\left(\frac{(2n-1)\pi z}{2\ell}\right).
$$

![Mode profiles of a quarter-wave resonator](figures/qw_mode_profiles.png)

*Figure 2. Voltage and current standing waves for the first three modes. Every mode has a voltage antinode at the open end and a voltage node at the short, so a quarter-wave resonator has only odd harmonics.*

Only odd multiples of $\lambda/4$ fit the open/short boundary conditions. This sets the harmonic spectrum apart from a $\lambda/2$ resonator (open/open or short/short), which supports every integer harmonic. The absence of a $2f_1$ mode gives a quarter-wave resonator a clean spectrum up to $3f_1$, which helps when other circuit elements operate near twice the fundamental frequency.

## Resonant Frequency

Using $\beta = \omega/v_\mathrm{p}$, the resonance condition gives

$$
f_n = (2n - 1)\,\frac{v_\mathrm{p}}{4\ell} = (2n - 1)\,\frac{c}{4\ell\sqrt{\varepsilon_\mathrm{eff}}},
\qquad
f_1 \equiv f_0 = \frac{c}{4\ell\sqrt{\varepsilon_\mathrm{eff}}} .
$$

### Lumped-element equivalent

Near a single resonance, the resonator behaves like a parallel *RLC* circuit as seen from its open end. Expanding $Z_\mathrm{in}$ around $\omega_0 = 2\pi f_0$ for a line with small attenuation $\alpha$ gives [1]

$$
C = \frac{C'\ell}{2} = \frac{\pi}{4\omega_0 Z_0},
\qquad
L = \frac{1}{\omega_0^2 C} = \frac{4 Z_0}{\pi\omega_0},
\qquad
R = \frac{Z_0}{\alpha\ell}.
$$

The equivalent capacitance is half the total line capacitance, because the voltage varies as a cosine along the line and only its mean-square value stores energy. This equivalent circuit is the standard interface to circuit-QED models: the resonator mode is a harmonic oscillator with $\omega_0 = 1/\sqrt{LC}$, and the coupling to a qubit or feedline can be computed from the lumped $C$ and the coupling capacitance.

### Frequency shifts from loading and kinetic inductance

The bare formula for $f_0$ is a starting point. Several effects shift the actual frequency:

- **Coupling capacitance.** A capacitance $C_c$ at the open end adds to the equivalent $C$, lowering the frequency by approximately $\delta f/f_0 \approx -C_c/(2C)$.
- **Open-end fringing.** The fringing field at the open end of the center conductor acts as a small extra length. This is typically a few micrometers to tens of micrometers, depending on the gap at the end.
- **Kinetic inductance.** With kinetic-inductance fraction $\alpha_k = L_k'/(L_m' + L_k')$, the frequency drops to $f_0\sqrt{1 - \alpha_k}$. Since $L_k$ depends on temperature, this shift varies with temperature too.
- **Bends and meanders.** The effective length of a meander is close to its centerline length, but closely spaced turns couple to each other and shift the frequency slightly.
- **Two-level systems.** A weak, temperature-dependent frequency shift is a standard signature of TLS loss [3, 5].

In practice, the final length is tuned with electromagnetic simulation, and the systematic offset is calibrated from measurements on earlier devices.

## Electrical Length

The **electrical length** of a line is the phase a wave accumulates while traversing it:

$$
\theta = \beta\ell = \frac{2\pi\ell}{\lambda} = \frac{\omega\ell}{v_\mathrm{p}} .
$$

At the fundamental resonance of a quarter-wave resonator, $\theta = \pi/2$ (90°). Away from resonance $\theta$ scales linearly with frequency, so a small frequency change $\delta f$ corresponds to a fractional length change:

$$
\frac{\delta f}{f_0} = -\frac{\delta\ell}{\ell}.
$$

For the 6 GHz example below ($\ell \approx 5$ mm), a 1 MHz frequency step corresponds to $\delta\ell \approx 0.8$ µm. This explains two practical observations:

- Resonators sharing a feedline can be spaced tens of MHz apart with length differences of only tens of micrometers.
- Fabrication variations in $\varepsilon_\mathrm{eff}$ or kinetic inductance at the 0.1 % level shift frequencies by several MHz. Absolute frequency targeting is therefore harder than relative spacing.

## Quality Factors and Coupling

A resonator loses energy through internal mechanisms and through its intentional coupling to the measurement circuit. Each loss channel defines a quality factor $Q = \omega_0 \times (\text{stored energy}) / (\text{power lost})$:

- **Internal quality factor $Q_i$.** Losses in the resonator itself: dielectric (TLS), conductor, radiation, and others. $1/Q_i = \sum_k 1/Q_k$.
- **Coupling (external) quality factor $Q_c$.** Energy leaking into the feedline through the coupling element.
- **Loaded quality factor $Q_l$.** The total, $1/Q_l = 1/Q_i + 1/Q_c$. It sets the linewidth $\kappa/2\pi = f_0/Q_l$.

For a quarter-wave resonator coupled capacitively at its open end, through a capacitance $C_c$, to a feedline of impedance $Z_\mathrm{f}$ that continues in both directions (the hanger geometry), the coupling quality factor is approximately

$$
Q_c \approx \frac{\pi}{2\,\omega_0^2 C_c^2\,Z_\mathrm{f}\,Z_0}.
$$

This follows from converting the series $C_c$ plus the feedline load $Z_\mathrm{f}/2$ into an equivalent parallel resistance across the resonator's $C$. Because $Q_c \propto 1/C_c^2$, small changes in the coupler geometry produce large changes in $Q_c$. For elbow couplers like the one in Figure 1, $C_c$ is distributed, and the coupling also has an inductive component, so $Q_c$ is normally extracted from simulation.

The **coupling regime** is set by the ratio $Q_c/Q_i$:

| Regime | Condition | Typical use |
|---|---|---|
| Over-coupled | $Q_c \ll Q_i$ | Qubit readout: fast response, linewidth set by design ($\kappa \approx \omega_0/Q_c$) |
| Critically coupled | $Q_c = Q_i$ | Maximum power absorbed on resonance |
| Under-coupled | $Q_c \gg Q_i$ | Materials studies: the linewidth reflects internal loss, so $Q_i$ is measured accurately |

### Measuring a hanger resonator

In the hanger configuration, the resonator removes power from the feedline at resonance, producing a dip in transmission. The ideal transmission is

$$
S_{21}(f) = 1 - \frac{Q_l/Q_c}{1 + 2jQ_l\,\dfrac{f - f_0}{f_0}} .
$$

On resonance $S_{21}(f_0) = Q_l/Q_i$, so the dip depth shows the coupling regime directly. In the complex plane, $S_{21}$ traces a circle of diameter $Q_l/Q_c$ that touches the off-resonance point $(1, 0)$.

![Hanger S21 response](figures/s21_hanger_response.png)

*Figure 3. Ideal hanger transmission for three coupling regimes at fixed $Q_i$: magnitude (left), phase (center), and the resonance circle in the complex plane (right). Over-coupled resonators give deep, wide dips; under-coupled resonators give shallow, narrow dips whose width approaches $f_0/Q_i$.*

Real measurements include cable delay, amplitude and phase background, and impedance mismatch around the coupler. The mismatch makes the resonance asymmetric. Standard fitting methods model this with a complex $Q_c$ (or, equivalently, a rotation of the circle) and fit the full complex response, not just the magnitude [2, 4].

## Design Considerations

### Worked design example

Target: a quarter-wave resonator at $f_0 = 6.0$ GHz on high-resistivity silicon, using the 50 Ω geometry from [CPW Fundamentals](cpw_fundamentals.md) ($w = 10$ µm, $s = 6$ µm, $\varepsilon_\mathrm{eff} \approx 6.23$, $v_\mathrm{p} \approx 1.20\times10^8$ m/s).

| Quantity | Formula | Value |
|---|---|---|
| Length | $\ell = v_\mathrm{p}/(4f_0)$ | 5.01 mm |
| Equivalent capacitance | $C = \pi/(4\omega_0 Z_0)$ | 409 fF |
| Equivalent inductance | $L = 4Z_0/(\pi\omega_0)$ | 1.72 nH |
| Coupling capacitance for $Q_c = 10^4$ (readout) | $C_c = \sqrt{\pi/(2\omega_0^2 Q_c Z_\mathrm{f} Z_0)}$ | 6.6 fF |
| Coupling capacitance for $Q_c = 10^5$ (materials) | same | 2.1 fF |
| Frequency with $\alpha_k = 2\,\%$ kinetic inductance | $f_0\sqrt{1 - \alpha_k}$ | 5.94 GHz |
| Pull from $C_c = 2.1$ fF | $-f_0 C_c/(2C)$ | ≈ −15 MHz |

All numbers are reproduced by [`scripts/generate_doc_figures.py`](../scripts/generate_doc_figures.py). The few-femtofarad coupling capacitances show why the coupler is usually a distributed elbow running alongside the feedline rather than a small gap capacitor.

### Layout and fabrication

- **Footprint.** A 5 mm line is meandered to fit on the chip. Keep adjacent meander segments at least a few times $w + 2s$ apart to limit self-coupling. Use rounded bends to avoid current crowding at corners.
- **Ground continuity.** Place air bridges or crossovers across the resonator, especially near bends, to suppress the slotline mode, and bond the ground plane densely to the package.
- **Frequency planning.** Multiplexed resonators on a shared feedline are typically spaced tens of MHz apart, with spacing chosen against expected fabrication scatter. Keep harmonics ($3f_0, 5f_0, \ldots$) and package box modes away from the operating band of other circuit elements.
- **Flux trapping.** Vortices trapped in the film near the resonator cause loss. Magnetic shielding, slow cooldowns, and arrays of small holes in the ground plane reduce their impact.

### Loss and power

- **Geometry and surface loss.** A wider $w$ and $s$ at the same $Z_0$ reduce surface participation and so reduce TLS loss, at the cost of area and stronger coupling to box modes.
- **Power dependence.** TLS loss saturates at high field. $Q_i$ is therefore typically reported at the single-photon level (relevant for qubits) and at high power. The average intracavity photon number of a hanger resonator driven with input power $P_\mathrm{in}$ at the feedline is [7]

  $$
  \langle n \rangle = \frac{2 Q_l^2}{Q_c}\,\frac{P_\mathrm{in}}{\hbar\omega_0^2} .
  $$

  For $f_0 = 6$ GHz, $Q_l = 10^5$, and $Q_c = 2\times10^5$, an input power of −140 dBm at the chip gives $\langle n \rangle \approx 7$.
- **Temperature.** Measurements are normally done well below $T_c/10$ to suppress thermal quasiparticles. A weak, temperature-dependent shift of $f_0$ and $Q_i$ helps separate TLS loss from quasiparticle loss.

### From analytical design to simulation

The analytical model in this project is used to choose the cross-section, length, and coupler target. A typical workflow:

1. Choose $w$ and $s$ for the target $Z_0$ and loss budget ([CPW Fundamentals](cpw_fundamentals.md)).
2. Compute $\ell$ for the target $f_0$ and the $C_c$ needed for the target $Q_c$.
3. Draw the layout (meander, coupler, short), then simulate it to extract $f_0$ and $Q_c$, and adjust length and coupler.
4. Check sensitivity to fabrication tolerances, kinetic inductance, and package modes.
5. Compare against measurement and feed the systematic offsets back into the next design.

## References

1. D. M. Pozar, *Microwave Engineering*, 4th ed. (John Wiley & Sons, 2011), Chapter 6 (microwave resonators). [Wiley publisher page](https://www.wiley.com/en-us/Microwave+Engineering%2C+4th+Edition-p-9780470631553)
2. S. Probst, F. B. Song, P. A. Bushev, A. V. Ustinov, and M. Weides, "Efficient and robust analysis of complex scattering data under noise in microwave resonators," *Review of Scientific Instruments* **86**, 024706 (2015). [https://doi.org/10.1063/1.4907935](https://doi.org/10.1063/1.4907935)
3. C. R. H. McRae, H. Wang, J. Gao, M. R. Vissers, T. Brecht, A. Dunsworth, D. P. Pappas, and J. Mutus, "Materials loss measurements using superconducting microwave resonators," *Review of Scientific Instruments* **91**, 091101 (2020). [https://doi.org/10.1063/5.0017378](https://doi.org/10.1063/5.0017378)
4. M. S. Khalil, M. J. A. Stoutimore, F. C. Wellstood, and K. D. Osborn, "An analysis method for asymmetric resonator transmission applied to superconducting devices," *Journal of Applied Physics* **111**, 054510 (2012). [https://doi.org/10.1063/1.3692073](https://doi.org/10.1063/1.3692073)
5. J. Gao, *The Physics of Superconducting Microwave Resonators*, Ph.D. thesis, California Institute of Technology (2008). [https://doi.org/10.7907/RAT0-VM75](https://doi.org/10.7907/RAT0-VM75)
6. M. Göppl, A. Fragner, M. Baur, R. Bianchetti, S. Filipp, J. M. Fink, P. J. Leek, G. Puebla, L. Steffen, and A. Wallraff, "Coplanar waveguide resonators for circuit quantum electrodynamics," *Journal of Applied Physics* **104**, 113904 (2008). [https://doi.org/10.1063/1.3010859](https://doi.org/10.1063/1.3010859)
7. A. Bruno, G. de Lange, S. Asaad, K. L. van der Enden, N. K. Langford, and L. DiCarlo, "Reducing intrinsic loss in superconducting resonators by surface treatment and deep etching of silicon substrates," *Applied Physics Letters* **106**, 182601 (2015). [https://doi.org/10.1063/1.4919761](https://doi.org/10.1063/1.4919761)
