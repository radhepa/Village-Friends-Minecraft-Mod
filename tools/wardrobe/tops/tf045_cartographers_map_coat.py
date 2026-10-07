"""Cartographer's Map Coat: a pocketed open coat with rolled maps in the pockets, a map tube across the back and a compass."""
from kit import body, sleeves
from kit_female import neck, over_panel
from paint import fabric, solid

META = {
    "name": "Cartographer's Map Coat",
    "gender": "female",
    "description": "A long open coat with rolled maps poking from its pockets, a map tube across the back and a brass compass.",
    "tags": ["scholarly", "rugged"],
}


def build(g):
    b = body(g, "S", "weave", 14501, base=3)
    neck(b.front, "round", "S", 3)
    j = g.part("jacket")
    for face in (j.front,):
        fabric(face, "P", "twill", 14502, 2, 0, 0, 3, 12)
        fabric(face, "P", "twill", 14502, 2, 5, 0, 3, 12)
        face.vline(2, 0, 11, "P3"), face.vline(5, 0, 11, "P1")
        face.hline(0, 1, 7, "P1"), face.hline(6, 7, 7, "P1")         # pocket flaps
    for face in (j.right, j.left, j.back):
        fabric(face, "P", "twill", 14503, 2)
    fabric(j.top, "P", "twill", 14503, 3)
    j.back.vline(3, 4, 11, "P1")
    sleeves(g, "P", "twill", 14504, rows=(0, 11))
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "P3")
    for i, x in enumerate((-3.3, 3.3)):
        roll_ = g.piece(f"rolled_map_{i}", "TORSO", (-.5, -2, -.5), (1, 3, 1), pivot=(x, 8.0, -2.75), rotation=(0, 0, 12 - 24 * i))
        solid(roll_, "S", "plain", 14505 + i, 4)
        roll_.top.fill("S2")
    tube = g.piece("map_tube", "TORSO", (-1, -5, -1), (2, 10, 2), pivot=(0, 5.0, 3.4), rotation=(0, 0, 50))
    solid(tube, "L", "leather", 14507, 2)
    for face in tube.sides:
        face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 9, "M3")
    compass = g.piece("compass", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(0, 3.4, -2.8), inflate=.05)
    solid(compass, "M", "smooth", 14508, 3, edge=False)
    compass.front.set(0, 0, "S4"), compass.front.set(1, 1, "A2")
    for i, (x, width) in enumerate(((-3.2, 3), (3.2, 3))):
        face = over_panel(g, f"coat_front_{i}", 10, "P", "twill", 14509, width=width, top=9.0, x=x)
        face.vline(1 if i == 0 else 1, 0, 9, "P1" if i else "P3")
    back = over_panel(g, "coat_back", 10, "P", "twill", 14510, width=10, top=9.0, back=True)
    back.vline(4, 0, 9, "P1")
