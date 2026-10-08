"""Persian Qaba Wrap Coat: a brocade qaba crossing to the left hip, half sleeves over a pale under-robe, a sash and a tucked pen case."""
from kit import SIDES, body, sleeves
from kit_male import arm_blk, blk, sash
from kit_m08 import brocade, coat_skirt
from paint import strip_fabric

META = {
    "name": "Persian Qaba Wrap Coat",
    "gender": "male",
    "description": "A brocade qaba crossing over from the right shoulder to the left hip, half sleeves over a pale under-robe, a knotted sash and a lacquered pen case tucked in it.",
    "tags": ["fancy", "tailored", "scholarly"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 38081)
    for face in b.sides:
        brocade(face, "P", 2, ox=face.x0, core="A2")
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    # The crossover edge: from the right of the neck down to the left hip, lined in accent.
    for y in range(9):
        x = 2 + round(5 * y / 8)
        f.set(x, y, "A3"), f.set(x - 1, y, "A2")
        if x + 1 < 8:
            f.set(x + 1, y, "P0")                                          # its shadow on the under panel
    f.set(7, 9, "A2")
    sleeves(g, "P", "velvet", 38082, rows=(0, 10))
    for side in SIDES:
        arm, over = g.part(f"{side}_arm"), g.part(f"{side}_sleeve")
        strip_fabric(arm, "S", "weave", 38083, 3, 6, 10)                   # the under-robe's long sleeve
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")
        strip_fabric(over, "P", "velvet", 38084, 2, 0, 5)                  # the half sleeve stands off the arm
        brocade(over.strip, "P", 2, oy=3, core="A2", rows=range(0, 5))
        arm_blk(g, f"{side}_half_sleeve_hem", side, 3.2, (5, 1, 5), "A", 2, "plain", 38085, inflate=.1)
    band = sash(g, "qaba_sash", "S", y=8.6, height=2, texture="weave", seed=38086, tails=((-2.6, 5),), tail_len=5)
    for face in band.sides:
        face.hline(0, face.w - 1, 1, "A2")
    case = blk(g, "qalamdan", (-1.6, 7.2, -3.0), (1, 4, 1), "L", 3, "smooth", 38088, rotation=(0, 0, -12))
    for face in case.sides:
        face.set(0, 0, "M3"), face.set(0, 2, "A3")
    case.top.fill("M4")
    front, back, sides = coat_skirt(g, "qaba_skirt", 8, "P", "velvet", 38089, top=10.6, hem="A1")
    for face in (front, back):
        brocade(face, "P", 2, ox=1, oy=2, core="A2", rows=range(1, 7))
    front.vline(6, 0, 7, "A3"), front.vline(7, 0, 7, "P0")                  # the overlap runs on down the skirt
