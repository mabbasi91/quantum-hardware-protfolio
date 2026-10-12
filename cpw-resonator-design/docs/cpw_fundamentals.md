# CPW Fundamentals

## Introduction and motivation

A coplanar waveguide (CPW) is a planar transmission line in which a center conductor and two return conductors lie on the same face of a dielectric substrate. The center strip is separated from each ground plane by a narrow slot. A microwave signal propagates along the line as electromagnetic fields associated with voltage between the center conductor and grounds and current flowing on the conductors.

CPW is widely used in microwave integrated circuits because signal and return conductors are accessible from the same side of the chip. This simplifies planar fabrication, probing, and the placement of shunt elements, and it avoids requiring a continuous backside ground plane for the basic line. In superconducting quantum hardware, CPW structures can form feedlines and resonators and provide a planar way to couple microwave fields to circuit elements. Their field distribution and interfaces also make them useful structures for studying dielectric and surface losses.

Relative to microstrip, CPW can ease same-side component integration and ground access. Microstrip instead places a signal strip above a ground plane on the opposite side of a dielectric, usually concentrating more of its field in the substrate. Neither geometry is universally superior: loss, size, impedance, coupling, and packaging depend on the complete stack-up and operating conditions. CPW can require careful ground continuity and suppression of unwanted slotline-like modes; its fields can interact strongly with exposed surfaces and interfaces, and discontinuities or finite grounds can contribute parasitics and radiation. Other planar lines, such as stripline, can confine fields differently but may require more complex multilayer fabrication and access.

## Physical geometry

The idealized CPW cross-section has a central conducting strip of width \(w\), two slots of width \(s\), and ground planes extending outward on both sides. The conductors are patterned on the top surface of a substrate. In a symmetric CPW, the two slots and surrounding materials are mirror-symmetric about the centerline.

```text
Cross-section (not to scale; x is transverse, z is along the line)

                       center conductor
                         <--- w --->
      left ground                         right ground
   ━━━━━━━━━━━━━━━       ━━━━━━━       ━━━━━━━━━━━━━━━  metal (thickness t)
        width g      <s>             <s>      width g
   ───────────────────────────────────────────────────  substrate
                            thickness h
```

The patterned cross-section is uniform along the propagation direction \(z\): the center strip and grounds continue along the line, separated by the two slots. The substrate extends beneath the conductors and slots. In a real device, the ground planes have finite lateral extent, the metal has finite thickness \(t\), and the substrate may have a backside metallization or additional dielectric and packaging layers.

The principal lateral dimensions are:

- \(w\): center-conductor width.
- \(s\): width of each center-to-ground slot.
- \(g\): lateral width of each ground plane, when the grounds are finite.
- \(h\): substrate thickness.
- \(t\): conductor-film thickness.

The ratios among these dimensions, rather than any one dimension alone, set much of the quasi-static field geometry. For example, changing \(w\) relative to \(s\) changes the electric-field distribution and the balance between center-conductor and ground currents. Increasing the relative extent of the grounds can make the central cross-section more like the idealized infinite-ground model, although package boundaries and backside conductors can still matter. The substrate thickness is relevant when fields reach the backside or interact with a backside ground plane.

## Electromagnetic field distribution

In the usual symmetric CPW mode, the center conductor carries signal current and the two ground planes carry the return current. The center conductor and grounds have different microwave potentials; the slots are therefore regions of strong transverse electric field. The electric field is particularly concentrated near the metal edges. For ideal, perfectly sharp conductors, the local edge field has a mathematical singularity; real edge rounding, finite thickness, and microscopic surface structure regularize it.

The magnetic field circulates around the currents. Its energy is concentrated near the conductors, with field lines encircling the center-strip current and closing through the return-current distribution on the grounds. Current and field crowding near edges can make losses and material-interface participation sensitive to geometry and fabrication details.

The fields are not confined to the substrate. The slots and conductors are exposed to the surrounding medium, commonly vacuum or air in a cryogenic package, so electric-field lines pass partly through the substrate and partly through the space above it. The substrate permittivity changes the field energy and phase velocity; the surrounding dielectric, substrate-air interface, surface oxides, residues, and any package materials can also affect fields and losses. How much field energy lies in each region depends on geometry and the full dielectric stack, not just on the substrate's bulk permittivity.

## Quasi-TEM propagation

TEM means transverse electromagnetic: in an exact TEM wave, both electric and magnetic fields are entirely transverse to the propagation direction, with no longitudinal field components. An ideal TEM transmission line has a cross-section whose transverse field pattern can be described independently of position along the line.

A conventional CPW patterned on a dielectric substrate is generally treated as **quasi-TEM** over a useful range of frequencies. The approximation is often justified when the transverse dimensions are electrically small and the line is sufficiently uniform: the cross-sectional field pattern changes slowly along the propagation direction, and longitudinal field components are small. Quasi-static solutions for the cross-section can then estimate distributed line properties and phase propagation efficiently. This is useful for first-pass design and for understanding trends, but it does not replace a full electromagnetic solution when discontinuities, package boundaries, or higher-order effects matter.

Because the CPW fields occupy both air (or vacuum) and dielectric, the structure is inhomogeneous in the transverse plane. It is therefore not, in general, an exact TEM line with a single uniform dielectric filling. A common quasi-TEM description uses an effective relative permittivity \(\varepsilon_{\mathrm{eff}}\), a dimensionless parameter representing the net effect of the field distribution in the different dielectrics. In this approximation,

\[
v_{\mathrm{p}} \approx \frac{c}{\sqrt{\varepsilon_{\mathrm{eff}}}},
\qquad
\beta \approx \frac{\omega}{c}\sqrt{\varepsilon_{\mathrm{eff}}},
\]

where \(v_{\mathrm{p}}\) is phase velocity, \(c\) is the speed of light in vacuum, \(\beta\) is phase propagation constant, and \(\omega\) is angular frequency. These relations express the approximate slowing of the wave by the dielectric-loaded field; they are not a complete model of dispersion or loss. For a simple isotropic substrate and air above it, quasi-static estimates commonly place \(\varepsilon_{\mathrm{eff}}\) between the relative permittivities of those two regions. That bound should not be applied blindly to multilayer, anisotropic, dispersive, or strongly frequency-dependent structures.

The physical description remains Maxwell's electromagnetic fields and boundary conditions. A transmission-line model is a reduced description that assigns voltage and current to the conductors and represents the line through distributed circuit quantities per unit length. The latter is powerful because it converts propagation along a uniform structure into a one-dimensional model; it is not a claim that the actual fields are confined to a wire or that the CPW is literally a lumped circuit. Detailed line parameters and their derivations are treated in [Transmission Line Theory](transmission_line_theory.md).

## Materials and superconducting implementation

The substrate provides mechanical support and contributes to the electromagnetic boundary-value problem. Its permittivity, dielectric loss, conductivity, anisotropy, thickness, surface condition, and temperature dependence may all matter. High-resistivity silicon and sapphire are common substrates for superconducting circuits; quartz and other materials are used in some microwave applications. These are design options rather than universal recommendations. For example, silicon's suitability depends on resistivity and processing, while sapphire's anisotropy and crystallographic orientation may need consideration. Material grades, surface preparation, and fabrication processes can be as important as the material name.

The patterned conductor defines the signal and return paths. Aluminum and niobium are widely used superconducting films; titanium nitride and niobium-titanium nitride are also used in superconducting microwave devices. Suitability depends on the desired transition temperature, film properties, interface chemistry, process compatibility, and operating regime. Superconductivity suppresses ordinary DC resistance below the transition, but it does not make a microwave device lossless. At finite frequency and temperature, the conductor has a complex surface impedance; its dissipative part produces conductor loss, while its reactive part is associated with stored magnetic energy and kinetic inductance.

Dielectric loss can arise in the substrate and in thin interfacial or surface layers. In superconducting circuits, dielectric defects, including two-level systems in amorphous materials, can absorb microwave energy. Conductive substrates, imperfect superconducting films, trapped magnetic flux, and radiation or package leakage can also contribute to measured loss. The relative importance of these mechanisms depends on temperature, frequency, microwave field amplitude, materials, processing, and geometry. The strong electric fields near CPW edges can make small-volume surface and interface dielectrics relevant, even when their volume is negligible compared with the substrate. Quantifying such participation requires an explicit field model and material-loss assumptions.

## Design trade-offs

The geometrical parameters are coupled: a change to one dimension generally alters field distribution, impedance, current density, and sensitivity to fabrication. Qualitative trends are useful for intuition, but a trend should always be stated with its assumptions.

- **Center width \(w\) and gap width \(s\):** In the standard thin-metal, symmetric, wide-ground quasi-static geometry, increasing the center width relative to the gaps tends to increase capacitance per unit length and reduce characteristic impedance. Narrower gaps strengthen fields in the slots and can increase electric-field participation in nearby interfaces. The precise changes depend on the ratios of dimensions, substrate and package stack, conductor thickness, and ground extent. A smaller gap also makes lithographic bias and edge roughness a larger fraction of the designed dimension.
- **Substrate properties:** A higher-permittivity substrate generally increases dielectric loading and reduces phase velocity for a comparable field geometry. Dielectric loss depends on both the loss properties of each region and the fraction of electric-field energy stored there. Changing substrate thickness, adding a backside ground, or introducing a superstrate can redistribute fields, so bulk permittivity alone does not determine the outcome.
- **Conductor thickness \(t\):** The zero-thickness approximation is useful when thickness is small compared with relevant lateral dimensions, but real thickness changes edge fields and current distribution. Increasing thickness can reduce some conductor-loss contributions in normal-metal models when it approaches or exceeds the relevant current-penetration scale; superconducting surface impedance and kinetic inductance require their own treatment. Thickness effects therefore cannot be inferred from a simple geometric rule alone.
- **Ground extent and layout:** Wider grounds and deliberate ground connections can help approximate the intended return path, but finite grounds, slots, bridges, and package connections can introduce additional modes and parasitic coupling. They also consume chip area and affect routing and fabrication.

These trade-offs motivate keeping the nominal geometry, material stack, and process assumptions explicit. A geometry should be selected against the desired electrical behavior and loss budget, then checked for sensitivity to plausible fabrication variation.

## Limitations of the simplified picture

The ideal CPW model assumes a uniform cross-section, perfectly conducting infinitesimally thin metal, infinite ground planes, and simple dielectric regions. Fabricated quantum hardware departs from several of these assumptions. Finite metal thickness and rounded or trapezoidal etched sidewalls alter fields and current crowding. Finite ground planes, backside metallization, package walls, wirebonds, air bridges, and connectors change return paths and can couple to unwanted modes. Substrate-air, metal-substrate, and metal-air interfaces introduce dielectric regions whose thickness and loss may be small but whose field participation can be consequential.

The quasi-TEM model also neglects or approximates frequency-dependent effects. Material permittivity and conductor surface impedance can be dispersive; superconductors can have frequency- and temperature-dependent response, and kinetic inductance can contribute to the line's distributed inductance. As frequency rises, field patterns may change, radiation and package modes can become relevant, and an effective-permittivity description may no longer capture propagation accurately. Asymmetric grounds can support a slotline-like mode in addition to the intended CPW mode unless the layout and grounding suppress it.

Full-wave electromagnetic simulation becomes important when the structure includes finite grounds or a package, significant thickness or multilayer interfaces, bends and transitions, coupling gaps, ports, air bridges, or possible radiation and mode conversion. It is also useful when losses depend on where fields concentrate in thin dielectric interfaces. A simulation is only as reliable as its geometry, material models, boundary conditions, meshing, and convergence checks; it should complement analytical reasoning and be compared against simpler limits where possible.

## References

1. G. Ghione and C. U. Naldi, “Coplanar waveguides for MMIC applications: effect of upper shielding, conductor backing, finite-extent ground planes, and line-to-line coupling,” *IEEE Transactions on Microwave Theory and Techniques* **35**, 260–267 (1987). [https://doi.org/10.1109/TMTT.1987.1133637](https://doi.org/10.1109/TMTT.1987.1133637)
2. M. Goano, F. Bertazzi, P. Caravelli, G. Ghione, and T. A. Driscoll, “A general conformal-mapping approach to the optimum electrode design of coplanar waveguides with arbitrary cross section,” *IEEE Transactions on Microwave Theory and Techniques* **49**, 1573–1580 (2001). [https://doi.org/10.1109/22.942569](https://doi.org/10.1109/22.942569)
3. J. Gao, *The Physics of Superconducting Microwave Resonators*, Ph.D. thesis, California Institute of Technology (2008). [CaltechTHESIS record](https://thesis.caltech.edu/2530/)
4. W. Woods et al., “Determining interface dielectric losses in superconducting coplanar-waveguide resonators,” *Physical Review Applied* **12**, 014012 (2019). [https://doi.org/10.1103/PhysRevApplied.12.014012](https://doi.org/10.1103/PhysRevApplied.12.014012)
5. W. Chen, D. A. Bennett, V. Patel, and J. E. Lukens, “Substrate and process dependent losses in superconducting thin film resonators,” *Superconductor Science and Technology* **21**, 075013 (2008). [https://doi.org/10.1088/0953-2048/21/7/075013](https://doi.org/10.1088/0953-2048/21/7/075013)

The publisher records for references 1, 2, 4, and 5 and the Caltech thesis record were checked while preparing this document. The references support general CPW modeling and superconducting-resonator loss context; they do not substitute for validating a particular material stack or device design.
