"""Palmer's Scallop Cloak: a long travelling cloak with a hood, a scallop-shell badge, a pilgrim's scrip and an ampulla."""
from kit import body, neckline, sleeves
from kit_male import back_drape, blk, hood_down, shoulder_cape
from paint import grid, line

META = {
    "name": "Palmer's Scallop Cloak",
    "gender": "male",
    "description": "A palmer's calf-length travelling cloak with a hood, a scallop-shell badge on the cape, a scrip on a strap and a holy-water ampulla.",
    "tags": ["holy", "rugged"],
    "locked_to": "b57_palmers_road_worn_hose",
    "covers_waist": True,
}

SHELL = ["a.a.a",
         ".aaa.",
         "..a.."]


def build(g):
    b = body(g, "S", "weave", 5701, base=2)
    neckline(b.front, "round", "S")
    sleeves(g, "S", "weave", 5702, rows=(0, 10), cuff="S1")
    jacket = g.part("jacket")
    line(jacket.front, 0, 1, 7, 9, "L2"), line(jacket.back, 7, 1, 0, 9, "L2")   # scrip strap
    cape = shoulder_cape(g, "cloak_cape", "P", "weave", 5703, length=4, width=12)
    for face in cape.sides:
        face.hline(0, face.w - 1, 3, "P1")
    cape.front.vline(6, 0, 3, "P0")
    grid(cape.front, 1, 0, SHELL, {"a": "S4"})
    hood_down(g, "P", "weave", 5704, y=-1.0, z=3.1)
    upper = back_drape(g, "cloak_back", "P", 11, "weave", 5705, width=10, y=1.4, z=3.1, tilt=4)
    upper.back.vline(3, 0, 10, "P1"), upper.back.vline(7, 2, 10, "P3")
    lower = back_drape(g, "cloak_hem", "P", 6, "weave", 5706, width=10, y=12.2, z=3.4, tilt=4, motion="flap_back")
    lower.back.vline(3, 0, 5, "P1"), lower.back.hline(0, 9, 5, "P0")
    scrip = blk(g, "scrip", (2.9, 9.0, -2.4), (3, 3, 2), "L", 2, "leather", 5707)
    scrip.front.hline(0, 2, 0, "L3"), scrip.front.set(1, 1, "S4")
    flask = blk(g, "ampulla", (-2.8, 9.6, -2.75), (1, 2, 1), "M", 2, "smooth", 5708)
    flask.strip.hline(0, flask.strip.w - 1, 0, "M3")
