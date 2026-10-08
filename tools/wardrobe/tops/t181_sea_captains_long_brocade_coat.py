"""Sea Captain's Long Brocade Coat: a long, full-skirted brocade coat to the calf, edged in braid, with great turned
cuffs, a lace jabot at the throat and a brass spyglass hung at the hip."""
from kit import belt, body, flaps, sleeves
from kit_male import arm_blk, blk, embroider
from paint import k

META = {
    "name": "Sea Captain's Long Brocade Coat",
    "gender": "male",
    "description": "A long, full-skirted brocade coat to the calf, edged in braid, with great turned cuffs, a lace jabot "
                   "at the throat and a brass spyglass hung at the hip.",
    "tags": ["fancy", "tailored", "sea"],
    "covers_waist": True,
}

GLASS = (2.6, 9.6, -3.9)     # the spyglass hangs from the sword belt here; tube, eyepiece and lens share the hinge


MOTIF = {(1, 0): "P3", (0, 1): "P3", (1, 1): "A2", (2, 1): "P3", (1, 2): "P3"}


def brocade(face, rows=None):
    """Damask ground with small woven flowers in a half-drop repeat."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            gx = x + face.x0
            col = gx // 5
            mx, my = gx % 5, (y + 3 * (col % 2)) % 6
            face.set(x, y, MOTIF.get((mx, my), "P1" if (mx, my) == (3, 4) else "P2"))


def build(g):
    b = body(g, "P", "velvet", 33400)
    for face in b.sides:
        brocade(face)
    f = b.front
    f.vline(2, 0, 11, "A3"), f.vline(5, 0, 11, "A3")                    # braid down the open front edges
    for y in range(12):
        f.set(3, y, "S3"), f.set(4, y, "S3" if y % 3 else "S2")         # the waistcoat beneath
    for y in (2, 5, 8):
        f.set(3, y, "M3")
    sleeves(g, "P", "velvet", 33401, rows=(0, 10))
    for side in ("right", "left"):
        brocade(g.part(f"{side}_arm").strip, rows=range(0, 7))
        cuff = arm_blk(g, f"{side}_great_cuff", side, 5.6, (5, 4, 5), "A", 2, "velvet", 33402 + (side == "left"),
                       inflate=.18)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "A4")
            face.hline(0, face.w - 1, 3, "A1")
            embroider(face, 1, "dots", "M3", x1=face.w - 1, shift=1)
    # The lace jabot: falling ruffles of pale linen at the throat.
    jabot = blk(g, "lace_jabot", (0, -.2, -2.6), (2, 3, 1), "S", 4, "plain", 33404)
    for y in range(3):
        jabot.front.set(y % 2, y, "S2")
    jabot.front.hline(0, 1, 2, "S3")
    belt(g, "sword_belt", 9.2, height=1, role="L", base=1)
    # The brass spyglass: a drawn tube with a broad lens end and a narrow eyepiece.
    tube = blk(g, "spyglass_tube", GLASS, (1, 4, 1), "M", 3, "smooth", 33405, origin=(-.5, .6, -.5), motion="flap_front")
    tube.strip.hline(0, tube.strip.w - 1, 1, "M1"), tube.strip.hline(0, tube.strip.w - 1, 3, "L1")
    lens = blk(g, "spyglass_lens", GLASS, (2, 2, 2), "M", 2, "smooth", 33406, origin=(-1, 4.6, -1), motion="flap_front",
               edge=False)
    lens.bottom.fill("K1"), lens.bottom.set(0, 0, "S4")
    for face in lens.sides:
        face.hline(0, 1, 0, "M4")
    # The long skirts, front and back, and full side panels so the coat flares at the calf.
    for face in flaps(g, "coat_skirt", 9, "P", "velvet", 33407, top=10.6, slit=True):
        brocade(face)
        face.vline(4, 1, 8, "P0")
        face.hline(0, 8, 8, "A3"), face.hline(0, 8, 0, "P3")
    for name, x in (("coat_skirt_right", -5.0), ("coat_skirt_left", 4.0)):
        side = blk(g, name, (x + .5, 11.2, 0), (1, 8, 4), "P", 2, "velvet", 33408)
        for face in side.sides:
            brocade(face)
            face.hline(0, face.w - 1, 7, "A3")
        side.bottom.fill(k("P", 1))
