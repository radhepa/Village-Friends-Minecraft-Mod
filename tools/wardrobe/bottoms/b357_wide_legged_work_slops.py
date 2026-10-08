"""Wide-Legged Work Slops: wool slops cut very wide from the knee to mid-calf, over knitted stockings and low dark shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_m10 import leg_ring, outer, tie
from paint import k

META = {
    "name": "Wide-Legged Work Slops",
    "gender": "male",
    "description": "Hard-wearing wool slops cut very wide so the legs bell out from the knee to mid-calf, a drawstring waist, knitted stockings below and low dark shoes for the deck.",
    "tags": ["casual", "sea", "relaxed"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "weave", 40560, rows=(0, 7), crease=False)):
        outer(leg, side).vline(2, 0, 7, "P1")
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            for y in range(0, 3):
                face.set(1, y, "P1")
    for i, side in enumerate(SIDES):
        # The wide bell of each leg, pushed outward so the two never meet.
        bell = leg_ring(g, f"{side}_slop_bell", side, 2.6, (5, 5, 6), "P", 2, "weave", 40562 + i,
                        dx=-.5 if side == "right" else .5)
        for face in bell.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 4, "P1")
            for x in range(1, face.w, 2):
                face.vline(x, 1, 3, k("P", 1 if x % 4 == 1 else 3))        # deep soft folds
    # Knitted stockings and low shoes.
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(8, 10):
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "S2" if x % 3 == 2 else "S3")
    body = waistband(g, "P", "weave", 40564)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "P1" if x % 2 else "P3")
    for j, x in enumerate((-.5, .5)):
        tie(g, f"waist_drawcord_{j}", "TORSO", (x, 10.0, -2.5), "L", 2, 2, 40565 + j, rotation=(0, 0, 10 - 20 * j))
    footwear(g, "shoe", top=10, role="K", base=2, sole="K0")
