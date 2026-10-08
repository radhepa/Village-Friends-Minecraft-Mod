"""Short-Sleeved Summer Tunic: a light, loose pullover tunic with wide short sleeves, a tied neck slit and one woven stripe."""
from kit import SIDES, body, flaps
from kit_m10 import arm_ring, tie
from paint import dark_seams, fabric, k

META = {
    "name": "Short-Sleeved Summer Tunic",
    "gender": "male",
    "description": "A light, loose summer tunic with wide short sleeves, a cord-tied neck slit and one woven stripe round sleeves and hem.",
    "tags": ["casual", "simple", "relaxed"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 40040, base=3)
    f = b.front
    # Wide neck with a short slit, edged in the woven stripe and tied at the throat.
    for x in range(2, 6):
        f.clear(x, 0)
    f.clear(3, 1), f.clear(4, 1)
    for x, y in ((1, 0), (6, 0), (2, 1), (5, 1), (3, 2), (4, 2)):
        f.set(x, y, "A2")
    f.vline(4, 3, 4, "P1")
    b.back.hline(2, 5, 0, "A2")
    # Loose cloth falling from the shoulders.
    for x in (1, 6):
        f.vline(x, 6, 10, "P2")
        b.back.vline(x, 5, 10, "P2")
    dark_seams(b, faces=("right", "left"))
    tie(g, "neck_cord_r", "TORSO", (-.45, 2.2, -2.45), "A", 2, 2, 40041, rotation=(0, 0, 8))
    tie(g, "neck_cord_l", "TORSO", (.45, 2.2, -2.45), "A", 3, 2, 40042, rotation=(0, 0, -8))
    # Wide short sleeves: cloth over the shoulder and an open sleeve end above the elbow.
    for i, side in enumerate(SIDES):
        arm = g.part(f"{side}_arm")
        fabric(arm.strip, "P", "weave", 40043 + i, 3, 0, 0, arm.strip.w, 4)
        fabric(arm.top, "P", "weave", 40043, 4)
        sleeve = g.part(f"{side}_sleeve")
        fabric(sleeve.strip, "P", "weave", 40045 + i, 3, 0, 0, sleeve.strip.w, 3)
        fabric(sleeve.top, "P", "weave", 40045, 4)
        ring = arm_ring(g, f"{side}_sleeve_end", side, 1.0, (5, 3, 6), "P", 3, "weave", 40047 + i)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.hline(0, face.w - 1, 1, "A2")
            face.hline(0, face.w - 1, 2, "P2")
        ring.top.fill("P4")
    # Hip-length hem, slit at the sides, with the woven stripe.
    for face in flaps(g, "hem", 4, "P", "weave", 40049, width=8, base=3, top=11.2):
        face.hline(0, 7, 2, "A2")
        face.hline(0, 7, 3, "P1")
        face.set(0, 3, "P2"), face.set(7, 3, "P2")
