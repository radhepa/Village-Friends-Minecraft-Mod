"""Tucked Nape Twist: smooth, close-lying hair with a flat twist pinned at the nape; it sits neatly under a headscarf."""
from anime import ring_shell
from anime_female import combed, paint, strand, swept_sides, wrap_face, SIDES
from paint import k, scalp

META = {"name": "Tucked Nape Twist", "gender": "female",
        "description": "Smooth, close-lying hair with a small flat twist pinned at the nape; neat under a headscarf."}


def build(g):
    scalp(g, 8201, side_rows=8, back_rows=8, sideburn=0, part=2)
    swept_sides(g, ear_from=4, ear_depth=4)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6), rows=range(0, 6))
    combed(head.top, (3, 4, 6, 7))
    hat = ring_shell(g, 8202, side_rows=2, back_rows=3, ring_row=0)
    hat.top.vline(2, 0, 7, "H1")
    # Two flat sections smoothed back from the part, lying close to the head.
    for side, sign, x, w in (("right", -1, -2.2, 3), ("left", 1, 1.4, 5)):
        sec = g.piece(f"{side}_section", "HEAD", (-w / 2, -1, -3.8), (w, 1, 8), pivot=(x, -8.15, .2), rotation=(-3, 0, 5 * sign))
        paint(sec, "sleek", 8210 + (sign > 0), 2, ring=None)
        for z in range(8):
            for xx in range(w):
                sec.top.set(xx, z, k("H", 3 if (xx + (sign > 0)) % 2 else 2))
    # The twist: two crossed coils laid flat against the nape and a tucked end.
    for i, rz in enumerate((32, -32)):
        coil = g.piece(f"nape_twist_{i}", "HEAD", (-2, -.5, -.5), (4, 1, 1), pivot=(0, -2.6 + i * .9, 4.45), rotation=(0, 0, rz),
                       inflate=.15)
        for f in coil.faces:
            wrap_face(f, 8220 + i, 2)
    tuck = g.piece("nape_tuck", "HEAD", (-1, -1, -.5), (2, 2, 1), pivot=(0, -2.2, 4.7))
    paint(tuck, "cel", 8225, 3, ring=None)
    for side, sign in SIDES:
        strand(g, f"{side}_edge", (4.2 * sign, -6.6, -3.6), (0, 0, 24 * sign), ((1, 2),), 1, 8230 + (sign > 0), ring=None)
