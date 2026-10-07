"""Brocade Partlet Bodice: a brocade bodice under a high linen partlet with a frilled throat, linen puffed through the elbows."""
from kit import sleeves
from kit_female import arm_rings, bodice, lozenges
from paint import fabric, solid

META = {
    "name": "Brocade Partlet Bodice",
    "gender": "female",
    "description": "A brocade bodice over a high linen partlet with a frilled throat, and linen puffed through slashed elbows.",
    "tags": ["fancy"],
}


def build(g):
    body = g.part("body")
    fabric(body.front, "S", "weave", 15501, 4)
    for face in (body.back, body.right, body.left):
        fabric(face, "S", "weave", 15501, 4)
    fabric(body.top, "S", "weave", 15501, 4)
    for x in range(8):
        body.front.set(x, 1, "S3" if x % 2 else "S4")                # partlet pleats
    b = bodice(g, "P", "velvet", 15502, rows=(3, 10), neckline="square", point=True, straps=True)
    for face in (b.front, b.back):
        lozenges(face, 0, 3, 8, 7, "P2", "P3", "P1")
    b.front.hline(1, 6, 3, "M3")
    for face in b.sides:
        face.hline(0, face.w - 1, 10, "M2")
    sleeves(g, "P", "velvet", 15503, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        lozenges(arm.strip, 0, 0, 16, 4, "P2", "P3", "P1")
        lozenges(arm.strip, 0, 7, 16, 4, "P2", "P3", "P1")
    for box in arm_rings(g, "elbow_puff", 2.6, 3, 5, inflate=.12):
        solid(box, "S", "weave", 15504, 4)
        for face in box.sides:
            for x in range(1, face.w, 2):
                face.vline(x, 0, 2, "S3")
    ruff = g.piece("throat_frill", "TORSO", (-3, -1.6, -2.4), (6, 2, 5), inflate=.1)
    solid(ruff, "S", "plain", 15505, 4, edge=False)
    for face in ruff.sides:
        for x in range(face.w):
            face.set(x, 0, "S3" if x % 2 else "S4")
