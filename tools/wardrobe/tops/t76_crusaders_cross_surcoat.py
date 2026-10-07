"""Crusader's Cross Surcoat: a long pale surcoat with a great cross over a mail shirt and mail sleeves, girt with a sword belt."""
from kit import body, sleeves
from kit_male import mail
from paint import fabric, solid

META = {
    "name": "Crusader's Cross Surcoat",
    "gender": "male",
    "description": "A long pale surcoat bearing a great cross over a mail hauberk with mail sleeves, girt with a broad sword belt.",
    "tags": ["armor", "martial", "holy"],
    "locked_to": "b76_crusaders_mail_chausses",
    "covers_waist": True,
}


def cross(face, x0, y0, h):
    face.vline(x0, y0, y0 + h - 1, "A2"), face.vline(x0 + 1, y0, y0 + h - 1, "A2")
    face.hline(x0 - 2, x0 + 3, y0 + 2, "A2"), face.hline(x0 - 2, x0 + 3, y0 + 3, "A1")


def build(g):
    b = body(g, "M", "smooth", 7601)
    for face in b.sides:
        mail(face, ox=face.x0)
    jacket = g.part("jacket")
    for face in (jacket.front, jacket.back):
        fabric(face, "S", "weave", 7602, 3)
        cross(face, 3, 1, 9)
    jacket.front.hline(2, 5, 0, None)
    fabric(jacket.top, "S", "weave", 7602, 4)
    jacket.top.hline(2, 5, 1, None), jacket.top.hline(2, 5, 2, None)
    sleeves(g, "M", "smooth", 7603, rows=(0, 10))
    for side in ("right", "left"):
        mail(g.part(f"{side}_arm").strip, rows=range(0, 11))
    girdle = g.piece("sword_belt", "TORSO", (-4.6, 9.2, -2.6), (9, 2, 5), inflate=.06)
    solid(girdle, "L", "leather", 7604, 1, edge=False)
    girdle.front.hline(3, 5, 0, "M3"), girdle.front.set(4, 1, "M2")
    for name, z, motion, face_name in (("surcoat_front", -2.85, "flap_front", "front"),
                                        ("surcoat_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4, 0, 0), (8, 7, 1), pivot=(0, 11.2, z), motion=motion)
        solid(panel, "S", "weave", 7605, 3)
        face = getattr(panel, face_name)
        face.vline(3, 0, 6, "A2"), face.vline(4, 0, 6, "A2")
        face.vline(0, 1, 6, "S2"), face.vline(7, 1, 6, "S2")
        face.hline(0, 7, 6, "S1")
