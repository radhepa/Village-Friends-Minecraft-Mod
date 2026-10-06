"""Friar's Corded Robe: a patched mendicant's robe with a pointed capuce, a knotted cord and a string of paternoster beads."""
from kit import belt, body, sleeves
from kit_male import blk, hood_down, shoulder_cape, sleeve_shapes

META = {
    "name": "Friar's Corded Robe",
    "gender": "male",
    "description": "A mendicant friar's patched robe with a pointed capuce over the shoulders, a knotted cord and paternoster beads.",
    "tags": ["holy", "robe"],
    "locked_to": "b52_friars_patched_robe_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 5201)
    b.front.rect(5, 6, 2, 2, "P3"), b.front.set(5, 6, "P1")             # a patch over the heart
    sleeves(g, "P", "weave", 5202, rows=(0, 10))
    g.part("left_arm").strip.rect(9, 3, 2, 2, "P3")
    for s in sleeve_shapes(g, "friar_sleeve", "P", 4.4, (5, 5, 5), "weave", 5203, inflate=.14):
        s.bottom.fill("P0")
    capuce = shoulder_cape(g, "capuce", "P", "weave", 5205, length=3, width=11)
    for face in capuce.sides:
        face.hline(0, face.w - 1, 2, "P1")
    capuce.front.vline(5, 0, 2, "P0")
    hood_down(g, "P", "weave", 5206, y=-1.0, z=3.0, tilt=12, lining="P0")
    point = blk(g, "capuce_point", (0, 1.6, 3.4), (1, 3, 1), "P", 2, "weave", 5207, rotation=(14, 0, 0))
    point.strip.hline(0, point.strip.w - 1, 2, "P1")
    belt(g, "cord", 9.6, role="S", base=3, height=1, buckle=None)
    cord = blk(g, "cord_end", (1.6, 10.2, -3.2), (1, 8, 1), "S", 3, "plain", 5208, motion="sway")
    for y in (3, 5, 7):
        cord.strip.hline(0, cord.strip.w - 1, y, "S1")
    beads = blk(g, "paternoster", (-2.8, 10.2, -3.0), (1, 6, 1), "A", 2, "plain", 5209, motion="sway")
    for y in range(6):
        beads.strip.hline(0, beads.strip.w - 1, y, "A3" if y % 2 else "L2")
    beads.strip.hline(0, beads.strip.w - 1, 5, "M3")
