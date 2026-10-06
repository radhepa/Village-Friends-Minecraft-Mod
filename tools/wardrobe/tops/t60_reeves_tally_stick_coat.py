"""Reeve's Tally-Stick Coat: a toggled wool coat with a bundle of notched tally sticks and a wax tablet at the belt."""
from kit import belt, body, collar, flaps, sleeves
from kit_male import blk, toggles

META = {
    "name": "Reeve's Tally-Stick Coat",
    "gender": "male",
    "description": "The manor reeve's toggled wool coat with a pale collar, notched tally sticks bundled at the belt and a wax tablet.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 6001)
    b.front.vline(3, 0, 11, "P0"), b.front.vline(4, 0, 11, "P3")
    toggles(b.front, 2, (2, 5, 8), "L4", "L1")
    sleeves(g, "P", "twill", 6002, rows=(0, 10), cuff="S2")
    pale = collar(g, "collar", "S", "weave", base=3, height=1, y=-.6)
    pale.front.set(4, 0, "S1")
    belt(g, "belt", 9.4, height=1)
    for i, (x, h) in enumerate(((-3.4, 4), (-2.8, 3), (-2.2, 4))):
        stick = blk(g, f"tally_stick_{i}", (x, 8.6, -2.8), (1, h, 1), "L", 4, "plain", 6003 + i, rotation=(0, 0, 6 - 6 * i))
        for y in range(0, h, 2):
            stick.front.set(0, y, "K3")                                  # notches
    blk(g, "tally_tie", (-2.8, 9.6, -2.95), (3, 1, 1), "L", 1, "leather", 6006, edge=False)
    tablet = blk(g, "wax_tablet", (2.8, 10.0, -2.8), (2, 3, 1), "L", 3, "plain", 6007)
    tablet.front.rect(0, 0, 2, 2, "A1"), tablet.front.set(1, 1, "A3"), tablet.front.hline(0, 1, 2, "L2")
    for face in flaps(g, "coat_skirt", 4, "P", "twill", 6008, top=10.8, slit=True):
        face.hline(0, 8, 3, "P1")
