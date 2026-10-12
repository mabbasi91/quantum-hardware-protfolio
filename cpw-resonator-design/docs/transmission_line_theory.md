# CPW Transmission Line Theory

## Introduction to the transmission-line model

A CPW is a distributed electromagnetic structure: a voltage or current disturbance does not appear everywhere along it at once, but propagates at a finite speed. When the cross-section and materials are uniform over the region of interest and the dominant mode is adequately described as quasi-TEM, the three-dimensional field problem can be reduced to a one-dimensional transmission-line model. This reduction is useful for analyzing propagation, reflections, and power flow while retaining the finite travel time that a lumped circuit model omits.

Let \(z\) denote distance along the line, increasing from source toward load, and \(t\) denote time. The line voltage \(V(z,t)\) is the voltage of the center conductor relative to the return conductors at position \(z\); \(I(z,t)\) is the current in the \(+z\) direction on the center conductor, with the corresponding return current flowing on the grounds. In a uniform line, the local voltage and current are related to distributed parameters per unit length. The model is a reduction of Maxwell's equations, not a claim that fields are confined to ideal wires; the CPW field picture and quasi-TEM approximation are introduced in [CPW Fundamentals](cpw_fundamentals.md).

## Distributed circuit parameters

For a small line segment of length \(dz\), the standard linear transmission-line model assigns a series impedance and shunt admittance:

| Parameter | Meaning per unit length | SI units |
|---|---|---|
| \(R'\) | Series resistance of the signal and return-current paths | \(\Omega\,\mathrm{m}^{-1}\) |
| \(L'\) | Series inductance associated with magnetic-field energy and, where relevant, kinetic energy in the conductors | \(\mathrm{H\,m}^{-1}\) |
| \(G'\) | Shunt conductance representing dielectric leakage and dielectric dissipation | \(\mathrm{S\,m}^{-1}\) |
| \(C'\) | Shunt capacitance between signal and return conductors | \(\mathrm{F\,m}^{-1}\) |

The prime indicates a quantity per unit length, not a derivative. Thus a uniform segment of length \(dz\) has series resistance \(R'dz\), series inductance \(L'dz\), shunt conductance \(G'dz\), and shunt capacitance \(C'dz\). \(R'\) and \(G'\) describe dissipative channels in this circuit representation; \(L'\) and \(C'\) describe stored magnetic and electric energy, respectively.

For ideal, lossless conductors and dielectrics, \(R'=G'=0\), while \(L'\) and \(C'\) remain finite. A real line is lossy, and its effective parameters can depend on frequency. Skin and proximity effects change current distributions and conductor loss; superconducting surface impedance and kinetic inductance also vary with frequency, temperature, and material state. Dielectric permittivity and loss can be dispersive. In a simple low-loss dielectric model, dielectric loss is often represented by \(G'\approx\omega C'\tan\delta\), where \(\omega\) is angular frequency and \(\tan\delta\) is the dielectric loss tangent. For a CPW with multiple dielectric regions, the effective shunt loss depends on field participation in each region, so this expression is a simplified representation rather than a universal material law.

## Telegrapher's equations

Use the passive sign convention: current \(I(z,t)\) enters the segment at its \(z\) end in the \(+z\) direction, and voltage is measured from the signal conductor to the return conductors. Over a short segment \(dz\), the series voltage drop is \(R'dz\,I+L'dz\,\partial I/\partial t\). Kirchhoff's voltage law gives, to first order in \(dz\),

\[
V(z,t)-V(z+dz,t)
=R'dz\,I(z,t)+L'dz\,\frac{\partial I(z,t)}{\partial t}.
\]

Dividing by \(dz\) and taking \(dz\to 0\) yields the voltage equation. The shunt current drawn by the segment is \(G'dz\,V+C'dz\,\partial V/\partial t\); current conservation similarly gives the current equation:

\[
\frac{\partial V}{\partial z}
=-R'I-L'\frac{\partial I}{\partial t},
\qquad
\frac{\partial I}{\partial z}
=-G'V-C'\frac{\partial V}{\partial t}.
\]

These are the time-domain telegrapher's equations for a uniform line with parameters that are constant in space and adequately represented by the linear model. The negative signs follow from measuring voltage drop and current flow in the \(+z\) direction: in a passive line, both decrease along a forward-traveling wave when there is attenuation.

Adopt the phasor convention

\[
v(z,t)=\operatorname{Re}\{V(z)e^{+j\omega t}\},
\qquad
i(z,t)=\operatorname{Re}\{I(z)e^{+j\omega t}\},
\]

where \(j=\sqrt{-1}\), \(\omega=2\pi f\) is angular frequency in radians per second, and \(f\) is frequency in hertz. With this convention, a time derivative becomes multiplication by \(+j\omega\), so the phasor equations are

\[
\frac{dV}{dz}=-(R'+j\omega L')I=-Z'I,
\qquad
\frac{dI}{dz}=-(G'+j\omega C')V=-Y'V,
\]

where \(Z'=R'+j\omega L'\) is the series impedance per unit length in \(\Omega/\mathrm{m}\), and \(Y'=G'+j\omega C'\) is the shunt admittance per unit length in \(\mathrm{S}/\mathrm{m}\). For frequency-dependent line parameters, \(Z'\) and \(Y'\) are evaluated at the frequency under consideration.

For a uniform line, \(Z'\) and \(Y'\) do not vary with \(z\). Differentiating the first phasor equation and substituting the second gives

\[
\frac{d^2V}{dz^2}=Z'Y'V.
\]

Differentiating the current equation in the same way gives

\[
\frac{d^2I}{dz^2}=Z'Y'I.
\]

Define the propagation constant \(\gamma\) by

\[
\gamma^2=Z'Y'
=(R'+j\omega L')(G'+j\omega C'),
\qquad
\gamma=\alpha+j\beta.
\]

Then both wave equations take the form \(d^2V/dz^2=\gamma^2V\) and \(d^2I/dz^2=\gamma^2I\). The square-root branch is chosen for a passive line so a forward wave decays, rather than grows, in the direction of propagation. Here \(\alpha\) is the attenuation constant in nepers per metre and \(\beta\) is the phase constant in radians per metre.

## Characteristic impedance

For a forward-traveling solution with the chosen convention, write

\[
V(z)=V^+e^{-\gamma z},
\qquad
I(z)=I^+e^{-\gamma z}.
\]

Substitution into \(dV/dz=-Z'I\) gives \(-\gamma V^+=-Z'I^+\), or \(V^+/I^+=Z'/\gamma\). Since \(\gamma^2=Z'Y'\), the forward-wave voltage-to-current ratio is

\[
Z_0\equiv\frac{V^+}{I^+}
=\frac{Z'}{\gamma}
=\sqrt{\frac{Z'}{Y'}}
=\sqrt{\frac{R'+j\omega L'}{G'+j\omega C'}}.
\]

This is the characteristic impedance of the uniform line. The square-root branch must be consistent with the selected forward-wave propagation constant and passivity. In a lossy line, \(Z_0\) is generally complex. It describes the ratio of forward-wave voltage to current; it is not the DC resistance of the metal. For a wave traveling in the reverse direction, the current sign reverses relative to voltage, so \(I^-=-V^-/Z_0\).

For an ideal lossless line, \(R'=G'=0\), and therefore

\[
Z_0=\sqrt{\frac{j\omega L'}{j\omega C'}}
=\sqrt{\frac{L'}{C'}}.
\]

The units are \(\sqrt{(\mathrm{H/m})/(\mathrm{F/m})}=\Omega\). Physically, this ratio is set by the relative magnetic and electric energy storage per unit length and determines the voltage-current ratio of a traveling wave. In a CPW, geometry and material stack determine the cross-sectional electric and magnetic fields, and therefore \(C'\) and \(L'\). Finite thickness, superconducting kinetic inductance, finite grounds, and dielectric loading can all modify those parameters. CPW-specific conformal-mapping expressions are intentionally left for a focused treatment.

## Propagation constant and wave velocity

The propagation constant \(\gamma=\alpha+j\beta\) separates two effects for a forward wave \(e^{-\gamma z}\): the amplitude decays as \(e^{-\alpha z}\), while the phase changes by \(-\beta z\). Thus \(\alpha\) is attenuation per unit length and \(\beta\) is phase accumulation per unit length. The phase velocity and wavelength are

\[
v_{\mathrm{p}}=\frac{\omega}{\beta},
\qquad
\lambda=\frac{2\pi}{\beta},
\]

where these quantities refer to phase propagation at the frequency of interest. In a dispersive line, phase velocity can vary with frequency and is distinct from group velocity, which describes the propagation of a narrowband envelope.

For a lossless line,

\[
\gamma^2=(j\omega L')(j\omega C')=-\omega^2L'C',
\]

so for positive \(\omega\),

\[
\alpha=0,
\qquad
\beta=\omega\sqrt{L'C'},
\qquad
v_{\mathrm{p}}=\frac{1}{\sqrt{L'C'}},
\qquad
\lambda=\frac{2\pi}{\omega\sqrt{L'C'}}.
\]

The dimensions are consistent: \(L'C'\) has units of \(\mathrm{s^2/m^2}\), so \(1/\sqrt{L'C'}\) is a velocity. These lossless results assume frequency-independent \(L'\) and \(C'\) over the band considered and no radiation or other loss channel outside the model.

For a conventional, nonmagnetic quasi-TEM CPW with negligible kinetic-inductance contribution and weak dispersion, the phase velocity can be written approximately as

\[
v_{\mathrm{p}}\approx\frac{c}{\sqrt{\varepsilon_{\mathrm{eff}}}},
\qquad
\varepsilon_{\mathrm{eff}}\approx c^2L'C',
\]

where \(c=1/\sqrt{\mu_0\varepsilon_0}\) is the speed of light in vacuum, and \(\mu_0\) and \(\varepsilon_0\) are the vacuum permeability and permittivity. This \(\varepsilon_{\mathrm{eff}}\) captures dielectric loading by the substrate and surrounding medium, as described in [CPW Fundamentals](cpw_fundamentals.md). If superconducting kinetic inductance is appreciable, \(L'\) includes that additional inductance: the measured phase velocity still follows the line-model relation \(v_{\mathrm{p}}=1/\sqrt{L'C'}\) in the lossless limit, but the resulting \(c^2L'C'\) is then an effective phase index squared, not solely a dielectric effective permittivity. Dispersion can also make these quantities frequency dependent.

## Loss mechanisms

In the RLGC model, series resistance \(R'\) accounts for conductor dissipation and shunt conductance \(G'\) represents dielectric dissipation or leakage. For a low-loss line satisfying \(R'\ll\omega L'\) and \(G'\ll\omega C'\), a first-order approximation is

\[
\alpha\approx\frac{R'}{2Z_{0,\mathrm{lossless}}}
+\frac{G'Z_{0,\mathrm{lossless}}}{2},
\qquad
Z_{0,\mathrm{lossless}}=\sqrt{\frac{L'}{C'}}.
\]

The first term is conductor attenuation and the second is dielectric attenuation. Each term has units of inverse length. This expression assumes weak loss and uses the real, lossless characteristic impedance; it is not a general formula for a strongly lossy or dispersive structure.

Several physical effects can contribute:

- **Conductor loss:** Finite normal-metal conductivity causes Joule heating. In superconductors, dissipation is governed by the real part of the microwave surface impedance and can arise from quasiparticles, vortices, or other nonidealities. The imaginary part contributes to stored energy and effective inductance, including kinetic inductance; superconductivity does not imply zero microwave attenuation.
- **Dielectric loss:** Lossy substrate and interfacial dielectrics dissipate electric-field energy. In superconducting circuits, amorphous surface or interface layers and two-level-system defects can be important, with their contribution depending on field participation and operating conditions.
- **Radiation and mode conversion:** Bends, discontinuities, finite grounds, transitions, and packaging can radiate power or couple energy into unwanted modes. These effects are not generally represented by the basic two-conductor RLGC model; they may be treated with added equivalent loss terms in a reduced model, but often require a multimode or full-wave analysis.
- **Other device-specific mechanisms:** Substrate conduction, trapped magnetic flux, seams or contacts in a package, and nonequilibrium quasiparticles can add loss beyond the simplest distributed model.

Distributed attenuation reduces the power reaching the end of a line and, in a resonator made from a transmission line, contributes to energy decay. The measured resonator performance also depends on coupling and other internal loss channels; those resonator relations are covered in [Quarter-Wave Resonators](quarter_wave_resonators.md), not derived here.

## Practical design interpretation

The transmission-line parameters summarize how the CPW geometry and materials store and dissipate electromagnetic energy per unit length. In a quasi-static model, \(C'\) follows from the transverse electric-field solution and dielectric properties; the magnetic contribution to \(L'\) follows from the magnetic field and return-current distribution. For superconducting conductors, kinetic inductance may add to the magnetic inductance. Geometry such as center width, slot width, conductor thickness, and ground extent therefore influences \(L'\), \(C'\), and \(R'\), while substrate and interface properties influence \(C'\) and \(G'\). These relationships are coupled: a geometry change can redistribute both electric and magnetic fields, so no single dimension determines impedance or attenuation independently.

Analytical RLGC models are most useful for uniform sections and for identifying trends under stated assumptions. They can become inaccurate when the cross-section is strongly nonuniform, material properties are dispersive, finite ground planes or package boundaries alter fields, conductor thickness and edge shape matter, or radiation and mode conversion are significant. Full-wave electromagnetic simulation is appropriate for those cases and for realistic transitions, couplers, launches, and packages. Simulation results should be checked for mesh and boundary convergence and interpreted using material models appropriate to the superconducting film and dielectrics; a numerical solution does not by itself validate those inputs.

## References

1. D. M. Pozar, *Microwave Engineering*, 4th ed. (John Wiley & Sons, 2011), especially the chapters on transmission-line theory and transmission lines. [Wiley publisher page](https://www.wiley.com/en-us/Microwave+Engineering%2C+4th+Edition-p-9780470631553)
2. G. Ghione and C. U. Naldi, “Coplanar waveguides for MMIC applications: effect of upper shielding, conductor backing, finite-extent ground planes, and line-to-line coupling,” *IEEE Transactions on Microwave Theory and Techniques* **35**, 260–267 (1987). [https://doi.org/10.1109/TMTT.1987.1133637](https://doi.org/10.1109/TMTT.1987.1133637)
3. M. Goano, F. Bertazzi, P. Caravelli, G. Ghione, and T. A. Driscoll, “A general conformal-mapping approach to the optimum electrode design of coplanar waveguides with arbitrary cross section,” *IEEE Transactions on Microwave Theory and Techniques* **49**, 1573–1580 (2001). [https://doi.org/10.1109/22.942569](https://doi.org/10.1109/22.942569)
4. J. Gao, *The Physics of Superconducting Microwave Resonators*, Ph.D. thesis, California Institute of Technology (2008). [CaltechTHESIS record and DOI](https://thesis.caltech.edu/2530/) (DOI: [10.7907/RAT0-VM75](https://doi.org/10.7907/RAT0-VM75))
5. W. Woods et al., “Determining interface dielectric losses in superconducting coplanar-waveguide resonators,” *Physical Review Applied* **12**, 014012 (2019). [https://doi.org/10.1103/PhysRevApplied.12.014012](https://doi.org/10.1103/PhysRevApplied.12.014012)

Publisher or institutional records for the references above were checked while preparing this document. References 2 and 3 concern CPW modeling; reference 5 concerns superconducting CPW dielectric loss. The sources provide general background and do not validate a particular device's parameters or losses.
