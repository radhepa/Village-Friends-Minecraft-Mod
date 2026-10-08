"""Lambswool Cowl Bodice: a snug wool bodice with a deep cowl of curly lambswool round the neck and fleece at the wrists."""
from kit import SIDES, body
from kit_female import arm_rings
from kit_f10 import lambswool
from paint import fabric, k, strip_fabric

META = {
    "name": "Lambswool Cowl Bodice",
    "gender": "female",
    "description": "A snug shepherd's bodice in thick wool, a deep cowl of curly lambswool rolled round the neck and falling onto the chest, and fleece at the wrists.",
    "tags": ["rugged", "casual"],
}


def build(g):
    b = body(g, "P", "weave", 60480)
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P1"), face.vline(6, 3, 11, "P1")
        face.vline(2, 4, 11, "P3")
    b.front.vline(3, 3, 11, "P1"), b.front.vline(4, 3, 11, "P3")       # the centre-front seam
    for y in (6, 9):
        b.front.set(3, y, "L3"), b.front.set(4, y, "L2")               # two horn buttons below the cowl
    b.back.vline(3, 2, 11, "P1")
    for face in (b.right, b.left):
        face.vline(2, 2, 11, "P1")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60481 + (side == "left"), 2, 0, 11)
        fabric(arm.top, "P", "weave", 60483, 3)
        outer = arm.right if side == "right" else arm.left
        outer.vline(2, 1, 8, "P1")
    # The cowl: a thick ring round the neck with a soft fold dropping onto the chest.
    cowl = g.piece("cowl", "TORSO", (-5, -1.4, -3.1), (10, 3, 6), inflate=.06)
    for f in cowl.faces:
        lambswool(f, 60484)
    for face in cowl.sides:
        face.hline(0, face.w - 1, face.h - 1, "S2")
    drop = g.piece("cowl_drop", "TORSO", (-3, 0, 0), (6, 3, 1), pivot=(0, 1.4, -3.15), rotation=(-8, 0, 0))
    for f in drop.faces:
        lambswool(f, 60485)
    drop.front.hline(0, 5, 2, "S2"), drop.front.set(0, 2, "S1"), drop.front.set(5, 2, "S1")
    for ring in arm_rings(g, "fleece_cuff", 7.6, 2, 5, inflate=.12):
        for f in ring.faces:
            lambswool(f, 60486)
        ring.bottom.fill("S2")
