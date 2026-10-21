# CPW Resonator Design

## Overview

This project studies coplanar waveguide (CPW) transmission lines and quarter-wave resonators for superconducting quantum hardware. It starts with the physics and analytical design equations, then uses Python to explore the design space and, later, electromagnetic simulation to check the analytical estimates.

![Quasi-static electric field of a CPW](docs/figures/cpw_field_lines.png)

## Objectives

- Understand CPW geometry and microwave transmission-line behavior.
- Estimate characteristic impedance, propagation velocity, and resonator dimensions.
- Explore design parameters through Python analysis.
- Compare analytical estimates with electromagnetic simulation.

## Methodology

The work moves from theory and analytical design to Python analysis, visualization, and electromagnetic simulation. The reference design used throughout the docs is a 50 Ω CPW ($w = 10$ µm, $s = 6$ µm) on high-resistivity silicon and a 6 GHz quarter-wave resonator built from it, about 5.0 mm long.

## Tools

Python, NumPy, Matplotlib, and an electromagnetic simulation tool (planned).

## Project Status

In progress. The theory documentation is complete; analysis notebooks and simulation are next.

## Documentation

- [CPW Fundamentals](docs/cpw_fundamentals.md): geometry, field distribution, quasi-TEM propagation, conformal-mapping design equations, materials, and trade-offs.
- [Transmission Line Theory](docs/transmission_line_theory.md): the RLGC model, telegrapher's equations, characteristic impedance, reflections and input impedance, and loss.
- [Quarter-Wave Resonators](docs/quarter_wave_resonators.md): resonance conditions, lumped-element equivalent, quality factors and coupling, hanger measurement, and a worked 6 GHz design.

## Repository layout

```text
cpw-resonator-design/
├── README.md
├── docs/
│   ├── cpw_fundamentals.md
│   ├── transmission_line_theory.md
│   ├── quarter_wave_resonators.md
│   └── figures/                  # generated figures used in the docs
└── scripts/
    └── generate_doc_figures.py   # regenerates all figures and worked-example numbers
```

To regenerate the figures (requires NumPy and Matplotlib):

```bash
python3 cpw-resonator-design/scripts/generate_doc_figures.py
```
