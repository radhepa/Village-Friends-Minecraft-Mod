"""Geometer's Compass-Belt Gown: a wrap-over gown with a stepped geometric border, great brass dividers and a wooden set square hung from the belt."""
from kit import belt, body, flaps, sleeves
from kit_male import embroider
from paint import line, solid

META = {
    "name": "Geometer's Compass-Belt Gown",
    "gender": "male",
    "description": "A geometer's wrap-over gown edged with a stepped border, a pair of great brass dividers swinging open at one hip and a wooden set square marked in measures at the other.",
    "tags": ["scholarly", "robe"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 35400)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(3, 0, "S3"), f.set(4, 0, "S2")                                # linen at the throat
    for y in range(1, 9):                                                # the under-flap, in shadow
        for x in range(0, max(0, 6 - (y * 4) // 8)):
            if f.get(x, y):
                f.set(x, y, "P1")
    line(f, 6, 0, 2, 8, "A2")                                            # the wrap edge, bound in colour
    line(f, 7, 0, 3, 8, "P3")
    f.set(2, 9, "A3"), f.set(1, 9, "A1")                                 # ties at the hip
    f.vline(2, 9, 11, "A2")
    sleeves(g, "P", "twill", 35401, rows=(0, 10), cuff="A2")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "A3")
    belt(g, "compass_belt", 9.6, height=1)
    # Great brass dividers, hinged at the top, legs swung a little open.
    hinge = g.piece("divider_hinge", "TORSO", (-.5, 0, -.5), (1, 1, 1), pivot=(-2.7, 10.6, -3.0), motion="flap_front")
    solid(hinge, "M", "smooth", 35402, 4, edge=False)
    for i, rz in enumerate((14, -14)):
        leg = g.piece(f"divider_leg_{i}", "TORSO", (-.5, 1, -.5), (1, 5, 1), pivot=(-2.7, 10.6, -3.0),
                      rotation=(0, 0, rz), motion="flap_front")
        solid(leg, "M", "smooth", 35403 + i, 3, edge=False)
        leg.strip.hline(0, leg.strip.w - 1, 4, "M1")                     # the steel points
        leg.bottom.fill("M0")
    # A wooden set square, ticked in measures.
    upright = g.piece("set_square_upright", "TORSO", (-.5, 0, -.5), (1, 4, 1), pivot=(2.2, 10.6, -3.0), motion="flap_front")
    solid(upright, "L", "plain", 35405, 3, edge=False)
    upright.front.set(0, 1, "K2"), upright.front.set(0, 3, "K2")
    foot = g.piece("set_square_foot", "TORSO", (.5, 3, -.5), (2, 1, 1), pivot=(2.2, 10.6, -3.0), motion="flap_front")
    solid(foot, "L", "plain", 35406, 3, edge=False)
    foot.front.set(1, 0, "K2")
    front, back = flaps(g, "gown", 7, "P", "twill", 35407, top=10.6)
    front.vline(2, 0, 6, "A2"), front.vline(3, 0, 6, "P3")             # the wrap edge runs on down
    for face in (front, back):
        face.hline(0, 8, 4, "A1")
        embroider(face, 5, "step", "A3", "A1")
