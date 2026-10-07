"""Midwife's Bib Apron: a full white bib apron over a plain kirtle, a pocket of linen and a chatelaine of keys and shears."""
from kit import body, sleeves
from kit_female import girdle, hanging, neck, over_panel
from paint import fabric, grid, line

META = {
    "name": "Midwife's Bib Apron",
    "gender": "female",
    "description": "A spotless full bib apron over a plain kirtle, with turned-back cuffs and a chatelaine of keys and shears.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 10901)
    neck(b.front, "round", "P", 2, edge="P3")
    sleeves(g, "P", "weave", 10902, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 8, "S4"), arm.strip.hline(0, 15, 9, "S3"), arm.strip.hline(0, 15, 10, "S2")
    j = g.part("jacket")
    fabric(j.front, "S", "weave", 10903, 4, 1, 1, 6, 10)
    j.front.vline(1, 1, 10, "S3"), j.front.vline(6, 1, 10, "S3")
    for x in (1, 6):
        j.front.set(x, 0, "S3")
        j.top.vline(x, 0, 3, "S3")
    line(j.back, 1, 0, 6, 7, "S3"), line(j.back, 6, 0, 1, 7, "S3")          # crossed straps at the back
    grid(j.front, 2, 3, ["ssss", "s..s", "ssss"], {"s": "S3"})             # bib pocket
    girdle(g, "apron_band", 8.0, role="S", base=4, height=1, buckle=None, texture="weave", wide=True)
    apron = over_panel(g, "apron", 10, "S", "weave", 10904, base=4, width=8, top=9.0)
    apron.vline(0, 0, 9, "S3"), apron.vline(7, 0, 9, "S3"), apron.hline(0, 7, 9, "S3")
    grid(apron, 4, 3, ["sss", "s.s", "sss"], {"s": "S3"})
    chain = hanging(g, "chatelaine", -3.4, 5, role="M", base=2, top=9.0)
    chain.front.set(0, 3, "M4"), chain.front.set(0, 4, "M1")
    # Keys and shears hang from the chain's own hinge so they ride the stride with it.
    keys = g.piece("chatelaine_keys", "TORSO", (-1, 5, -.1), (2, 2, 1), pivot=(-3.4, 9.0, -3.25), motion="flap_front")
    for f in keys.faces:
        fabric(f, "M", "smooth", 10906, 3)
    keys.front.set(0, 1, "M1"), keys.front.set(1, 0, "M4")
