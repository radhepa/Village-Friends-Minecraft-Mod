"""Verderer's Antler-Button Jerkin: a winged forest-court jerkin closed with antler toggles, an oak badge and the iron dog-gauge stirrup at the belt."""
from kit import SIDES, belt, body, flaps, neckline, sleeves
from kit_male import arm_blk, blk
from kit_m07 import coil
from paint import fabric, grid, k, strip_fabric

META = {
    "name": "Verderer's Antler-Button Jerkin",
    "gender": "male",
    "description": "A forest-court officer's winged jerkin over a full shirt, closed with three antler toggles on leather loops, an oak-leaf badge on the breast and the iron dog-gauge stirrup hung at his belt.",
    "tags": ["tailored", "rugged", "casual"],
    "covers_waist": True,
}

BADGE = [".m.",
         "mam",
         ".m."]


def metal(box, role="M", base=2):
    for face in box.faces:
        fabric(face, role, "smooth", 37164, base)
    return box


def build(g):
    b = body(g, "S", "weave", 37160, base=3)                             # the shirt
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 37161, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "S2"), arm.strip.hline(0, arm.strip.w - 1, 10, "S1")
    jacket = g.part("jacket")                                            # the jerkin
    strip_fabric(jacket, "P", "twill", 37162, 2, 0, 11)
    fabric(jacket.top, "P", "twill", 37162, 3)
    fabric(jacket.bottom, "P", "twill", 37163, 1)
    jf = jacket.front
    for y in range(12):
        jf.set(3, y, "P1"), jf.set(4, y, "P1")                           # the jerkin meets edge to edge
    for x in (2, 3, 4, 5):
        jf.clear(x, 0)
    jf.clear(3, 1), jf.clear(4, 1)
    for y in (3, 6, 9):
        jf.set(2, y, "L1"), jf.set(5, y, "L1")                          # leather loops for the toggles
    grid(jf, 0, 2, BADGE, {"m": "M3", "a": "A2"})                       # the forest court's brass badge
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "P1")
    # Three antler toggles across the closure.
    for i, y in enumerate((3.1, 6.1, 9.1)):
        t = blk(g, f"antler_toggle_{i}", (0, y, -2.45), (3, 1, 1), "S", 4, "plain", 37165 + i, edge=False,
                rotation=(0, 0, 8 if i % 2 else -8))
        t.front.set(0, 0, "S2"), t.front.set(2, 0, "S3")
        t.top.set(1, 0, "S4"), t.bottom.fill("S2")
    # Jerkin wings: stiff rolled welts over the shoulder seams.
    for side in SIDES:
        wing = arm_blk(g, f"{side}_wing", side, -1.8, (5, 2, 5), "P", 2, "twill", 37170, inflate=.02)
        for face in wing.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 2 else "P2")
            face.hline(0, face.w - 1, 1, "P1")
    belt(g, "belt", 9.5, height=1)
    # The dog-gauge: an iron stirrup a hound's paw had to pass through, hung from the left of the belt.
    strap = blk(g, "gauge_strap", (2.6, 10.0, -3.1), (1, 2, 1), "L", 2, "plain", 37171, edge=False,
                motion="flap_front")
    strap.front.set(0, 0, "L3")
    for bar in coil(g, "dog_gauge", (2.6, 11.6, -3.3), size=3, thick=1, depth=1, role="M", base=2, painter=metal,
                    hang=True, motion="flap_front"):
        bar.front.set(0, 0, k("M", 3))
    for face in flaps(g, "jerkin_skirt", 3, "P", "twill", 37172, top=10.4):
        face.vline(4, 0, 2, "P1")
        face.hline(0, 8, 2, "P1")
