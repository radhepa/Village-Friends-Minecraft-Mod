"""Geometer's Chalk-Dusted Hose: dark hose whitened at the knees from kneeling over floor drawings, finger-wipes of chalk on the thigh and a chalk-line reel at the hip."""
from kit import SIDES, waistband
from kit_m05 import hose, knee_patch, leg_prop, soft_shoes

META = {
    "name": "Geometer's Chalk-Dusted Hose",
    "gender": "male",
    "description": "Dark hose whitened at both knees from kneeling over setting-out drawings on the floor, chalky finger-wipes down one thigh and a snapped chalk-line reel tied at the hip, in buckled shoes.",
    "tags": ["scholarly", "slim", "casual"],
}


def build(g):
    hose(g, "K", 2, "weave", 35420, end=9)
    waistband(g, "K", "weave", 35421)
    soft_shoes(g, "L", 2, top=10, strap="M3")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        knee = leg.front
        knee_patch(knee, 0, 4, "S2", "S4", w=4, h=2)                       # chalk ground into the knee
        knee.set(1 if side == "right" else 2, 6, "S1")
        (leg.right if side == "right" else leg.left).hline(1, 2, 4, "S1")
    thigh = g.part("right_leg").front
    for x in (0, 1, 2):                                                   # finger-wipes on the right thigh
        thigh.vline(x, 0, 1 + x % 2, "S3")
    reel = leg_prop(g, "chalk_line_reel", "left", (2.6, .4, -.4), (1, 3, 2), "L", 3, "plain", 35422)
    for face in (reel.left, reel.right):
        face.hline(0, face.w - 1, 1, "S4")                                # the chalked line wound on
    reel.left.set(0, 0, "L4"), reel.left.set(1, 2, "L1")
    line = leg_prop(g, "chalk_line_end", "left", (2.6, 3.4, -.9), (1, 2, 1), "S", 4, "plain", 35423)
    line.bottom.fill("M3")
