"""Seer's Moon-Embroidered Robe: a deep-hooded robe with crescent moons worked down both front edges,
a great full moon embroidered between the shoulders, bell sleeves with a crescent at each cuff, and a
scrying glass carried in a knotted net at the girdle."""
from kit import body, sleeves
from kit_female import bells, girdle, motif, neck, over_flaps
from kit_f05 import dangle
from paint import fabric, grid, solid

META = {
    "name": "Seer's Moon-Embroidered Robe",
    "gender": "female",
    "description": "A deep-hooded robe with crescent moons down the front, a full moon between the shoulders and a scrying glass in a net.",
    "tags": ["whimsical", "robe", "holy"],
    "covers_waist": True,
}

FULL_MOON = [".mmm.", "mbmmm", "mmmdm", "mmdmm", ".mmm."]


def build(g):
    b = body(g, "P", "velvet", 55401, base=1)
    neck(b.front, "v", "P", 1, edge="S4")
    for y in (4, 8):
        motif(b.front, 0, y, "moon", "S4", c="P0")
        grid(b.front, 5, y, [".a.", "..a", ".a."][0:0] or ["aa.", "..a", "aa."], {"a": "S4"})
    grid(b.back, 2, 2, FULL_MOON, {"m": "M3", "b": "M4", "d": "M2"})
    sleeves(g, "P", "velvet", 55402, base=1, rows=(0, 11))
    for box in bells(g, "P", "velvet", 55403, base=1, y=4.0, h=6, size=6, lining="A1"):
        for face in box.sides:
            face.hline(0, face.w - 1, 5, "S4")
        motif(box.front, 2, 1, "moon", "S4")
    # The deep hood lying back on the shoulders, lined in the accent.
    hood = g.piece("deep_hood", "TORSO", (-4, 0, 0), (8, 4, 2), pivot=(0, -.8, 2.2), rotation=(16, 0, 0))
    solid(hood, "P", "velvet", 55404, 1)
    fabric(hood.top, "A", "plain", 55405, 1)
    hood.top.hline(0, 7, 0, "P2")
    hood.back.vline(3, 0, 3, "P0"), hood.back.vline(4, 0, 3, "P2")
    motif(hood.back, 5, 0, "moon", "S4")
    girdle(g, "girdle", 8.2, role="A", base=1, height=1, buckle=None, texture="plain")
    f, bk = over_flaps(g, "robe", 9, "P", "velvet", 55406, base=1, width=10, top=9.0)
    f.vline(4, 0, 8, "S4"), f.vline(5, 0, 8, "P0")
    for y in (2, 6):
        motif(f, 1, y, "moon", "S4")
        grid(f, 6, y, ["aa.", "..a", "aa."], {"a": "S4"})
    bk.hline(0, 9, 8, "S4")
    # The scrying glass in a knotted net, hung from the girdle at the left hip.
    cord = dangle(g, "glass_cord", 2.6, -.6, (1, 1, 1), "L", 2, "plain", top=9.0, seed=55407, edge=False)
    cord.front.fill("L3")
    orb = dangle(g, "scrying_glass", 2.6, .4, (3, 3, 2), "S", 4, "plain", top=9.0, seed=55408, edge=False)
    for face in orb.sides:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "L2" if (x + y) % 2 == 0 else ("S4" if y == 0 else "A2"))
        face.set(0, 0, "S4")
    orb.top.fill("L2"), orb.bottom.fill("L1")
