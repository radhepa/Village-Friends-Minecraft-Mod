"""Sailor's Wide Slops: short canvas slops that bell out in stiff pleats to just below the knee, a drawstring waist,
grey knitted stockings and square-buckled shoes."""
from kit import SIDES, legs, waistband
from kit_m03 import knit_stockings, low_shoes
from kit_male import blk, leg_blk

META = {
    "name": "Sailor's Wide Slops",
    "gender": "male",
    "description": "Short canvas slops belling out in stiff pleats to just below the knee, gathered on a drawstring, over "
                   "grey knitted stockings and square-buckled shoes.",
    "tags": ["casual", "sea", "relaxed"],
}


def pleats(face, role="P", base=2):
    """Stiff box pleats: a lit fold and a shaded valley every two texels."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, f"{role}{base + 1}" if x % 2 == 0 else f"{role}{base - 1}" if (x + y) % 4 == 1 else f"{role}{base}")


def build(g):
    legs(g, "P", "twill", 33100, rows=(0, 6), crease=False)
    body = waistband(g, "P", "twill", 33101)
    for x in range(8):
        body.front.set(x, 9, "P3" if x % 2 else "P1")                    # gathered on the drawstring
        body.back.set(x, 9, "P3" if x % 2 else "P1")
    knit_stockings(g, "S", (7, 9), base=2, seed=33102)
    low_shoes(g, "K", 2, top=10, sole="K0", seed=33103)
    for i, side in enumerate(SIDES):
        # The upper leg: full and soft. The bell: wider still, its pleats standing stiff at the knee.
        upper = leg_blk(g, f"{side}_slop_seat", side, 0.0, (5, 4, 5), "P", 2, "twill", 33104 + i,
                        dx=-.25 if side == "right" else .25, inflate=.1 + .04 * i)
        for face in upper.sides:
            face.vline(1, 1, 3, "P1"), face.vline(3, 2, 3, "P3")
        bell = leg_blk(g, f"{side}_slop_bell", side, 4.0, (5, 3, 5), "P", 2, "twill", 33106 + i,
                       dx=-.35 if side == "right" else .35, inflate=.42 + .04 * i)
        for face in bell.sides:
            pleats(face)
            face.hline(0, face.w - 1, 2, "P1")                            # the turned hem
        bell.bottom.fill("K1")
        g.part(f"{side}_leg").strip.hline(0, 15, 6, "S1")                # stocking tops tied off under the bell
        # Square buckles on the shoes.
        pants = g.part(f"{side}_pants")
        pants.front.hline(1, 2, 10, "M3")
        pants.front.set(1, 11, "M1"), pants.front.set(2, 11, "M1")
    for i, x in enumerate((-.6, .6)):                                    # drawstring ends
        tail = blk(g, f"waist_drawstring_{i}", (x, 9.8, -2.75), (1, 3, 1), "S", 3, "plain", 33108 + i, motion="sway")
        tail.front.set(0, 2, "S1")
