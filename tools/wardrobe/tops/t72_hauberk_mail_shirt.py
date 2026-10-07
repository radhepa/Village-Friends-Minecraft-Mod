"""Hauberk Mail Shirt: a mail shirt to mid-thigh with elbow sleeves over a padded tunic, its coif lowered round the neck."""
from kit import belt, body, sleeves
from kit_male import mail
from paint import solid

META = {
    "name": "Hauberk Mail Shirt",
    "gender": "male",
    "description": "A riveted mail hauberk to mid-thigh with elbow-length sleeves over a padded tunic, its mail coif lowered round the neck.",
    "tags": ["armor", "martial"],
    "requires": ["sturdy"],
    "covers_waist": True,
}


def build(g):
    body(g, "P", "quilt", 7201)
    jacket = g.part("jacket")
    for face in jacket.sides:
        mail(face, ox=face.x0)
    mail(jacket.top)
    jacket.front.hline(2, 5, 0, None)
    sleeves(g, "P", "quilt", 7202, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        over = g.part(f"{side}_sleeve")
        mail(over.strip, rows=range(0, 6))
        over.strip.hline(0, over.strip.w - 1, 5, "M1")
        mail(over.top)
    coif = g.piece("lowered_coif", "TORSO", (-4.6, -1.2, -2.7), (9, 2, 5), inflate=.1)
    for face in coif.faces:
        mail(face, ox=face.x0)
    belt(g, "belt", 9.6)
    for name, z, motion, face_name in (("mail_skirt_front", -2.85, "flap_front", "front"),
                                        ("mail_skirt_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 5, 1), pivot=(0, 11.4, z), motion=motion)
        solid(panel, "M", "smooth", 7203, 2)
        for face in panel.faces:
            mail(face, ox=face.x0)
        face = getattr(panel, face_name)
        face.vline(4, 1, 4, "M0")                                        # riding slit
        face.hline(0, 8, 4, "M1")
