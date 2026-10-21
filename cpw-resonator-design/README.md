# CPW Resonator Design

## Overview

This project studies coplanar waveguide (CPW) transmission lines and the half-wave and quarter-wave resonators built from them for superconducting quantum hardware. It starts with the physics and analytical design equations, then uses Python to explore the design space and, later, electromagnetic simulation to check the analytical estimates.

![Quasi-static electric field of a CPW](docs/figures/cpw_field_lines.png)

## Objectives

- Understand CPW geometry and microwave transmission-line behavior.
- Estimate characteristic impedance, propagation velocity, and resonator dimensions.
- Explore design parameters through Python analysis.
- Compare analytical estimates with electromagnetic simulation.

## Methodology

The work moves from theory and analytical design to Python analysis, visualization, and electromagnetic simulation. The reference design used throughout the docs is a 50 Ω CPW ($w = 10$ µm, $s = 6$ µm) on high-resistivity silicon and 6 GHz resonators built from it: a 10.0 mm half-wave and a 5.0 mm quarter-wave design.

## Tools

Python, NumPy, Matplotlib, and an electromagnetic simulation tool (planned).

## Project Status

In progress. The theory documentation is complete; analysis notebooks and simulation are next.

## Documentation

1. [CPW Fundamentals](docs/01_cpw_fundamentals.md): geometry, field distribution, quasi-TEM propagation, conformal-mapping design equations, materials, and trade-offs.
2. [Transmission Line Theory](docs/02_transmission_line_theory.md): the RLGC model, telegrapher's equations, characteristic impedance, reflections and input impedance, and loss.
3. [CPW Resonators](docs/03_cpw_resonators.md): half-wave and quarter-wave resonators: resonance conditions, lumped-element equivalents, quality factors, in-line and hanger coupling, how to choose between them, and a worked 6 GHz design comparison.

## Repository layout

```text
cpw-resonator-design/
├── README.md
├── docs/
│   ├── 01_cpw_fundamentals.md
│   ├── 02_transmission_line_theory.md
│   ├── 03_cpw_resonators.md
│   └── figures/                  # generated figures used in the docs
└── scripts/
    └── generate_doc_figures.py   # regenerates all figures and worked-example numbers
```

To regenerate the figures (requires NumPy and Matplotlib):

```bash
python3 cpw-resonator-design/scripts/generate_doc_figures.py
```
