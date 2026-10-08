"""Forager's Basket Harness: a laced bodice under a leather harness with a buckled chest strap, a sheathed
knife, and a deep wicker basket on her back with ferns and a forked stick poking out."""
from kit_f07 import prop, wicker_box
from kit_female import bodice, chemise, lacing

META = {
    "name": "Forager's Basket Harness",
    "gender": "female",
    "description": "A close-laced bodice under a leather carrying harness with a buckled chest strap and a sheathed knife, "
                   "and a deep wicker basket on her back spilling ferns.",
    "tags": ["work", "rugged"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 57401, neckline="scoop", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 10, "S1"), arm.strip.hline(0, 15, 11, "S2")
    b = bodice(g, "P", "weave", 57402, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "tight", lace="P3", eyelet=None)
    # The harness: shoulder straps down the front and back, joined by a buckled chest strap.
    for face in (b.front, b.back):
        for x in (1, 6):
            face.vline(x, 0, 9, "L2")
            face.set(x, 0, "L3")
    b.front.hline(1, 6, 4, "L1")
    b.front.set(3, 4, "M3"), b.front.set(4, 4, "M3"), b.front.set(3, 5, "M2")
    for x in (1, 6):
        b.top.vline(x, 0, 3, "L3")
    b.back.hline(1, 6, 8, "L1")
    # A sheathed foraging knife on the right strap.
    sheath = prop(g, "knife_sheath", "TORSO", (-.5, 0, -1), (1, 3, 1), pivot=(-2.6, 4.6, -2.25), role="L",
                  texture="leather", seed=57403, base=1)
    sheath.front.set(0, 0, "L3")
    hilt = prop(g, "knife_hilt", "TORSO", (-.5, -1, -1), (1, 1, 1), pivot=(-2.6, 4.6, -2.25), role="M", base=3,
                seed=57404, edge=False)
    hilt.top.fill("M4")

    # The basket: a deep wicker creel standing off her back, a lit rim and a cloth over the gatherings.
    basket = prop(g, "basket", "TORSO", (-3, 0, 0), (6, 8, 4), pivot=(0, .9, 2.4), role="L", seed=57405)
    wicker_box(basket, "L", 2, 57405)
    rim = prop(g, "basket_rim", "TORSO", (-3.5, 0, 0), (7, 1, 5), pivot=(0, .4, 1.9), role="L", texture="smooth",
               seed=57406, base=3, edge=False)
    for face in rim.sides:
        for x in range(face.w):
            face.set(x, 0, "L4" if x % 2 else "L3")
    rim.top.fill("S2"), rim.top.hline(0, 6, 4, "L3")
    for face in rim.sides:
        face.set(0, 0, "L2")
    # Ferns and a forked stick rising out of the back of the basket, clear of her head.
    for i, (x, h, z) in enumerate(((-2.4, 3, 5.0), (-1.0, 4, 5.4), (.4, 2, 5.0))):
        fern = prop(g, f"fern_{i}", "TORSO", (0, 0, 0), (1, h, 1), pivot=(x, .5 - h, z), role="A", texture="plain",
                    seed=57407 + i, base=2, edge=False)
        for face in fern.sides:
            for y in range(h):
                face.set(0, y, "A3" if y % 2 == 0 else "A1")
        fern.top.fill("A3")
    stick = prop(g, "forked_stick", "TORSO", (0, 0, 0), (1, 5, 1), pivot=(1.8, -4.1, 5.2), role="L", texture="smooth",
                 seed=57410, base=2, edge=False, rotation=(0, 0, -8))
    stick.top.fill("L3")
    fork = prop(g, "forked_stick_tip", "TORSO", (0, 0, 0), (1, 2, 1), pivot=(2.9, -4.6, 5.2), role="L", base=2,
                seed=57411, edge=False, rotation=(0, 0, 30))
    fork.top.fill("L3")
