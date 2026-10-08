"""Grape-Treader's Kilted Skirt: a skirt drawn up the front and knotted in a big knot at the middle so she can
tread the vat, bare legs stained with must to mid-calf."""
from kit import SIDES
from kit_female import skirt
from paint import k, line, rnd, solid

META = {
    "name": "Grape-Treader's Kilted Skirt",
    "gender": "female",
    "description": "A skirt drawn up and knotted in a big knot at the front for treading the vat, bare legs and feet stained deep with grape must.",
    "tags": ["work", "casual", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51180, top=9.8, length=5, back_length=8, side_length=6, flare=7, folds=False,
              gather=False)
    front = s.front.front
    # Folds pulled up toward the knot from both lower corners.
    line(front, 4, 1, 0, 4, "P1"), line(front, 5, 1, 9, 4, "P1")
    line(front, 3, 1, 0, 3, "P3"), line(front, 6, 1, 9, 3, "P3")
    front.vline(4, 2, 4, "P1"), front.vline(5, 2, 4, "P3")
    front.hline(0, 9, 4, "P1")
    for face in (s.back.back, s.right.right, s.left.left):
        face.hline(0, face.w - 1, face.h - 1, "P1")
        for x in range(1, face.w - 1, 3):
            face.vline(x, 2, face.h - 2, "P1")
    knot = g.piece("waist_skirt_knot", "TORSO", (-1.5, -.6, -1.05), (3, 3, 1), pivot=(0, 9.8, -2.95), inflate=.1,
                   motion="flap_front")
    solid(knot, "P", "weave", 51181, 2)
    knot.front.set(1, 1, "P0"), knot.front.set(0, 0, "P3"), knot.front.set(2, 2, "P1")
    for i, (dx, rot) in enumerate(((-1.0, 16), (.9, -14))):
        tail = g.piece(f"waist_knot_end_{i}", "TORSO", (dx - .5, 2.2, -1.05), (1, 2, 1), pivot=(0, 9.8, -2.95),
                       rotation=(0, 0, rot), motion="flap_front")
        solid(tail, "P", "weave", 51182 + i, 2)
        tail.front.set(0, 1, "P1")
    # Bare legs stained with must: the feet dark, splashes thinning toward mid-calf.
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip = leg.strip
        for y in range(6, 12):
            for x in range(strip.w):
                depth = y - 6                                         # 0 at mid-calf .. 5 at the sole
                r = rnd(x, y, 51184 + (side == "left"))
                if depth >= 4 or r < depth * .22:
                    strip.set(x, y, k("A", 0 if depth >= 5 or r < .1 else 1))
        for x in (1, 6, 9, 14):
            strip.set(x, 5, "A1")                                     # a few drips higher up
        leg.bottom.fill("A0")
