"""Design parameters for the inductively coupled quarter-wave resonator chip.

Every dimension used by the layout (and later by the simulation) is defined
here. The resonator length is derived from the analytical CPW model in
docs/01_cpw_fundamentals.md rather than typed in, so changing the target
frequency or the substrate updates the layout consistently.

All lengths are in micrometres unless stated otherwise.
"""

from dataclasses import dataclass

import numpy as np

C0 = 299_792_458.0  # speed of light in vacuum, m/s


# ---------------------------------------------------------------------------
# Analytical CPW model (conformal mapping, zero-thickness metal)
# ---------------------------------------------------------------------------


def ellipk(k):
    """Complete elliptic integral of the first kind K(k), modulus k, via the AGM."""
    a, b = 1.0, np.sqrt(1.0 - k**2)
    for _ in range(30):
        a, b = (a + b) / 2.0, np.sqrt(a * b)
    return np.pi / (2.0 * a)


def k_ratio(k):
    """K(k)/K(k'), with k' = sqrt(1 - k^2)."""
    return ellipk(k) / ellipk(np.sqrt(1.0 - k**2))


def cpw_quasi_static(w, s, eps_r, h):
    """Return (eps_eff, Z0) for a CPW on a substrate of finite thickness h."""
    k0 = w / (w + 2.0 * s)
    k1 = np.sinh(np.pi * w / (4.0 * h)) / np.sinh(np.pi * (w + 2.0 * s) / (4.0 * h))
    eps_eff = 1.0 + (eps_r - 1.0) / 2.0 * k_ratio(k1) / k_ratio(k0)
    z0 = 30.0 * np.pi / np.sqrt(eps_eff) / k_ratio(k0)
    return eps_eff, z0


# ---------------------------------------------------------------------------
# Design parameters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Design:
    # Target
    f0_target_hz: float = 6.0e9

    # Substrate (high-resistivity silicon at millikelvin temperature)
    eps_r: float = 11.45
    substrate_thickness: float = 500.0

    # CPW cross-section, shared by feedline and resonator (QPDK "cpw" default)
    cpw_width: float = 10.0
    cpw_gap: float = 6.0

    # Resonator meander
    meanders: int = 6  # number of 180-degree bends
    bend_radius: float = 100.0

    # Inductive coupler: the resonator's shorted end (current antinode) starts
    # the first straight section, which runs parallel to the feedline. The
    # coupling length is that section's length (derived below).
    coupling_gap: float = 20.0  # edge to edge of the two centre conductors

    # Air bridges (crossovers) tying the feedline's two ground planes together.
    # None are placed on the coupling section.
    airbridge_spacing: float = 250.0
    airbridge_padding: float = 50.0  # distance from each feedline section's start to its first bridge

    # Chip
    chip_size: tuple[float, float] = (3000.0, 2500.0)
    chip_edge_width: float = 100.0
    feedline_y: float = 600.0  # feedline height above the chip centre

    @property
    def eps_eff(self) -> float:
        return cpw_quasi_static(self.cpw_width, self.cpw_gap, self.eps_r, self.substrate_thickness)[0]

    @property
    def z0(self) -> float:
        return cpw_quasi_static(self.cpw_width, self.cpw_gap, self.eps_r, self.substrate_thickness)[1]

    @property
    def phase_velocity(self) -> float:
        return C0 / np.sqrt(self.eps_eff)

    @property
    def resonator_length(self) -> float:
        """Quarter-wave length (um) for the target frequency, ignoring coupling and kinetic inductance."""
        return self.phase_velocity / (4.0 * self.f0_target_hz) * 1e6

    @property
    def straight_section_length(self) -> float:
        """Length (um) of each straight section of the meander (QPDK splits the length evenly)."""
        bends = self.meanders * np.pi * self.bend_radius
        return (self.resonator_length - bends) / (self.meanders + 1)

    @property
    def coupling_length(self) -> float:
        """Length (um) over which the resonator's shorted-end section runs alongside the feedline."""
        return self.straight_section_length

    @property
    def ground_strip_width(self) -> float:
        """Width of the ground strip separating feedline and resonator in the coupler."""
        return self.coupling_gap - 2.0 * self.cpw_gap


DESIGN = Design()


def summary(d: Design = DESIGN) -> str:
    return "\n".join(
        [
            f"CPW w/s               : {d.cpw_width:.1f} / {d.cpw_gap:.1f} um",
            f"eps_eff, Z0           : {d.eps_eff:.3f}, {d.z0:.2f} ohm",
            f"phase velocity        : {d.phase_velocity / C0:.4f} c",
            f"target f0             : {d.f0_target_hz / 1e9:.3f} GHz",
            f"resonator length      : {d.resonator_length:.1f} um",
            f"meanders, bend radius : {d.meanders}, {d.bend_radius:.0f} um",
            f"coupling length, gap  : {d.coupling_length:.0f} um, {d.coupling_gap:.0f} um "
            f"(ground strip {d.ground_strip_width:.0f} um)",
            f"feedline air bridges  : every {d.airbridge_spacing:.0f} um",
            f"chip size             : {d.chip_size[0]:.0f} x {d.chip_size[1]:.0f} um",
        ]
    )


if __name__ == "__main__":
    print(summary())
