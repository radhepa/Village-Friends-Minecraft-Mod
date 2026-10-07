"""Henley: a long-sleeved cotton henley with a three-button placket."""
from kit_casual import long_sleeves, shirt_body

META = {
    "name": "Henley",
    "gender": "male",
    "description": "A long-sleeved cotton henley with a three-button placket, worn loose.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "P", 2, "weave", 11501)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "P1"), f.set(5, 0, "P1")
    for y in range(1, 5):
        f.set(3, y, "P3"), f.set(4, y, "P1")
    for y in (1, 2, 4):
        f.set(3, y, "L3")
    body.back.hline(2, 5, 0, "P1")
    long_sleeves(g, "P", 2, "weave", 11502, cuff="P3")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "P1")   # pushed-up rib ruck above the cuff
