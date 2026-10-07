"""Farrier's Split Apron: a leather apron split between the legs, a horseshoe on the belt and a hoof knife."""
from kit import belt, body, neckline, roll, sleeves
from kit_male import blk, flecks
from paint import fabric, line, solid

META = {
    "name": "Farrier's Split Apron",
    "gender": "male",
    "description": "A shoeing smith's leather apron split between the legs and fringed, a horseshoe on the belt and a hoof knife.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 3101, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 3102, base=3, rows=(0, 5))
    roll(g, "S", 3.4, base=3)
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    # Leather bib from mid-chest down, hung from straps over the shoulders and crossed on the back.
    fabric(jf, "L", "leather", 3103, 2, 1, 3, 6, 9)
    jf.hline(1, 6, 3, "L3")
    jf.vline(1, 0, 2, "L2"), jf.vline(6, 0, 2, "L2")
    flecks(jf, "L0", 3104, .07, rows=range(5, 12), cols=range(1, 7))   # spark burns
    for y in range(4):
        jacket.top.set(1, y, "L2"), jacket.top.set(6, y, "L2")
    line(jb, 1, 0, 6, 9, "L2"), line(jb, 6, 0, 1, 9, "L1")
    belt(g, "belt", 9.6)
    # The split skirt: one leather leaf per leg, fringed at the hem.
    for name, x in (("apron_right", -2.1), ("apron_left", 2.1)):
        leaf = g.piece(name, "TORSO", (-2, 0, 0), (4, 7, 1), pivot=(x, 10.8, -2.85), motion="flap_front")
        solid(leaf, "L", "leather", 3105 + (x > 0), 2)
        leaf.front.hline(0, 3, 0, "L3")
        leaf.front.vline(0 if x < 0 else 3, 1, 5, "L1")
        for i in range(4):
            leaf.front.set(i, 6, "L3" if i % 2 else "L0")
        leaf.front.set(1 if x < 0 else 2, 3, "L0")
    # A spare shoe hung on the belt hook, and the hoof knife in its sheath.
    shoe = blk(g, "horseshoe", (-3.0, 10.4, -2.85), (3, 3, 1), "M", 2, "smooth", 3107, rotation=(0, 0, 8))
    for face in (shoe.front, shoe.back):
        face.hline(0, 2, 0, "M3"), face.vline(0, 0, 2, "M3"), face.vline(2, 0, 2, "M3")
        face.set(1, 1, "M0"), face.set(1, 2, "M0")
    knife = blk(g, "hoof_knife", (3.1, 9.9, -2.75), (1, 4, 1), "L", 1, "leather", 3108, rotation=(0, 0, -12))
    knife.strip.hline(0, knife.strip.w - 1, 0, "L3")
    knife.strip.hline(0, knife.strip.w - 1, 1, "M3")
