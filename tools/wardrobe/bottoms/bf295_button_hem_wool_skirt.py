"""Button-Hem Wool Skirt: a wool skirt faced at the hem with a dark band studded with a row of buttons, buttoned shut at the left hip."""
from kit_female import buttons, shoes, skirt

META = {
    "name": "Button-Hem Wool Skirt",
    "gender": "female",
    "description": "A wool skirt with a dark faced band at the hem studded with a row of bright buttons, a buttoned placket at the left hip and laced ankle boots.",
    "tags": ["casual", "tailored", "skirt"],
}


def button_band(face):
    h = face.h
    face.hline(0, face.w - 1, h - 4, "P3")
    for y in (h - 3, h - 2, h - 1):
        face.hline(0, face.w - 1, y, "P1")
    face.hline(0, face.w - 1, h - 1, "P0")
    for x in range(1, face.w, 3):
        face.set(x, h - 2, "M3")


def build(g):
    s = skirt(g, "P", "weave", 60380, top=9.8, length=10, flare=6)
    s.paint(button_band, sides=False)
    for box in (s.right, s.left):
        for face in (box.front, box.back):
            face.vline(0, face.h - 3, face.h - 1, "P1")
    placket = s.left.left
    placket.vline(2, 1, 5, "P1")
    buttons(placket, 3, 1, 5, "M3", step=2)
    shoes(g, "ankle", "L", 2, top=8)
