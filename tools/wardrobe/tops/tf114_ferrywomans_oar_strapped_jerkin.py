"""Ferrywoman's Oar-Strapped Jerkin: a sleeveless hip-length leather jerkin closed with wooden toggles
over a full-sleeved shirt, a spare oar strapped up her back with its blade above the left shoulder,
and a fare pouch on the belt."""
from kit import flaps
from kit_female import chemise, girdle
from paint import fabric, line, solid

META = {
    "name": "Ferrywoman's Oar-Strapped Jerkin",
    "gender": "female",
    "description": "A toggled leather jerkin over a full-sleeved shirt, an oar strapped up her back with the blade over her shoulder and a fare pouch.",
    "tags": ["sea", "work", "sturdy", "rugged"],
    "covers_waist": True,
}

SEED = 53120
OAR_PIVOT, OAR_ROT = (0.6, 3.6, 3.7), (-10, 0, -27)


def build(g):
    body, arms = chemise(g, "S", 3, "weave", SEED, neckline="slit", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4")
        arm.front.vline(1, 2, 8, "S2")
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "L", "leather", SEED + 1, 2)
    fabric(j.top, "L", "leather", SEED + 1, 3)
    for x in range(2, 6):                                            # open neck over the shirt
        j.front.clear(x, 0)
    j.front.clear(3, 1), j.front.clear(4, 1)
    j.front.vline(3, 2, 11, "L1"), j.front.vline(4, 2, 11, "L3")    # the meeting edges
    for y in (3, 6, 9):                                              # wooden toggles on cord loops
        j.front.set(2, y, "S2"), j.front.set(3, y, "L4"), j.front.set(4, y, "L4"), j.front.set(5, y, "S2")
    for face in (j.right, j.left):
        face.vline(1, 0, 11, "L1")
        for y in range(1, 11, 3):
            face.set(2, y, "L3")                                     # stitched side seam
    for face in j.sides:
        face.hline(0, face.w - 1, 11, "L1")
    # The oar harness: a strap from the left shoulder to the right hip, front and back.
    line(j.front, 7, 0, 1, 7, "K2"), line(j.back, 0, 0, 6, 7, "K2")
    j.top.vline(6, 0, 3, "K2")
    girdle(g, "belt", 8.4, role="K", base=2, height=1, buckle="M")
    jf, jb = flaps(g, "jerkin_skirt", 2, "L", "leather", SEED + 2, width=9, base=2, hem="L1", top=11.6)
    jf.vline(4, 0, 1, "L0")
    # The oar: a long loom up the back, the blade standing above the left shoulder.
    loom = g.piece("oar_loom", "TORSO", (-.5, -6, 0), (1, 11, 1), pivot=OAR_PIVOT, rotation=OAR_ROT)
    solid(loom, "L", "smooth", SEED + 3, 3)
    blade = g.piece("oar_blade", "TORSO", (-2, -13, -.1), (4, 7, 1), pivot=OAR_PIVOT, rotation=OAR_ROT, inflate=.02)
    solid(blade, "L", "smooth", SEED + 4, 3)
    for f in (blade.back, blade.front):
        f.vline(1, 2, 6, "L2"), f.vline(2, 2, 6, "L2")              # the loom runs on as a ridge
        f.hline(0, 3, 0, "L4")
        f.set(0, 0, "L3"), f.set(3, 0, "L3")
    grip = g.piece("oar_grip", "TORSO", (-.5, 5, 0), (1, 2, 1), pivot=OAR_PIVOT, rotation=OAR_ROT, inflate=.08)
    solid(grip, "L", "smooth", SEED + 5, 1, edge=False)
    for i, y in enumerate((-1.0, 3.0)):                              # the two straps lashing it on
        lash = g.piece(f"oar_lashing_{i}", "TORSO", (-1, y, -.2), (2, 1, 1), pivot=OAR_PIVOT, rotation=OAR_ROT, inflate=.12)
        solid(lash, "K", "plain", SEED + 6, 2, edge=False)
    # The fare pouch on the belt, a ferry token stitched on its flap.
    pouch = g.piece("fare_pouch", "TORSO", (-1, 0, -1), (2, 2, 1), pivot=(-2.6, 8.6, -2.25))
    solid(pouch, "L", "leather", SEED + 7, 1)
    pouch.front.hline(0, 1, 0, "L3"), pouch.front.set(1, 1, "M3")
