"""Sergeant's Splinted Boots: dark trousers in knee boots armed with three raised steel splints down each shin."""
from kit import SIDES, footwear, leg_ring, legs, waistband
from kit_m04 import leg_prop, sides_of

META = {
    "name": "Sergeant's Splinted Boots",
    "gender": "male",
    "description": "Dark wool trousers in turned-cuff knee boots, each shin armed with three raised steel splints riveted"
                   " between two buckled leather straps.",
    "tags": ["martial", "sturdy"],
}

S = 34180


def build(g):
    legs(g, "K", "twill", S, rows=(0, 9), crease=False)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.front.vline(1 if side == "right" else 2, 1, 4, "K3")
    waistband(g, "K", "twill", S + 2)
    footwear(g, "boot", top=5, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for y in (6, 10):
            pants.strip.hline(0, pants.strip.w - 1, y, "L0")
            getattr(pants, sides_of(side)[0]).set(2, y, "M3")
    for ring in leg_ring(g, "boot_cuff", 4.4, "L", base=2, size=(5, 2, 5), texture="leather", inflate=.1):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 1, "L1")
    for i, side in enumerate(SIDES):
        for j, x in enumerate((-1.5, 0.0, 1.5)):
            splint = leg_prop(g, f"splint_{j}", side, (x - .5, 0, -1), (1, 3, 1), "M", 2, "smooth", S + 4 + 3 * i + j,
                              pivot=(0, 7.0, -2.3))
            for face in splint.sides:
                face.vline(0, 0, 2, "M1")
            splint.front.vline(0, 0, 2, "M3" if j != 1 else "M2")
            splint.front.set(0, 0, "M4")                                   # rivet
            splint.top.fill("M4")
