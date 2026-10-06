"""Cook's Oven-Mitt Tunic: a pale kitchen tunic scorched at the hem, a big quilted mitt on one hand and a basting ladle."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import arm_blk, blk, flecks, lozenge

META = {
    "name": "Cook's Oven-Mitt Tunic",
    "gender": "male",
    "description": "A pale kitchen tunic scorched along the hem from the hearth, a big quilted mitt on the right hand and a basting ladle.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 4301, base=3)
    neckline(b.front, "v", "S", base=3)
    sleeves(g, "S", "weave", 4302, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):
        flecks(g.part(f"{side}_arm").strip, "K3", 4303, .05, rows=range(7, 10))
    # The oven mitt: a padded, diamond-quilted mitten over the right hand.
    mitt = arm_blk(g, "oven_mitt", "right", 6.8, (5, 4, 5), "A", 2, "quilt", 4304, inflate=.15)
    for face in mitt.sides:
        lozenge(face, "A", 2, step=3)
        face.hline(0, face.w - 1, 0, "S3")                             # linen cuff of the mitt
    mitt.bottom.fill("A1")
    belt(g, "belt", 9.4, height=1)
    ladle = blk(g, "ladle_handle", (2.8, 8.6, -2.75), (1, 4, 1), "M", 3, "smooth", 4305, edge=False)
    ladle.strip.hline(0, ladle.strip.w - 1, 0, "M2")
    bowl = blk(g, "ladle_bowl", (2.8, 12.4, -2.75), (2, 2, 2), "M", 2, "smooth", 4306)
    bowl.top.fill("M0")
    for face in flaps(g, "hem", 3, "S", "weave", 4307, base=3, top=10.6):
        face.hline(0, 8, 2, "S1")
        for x in (1, 2, 5, 7):
            face.set(x, 2, "K3")                                       # scorch marks from the hearth
        face.set(2, 1, "K3"), face.set(6, 1, "S1")
