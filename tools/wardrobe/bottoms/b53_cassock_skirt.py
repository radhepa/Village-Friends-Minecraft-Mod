"""Cassock Skirt: the cassock's ankle-length skirts with their buttons running on to the hem, and buckled black shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import buttons, skirt_panels

META = {
    "name": "Cassock Skirt",
    "gender": "male",
    "description": "The cassock's ankle-length skirts with the long run of buttons continuing to the hem, over buckled black shoes.",
    "tags": ["holy", "robe", "scholarly"],
    "locked_to": "t53_clerks_buttoned_cassock",
}


def build(g):
    legs(g, "P", "smooth", 5311, base=1, rows=(0, 9), crease=False)
    waistband(g, "P", "smooth", 5312, base=1)
    footwear(g, "shoe", top=10, role="K", base=1, sole="K0")
    for side in SIDES:
        g.part(f"{side}_pants").front.set(1, 10, "M3"), g.part(f"{side}_pants").front.set(2, 10, "M3")
    front, back, sides = skirt_panels(g, "cassock", 11, "P", "smooth", 5313, base=1, top=10.6, side_len=10)
    front.vline(5, 0, 10, "P0")
    buttons(front, 4, 0, 10, 1, "M3")
    back.vline(4, 1, 10, "P0")
    for face in (front, back):
        face.hline(0, 8, 10, "P0")
