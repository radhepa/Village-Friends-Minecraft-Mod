"""Cross-Gartered Hose: close-fitting hose bound with criss-crossed leather garters, low turnshoes."""
from kit import SIDES, footwear, legs, waistband
from paint import line

META = {
    "name": "Cross-Gartered Hose",
    "description": "Fitted wool hose with leather garters criss-crossed up the shins, and low turnshoes.",
    "tags": ["casual", "slim"],
}


def build(g):
    legs(g, "P", "velvet", 1101, rows=(0, 10), crease=False)
    waistband(g, "P", "velvet", 1102)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            for y0 in (4, 7):   # two bold X's of leather garter up each shin
                line(face, 0, y0, 3, y0 + 3, "L3")
                line(face, 3, y0, 0, y0 + 3, "L2")
            face.hline(0, face.w - 1, 4, "L2")
    footwear(g, "shoe", top=10)
