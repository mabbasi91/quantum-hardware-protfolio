"""Generate the figures used in the cpw-resonator-design documentation.

Run from anywhere:
    python3 cpw-resonator-design/scripts/generate_doc_figures.py

Figures are written to cpw-resonator-design/docs/figures/. Only NumPy and
Matplotlib are required.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

FIG_DIR = Path(__file__).resolve().parents[1] / "docs" / "figures"

C0 = 299_792_458.0  # speed of light in vacuum, m/s
HBAR = 1.054_571_817e-34  # reduced Planck constant, J s
EPS_R_SI = 11.45  # silicon relative permittivity at cryogenic temperature

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


# ---------------------------------------------------------------------------
# CPW quasi-static model (conformal mapping)
# ---------------------------------------------------------------------------


def ellipk(k):
    """Complete elliptic integral of the first kind K(k), modulus k, via the AGM."""
    a = np.ones_like(np.asarray(k, dtype=float))
    b = np.sqrt(1.0 - np.asarray(k, dtype=float) ** 2)
    for _ in range(30):
        a, b = (a + b) / 2.0, np.sqrt(a * b)
    return np.pi / (2.0 * a)


def k_ratio(k):
    """K(k)/K(k'), with k' = sqrt(1 - k^2)."""
    return ellipk(k) / ellipk(np.sqrt(1.0 - k**2))


def cpw_quasi_static(w, s, eps_r, h=None):
    """Return (eps_eff, Z0) for a zero-thickness CPW with infinite grounds.

    If h is None the substrate is treated as infinitely thick.
    """
    k0 = w / (w + 2.0 * s)
    if h is None:
        eps_eff = (eps_r + 1.0) / 2.0
    else:
        k1 = np.sinh(np.pi * w / (4.0 * h)) / np.sinh(np.pi * (w + 2.0 * s) / (4.0 * h))
        eps_eff = 1.0 + (eps_r - 1.0) / 2.0 * k_ratio(k1) / k_ratio(k0)
    z0 = 30.0 * np.pi / np.sqrt(eps_eff) / k_ratio(k0)
    return eps_eff, z0


# ---------------------------------------------------------------------------
# CPW fundamentals figures
# ---------------------------------------------------------------------------


def fig_cpw_cross_section():
    """Quasi-static electric field of a zero-thickness CPW (analytic)."""
    w, s = 10.0, 6.0  # um
    a, b = w / 2.0, w / 2.0 + s

    x = np.linspace(-40, 40, 801)
    dy = 25.0 / 400
    y = (np.arange(400) + 0.5) * dy  # offset so the mirrored grid stays uniform
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Complex field of a CPW with metal on the real axis: E* ∝ 1/sqrt((z²-a²)(z²-b²)).
    # Each principal sqrt has its cut on the real axis, so the product is analytic for y > 0.
    root = np.sqrt(Z - a) * np.sqrt(Z + a) * np.sqrt(Z - b) * np.sqrt(Z + b)
    field = 1j * np.conj(1.0 / root)  # phase chosen so lines run from centre to ground
    ex, ey = field.real, field.imag

    # The field pattern is identical in the substrate (mirror image), see docs.
    xs = x
    ys = np.concatenate([-y[::-1], y])
    EX = np.vstack([ex[::-1], ex])
    EY = np.vstack([-ey[::-1], ey])
    mag = np.hypot(EX, EY)

    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.add_patch(Rectangle((-40, -25), 80, 25, color="#d9e6f2", zorder=0))
    ax.text(-38, -23, r"substrate ($\varepsilon_r \approx 11.45$, Si)", fontsize=9, color="#34495e")
    ax.text(-38, 22, "vacuum", fontsize=9, color="#34495e")

    strm = ax.streamplot(
        xs,
        ys,
        EX,
        EY,
        color=np.log10(mag),
        cmap="magma_r",
        density=1.6,
        linewidth=0.8,
        arrowsize=0.6,
        broken_streamlines=False,
    )
    metal = dict(color="#b8860b", zorder=5)
    ax.add_patch(Rectangle((-a, -0.4), w, 0.8, **metal))
    ax.add_patch(Rectangle((b, -0.4), 40 - b, 0.8, **metal))
    ax.add_patch(Rectangle((-40, -0.4), 40 - b, 0.8, **metal))

    def dim(x0, x1, yy, label):
        ax.annotate("", (x0, yy), (x1, yy), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text((x0 + x1) / 2, yy + 0.8, label, ha="center", fontsize=9)

    dim(-a, a, 3.0, r"$w$")
    dim(a, b, 3.0, r"$s$")
    dim(-b, -a, 3.0, r"$s$")
    ax.text(0, -3.0, "signal", ha="center", fontsize=9, zorder=6)
    ax.text(24, -3.0, "ground", ha="center", fontsize=9, zorder=6)
    ax.text(-24, -3.0, "ground", ha="center", fontsize=9, zorder=6)

    cbar = fig.colorbar(strm.lines, ax=ax, pad=0.02)
    cbar.set_label(r"$\log_{10}|E|$ (arb. units)")
    ax.set_xlim(-40, 40)
    ax.set_ylim(-25, 25)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$ (µm)")
    ax.set_ylabel(r"$y$ (µm)")
    ax.set_title(r"Quasi-static electric field of a CPW ($w = 10$ µm, $s = 6$ µm)")
    fig.savefig(FIG_DIR / "cpw_field_lines.png")
    plt.close(fig)


def fig_cpw_impedance_map():
    """Z0 over (w, s) on silicon, with the 50-ohm contour highlighted."""
    w = np.linspace(2, 40, 300)
    s = np.linspace(1, 30, 300)
    W, S = np.meshgrid(w, s)
    _, z0 = cpw_quasi_static(W, S, EPS_R_SI, h=500.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))

    cf = ax1.contourf(W, S, z0, levels=np.arange(20, 121, 5), cmap="viridis")
    cs = ax1.contour(W, S, z0, levels=[30, 40, 60, 70, 80], colors="white", linewidths=0.6)
    ax1.clabel(cs, fmt="%d Ω", fontsize=8)
    c50 = ax1.contour(W, S, z0, levels=[50], colors="#e74c3c", linewidths=1.8)
    ax1.clabel(c50, fmt="50 Ω", fontsize=9)
    ax1.plot(10, 6, "o", color="#e74c3c", ms=5)
    ax1.annotate("10 / 6 µm", (10, 6), (14, 2.5), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6))
    fig.colorbar(cf, ax=ax1, label=r"$Z_0$ (Ω)")
    ax1.set_xlabel(r"centre width $w$ (µm)")
    ax1.set_ylabel(r"gap $s$ (µm)")
    ax1.set_title(r"$Z_0$ on Si ($\varepsilon_r = 11.45$, $h = 500$ µm)")

    k0 = np.linspace(0.02, 0.98, 300)
    for eps_r, label in [(EPS_R_SI, "Si (11.45)"), (9.9, "sapphire, isotropic approx. (9.9)"), (3.8, "quartz (3.8)")]:
        eps_eff = (eps_r + 1) / 2
        ax2.plot(k0, 30 * np.pi / np.sqrt(eps_eff) / k_ratio(k0), label=label)
    ax2.axhline(50, color="0.5", lw=0.8, ls="--")
    ax2.set_xlabel(r"aspect ratio $k_0 = w/(w + 2s)$")
    ax2.set_ylabel(r"$Z_0$ (Ω)")
    ax2.set_ylim(0, 200)
    ax2.set_title("Thick-substrate limit")
    ax2.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "cpw_impedance_map.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Transmission-line theory figures
# ---------------------------------------------------------------------------


def _resistor(ax, x0, x1, y, vertical=False, n=6, amp=0.08):
    t = np.linspace(0, 1, 2 * n + 1)
    off = amp * np.array([0] + [(-1) ** i for i in range(2 * n - 1)] + [0])
    if vertical:
        ax.plot(y + off, x0 + (x1 - x0) * t, "k", lw=1.2)
    else:
        ax.plot(x0 + (x1 - x0) * t, y + off, "k", lw=1.2)


def _inductor(ax, x0, x1, y, n=4):
    r = (x1 - x0) / (2 * n)
    for i in range(n):
        th = np.linspace(np.pi, 0, 30)
        ax.plot(x0 + r * (2 * i + 1) + r * np.cos(th), y + r * np.sin(th), "k", lw=1.2)


def _capacitor(ax, x, y0, y1, gap=0.06, width=0.18):
    ym = (y0 + y1) / 2
    ax.plot([x, x], [y0, ym + gap], "k", lw=1.2)
    ax.plot([x, x], [ym - gap, y1], "k", lw=1.2)
    for yy in (ym + gap, ym - gap):
        ax.plot([x - width, x + width], [yy, yy], "k", lw=1.6)


def fig_rlgc_segment():
    fig, ax = plt.subplots(figsize=(7, 2.6))
    top, bot = 1.0, 0.0

    ax.plot([0, 0.6], [top, top], "k", lw=1.2)
    _resistor(ax, 0.6, 1.6, top)
    ax.plot([1.6, 1.9], [top, top], "k", lw=1.2)
    _inductor(ax, 1.9, 3.1, top)
    ax.plot([3.1, 5.0], [top, top], "k", lw=1.2)
    ax.plot([0, 5.0], [bot, bot], "k", lw=1.2)

    for xx in (3.5, 4.4):
        ax.plot([xx, xx], [top, 0.8], "k", lw=1.2)
        ax.plot([xx, xx], [0.2, bot], "k", lw=1.2)
    _resistor(ax, 0.8, 0.2, 3.5, vertical=True, n=4)
    _capacitor(ax, 4.4, 0.8, 0.2)
    for xx in (3.5, 4.4):
        ax.plot(xx, top, "ko", ms=3)
        ax.plot(xx, bot, "ko", ms=3)

    ax.text(1.1, top + 0.17, r"$R'\,dz$", ha="center")
    ax.text(2.5, top + 0.22, r"$L'\,dz$", ha="center")
    ax.text(3.68, 0.5, r"$G'\,dz$", va="center")
    ax.text(4.62, 0.5, r"$C'\,dz$", va="center")

    for xx, lab in ((0, "z"), (5.0, "z+dz")):
        ax.plot(xx, top, "o", mfc="white", mec="k", ms=6)
        ax.plot(xx, bot, "o", mfc="white", mec="k", ms=6)
        ax.text(xx, -0.3, rf"${lab}$", ha="center")
    ax.annotate("", (0.35, top - 0.1), (0.05, top - 0.1), arrowprops=dict(arrowstyle="->", lw=0.9))
    ax.text(0.2, top - 0.28, r"$I(z)$", ha="center", fontsize=9)
    ax.text(-0.15, 0.5, r"$V(z)$", ha="right", va="center")
    ax.text(5.15, 0.5, r"$V(z+dz)$", ha="left", va="center")
    ax.text(-0.15, top, "+", ha="right", va="center")
    ax.text(-0.15, bot, "−", ha="right", va="center")
    ax.text(2.5, -0.17, "return conductors (CPW grounds)", ha="center", fontsize=8, color="0.35")

    ax.set_xlim(-1.0, 6.2)
    ax.set_ylim(-0.45, 1.45)
    ax.axis("off")
    fig.savefig(FIG_DIR / "rlgc_segment.png")
    plt.close(fig)


def fig_standing_waves():
    z0 = 50.0
    beta_l = np.linspace(0, 2 * np.pi, 600)  # distance from load in units of 1/beta
    d_over_lambda = beta_l / (2 * np.pi)
    loads = [
        ("matched, $Z_L = Z_0$", z0),
        ("short, $Z_L = 0$", 0.0),
        ("open, $Z_L \\to \\infty$", 1e12),
        ("$Z_L = 100$ Ω (VSWR 2)", 100.0),
    ]

    fig, ax = plt.subplots(figsize=(7, 3.2))
    for label, zl in loads:
        gamma_l = (zl - z0) / (zl + z0)
        v = np.abs(1 + gamma_l * np.exp(-2j * beta_l))
        ax.plot(d_over_lambda, v, label=label)
    ax.set_xlabel(r"distance from load $d/\lambda$")
    ax.set_ylabel(r"$|V(d)|\,/\,|V^+|$")
    ax.set_xlim(1, 0)  # load on the right, as on a schematic
    ax.set_ylim(0, 2.1)
    ax.axvline(0.25, color="0.6", lw=0.7, ls=":")
    ax.text(0.25, 2.03, r"$\lambda/4$", ha="center", fontsize=9, color="0.4")
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower left")
    ax.set_title("Standing-wave voltage on a lossless line")
    fig.savefig(FIG_DIR / "standing_waves.png")
    plt.close(fig)


def fig_stub_input_impedance():
    bl = np.linspace(0.001, 2 * np.pi - 0.001, 3000)
    x_short = np.tan(bl)
    x_open = -1 / np.tan(bl)
    for arr in (x_short, x_open):
        arr[np.abs(arr) > 12] = np.nan  # break the line at the poles

    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(bl / (2 * np.pi), x_short, label=r"shorted stub: $Z_\mathrm{in} = jZ_0\tan\beta\ell$")
    ax.plot(bl / (2 * np.pi), x_open, label=r"open stub: $Z_\mathrm{in} = -jZ_0\cot\beta\ell$")
    for q in (0.25, 0.5, 0.75):
        ax.axvline(q, color="0.7", lw=0.7, ls=":")
    ax.axhline(0, color="0.5", lw=0.6)
    ax.set_xlabel(r"stub length $\ell/\lambda$")
    ax.set_ylabel(r"$\mathrm{Im}\,Z_\mathrm{in}/Z_0$")
    ax.set_ylim(-8, 8)
    ax.set_xlim(0, 1)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.set_title("Input reactance of lossless stubs")
    fig.savefig(FIG_DIR / "stub_input_impedance.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Quarter-wave resonator figures
# ---------------------------------------------------------------------------


def _mode_figure(kind):
    """Voltage and current standing waves of the first three modes of one resonator type."""
    u = np.linspace(0, 1, 400)  # position along the resonator, z / ell
    fig, axes = plt.subplots(1, 3, figsize=(10, 2.8), sharey=True)
    for ax, n in zip(axes, (1, 2, 3)):
        if kind == "half":
            k = n * np.pi
            m = "" if n == 1 else str(n)
            title = rf"$n = {n}$:  $\ell = {m}\lambda_{n}/2$,  $f_{n} = {m}f_1$"
            ticks = ["0\nopen", "1\nopen"]
        else:
            k = (2 * n - 1) * np.pi / 2
            m = "" if n == 1 else str(2 * n - 1)
            title = rf"$n = {n}$:  $\ell = {m}\lambda_{n}/4$,  $f_{n} = {m}f_1$"
            ticks = ["0\nopen", "1\nshort"]
        ax.plot(u, np.cos(k * u), label=r"voltage $V$")
        ax.plot(u, np.sin(k * u), label=r"current $I$", ls="--")
        ax.axhline(0, color="0.6", lw=0.6)
        ax.set_title(title)
        ax.set_xticks([0, 1], ticks)
        ax.set_xlabel(r"position $z/\ell$")
    axes[0].set_ylabel("normalised amplitude")
    axes[0].legend(frameon=False, fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{'hw' if kind == 'half' else 'qw'}_mode_profiles.png")
    plt.close(fig)


def fig_resonator_modes():
    _mode_figure("half")
    _mode_figure("quarter")


def fig_hw_layout():
    """Schematic top view of an in-line (transmission) half-wave resonator."""
    fig, ax = plt.subplots(figsize=(7, 3.4))
    gnd, gap = "#c9a227", "white"
    ax.add_patch(Rectangle((0, 0), 10, 6, color=gnd))

    # Symmetric meander between the two coupling gaps (x = 1.9 and x = 7.9).
    res = [(2.0, 5.0), (3.0, 5.0), (3.0, 1.2), (4.2, 1.2), (4.2, 4.0), (5.6, 4.0),
           (5.6, 1.2), (6.8, 1.2), (6.8, 5.0), (7.8, 5.0)]
    slot = [(0, 5.0)] + res + [(10, 5.0)]
    xs, ys = zip(*slot)
    ax.plot(xs, ys, color=gap, lw=9, solid_capstyle="butt", solid_joinstyle="miter")
    for piece in ([(0, 5.0), (1.82, 5.0)], res, [(7.98, 5.0), (10, 5.0)]):
        xs, ys = zip(*piece)
        ax.plot(xs, ys, color=gnd, lw=3, solid_capstyle="butt", solid_joinstyle="miter")

    for x in (1.91, 7.89):
        ax.annotate(r"$C_\kappa$", (x, 5.1), (x, 5.75), ha="center", fontsize=9,
                    arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.text(0.9, 5.35, "input", ha="center", fontsize=8)
    ax.text(9.1, 5.35, "output", ha="center", fontsize=8)
    ax.plot(4.9, 4.0, "o", color="#c0392b", ms=5, zorder=5)
    ax.annotate("midpoint:\ncurrent antinode,\nvoltage node", (4.9, 4.0), (7.15, 2.3),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.annotate("open end:\nvoltage antinode", (2.05, 4.95), (0.15, 3.0), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.text(3.6, 0.35, r"meandered length $\ell \approx \lambda/2$", ha="center", fontsize=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("In-line half-wave CPW resonator (schematic, not to scale)", fontsize=10)
    fig.savefig(FIG_DIR / "hw_inline_layout.png")
    plt.close(fig)


def fig_qw_layout():
    """Schematic top view of a hanger-coupled quarter-wave resonator."""
    fig, ax = plt.subplots(figsize=(7, 3.4))
    gnd = "#c9a227"
    gap = "white"
    ax.add_patch(Rectangle((0, 0), 10, 6, color=gnd))

    # feedline (horizontal) with gaps
    ax.add_patch(Rectangle((0, 4.6), 10, 0.8, color=gap))
    ax.add_patch(Rectangle((0, 4.85), 10, 0.3, color=gnd))
    # resonator: elbow parallel to feedline, then meander down to short
    path = [(2.0, 4.2), (6.0, 4.2), (6.0, 3.3), (2.6, 3.3), (2.6, 2.4), (6.0, 2.4), (6.0, 1.5), (2.6, 1.5), (2.6, 0.6)]
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=gap, lw=9, solid_capstyle="butt", solid_joinstyle="miter")
    ax.plot(xs, ys, color=gnd, lw=3, solid_capstyle="butt", solid_joinstyle="miter")
    ax.add_patch(Rectangle((1.75, 4.05), 0.3, 0.3, color=gap))  # open end gap

    ax.text(10, 6.15, "feedline (port 1 → port 2)", fontsize=8, ha="right")
    ax.annotate("open end\n(voltage antinode)", (1.9, 4.2), (0.15, 2.9), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.annotate(r"coupling length $\ell_c$", (4.0, 4.4), (6.6, 3.9), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.annotate("shorted end: centre merges\ninto ground (current antinode)", (2.6, 0.6), (3.3, 0.45), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.text(7.0, 2.0, r"meandered length $\ell \approx \lambda/4$", fontsize=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Hanger-coupled quarter-wave CPW resonator (schematic, not to scale)", fontsize=10)
    fig.savefig(FIG_DIR / "qw_hanger_layout.png")
    plt.close(fig)


def fig_s21_notch():
    f0 = 6.0e9
    qi = 2.0e5
    detune = np.linspace(-6, 6, 2001)  # in units of f0 / qi
    f = f0 * (1 + detune / qi)
    cases = [(qi / 5, "over-coupled  $Q_c = Q_i/5$"), (qi, "critically coupled  $Q_c = Q_i$"), (5 * qi, "under-coupled  $Q_c = 5Q_i$")]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 3.3))
    for qc, label in cases:
        ql = 1 / (1 / qi + 1 / qc)
        s21 = 1 - (ql / qc) / (1 + 2j * ql * (f - f0) / f0)
        ax1.plot(detune, 20 * np.log10(np.abs(s21)), label=label)
        ax2.plot(detune, np.degrees(np.angle(s21)))
        f_wide = f0 * (1 + np.linspace(-200, 200, 4001) / qi)  # wide span closes the circle
        s21_wide = 1 - (ql / qc) / (1 + 2j * ql * (f_wide - f0) / f0)
        ax3.plot(s21_wide.real, s21_wide.imag)
    ax1.set_xlabel(r"$(f - f_0)\,Q_i/f_0$")
    ax1.set_ylabel(r"$|S_{21}|$ (dB)")
    ax1.set_ylim(-25, 1)
    ax1.legend(frameon=False, fontsize=7.5, loc="lower left")
    ax2.set_xlabel(r"$(f - f_0)\,Q_i/f_0$")
    ax2.set_ylabel(r"$\arg S_{21}$ (deg)")
    ax3.set_xlabel(r"Re $S_{21}$")
    ax3.set_ylabel(r"Im $S_{21}$")
    ax3.set_aspect("equal")
    ax3.plot(1, 0, "k.", ms=4)
    ax3.text(1.0, 0.03, "off resonance", fontsize=7, ha="right")
    fig.suptitle(r"Ideal hanger response, $Q_i = 2\times10^5$", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "s21_hanger_response.png")
    plt.close(fig)


def fig_s21_inline():
    f0 = 6.0e9
    qi = 2.0e5
    detune = np.linspace(-6, 6, 2001)
    f = f0 * (1 + detune / qi)
    cases = [(qi / 5, "over-coupled  $Q_c = Q_i/5$"), (qi, "critically coupled  $Q_c = Q_i$"), (5 * qi, "under-coupled  $Q_c = 5Q_i$")]

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    for qc, label in cases:
        ql = 1 / (1 / qi + 1 / qc)
        s21 = (ql / qc) / (1 + 2j * ql * (f - f0) / f0)
        ax.plot(detune, 20 * np.log10(np.abs(s21)), label=label)
    ax.set_xlabel(r"$(f - f_0)\,Q_i/f_0$")
    ax.set_ylabel(r"$|S_{21}|$ (dB)")
    ax.set_ylim(-30, 1)
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    ax.set_title(r"Ideal in-line response, $Q_i = 2\times10^5$", fontsize=10)
    fig.savefig(FIG_DIR / "s21_inline_response.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Worked example printed to stdout (numbers quoted in the docs)
# ---------------------------------------------------------------------------


def worked_example():
    w, s, h = 10e-6, 6e-6, 500e-6
    eps_eff, z0 = cpw_quasi_static(w, s, EPS_R_SI, h=h)
    vp = C0 / np.sqrt(eps_eff)
    lp = z0 / vp
    cp = 1 / (z0 * vp)
    f0 = 6.0e9
    w0 = 2 * np.pi * f0
    z_feed = 50.0
    print(f"w = 10 um, s = 6 um, Si, h = 500 um")
    print(f"  eps_eff = {eps_eff:.3f}, Z0 = {z0:.2f} ohm, v_p = {vp / C0:.4f} c = {vp:.4e} m/s")
    print(f"  L' = {lp * 1e9:.1f} nH/m, C' = {cp * 1e12:.1f} pF/m")

    # Equivalent parallel LC seen at a voltage antinode: C = C' ell / 2 for both types.
    for name, ell in (("half-wave", vp / (2 * f0)), ("quarter-wave", vp / (4 * f0))):
        c_eq = cp * ell / 2
        l_eq = 1 / (w0**2 * c_eq)
        print(f"{name} at {f0 / 1e9:.1f} GHz: length = {ell * 1e3:.3f} mm")
        print(f"  equivalent parallel LC: C = {c_eq * 1e15:.1f} fF, L = {l_eq * 1e9:.3f} nH")
        # Qc = C / (w0 Cc^2 R_ext): hanger sees Z_feed/2; symmetric in-line has two ports of Z_feed.
        for qc in (1e4, 1e5):
            cc_hanger = np.sqrt(2 * c_eq / (w0 * qc * z_feed))
            line = f"  Qc = {qc:.0e}: hanger Cc = {cc_hanger * 1e15:.2f} fF"
            if name == "half-wave":
                cc_inline = np.sqrt(c_eq / (2 * w0 * qc * z_feed))
                line += f", in-line Cc (each end) = {cc_inline * 1e15:.2f} fF"
            print(line)
        print(f"  pull from 2.08 fF at the open end: {-f0 * 2.08e-15 / (2 * c_eq) / 1e6:.1f} MHz")
    for alpha in (0.02, 0.1):
        print(f"kinetic-inductance fraction {alpha}: 6 GHz shifts to {f0 * np.sqrt(1 - alpha) / 1e9:.3f} GHz")
    ql, qc, p_dbm = 1e5, 2e5, -140
    p = 1e-3 * 10 ** (p_dbm / 10)
    n_ph = 2 * ql**2 * p / (qc * HBAR * w0**2)
    print(f"hanger photon number at {p_dbm} dBm, Ql = {ql:.0e}, Qc = {qc:.0e}: <n> = {n_ph:.1f}")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_cpw_cross_section()
    fig_cpw_impedance_map()
    fig_rlgc_segment()
    fig_standing_waves()
    fig_stub_input_impedance()
    fig_resonator_modes()
    fig_hw_layout()
    fig_qw_layout()
    fig_s21_notch()
    fig_s21_inline()
    worked_example()
    print(f"figures written to {FIG_DIR}")


if __name__ == "__main__":
    main()
