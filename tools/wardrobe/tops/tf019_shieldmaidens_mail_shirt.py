"""Shieldmaiden's Mail Shirt: a ring-mail shirt over a wool tunic, a fur shoulder mantle and a painted round shield on her back."""
from kit_female import fur_box, girdle, mail, mantle, over_flaps
from paint import fabric, solid, strip_fabric

META = {
    "name": "Shieldmaiden's Mail Shirt",
    "gender": "female",
    "description": "A ring-mail shirt over a wool tunic, a fur mantle over the shoulders and a painted round shield slung behind.",
    "tags": ["armor", "martial"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    for face in b.sides:
        mail(face, "M", 2)
    fabric(b.top, "M", "smooth", 11901, 3), fabric(b.bottom, "M", "smooth", 11901, 1)
    b.front.hline(2, 5, 0, "P2"), b.front.hline(3, 4, 1, "P2")      # the tunic's neck
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        mail(arm.strip, "M", 2, 0, 5)
        strip_fabric(arm, "P", "weave", 11902, 2, 6, 11)
        arm.strip.hline(0, 15, 6, "M1")
        arm.strip.hline(0, 15, 10, "A2")
        fabric(arm.top, "M", "smooth", 11903, 3)
    fur = mantle(g, "fur_mantle", "S", "plain", 11904, 3, height=3, width=17, depth=6, y=-1.0)
    fur_box(fur, "S", 11905, 3)
    shield = g.piece("shield", "TORSO", (-3.5, -3.5, 0), (7, 7, 1), pivot=(.6, 5.0, 2.7))
    solid(shield, "P", "plain", 11906, 2)
    face = shield.back
    for y in range(7):
        for x in range(7):
            if (x < 3) == (y < 3) and x != 3 and y != 3:
                face.set(x, y, "A2")
        face.set(3, y, "S3")
    face.hline(0, 6, 3, "S3")
    for x, y in [(0, 0), (6, 0), (0, 6), (6, 6)]:
        face.set(x, y, "M2")
    boss = g.piece("shield_boss", "TORSO", (-1, -1, 0), (2, 2, 1), pivot=(.6, 5.0, 3.6))
    solid(boss, "M", "smooth", 11907, 3, edge=False)
    girdle(g, "belt", 8.0, role="L", height=1)
    f, bk = over_flaps(g, "mail_skirt", 3, "M", "smooth", 11908, base=2, width=10, top=9.0)
    for face in (f, bk):
        mail(face, "M", 2)
