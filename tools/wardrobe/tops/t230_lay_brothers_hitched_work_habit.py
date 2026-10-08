"""Lay Brother's Hitched Work Habit: a working habit with its front skirts hitched up into the belt, long behind, hood thrown back and sleeves pushed up, a wooden costrel at the hip."""
from kit import belt, body, roll, side_panels, sleeves
from kit_male import blk, hood_down
from paint import fabric, solid

META = {
    "name": "Lay Brother's Hitched Work Habit",
    "gender": "male",
    "description": "A lay brother's coarse working habit with its front skirts hitched up into the belt for the fields, still long behind, the hood thrown back, sleeves shoved past the elbow and a hooped wooden costrel at his hip.",
    "tags": ["holy", "work", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 35360, base=1)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "P0"), f.set(5, 0, "P0")
    f.vline(3, 1, 3, "P0")                                              # slit neck
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P0"), face.vline(6, 3, 11, "P0")
    sleeves(g, "P", "weave", 35361, base=1, rows=(0, 4))
    for side in ("right", "left"):                                      # bare forearms below the pushed-up sleeves
        arm = g.part(f"{side}_arm")
        fabric(arm.strip, "S", "weave", 35362, 3, 0, 5, arm.strip.w, 2)
    roll(g, "P", 2.4, base=2, prefix="pushed_sleeve")
    hood_down(g, "P", "weave", 35363, base=1, y=-1.1, z=3.1, tilt=12, lining="P0")
    belt(g, "work_belt", 9.4, height=1)
    # The hitch: the front skirt hauled up and bunched over the belt, corners tucked in at the hips.
    bunch = g.piece("hitched_bunch", "TORSO", (-4.5, 0, -1), (9, 2, 1), pivot=(0, 10.2, -2.0), inflate=.1)
    solid(bunch, "P", "weave", 35364, 2, edge=False)
    for x in range(0, 9, 2):
        bunch.front.vline(x, 0, 1, "P1")
    bunch.front.hline(0, 8, 0, "P3")
    for name, x, rz in (("hitched_corner_right", -3.4, 28), ("hitched_corner_left", 3.4, -28)):
        corner = g.piece(name, "TORSO", (-1, 0, -.5), (2, 3, 1), pivot=(x, 10.0, -2.9), rotation=(0, 0, rz),
                         motion="flap_front")
        solid(corner, "P", "weave", 35365, 1)
        corner.front.vline(0, 0, 2, "P2")
    front = g.piece("habit_front", "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 11.6, -2.85), motion="flap_front")
    solid(front, "P", "weave", 35366, 1)
    for x in (1, 4, 7):
        front.front.vline(x, 0, 2, "P0")
    front.front.hline(0, 8, 0, "P2")
    back = g.piece("habit_back", "TORSO", (-4.5, 0, 0), (9, 9, 1), pivot=(0, 11.4, 1.85), motion="flap_back")
    solid(back, "P", "weave", 35367, 1)
    for x in (2, 6):
        back.back.vline(x, 0, 8, "P0")
    back.back.hline(0, 8, 8, "P0")
    side_panels(g, "habit_side", 5, "P", "weave", top=11.4)
    # A hooped wooden costrel on a thong at the left hip.
    costrel = blk(g, "costrel", (3.0, 9.6, -2.9), (2, 3, 2), "L", 3, "plain", 35368, motion="flap_front")
    for face in costrel.sides:
        face.hline(0, face.w - 1, 0, "M2"), face.hline(0, face.w - 1, 2, "M2")
    spout = blk(g, "costrel_spout", (3.0, 9.0, -2.9), (1, 1, 1), "L", 2, "plain", 35369, motion="flap_front", edge=False)
    spout.top.fill("L0")
