"""Mason's Leather Lap Apron: dusty trousers under a heavy leather lap apron on a strap, and laced ankle boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import flecks, lacing
from paint import solid

META = {
    "name": "Mason's Leather Lap Apron",
    "gender": "male",
    "description": "Stone-dusted trousers under a heavy leather lap apron strapped at the hip, with laced ankle boots.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "S", "twill", 3811, base=2, rows=(0, 9), crease=False)
    waistband(g, "S", "twill", 3812)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        flecks(leg.strip, "S4", 3813, .06, rows=range(0, 9))
        leg.front.rect(1, 4, 2, 2, "S1")                              # kneeling wear
        lacing(pants.front, 1, 9, 10, "L3", "L1")
    strap = g.piece("waist_apron_strap", "TORSO", (-4.6, 9.8, -2.6), (9, 1, 5), inflate=.05)
    solid(strap, "L", "leather", 3814, 2, edge=False)
    strap.right.set(1, 0, "M3")
    apron = g.piece("lap_apron", "TORSO", (-3.5, 0, 0), (7, 7, 1), pivot=(0, 10.4, -2.95), motion="flap_front")
    solid(apron, "L", "leather", 3815, 2)
    f = apron.front
    f.hline(0, 6, 0, "L3"), f.vline(0, 1, 6, "L1"), f.vline(6, 1, 6, "L1"), f.hline(0, 6, 6, "L0")
    f.set(1, 4, "L1"), f.set(2, 5, "L1"), f.set(4, 2, "L3"), f.set(5, 3, "L3")   # chisel scratches
