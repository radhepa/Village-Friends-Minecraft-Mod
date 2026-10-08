"""Alchemist's Retort Bodice: a cross-laced leather bodice over a linen chemise, stitched leather guards
on the forearms, a bandolier of stoppered vials across the breast and a glass retort slung at the hip,
its long beak reaching across her lap."""
from kit_female import arm_rings, bodice, chemise, lacing
from kit_f05 import dangle, fixed, glass
from paint import line

META = {
    "name": "Alchemist's Retort Bodice",
    "gender": "female",
    "description": "A laced leather bodice with forearm guards, a bandolier of stoppered vials and a glass retort slung at the hip.",
    "tags": ["work", "rugged", "whimsical"],
}


def build(g):
    chemise(g, "S", 3, "weave", 55321, neckline="square", sleeve_rows=(0, 11))
    b = bodice(g, "L", "leather", 55322, base=2, rows=(2, 9), neckline="square", edge="L3")
    lacing(b.front, 3, 3, 8, "x", lace="S3", under="L0", eyelet="M3")
    # Stitched leather guards against sparks and spills.
    for box in arm_rings(g, "forearm_guard", 4.6, 4, 5, inflate=.06):
        for face in box.faces:
            for y in range(face.h):
                face.hline(0, face.w - 1, y, "L2")
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 3, "L1")
            for y in (1, 2):
                face.set(face.w // 2, y, "S2" if y == 1 else "L1")       # the stitched seam
    # The bandolier from the left shoulder to the right hip, its loops holding three vials.
    j = g.part("jacket")
    line(j.front, 7, 0, 0, 8, "K2"), line(j.front, 7, 1, 1, 8, "K1")
    line(j.back, 0, 0, 7, 8, "K2"), line(j.back, 0, 1, 6, 8, "K1")
    j.top.vline(7, 0, 3, "K2")
    for i, ((x, y), fill) in enumerate((((1.4, 2.9), "A3"), ((0.0, 4.5), "P3"), ((-1.4, 6.1), "M3"))):
        vial = fixed(g, f"vial_{i}", (x, y, -2.75), (1, 2, 1), "S", 4, "plain", 55323 + i, edge=False)
        glass(vial, "S", 4, fill=fill, fill_from=1)
        cork = fixed(g, f"vial_cork_{i}", (x, y - 1.5, -2.75), (1, 1, 1), "L", 3, "plain", 55326 + i, edge=False)
        cork.top.fill("L4")
    # The retort in a leather sling at the right hip: a glass bulb and its long beak.
    sling = dangle(g, "retort_sling", -2.5, -.6, (1, 1, 1), "L", 1, "plain", top=9.0, seed=55329, edge=False)
    sling.front.fill("L2")
    bulb = dangle(g, "retort_bulb", -2.5, .4, (3, 3, 2), "S", 4, "plain", top=9.0, seed=55330)
    glass(bulb, "S", 4, fill="A2", fill_from=2)
    for face in bulb.sides:
        face.set(0, 1, "S4"), face.set(face.w - 1, 0, "S3")
    beak = dangle(g, "retort_beak", .5, .4, (3, 1, 1), "S", 3, "plain", top=9.0, seed=55331, edge=False)
    for face in beak.sides:
        face.hline(0, face.w - 1, 0, "S3")
        face.set(face.w - 1, 0, "S4")
    tip = dangle(g, "retort_beak_tip", 2.5, 1.2, (1, 1, 1), "S", 3, "plain", top=9.0, seed=55332, edge=False)
    tip.front.fill("S3")
