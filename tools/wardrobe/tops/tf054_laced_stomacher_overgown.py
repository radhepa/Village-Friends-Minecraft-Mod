"""Laced-Stomacher Overgown: an open overgown laced across a contrasting stomacher, with slashed puffed upper sleeves."""
from kit import body, sleeves
from kit_female import lacing, neck, over_panel, puffs
from paint import fabric

META = {
    "name": "Laced-Stomacher Overgown",
    "gender": "female",
    "description": "An overgown open over a jeweled stomacher and laced across it, with slashed and puffed upper sleeves.",
    "tags": ["fancy", "tailored"],
}


def build(g):
    b = body(g, "S", "weave", 15401, base=3)
    neck(b.front, "square", "S", 3)
    for y in range(2, 12):
        for x in (3, 4):
            b.front.set(x, y, "A2")                                  # the stomacher
    for y in range(3, 12, 3):
        b.front.set(3, y, "M3")
    j = g.part("jacket")
    fabric(j.front, "P", "velvet", 15402, 2, 0, 1, 3, 11)
    fabric(j.front, "P", "velvet", 15402, 2, 5, 1, 3, 11)
    for face in (j.right, j.left, j.back):
        fabric(face, "P", "velvet", 15403, 2, 0, 0, face.w, 12)
    for x in (0, 1, 6, 7):
        j.front.set(x, 0, "P2")
    fabric(j.top, "P", "velvet", 15404, 3)
    lacing(j.front, 3, 2, 10, "ladder", lace="M3", under=None, eyelet=None)
    for y in range(2, 11, 2):
        j.front.set(3, y, "M3"), j.front.set(4, y, "M3")
        j.front.set(3, y + 1, None), j.front.set(4, y + 1, None)
    j.front.vline(2, 1, 11, "P3"), j.front.vline(5, 1, 11, "P1")
    sleeves(g, "P", "velvet", 15405, rows=(0, 11))
    puffs(g, "P", "velvet", 15406, base=2, y=-2.2, h=5, slash="S4", band_key="M3")
    for i, x in enumerate((-3.5, 3.5)):
        f = over_panel(g, f"overgown_front_{i}", 11, "P", "velvet", 15407, width=3, top=9.0, x=x)
        f.vline(2 if i == 0 else 0, 0, 10, "M3")
    back = over_panel(g, "overgown_back", 12, "P", "velvet", 15408, width=10, top=9.0, back=True)
    back.vline(3, 1, 11, "P1"), back.vline(6, 1, 11, "P1")
