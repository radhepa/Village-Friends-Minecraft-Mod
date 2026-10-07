"""Padded Jack & Mail Standard: a short padded jack with a mail collar over the shoulders and splinted leather forearms."""
from kit import body, sleeves
from kit_male import arm_blk, lozenge, mail

META = {
    "name": "Padded Jack & Mail Standard",
    "gender": "male",
    "description": "A short diamond-padded jack with a mail standard over neck and shoulders and splinted leather forearm guards.",
    "tags": ["martial", "rugged"],
}


def build(g):
    b = body(g, "P", "quilt", 7801)
    for face in b.sides:
        lozenge(face, "P", 2, step=4, ox=face.x0)
    b.front.vline(4, 0, 11, "P0")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "P1")
    sleeves(g, "P", "quilt", 7802, rows=(0, 10))
    standard = g.piece("mail_standard", "TORSO", (-6, -1.0, -3.0), (12, 3, 6), inflate=.06)
    for face in standard.faces:
        mail(face, ox=face.x0)
    for face in standard.sides:
        face.hline(0, face.w - 1, 2, "M1")
    for i, side in enumerate(("right", "left")):
        splint = arm_blk(g, f"{side}_splinted_vambrace", side, 4.8, (5, 4, 5), "L", 2, "leather", 7803 + i, inflate=.08)
        for face in splint.sides:
            for x in range(0, face.w, 2):
                face.vline(x, 0, 3, "M2")                               # steel splints
            face.hline(0, face.w - 1, 1, "L1")
