"""Rumpled Slouch Boots: close hose in soft unlined boots that slump into loose folds round the calf."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Rumpled Slouch Boots",
    "gender": "male",
    "description": "Close twill hose in soft unlined boots that slump into loose rumpled folds round the calf.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    legs(g, "S", "twill", 5011, rows=(0, 4), crease=False)
    waistband(g, "S", "twill", 5012)
    footwear(g, "boot", top=4, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            for x in range(face.w):
                if (x + face.x0) % 4 != 0:
                    face.set(x, 6, "L3"), face.set(x, 7, "L1")             # two slumped folds
                if (x + face.x0) % 4 != 2:
                    face.set(x, 8 + (x % 2), "L3")
    for ring in leg_rings(g, "slouch", 3.0, "L", (5, 2, 5), 2, "leather", 5013, inflate=.12):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 1, "L1")
            face.set(1, 1, "L2")
