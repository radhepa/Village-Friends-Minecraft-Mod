"""Poultry-Yard Clogs and Skirt: a mid-calf skirt with a single bright band, thick knitted socks rolled at the
top and carved wooden sabots with long upturned toes for the hen-run muck."""
from kit import SIDES, leg_bone
from kit_female import leg_ring_fold, shoes, skirt
from paint import k, solid, strip_fabric

META = {
    "name": "Poultry-Yard Clogs and Skirt",
    "gender": "female",
    "description": "A mid-calf skirt with one bright band, thick knitted socks rolled at the top and carved wooden sabots with long upturned toes.",
    "tags": ["work", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51300, top=9.8, length=9, flare=6)
    s.band(3, "line", "A2", from_bottom=True)
    s.band(2, "line", "A1", from_bottom=True)
    s.hem("P1")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "knit", 51301 + (side == "left"), 2, 7, 10)
    for box in leg_ring_fold(g, "sock_roll", 6.8, role="S", base=2):
        for f in box.sides:
            for x in range(1, f.w, 2):
                f.set(x, 1, "S1")
    shoes(g, "clog", "L", 3, top=10)
    # The sabot's carved toe: a long block running ahead of the foot with an upturned tip.
    for side in SIDES:
        toe = g.piece(f"{side}_sabot_toe", leg_bone(side), (-2, 0, -2), (4, 2, 2), pivot=(0, 10.0, -1.9), inflate=.12)
        solid(toe, "L", "smooth", 51303, 3, edge=False)
        for f in toe.sides:
            f.hline(0, f.w - 1, 0, "L4"), f.hline(0, f.w - 1, 1, k("L", 2))
        toe.bottom.fill("L0")
        tip = g.piece(f"{side}_sabot_tip", leg_bone(side), (-1, -1, -1), (2, 1, 1), pivot=(0, 10.4, -3.4),
                      rotation=(-30, 0, 0), inflate=.05)
        solid(tip, "L", "smooth", 51304, 3, edge=False)
        tip.top.fill("L4")
