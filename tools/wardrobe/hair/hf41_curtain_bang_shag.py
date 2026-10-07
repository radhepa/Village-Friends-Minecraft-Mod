"""Curtain-Bang Shag: centre-parted curtain bangs sweeping to the cheekbones, choppy crown layers and flicked-out ends."""
from anime import ring_shell
from anime_female import curve, paint, SIDES
from paint import scalp

META = {"name": "Curtain-Bang Shag", "gender": "female",
        "description": "A choppy shoulder-length shag with centre-parted curtain bangs and ends flicked outward."}


def build(g):
    scalp(g, 9101, side_rows=8, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 9102, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    for i, (x, z, rx, rz) in enumerate(((-2.0, -1.8, -12, 16), (2.0, -1.6, -12, -16), (-1.6, 1.6, 14, 12), (1.8, 1.8, 16, -14))):
        layer = g.piece(f"crown_layer_{i}", "HEAD", (-1.5, -1, -2), (3, 1, 4), pivot=(x, -8.35, z), rotation=(rx, 0, rz))
        paint(layer, "cel", 9105 + i * 3, 2, ring=None)
    for side, sign in SIDES:
        # Curtain bang: out from the part across the brow, then down past the cheekbone, clear of the eyes.
        curve(g, f"{side}_curtain", (.4 * sign, -8.75, -4.35), ((2, 5, -6, -72 * sign), (2, 4, 6, -8 * sign), (1, 2, 6, 6 * sign)),
              seed=9120 + (sign > 0) * 7, ring=None)
        for j, (z, n) in enumerate(((-1.0, 6), (2.3, 7))):
            curve(g, f"{side}_layer_{j}", (4.45 * sign, -7.8, z), ((2, n, 0, -4 * sign), (2, 2, 0, -40 * sign), (1, 1, 0, -60 * sign)),
                  seed=9130 + j * 5 + (sign > 0), motion="sway" if j else "none")
    for i, (x, z, rz) in enumerate(((-3.0, 4.35, 6), (-1.0, 4.75, 2), (1.0, 4.35, -2), (3.0, 4.75, -6))):
        flick = 30 if i in (1, 2) else 24
        curve(g, f"back_{i}", (x, -7.8, z), ((3, 7, -2, rz), (2, 2, flick, rz * 3)), seed=9150 + i * 3, motion="sway")
