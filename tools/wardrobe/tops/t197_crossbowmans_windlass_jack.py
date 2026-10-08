"""Crossbowman's Windlass Jack: a jack quilted in level bands with a spanning hook at the belt, a bolt case and a windlass."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import blk, lacing
from kit_m04 import hanging, qrows

META = {
    "name": "Crossbowman's Windlass Jack",
    "gender": "male",
    "description": "A crossbowman's jack quilted in level bands and laced up the front, with an iron spanning hook on the belt, "
                   "a lidded bolt case at the right hip and a cranked windlass slung at the left.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}

S = 34040


def build(g):
    b = body(g, "P", "quilt", S)
    for face in b.sides:
        qrows(face, "P", 2, step=3, rows=range(1, 12))
    lacing(b.front, 3, 1, 8, "L3", "L1")                                  # laced closure
    b.front.vline(3, 9, 11, "P0"), b.front.vline(4, 9, 11, "P1")
    sleeves(g, "P", "quilt", S + 1, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        qrows(arm.strip, "P", 2, step=3, rows=range(0, 9), offset=1)
        sl = g.part(f"{side}_sleeve")
        for y in (8, 9, 10):                                               # leather wrist cuffs
            sl.strip.hline(0, sl.strip.w - 1, y, "L3" if y == 8 else "L2" if y == 9 else "L1")
    high = collar(g, "padded_collar", "P", "quilt", base=2, height=2, y=-1.2)
    for face in high.sides:
        face.hline(0, face.w - 1, 0, "P3"), face.hline(0, face.w - 1, 1, "P1")
    high.front.vline(4, 0, 1, "L2")
    belt = blk(g, "belt", (0, 9.4, 0), (9, 2, 5), "L", 2, "leather", S + 2, inflate=.06, edge=False)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    belt.front.set(2, 1, "M3")
    # The spanning hook: a forked iron claw hanging from the belt front.
    claw = blk(g, "spanning_hook", (0, 10.9, -2.95), (2, 1, 1), "M", 2, "smooth", S + 3, edge=False)
    claw.front.fill("M3")
    for i, x in enumerate((-.5, .5)):
        prong = hanging(g, f"spanning_hook_prong_{i}", x, 11.9, (1, 2, 1), "M", 2, "smooth", S + 4 + i, top=11.0,
                        dz=.4)
        prong.front.set(0, 0, "M3"), prong.front.set(0, 1, "M4")
    # Lidded bolt case on the right hip, fletchings showing under the lid.
    case = hanging(g, "bolt_case", -3.0, 10.0, (2, 5, 2), "L", 2, "leather", S + 6, top=10.4)
    for face in case.sides:
        face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 1, "L1")
        face.vline(face.w - 1, 2, 4, "L1")
    case.front.set(0, 3, "M3")
    for i, (x, y) in enumerate(((-3.5, 9.0), (-2.5, 9.3))):
        fletch = hanging(g, f"bolt_fletch_{i}", x, y, (1, 1, 1), "A", 3, "plain", S + 8 + i, top=10.4, dz=-.5)
        fletch.top.fill("A4"), fletch.front.fill("A2")
    # The windlass: a pulley block with two cranks, slung behind the left hip.
    drum = hanging(g, "windlass_drum", 1.6, 10.4, (3, 3, 2), "M", 2, "smooth", S + 11, top=10.4, z=1.85, front=False)
    for face in drum.sides:
        face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 2, "M1")
    drum.back.set(1, 1, "M4")
    crank = hanging(g, "windlass_crank", 1.6, 11.4, (4, 1, 1), "L", 3, "plain", S + 12, top=10.4, z=1.85, front=False, dz=2.0)
    crank.back.set(1, 0, "L1"), crank.back.set(2, 0, "L1")
    for i, x in enumerate((0.1, 3.1)):
        knob = hanging(g, f"windlass_knob_{i}", x, 10.4, (1, 2, 1), "L", 2, "plain", S + 13 + i, top=10.4,
                       z=1.85, front=False, dz=2.0)
        knob.back.set(0, 0, "L3")
    for face in flaps(g, "jack_skirt", 3, "P", "quilt", S + 16, top=10.8, slit=True):
        qrows(face, "P", 2, step=3, rows=range(1, 3))
        face.hline(0, 8, 2, "P1")
