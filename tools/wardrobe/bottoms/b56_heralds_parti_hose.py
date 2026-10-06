"""Herald's Parti Hose: mi-parti hose, one leg in each livery colour, pale garters and long-toed black shoes."""
from kit import SIDES, footwear, waistband
from kit_male import toe_pieces
from paint import fabric, strip_fabric

META = {
    "name": "Herald's Parti Hose",
    "gender": "male",
    "description": "Mi-parti livery hose, one leg in each of the tabard's colours, with pale garters and long-toed black shoes.",
    "tags": ["fancy", "slim"],
    "locked_to": "t56_heralds_livery_tabard",
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        role = "A" if side == "right" else "P"
        strip_fabric(leg, role, "velvet", 5611, 2, 0, 9)
        fabric(leg.top, role, "velvet", 5611, 2)
        leg.strip.hline(0, leg.strip.w - 1, 5, "S3")                      # garter
        leg.strip.hline(0, leg.strip.w - 1, 6, "S1")
    body = waistband(g, "P", "velvet", 5612)
    for face in body.sides:
        for y in (9, 10, 11):
            for x in range(face.w):
                if (x < face.w // 2) == (face.name != "back"):
                    face.set(x, y, "A2" if y > 9 else "A3")
    footwear(g, "shoe", top=10, role="K", base=1, sole="K0")
    for toe in toe_pieces(g, "long_toe", (2, 1, 2), "K", base=1, texture="smooth", y=11.0, z=-2.1):
        toe.top.fill("K2")
