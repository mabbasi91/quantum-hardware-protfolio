"""Build the GDS layout of an inductively coupled quarter-wave CPW resonator chip.

The chip contains a straight 50-ohm feedline between two launcher pads, with
air bridges tying its ground planes together, and a meandered quarter-wave
resonator whose shorted end runs alongside the feedline. Coupling at the
current antinode makes it inductive. The resonator is QPDK's
``resonator_coupled`` cell; this script sizes it from ``parameters.py`` and
places it on a chip.

Run with the quantum-design environment:
    python cpw-resonator-design/layout/make_layout.py

Outputs (next to this script):
    quarter_wave_resonator.gds   layout, open in KLayout
    quarter_wave_resonator.png   preview image
"""

from functools import partial
from pathlib import Path

import gdsfactory as gf
import matplotlib.pyplot as plt
import numpy as np
import qpdk
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath
from qpdk.cells.airbridge import cpw_with_airbridges
from qpdk.cells.chip import chip_edge
from qpdk.cells.launcher import launcher
from qpdk.cells.resonator import resonator_coupled
from qpdk.cells.waveguides import bend_circular, straight

from parameters import DESIGN, Design, summary

OUT_DIR = Path(__file__).resolve().parent
GDS_PATH = OUT_DIR / "quarter_wave_resonator.gds"
PNG_PATH = OUT_DIR / "quarter_wave_resonator.png"


def check_cross_section(d: Design) -> None:
    """Make sure QPDK's "cpw" cross-section matches the analytical design."""
    xs = gf.get_cross_section("cpw")
    etch = [s for s in xs.sections if s.name.startswith("etch")]
    if abs(xs.width - d.cpw_width) > 1e-9 or any(abs(s.width - d.cpw_gap) > 1e-9 for s in etch):
        raise ValueError(
            f"QPDK cpw is w={xs.width}, s={etch[0].width}; parameters.py expects "
            f"w={d.cpw_width}, s={d.cpw_gap}"
        )


@gf.cell
def resonator_chip(d: Design = DESIGN) -> gf.Component:
    c = gf.Component()
    chip_w, chip_h = d.chip_size

    # Resonator with its coupling section of feedline. The start, next to the
    # feedline, is shorted (inductive coupling); the end of the meander is open.
    res = c << resonator_coupled(
        length=d.resonator_length,
        meanders=d.meanders,
        bend_spec=partial(bend_circular, radius=d.bend_radius),
        open_start=False,
        open_end=True,
        coupling_straight_length=d.coupling_length,
        coupling_gap=d.coupling_gap,
    )
    # Centre the resonator horizontally and put the feedline at feedline_y.
    res.move((-res.dbbox().center().x, d.feedline_y - res.ports["coupling_o1"].y))

    # Feedline: launcher -> straight -> coupling section -> straight -> launcher.
    # The straights carry air bridges; the coupling section does not.
    feed_xs = cpw_with_airbridges(airbridge_spacing=d.airbridge_spacing, airbridge_padding=d.airbridge_padding)
    pad = launcher()
    pad_length = pad.dbbox().width()
    x_inner = chip_w / 2 - d.chip_edge_width  # launcher pads start at the chip edge frame

    for side, port in (("left", "coupling_o1"), ("right", "coupling_o2")):
        p = res.ports[port]
        length = x_inner - abs(p.x) - pad_length
        if length <= 0:
            raise ValueError(f"Chip too narrow for the {side} feedline section ({length:.1f} um)")
        line = c << straight(length=length, cross_section=feed_xs)
        line.connect("o1", p)
        lp = c << pad
        lp.connect("o1", line.ports["o2"])
        c.add_port(f"{side}_waveport", port=lp.ports["waveport"])

    frame = c << chip_edge(size=(chip_w, chip_h), width=d.chip_edge_width)
    frame.move((-frame.dbbox().center().x, -frame.dbbox().center().y))

    c.info["resonator_length"] = res.cell.info["length"]
    return c


def _polygon_path(poly, dbu: float) -> MplPath:
    """Matplotlib path for a KLayout polygon, holes included."""
    vertices, codes = [], []
    loops = [list(poly.each_point_hull())] + [list(poly.each_point_hole(i)) for i in range(poly.holes())]
    for loop in loops:
        pts = [(p.x * dbu, p.y * dbu) for p in loop]
        vertices += pts + [pts[0]]
        codes += [MplPath.MOVETO] + [MplPath.LINETO] * (len(pts) - 1) + [MplPath.CLOSEPOLY]
    return MplPath(np.array(vertices), codes)


def save_preview(c: gf.Component, d: Design) -> None:
    """Top view in the style of the docs: gold metal, white etched gaps, grey air bridges."""
    dbu = c.kcl.dbu
    chip_w, chip_h = d.chip_size
    fig, ax = plt.subplots(figsize=(8, 8 * chip_h / chip_w))
    ax.add_patch(Rectangle((-chip_w / 2, -chip_h / 2), chip_w, chip_h, color="#c9a227"))
    polys = c.dup().get_polygons(by="name", merge=True)  # dup: cached cells are locked
    styles = {"M1_ETCH": dict(facecolor="white"), "AB_DRAW": dict(facecolor="#5d6d7e"), "AB_VIA": dict(facecolor="#1b2631")}
    for layer, style in styles.items():
        for poly in polys.get(layer, []):
            ax.add_patch(PathPatch(_polygon_path(poly, dbu), edgecolor="none", **style))
    ax.set_xlim(-chip_w / 2, chip_w / 2)
    ax.set_ylim(-chip_h / 2, chip_h / 2)
    ax.set_aspect("equal")
    ax.set_xlabel("x (µm)")
    ax.set_ylabel("y (µm)")
    ax.set_title(
        f"Quarter-wave resonator chip: ℓ = {d.resonator_length:.0f} µm, "
        f"target f₀ = {d.f0_target_hz / 1e9:.1f} GHz",
        fontsize=10,
    )
    fig.savefig(PNG_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    qpdk.PDK.activate()
    check_cross_section(DESIGN)

    c = resonator_chip()
    c.write_gds(GDS_PATH)
    save_preview(c, DESIGN)

    bbox = c.dbbox()
    print(summary())
    print(f"drawn resonator length: {c.info['resonator_length']:.1f} um")
    print(f"layout bounding box   : {bbox.width():.0f} x {bbox.height():.0f} um")
    print(f"ports                 : {[p.name for p in c.ports]}")
    print(f"wrote {GDS_PATH.name} and {PNG_PATH.name}")


if __name__ == "__main__":
    main()
