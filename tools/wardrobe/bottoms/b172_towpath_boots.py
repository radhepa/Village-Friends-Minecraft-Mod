"""Towpath Boots: twill trousers tucked into knee boots laced up the front over a padded tongue, splashed with towpath
mud and strapped at the ankle."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import flecks, leg_rings
from paint import solid

META = {
    "name": "Towpath Boots",
    "gender": "male",
    "description": "Twill trousers tucked into knee boots laced up the front over tall padded tongues, splashed with "
                   "towpath mud and strapped at the ankle.",
    "tags": ["rugged", "sturdy", "work"],
}


def build(g):
    legs(g, "P", "twill", 33060, rows=(0, 4), crease=False)
    waistband(g, "P", "twill", 33061)
    footwear(g, "boot", top=4, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, 15, 4, "P1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "L3")
            face.vline(0, 5, 9, "L1"), face.vline(face.w - 1, 5, 9, "L1")
        for y in range(5, 10):                                          # lacing up the front
            pants.front.set(1, y, "L3" if y % 2 else "L1"), pants.front.set(2, y, "L1" if y % 2 else "L3")
        for face in pants.sides:                                        # a tide line of towpath mud
            face.hline(0, face.w - 1, 9, "K2")
            face.hline(0, face.w - 1, 10, "K1")
        for x in (1, 6, 10, 13):                                         # splashes above the tide line
            pants.strip.set(x, 8, "K2")
        flecks(leg.strip, "P1", 33066 + i, .08, rows=range(2, 4))       # mud flung up the trousers
        # The padded tongue stands proud of the lacing and flares forward at the top.
        tongue = g.piece(f"{side}_boot_tongue", leg_bone(side), (-1, -3, -.5), (2, 3, 1), pivot=(0, 5.6, -2.2),
                         rotation=(12, 0, 0))
        solid(tongue, "L", "leather", 33068 + i, 3)
        tongue.front.hline(0, 1, 0, "L4")
        tongue.front.set(0, 2, "L2"), tongue.front.set(1, 2, "L2")
    for ring in leg_rings(g, "ankle_strap", 8.6, "L", (5, 1, 5), 1, "leather", 33070, inflate=.06):
        ring.right.set(2, 0, "M3"), ring.left.set(1, 0, "M3")
