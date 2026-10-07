"""Bridegroom's Wedding Doublet: a pale brocade doublet with a rosemary sprig at the breast, ribbon favours and gloves in the belt."""
from kit import belt, body, sleeves
from kit_male import arm_blk, blk, lozenge

META = {
    "name": "Bridegroom's Wedding Doublet",
    "gender": "male",
    "description": "A pale brocade wedding doublet with a sprig of rosemary at the breast, ribbon favours on the sleeves and gloves tucked in the belt.",
    "tags": ["fancy", "tailored"],
    "locked_to": "b94_bridegrooms_ribboned_hose",
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "velvet", 9401, base=3)
    for face in b.sides:
        lozenge(face, "S", 3, step=6, line_key="M2", ox=face.x0)
    b.front.vline(4, 0, 11, "S1"), b.front.hline(2, 5, 0, "A2")
    sleeves(g, "S", "velvet", 9402, base=3, rows=(0, 10), cuff="A2")
    for side in ("right", "left"):
        lozenge(g.part(f"{side}_arm").strip, "S", 3, step=6, line_key="M2")
    sprig = blk(g, "rosemary_sprig", (-2.0, 2.2, -2.7), (1, 3, 1), "P", 2, "plain", 9403, rotation=(0, 0, -15))
    sprig.strip.hline(0, sprig.strip.w - 1, 0, "P3"), sprig.strip.hline(0, sprig.strip.w - 1, 2, "A2")
    for i, side in enumerate(("right", "left")):
        bow = arm_blk(g, f"{side}_favour", side, 0.4, (1, 2, 3), "A", 3, "plain", 9404 + i,
                      dx=-2.3 if side == "right" else 2.3)
        (bow.right if side == "right" else bow.left).set(1, 0, "A2")
    belt(g, "belt", 9.6, role="A", base=2, height=1, buckle="M")
    gloves = blk(g, "tucked_gloves", (2.6, 9.0, -2.85), (2, 3, 1), "S", 4, "plain", 9406)
    gloves.front.vline(1, 0, 2, "S2"), gloves.front.set(0, 0, "A2")
