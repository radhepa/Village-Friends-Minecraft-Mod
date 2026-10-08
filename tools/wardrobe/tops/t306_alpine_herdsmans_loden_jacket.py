"""Alpine Herdsman's Loden Jacket: a fulled loden jacket with a piped stand collar, horn buttons, a salt pouch on a strap and a mountain sprig."""
from kit import SIDES, body, collar, flaps, pouch, sleeves
from kit_male import blk
from paint import line

META = {
    "name": "Alpine Herdsman's Loden Jacket",
    "gender": "male",
    "description": "A thick fulled loden jacket with piped edges, a stand collar and pale horn buttons, a herdsman's salt pouch on a strap across the chest and a mountain sprig at the lapel.",
    "tags": ["rugged", "work", "casual"],
    "covers_waist": True,
}


def horn(face, x, y):
    face.set(x, y, "L4"), face.set(x, y + 1, "L1")                         # a pale horn button and its shadow


def build(g):
    b = body(g, "P", "plain", 38401)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.vline(3, 1, 11, "A2")                                                # piped front edge
    for y in (2, 4, 6, 8):
        horn(f, 4, y)
    for x0 in (0, 5):                                                       # slanted pocket flaps with piping
        f.hline(x0, x0 + 2, 9, "A2"), f.hline(x0, x0 + 2, 10, "P1")
    b.back.vline(1, 2, 11, "P1"), b.back.vline(6, 2, 11, "P1")              # back seams
    line(f, 0, 1, 2, 8, "L2")                                              # the pouch strap from the left shoulder
    line(b.back, 0, 1, 7, 8, "L2")
    stand = collar(g, "stand_collar", "A", "plain", base=2, height=1, y=-.5)
    for face in stand.sides:
        face.hline(0, face.w - 1, 0, "A3")
    sleeves(g, "P", "plain", 38402, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 8, "A2")
        outer = arm.right if side == "right" else arm.left
        horn(outer, 2, 9)
        arm.front.vline(1, 2, 7, "P1")
    sprig = blk(g, "lapel_sprig", (2.6, .8, -2.7), (1, 2, 1), "A", 1, "plain", 38403, edge=False)
    sprig.top.fill("S4"), sprig.front.set(0, 0, "S4")
    salt = pouch(g, "salt_pouch", (-2.5, 8.6, -2.9), size=(2, 3, 1), role="L", flap="L4")
    salt.front.hline(0, 1, 1, "L1")
    for face in flaps(g, "jacket_hem", 2, "P", "plain", 38404, top=11.0, hem="A2"):
        face.vline(4, 0, 1, "A2")
