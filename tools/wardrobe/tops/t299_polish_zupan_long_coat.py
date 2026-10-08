"""Polish Zupan Long Coat: a close ankle-length coat buttoned down the front, a stand collar, pointed cuffs and a broad silk sash with figured ends."""
from kit import SIDES, body, collar, sleeves
from kit_male import sash
from kit_m08 import coat_skirt, fringe, hanging_tail

META = {
    "name": "Polish Zupan Long Coat",
    "gender": "male",
    "description": "A close-fitting zupan reaching to the shin, a long row of small buttons from collar to waist, pointed cuffs and a broad striped silk sash whose figured ends hang at the hip.",
    "tags": ["fancy", "tailored"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 38121)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    for y in range(1, 12):
        f.set(3, y, "P0")                                                  # the closing edge
        f.set(4, y, "M3" if y % 2 else "P1")                               # close-set buttons and loops
    b.back.vline(3, 2, 11, "P1")
    stand = collar(g, "stand_collar", "A", "plain", base=2, height=1, y=-.5)
    for face in stand.sides:
        face.set(face.w // 2, 0, "M3")
    sleeves(g, "P", "twill", 38122, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2")
        arm.strip.hline(0, arm.strip.w - 1, 10, "A1")
        outer = arm.right if side == "right" else arm.left
        outer.set(1, 8, "A2"), outer.set(2, 8, "A2"), outer.set(1, 7, "A3")   # the pointed cuff
        arm.front.vline(2, 2, 8, "P1")
    band = sash(g, "pas_sash", "A", y=8.4, height=3, texture="smooth", seed=38123, tails=())
    for face in band.sides:
        face.hline(0, face.w - 1, 0, "A3")
        for x in range(face.w):
            face.set(x, 1, "M3" if x % 3 == 0 else "A1")                  # woven gold stripe
        face.hline(0, face.w - 1, 2, "A2")
    for i, (x, z, rz) in enumerate(((2.0, -3.15, -3), (3.3, -3.3, 5))):
        end = hanging_tail(g, f"pas_end_{i}", (x, 10.6, z), (2, 5, 1), "A", "smooth", 38124 + i, rotation=(0, 0, rz))
        for face in (end.front, end.back):
            face.set(0, 1, "M3"), face.set(1, 2, "M3"), face.set(0, 3, "A4")   # figured end panel
            face.hline(0, 1, 0, "A3")
            fringe(face, 4, "A3", "A1")
    front, back, sides = coat_skirt(g, "zupan_skirt", 10, "P", "twill", 38126, top=10.6)
    front.vline(4, 1, 9, "P0")
    front.hline(0, 8, 9, "P1"), back.hline(0, 8, 9, "P1")
    back.vline(4, 3, 9, "P1")
