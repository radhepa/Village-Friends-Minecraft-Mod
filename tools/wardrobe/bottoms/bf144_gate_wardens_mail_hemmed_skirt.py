"""Gate Warden's Mail-Hemmed Skirt: a long heavy wool skirt with a deep band of ring mail sewn round the hem
against blades and dogs, over sturdy boots."""
from kit_female import mail, shoes, skirt, tier, waist_belt

META = {
    "name": "Gate Warden's Mail-Hemmed Skirt",
    "gender": "female",
    "description": "A long heavy wool skirt with a deep band of ring mail sewn round the hem, over sturdy boots.",
    "tags": ["martial", "sturdy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 54341, top=9.8, length=12, flare=7)
    s.band(4, "line", "L2", from_bottom=True)
    faces = tier(g, s, "mail_hem", 8, 4, role="M", texture="smooth", seed=54342, base=2, grow=1, flare=8)
    for face in faces:
        mail(face, "M", 2)
        face.hline(0, face.w - 1, 0, "L2")                             # the leather band the mail is sewn to
        face.hline(0, face.w - 1, face.h - 1, "M1")
    shoes(g, "boot", "L", 2, top=8)
    belt = waist_belt(g, "waist_belt", 9.3, height=2)
    belt.front.set(1, 1, "M3"), belt.front.set(9, 1, "M3")
