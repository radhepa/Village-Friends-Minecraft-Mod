"""Patched Workpants: canvas trousers with a mended knee, suspenders and scuffed work boots."""
from paint import fabric, k, rnd, strip_fabric

META = {
    "name": "Patched Workpants",
    "gender": "male",
    "description": "Sturdy canvas trousers, a stitched knee patch, suspenders and lace-up boots.",
    "tags": ["work", "sturdy", "simple"],
}


def boot(leg, pants, seed):
    # Lace-up work boot: base leg rows 9-11, a chunkier shaft on the overlay rows 8-11.
    strip_fabric(leg, "L", "leather", seed, 2, 9, 11)
    leg.strip.hline(0, leg.strip.w - 1, 11, "K1")
    strip_fabric(pants, "L", "leather", seed + 1, 2, 8, 11)
    for f in pants.sides:
        f.hline(0, f.w - 1, 8, "L3")
        f.hline(0, f.w - 1, 11, "K1")
    fr = pants.front
    fr.set(1, 9, "S3"), fr.set(2, 9, "S3"), fr.set(1, 10, "L1"), fr.set(2, 10, "S3")
    fr.hline(0, 3, 11, "K0")
    fr.set(1, 11, "L3"), fr.set(2, 11, "L3")  # scuffed toe cap
    leg.bottom.fill("K1")
    pants.bottom.fill("K0")


def build(g):
    for side, leg_name, pants_name in (("right", "right_leg", "right_pants"), ("left", "left_leg", "left_pants")):
        leg, pants = g.part(leg_name), g.part(pants_name)
        strip_fabric(leg, "S", "twill", 21 if side == "right" else 22, 2, 0, 8)
        fabric(leg.top, "S", "twill", 5, 2)
        # Outer side seam and a pressed fold catching light down the front.
        outer = leg.right if side == "right" else leg.left
        for y in range(9):
            outer.set(1 if side == "right" else 2, y, "S1")
        leg.front.vline(1 if side == "right" else 2, 1, 7, "S3")
        leg.strip.hline(0, leg.strip.w - 1, 8, "S1")  # cuff shadow over the boot
        # Knee wrinkles.
        leg.front.set(0, 5, "S1"), leg.front.set(3, 6, "S1"), leg.back.set(1, 4, "S1"), leg.back.set(2, 4, "S1")
        boot(leg, pants, 31 if side == "right" else 32)
        # Folded hem resting on the boot.
        for f in pants.sides:
            f.hline(0, f.w - 1, 7, "S3")
        if side == "right":
            # Mended knee: a primary patch with ink running stitches.
            fr = leg.front
            for y in range(3, 7):
                for x in range(0, 3):
                    fr.set(x, y, k("P", 2 + (1 if rnd(x, y, 9) > .75 else 0)))
            for x, y in [(0, 3), (1, 3), (2, 3), (2, 4), (2, 5), (2, 6), (0, 6), (1, 6)]:
                if (x + y) % 2 == 0:
                    fr.set(x, y, "K2")

    body, jacket = g.part("body"), g.part("jacket")
    # Waistband with belt loops (rows 9-11) under the tucked shirt.
    strip_fabric(body, "S", "twill", 7, 2, 9, 11)
    for f in body.sides:
        f.hline(0, f.w - 1, 9, "S3")
        for x in range(1, f.w, 3):
            f.set(x, 10, "S1")
    body.front.set(3, 10, "M3"), body.front.set(4, 10, "M1")  # fly button
    fabric(body.bottom, "S", "twill", 6, 1)
    # Suspenders on the jacket layer, buttoned to the waistband.
    jf, jb = jacket.front, jacket.back
    for x in (1, 6):
        for y in range(0, 10):
            jf.set(x, y, "A3" if x == 1 else "A2")
        jf.set(x, 9, "M3")
    for y in range(0, 10):
        # Crossed at the shoulder blades.
        t = y / 9
        xa = round(1 + (6 - 1) * t * (1 if y < 5 else 1))
        jb.set(min(7, max(0, round(1 + 5 * t))), y, "A2")
        jb.set(min(7, max(0, round(6 - 5 * t))), y, "A2")
    jb.set(1, 9, "M3"), jb.set(6, 9, "M3")
    jacket.top.set(1, 3, "A2"), jacket.top.set(6, 3, "A2"), jacket.top.set(1, 0, "A2"), jacket.top.set(6, 0, "A2")
    for y in range(4):
        jacket.top.set(1, y, "A2"), jacket.top.set(6, y, "A2")
