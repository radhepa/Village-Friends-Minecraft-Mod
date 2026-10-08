"""Belted Everyday Skirt: a plain wool skirt with a leather belt whose long tipped tongue hangs down the front, and a purse at the hip."""
from kit_female import SKIRT_FRONT, shoes, side_pouch, skirt, waist_belt
from paint import solid

META = {
    "name": "Belted Everyday Skirt",
    "gender": "female",
    "description": "A plain everyday wool skirt girt with a leather belt whose long metal-tipped tongue hangs down the front, a little purse at the hip and ankle boots.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 60300, top=9.8, length=11, flare=5)
    s.band(0, "line", "P1", from_bottom=True)
    shoes(g, "ankle", "L", 2, top=9)
    belt = waist_belt(g, "waist_belt", 9.4, role="L", base=2, height=1, buckle=None)
    belt.front.set(6, 0, "M3"), belt.front.set(7, 0, "M2")             # the buckle off-centre
    # The tongue, pulled through and left to hang; it rides the front of the skirt.
    tongue = g.piece("waist_belt_tongue", "TORSO", (1.0, .3, -.45), (1, 5, 1), pivot=(0, s.top, SKIRT_FRONT),
                     motion="flap_front")
    solid(tongue, "L", "leather", 60301, 2, edge=False)
    for face in tongue.sides:
        face.set(0, 0, "L3")
        face.set(0, 4, "M3"), face.set(0, 3, "M2")                   # the metal strap-end
    tongue.bottom.fill("M2")
    purse = side_pouch(g, "waist_purse", side="right", y=9.9, size=(2, 3, 2), role="L", flap="M3")
    purse.front.hline(0, 1, 0, "L1")
