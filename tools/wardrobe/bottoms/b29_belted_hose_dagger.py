"""Belted Hose & Dagger: fitted hose and a plaque belt carrying a sheathed dagger and a small purse."""
from kit import footwear, legs, waistband
from paint import rivets, solid

META = {
    "name": "Belted Hose & Dagger",
    "gender": "male",
    "description": "Fitted hose, a plaque-studded belt with a sheathed dagger at the hip and a small purse.",
    "tags": ["fancy", "slim"],
}


def build(g):
    legs(g, "P", "velvet", 2901, rows=(0, 10), crease=False)
    waistband(g, "P", "velvet", 2902)
    belt_box = g.piece("waist_belt", "TORSO", (-4.6, 10.2, -2.6), (9, 1, 5), inflate=.06)
    solid(belt_box, "L", "leather", 2903, 2, edge=False)
    for face in belt_box.sides:
        rivets(face, 0, start=1, step=2)
    sheath = g.piece("waist_dagger_sheath", "TORSO", (-.5, 0, -.5), (1, 5, 1), pivot=(-4.8, 10.6, -.6), rotation=(0, 0, 16), inflate=.05)
    solid(sheath, "L", "leather", 2904, 1)
    sheath.strip.hline(0, sheath.strip.w - 1, 4, "M3")
    grip = g.piece("waist_dagger_grip", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(-4.8, 10.6, -.6), rotation=(0, 0, 16))
    solid(grip, "L", "leather", 2905, 3, edge=False)
    grip.strip.hline(0, grip.strip.w - 1, 0, "M4")
    guard = g.piece("waist_dagger_guard", "TORSO", (-.5, -.4, -1.5), (1, 1, 3), pivot=(-4.8, 10.6, -.6), rotation=(0, 0, 16))
    solid(guard, "M", "smooth", 2906, 3, edge=False)
    purse = g.piece("waist_purse", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(2.6, 10.8, -2.9))
    solid(purse, "A", "plain", 2907, 2)
    purse.front.set(0, 0, "A3"), purse.front.set(1, 1, "M3")
    footwear(g, "shoe", top=10)
