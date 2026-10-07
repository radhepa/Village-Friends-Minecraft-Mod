"""Mail Skirt over Trews: a short skirt of riveted mail hung from the hips over wool trews, with low buckled boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import mail, skirt_panels

META = {
    "name": "Mail Skirt over Trews",
    "gender": "male",
    "description": "A short skirt of riveted mail hung from the hips to mid-thigh over wool trews, with low buckled boots.",
    "tags": ["martial", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 7811, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 7812)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        (pants.right if side == "right" else pants.left).set(1, 9, "M3")
    front, back, sides = skirt_panels(g, "mail_skirt", 4, "M", "smooth", 7813, top=10.6, side_len=3)
    for face in (front, back):
        mail(face, ox=face.x0)
        face.hline(0, 8, 3, "M1")
    for box in sides:
        for face in box.sides:
            mail(face, ox=face.x0)
