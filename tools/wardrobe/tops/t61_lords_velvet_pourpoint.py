"""Lord's Velvet Pourpoint: a padded velvet pourpoint with a tall collar, sleeves buttoned to the wrist and a jewelled hip belt."""
from kit import body, collar, flaps, sleeves
from kit_male import buttons
from paint import solid

META = {
    "name": "Lord's Velvet Pourpoint",
    "gender": "male",
    "description": "A padded velvet pourpoint with a tall accent-edged collar, sleeves buttoned from elbow to wrist and a jewelled hip belt.",
    "tags": ["fancy", "tailored"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 6101)
    for face in (b.front, b.back):
        for x in (1, 3, 5):
            face.vline(x, 1, 9, "P1")                                    # padded channels
        face.vline(6, 1, 9, "P3")
    b.front.vline(4, 0, 11, "P0"), b.front.vline(3, 0, 11, "P3")
    sleeves(g, "P", "velvet", 6102, rows=(0, 10), cuff="A2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        buttons(outer, 2, 5, 10, 1, "M3")
    tall = collar(g, "tall_collar", "P", "velvet", base=2, height=2, y=-1.2)
    for face in tall.sides:
        face.hline(0, face.w - 1, 0, "A2")
    tall.front.set(4, 1, "P0")
    hip = g.piece("jewelled_belt", "TORSO", (-4.6, 10.8, -2.6), (9, 1, 5), inflate=.08)
    solid(hip, "M", "smooth", 6103, 2, edge=False)
    for face in hip.sides:
        for x in range(0, face.w, 3):
            face.set(x, 0, "A3")                                         # set stones
    for face in flaps(g, "skirt", 3, "P", "velvet", 6104, top=11.4):
        for x in range(1, 9, 2):
            face.vline(x, 0, 2, "P1")
        face.hline(0, 8, 2, "A2")
