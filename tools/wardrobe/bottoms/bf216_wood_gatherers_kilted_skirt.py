"""Wood Gatherer's Kilted Skirt: an overskirt whose front is kilted up into a bulging pouch full of
kindling, over a long striped-hem petticoat and turnshoes."""
from kit_f07 import prop
from kit_female import SKIRT_FRONT, shoes, skirt, stockings_row, trim
from paint import fabric, solid

META = {
    "name": "Wood Gatherer's Kilted Skirt",
    "gender": "female",
    "description": "A wool overskirt with its front kilted up into a bulging pouch of kindling, over a long "
                   "petticoat with a striped hem, and soft turnshoes.",
    "tags": ["work", "casual", "skirt"],
}

TOP = 9.8


def build(g):
    s = skirt(g, "P", "weave", 57621, top=TOP, length=6, back_length=11, side_length=8, flare=5)
    s.back.back.hline(0, 9, 10, "P1")
    # The petticoat showing below the kilted front.
    pet = g.piece("skirt_petticoat", "TORSO", (-4.5, 0, 0), (9, 11, 1), pivot=(0, TOP, SKIRT_FRONT + .1),
                  motion="flap_front")
    solid(pet, "S", "weave", 57622, 3)
    trim(pet.front, 7, "double", "A2")
    pet.front.hline(0, 8, 10, "S1")
    for x in range(1, 9, 2):
        pet.front.vline(x, 1, 6, "S2")
    # The kilted pouch: the overskirt's hem drawn up to the belly, bulging with kindling.
    pouch = prop(g, "waist_kilted_pouch", "TORSO", (-4.5, 3, -1.3), (9, 3, 2), pivot=(0, TOP, SKIRT_FRONT),
                 role="P", texture="weave", seed=57623, base=2, motion="flap_front")
    for x in range(pouch.front.w):
        pouch.front.set(x, 0, "P3" if x % 3 else "P1")
        pouch.front.set(x, 2, "P1" if x % 2 else "P2")
    pouch.front.set(0, 1, "P1"), pouch.front.set(8, 1, "P1")
    fabric(pouch.top, "L", "smooth", 57624, 2)
    for x in range(0, 9, 2):
        pouch.top.set(x, 0, "L4"), pouch.top.set(x + 1, 1, "L3")
    for i, (x, h) in enumerate(((-3.2, 2), (-1.4, 3), (.6, 2), (2.4, 3))):
        stick = prop(g, f"waist_kindling_{i}", "TORSO", (x, 3 - h, -1.0), (1, h, 1), pivot=(0, TOP, SKIRT_FRONT),
                     role="L", base=2 + i % 2, seed=57625 + i, edge=False, motion="flap_front")
        stick.top.fill("L4")
    for side in ("right", "left"):
        leg = g.part(f"{side}_leg")
        fabric(leg.strip, "S", "weave", 57629, 1, 0, 4, leg.strip.w, 6)   # the petticoat round the legs
    stockings_row(g, "S", 10, 10, base=2)
    shoes(g, "turnshoe", "L", 2, top=11)
