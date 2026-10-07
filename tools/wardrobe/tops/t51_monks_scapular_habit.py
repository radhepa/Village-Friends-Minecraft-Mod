"""Monk's Scapular Habit: a dark habit with a long scapular, a round cowl and hood, wide sleeves and a knotted cincture."""
from kit import belt, body, sleeves
from kit_male import blk, hood_down, shoulder_cape, sleeve_shapes
from paint import fabric, solid

META = {
    "name": "Monk's Scapular Habit",
    "gender": "male",
    "description": "A cloister habit with a long scapular front and back, round cowl and hood, wide sleeves and a three-knotted cincture.",
    "tags": ["holy", "robe"],
    "locked_to": "b51_monks_under_robe",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 5101, base=1)
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        fabric(face, "P", "weave", 5102, 2, 2, 0, 4, 12)               # the scapular, a shade lighter
        face.vline(2, 0, 11, "P0"), face.vline(5, 0, 11, "P0")
    fabric(jacket.top, "P", "weave", 5102, 2, 2, 0, 4, 4)
    sleeves(g, "P", "weave", 5103, base=1, rows=(0, 10))
    for s in sleeve_shapes(g, "wide_sleeve", "P", 3.6, (5, 6, 5), "weave", 5104, base=1, inflate=.18):
        s.bottom.fill("P0")
        for face in s.sides:
            face.vline(1, 1, 5, "P0")
    cowl = shoulder_cape(g, "cowl", "P", "weave", 5106, base=1, length=3, width=11)
    for face in cowl.sides:
        face.hline(0, face.w - 1, 2, "P0")
    hood_down(g, "P", "weave", 5107, base=1, y=-1.2, z=3.1, tilt=10, lining="P0")
    belt(g, "cincture", 9.6, role="S", base=3, height=1, buckle=None)
    end = blk(g, "cincture_end", (-1.6, 10.2, -3.25), (1, 7, 1), "S", 3, "plain", 5108, motion="sway")
    for y in (2, 4, 6):
        end.strip.hline(0, end.strip.w - 1, y, "S1")                     # the three knots
    for name, z, motion, face_name in (("scapular_front", -3.15, "flap_front", "front"),
                                        ("scapular_back", 2.15, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-2, 0, 0), (4, 10, 1), pivot=(0, 11.2, z), motion=motion)
        solid(panel, "P", "weave", 5109, 2)
        face = getattr(panel, face_name)
        face.vline(0, 0, 9, "P0"), face.vline(3, 0, 9, "P0"), face.hline(0, 3, 9, "P0")
