"""Smith's Scorched Bib: a scorched leather bib apron over a rolled-sleeve shirt, studded bracers and tongs at the hip."""
from kit import roll
from kit_female import arm_rings, chemise, hanging, over_panel, splotch, sub
from paint import fabric, solid

META = {
    "name": "Smith's Scorched Bib",
    "gender": "female",
    "description": "A scorch-marked leather bib apron over a rolled-sleeve shirt, studded leather bracers and forge tongs.",
    "tags": ["work", "sturdy", "apron"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 2, "weave", 14101, neckline="slit", sleeve_rows=(0, 4))
    roll(g, "S", 1.8, base=2)
    for box in arm_rings(g, "bracer", 5.0, 4, 5, inflate=.08):
        solid(box, "L", "leather", 14102, 2)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 3, "L1")
            face.set(1, 1, "M3"), face.set(face.w - 2, 2, "M3")
    j = g.part("jacket")
    fabric(j.front, "L", "leather", 14103, 2, 1, 1, 6, 11)
    j.front.vline(1, 1, 11, "L1"), j.front.vline(6, 1, 11, "L1")
    for x in (2, 5):
        j.front.set(x, 0, "L2")
        j.top.vline(x, 1, 3, "L2")
    j.back.hline(0, 7, 9, "L2")
    for face in (j.right, j.left):
        face.hline(0, 3, 9, "L2")
    splotch(sub(j.front, 1, 2, 6, 9), "L0", 14104, count=3, size=1)
    j.front.set(3, 6, "K1"), j.front.set(4, 7, "K1")                  # scorch marks
    apron = over_panel(g, "apron", 9, "L", "leather", 14105, width=8, top=9.0)
    apron.vline(0, 0, 8, "L1"), apron.vline(7, 0, 8, "L1")
    splotch(apron, "L0", 14106, count=3, y0=2, size=1)
    tongs = hanging(g, "tongs", -3.4, 6, role="M", base=2, top=9.0)
    jaw = g.piece("tongs_jaw", "TORSO", (-1, 6, -.1), (2, 2, 1), pivot=(-3.4, 9.0, -3.25), motion="flap_front")
    solid(jaw, "M", "smooth", 14107, 2)
    jaw.front.set(0, 1, "M1"), jaw.front.set(1, 1, "M1")
