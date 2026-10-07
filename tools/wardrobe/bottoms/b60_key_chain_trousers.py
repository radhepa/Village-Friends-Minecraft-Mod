"""Key-Chain Trousers: sturdy twill trousers with a long chain of iron keys swinging at the thigh, and ankle boots."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from paint import solid

META = {
    "name": "Key-Chain Trousers",
    "gender": "male",
    "description": "Sturdy twill trousers with a steward's long chain of iron keys swinging at the right thigh, and plain ankle boots.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 6011, rows=(0, 9))
    waistband(g, "P", "twill", 6012)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        g.part(f"{side}_pants").strip.hline(0, 15, 9, "L3")
    bone = leg_bone("right")
    chain = g.piece("key_chain", bone, (-.5, 0, -.5), (1, 4, 1), pivot=(-2.45, -.2, -.6))
    for face in chain.faces:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, "M3" if y % 2 else "M1")
    ring = g.piece("key_ring", bone, (-.5, 0, -1), (1, 2, 2), pivot=(-2.45, 3.8, -.6))
    solid(ring, "M", "smooth", 6013, 2)
    ring.right.set(0, 0, "M4"), ring.right.set(1, 1, "M0")
    for i, (dz, h) in enumerate(((-.8, 3), (.4, 2))):
        key = g.piece(f"key_{i}", bone, (-.5, 0, -.5), (1, h, 1), pivot=(-2.45, 5.6, -.6 + dz))
        solid(key, "M", "smooth", 6014 + i, 2 + i)
        key.strip.hline(0, key.strip.w - 1, h - 1, "M4")
