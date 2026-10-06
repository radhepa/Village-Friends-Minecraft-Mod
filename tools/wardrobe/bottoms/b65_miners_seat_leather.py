"""Miner's Seat Leather: twill trousers with patched knees and a hard leather seat flap strapped behind for sliding the adits."""
from kit import SIDES, footwear, legs, waistband
from paint import solid

META = {
    "name": "Miner's Seat Leather",
    "gender": "male",
    "description": "Hard-wearing twill trousers with leather knee patches and a stiff leather seat flap strapped behind, for sliding down the adits.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 6511, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 6512)
    footwear(g, "boot", top=9, base=1)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.front.rect(0, 3, 4, 3, "L2")
        leg.front.hline(0, 3, 3, "L3"), leg.front.hline(0, 3, 5, "L1")
    strap = g.piece("waist_seat_strap", "TORSO", (-4.6, 9.8, -2.6), (9, 1, 5), inflate=.06)
    solid(strap, "L", "leather", 6513, 1, edge=False)
    seat = g.piece("seat_leather", "TORSO", (-4, 0, 0), (8, 5, 1), pivot=(0, 10.2, 1.95), motion="flap_back")
    solid(seat, "L", "leather", 6514, 2)
    f = seat.back
    f.hline(0, 7, 0, "L3"), f.vline(0, 1, 4, "L1"), f.vline(7, 1, 4, "L1")
    for x in range(8):
        f.set(x, 4, "L3" if x % 2 else "L1")                               # rounded, stitched edge
    f.set(2, 2, "L1"), f.set(5, 3, "L1")
