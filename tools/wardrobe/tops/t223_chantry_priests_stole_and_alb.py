"""Chantry Priest's Stole and Alb: a linen alb with an amice collar, the stole crossed on the breast under a white cincture, its cross-marked ends hanging free."""
from kit import belt, body, collar, neckline, sleeves
from kit_m05 import cord_end
from paint import grid, line, solid

META = {
    "name": "Chantry Priest's Stole and Alb",
    "gender": "male",
    "description": "A chantry priest's plain linen alb with an amice at the throat, the coloured stole crossed on his breast beneath the cincture and its fringed, cross-marked ends hanging to the knee.",
    "tags": ["holy", "robe"],
    "locked_to": "b223_chantry_alb_skirt_and_soft_shoes",
    "covers_waist": True,
}

CROSS = [".m.",
         "mmm",
         ".m."]


def build(g):
    b = body(g, "S", "weave", 35080, base=3)
    neckline(b.front, "round", "S", base=3)
    for face in (b.front, b.back):
        face.vline(2, 3, 11, "S2"), face.vline(5, 3, 11, "S2")       # soft linen folds
    sleeves(g, "S", "weave", 35081, base=3, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2")                   # apparels at the cuffs
        arm.front.set(1, 9, "A3"), arm.front.set(2, 9, "A3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")
    amice = collar(g, "amice", "S", "weave", base=4, height=1, y=-.5)
    amice.front.hline(3, 5, 0, "A2"), amice.front.set(4, 0, "A3")
    # The stole: over the neck behind, crossed on the breast in front.
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    line(jf, 0, 0, 5, 9, "A2"), line(jf, 1, 0, 6, 9, "A3")
    line(jf, 7, 0, 2, 9, "A2"), line(jf, 6, 0, 1, 9, "A1")
    jf.set(3, 5, "A3"), jf.set(4, 5, "A3")
    jb.hline(1, 6, 0, "A2"), jb.hline(1, 6, 1, "A1")
    jacket.top.vline(1, 0, 3, "A2"), jacket.top.vline(6, 0, 3, "A2")
    belt(g, "cincture", 9.6, role="S", base=4, height=1, buckle=None)
    cord_end(g, "cincture_tail", (2.9, 10.2, -2.85), 6, "S", 4, 35082, knots=(2,), tassel="S2")
    for i, x in enumerate((-2.4, 2.4)):
        end = g.piece(f"stole_end_{i}", "TORSO", (-1.5, 0, 0), (3, 7, 1), pivot=(x, 10.0, -3.25), motion="flap_front")
        solid(end, "A", "weave", 35083 + i, 2)
        f = end.front
        f.vline(0, 0, 6, "A3"), f.vline(2, 0, 6, "A1")
        grid(f, 0, 2, CROSS, {"m": "M3"})
        for x2 in range(3):
            f.set(x2, 6, "A3" if x2 % 2 == 0 else "A0")                  # fringe
