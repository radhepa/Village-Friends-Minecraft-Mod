"""Bathhouse Wet: freshly washed hair slicked straight back, dark and glossy, thin wet locks clinging to the neck."""
from anime import ring_shell
from anime_female import combed, fall, paint, strand, wet_face, SIDES
from paint import k, scalp

META = {"name": "Bathhouse Wet", "gender": "female",
        "description": "Freshly washed hair slicked straight back, dark and glossy, with thin locks clinging to the neck."}


def build(g):
    scalp(g, 8601, side_rows=8, back_rows=8, sideburn=0, base=1)
    head = g.part("head")
    combed(head.top, range(8), base=1)
    combed(head.back, range(8), base=1)
    hat = ring_shell(g, 8602, side_rows=4, back_rows=6, base=1, ring_row=2)
    for f in (hat.back, hat.right, hat.left):
        wet_face(type(f)(f.layer, f.x0, f.y0, f.w, 4, f.name), 8603 + f.x0, 1, ring=1)
    for y in range(8):   # glossy streaks running back over the crown
        for x in (1, 4, 6):
            hat.top.set(x, y, k("H", 3 if y % 3 else 4))
    for i, (x, rz) in enumerate(((-1.7, 5), (1.7, -5))):
        sheet = g.piece(f"slick_{i}", "HEAD", (-2, -1, -4), (4, 1, 8), pivot=(x, -8.2, .3), rotation=(-2, 0, rz))
        paint(sheet, "wet", 8610 + i, 1, ring=0)
    for side, sign in SIDES:
        strand(g, f"{side}_cling", (4.35 * sign, -6.4, 1.2), (-4, 0, -2 * sign), ((1, 7), (1, 2)), 1, 8620 + (sign > 0),
               texture="wet", base=1, ring=1)
        strand(g, f"{side}_neck", (3.6 * sign, -3.0, 3.7), (-10, 0, 3 * sign), ((1, 5), (1, 2)), 1, 8624 + (sign > 0),
               texture="wet", base=1, ring=None)
    fall(g, "back", [(-3.0, -7.4, 4.4, ((2, 9), (1, 3)), -6, 4), (-1.3, -7.6, 4.6, ((2, 10), (1, 3)), -7, 1),
                     (.4, -7.5, 4.4, ((2, 11), (1, 2)), -7, -1), (2.1, -7.6, 4.6, ((2, 9), (1, 3)), -6, -3),
                     (3.5, -7.3, 4.4, ((1, 8), (1, 2)), -5, -5)], 8630, motion="sway", texture="wet", base=1)
