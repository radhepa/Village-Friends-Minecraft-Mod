"""Outrider's Dust Coat: a long dust-pale riding coat split four ways, a shoulder capelet and a map case slung across the back."""
from kit import body, sleeves
from kit_male import flecks, shoulder_cape, toggles
from kit_m04 import split_flaps
from paint import line, solid

META = {
    "name": "Outrider's Dust Coat",
    "gender": "male",
    "description": "A long, road-dusted riding coat split front and back to the hip for the saddle, with a short shoulder "
                   "capelet, wooden toggles and a leather map case slung across the back on a strap.",
    "tags": ["rugged", "casual", "martial"],
    "covers_waist": True,
}

S = 34360


def build(g):
    b = body(g, "S", "twill", S, base=2)
    f = b.front
    f.vline(4, 1, 11, "S0"), f.vline(5, 1, 11, "S3")                     # lapped front edge
    toggles(f, 1, (3, 6, 9), "L3", "L1")
    for face in b.sides:
        flecks(face, "S1", S + 1, .03, rows=range(7, 12))
    sleeves(g, "S", "twill", S + 2, rows=(0, 10), cuff="L2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        flecks(arm.strip, "S1", S + 3, .03, rows=range(7, 10))
    cape = shoulder_cape(g, "capelet", "S", "twill", S + 4, base=2, length=3, width=12, depth=6, y=-.8)
    for face in cape.sides:
        face.hline(0, face.w - 1, 2, "S1")
        face.hline(0, face.w - 1, 0, "S3")
    cape.front.vline(5, 0, 2, "S0"), cape.front.set(6, 1, "L3")
    jacket = g.part("jacket")                                               # the case strap, left shoulder to right hip
    line(jacket.front, 7, 2, 1, 10, "L2"), line(jacket.front, 6, 2, 0, 10, "L1")
    # Map case: a capped leather tube slung diagonally across the back.
    tube = g.piece("map_case", "TORSO", (-1, -4, -1), (2, 8, 2), pivot=(.3, 6.2, 3.4), rotation=(0, 0, 50))
    solid(tube, "L", "leather", S + 5, 2)
    for face in tube.sides:
        face.hline(0, 1, 0, "M3"), face.hline(0, 1, 7, "M2")
        face.hline(0, 1, 1, "L1"), face.hline(0, 1, 4, "L3")
    tube.top.fill("M3"), tube.bottom.fill("M1")
    for face, inner in zip(split_flaps(g, "coat_skirt", 8, "S", "twill", S + 6, top=10.8, half=4, gap=.5), (3, 0, 0, 3)):
        face.vline(inner, 1, 7, "S1")
        face.hline(0, 3, 7, "S1")
        flecks(face, "S1", S + 7, .07, rows=range(5, 8))
