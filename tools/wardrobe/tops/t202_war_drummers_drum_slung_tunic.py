"""War Drummer's Drum-Slung Tunic: a chevron-sleeved tunic with a rope-tensioned tabor slung at the hip and sticks in the strap."""
from kit import SIDES, body, flaps, neckline, sleeves
from kit_m04 import baldric, hanging
from paint import solid

META = {
    "name": "War Drummer's Drum-Slung Tunic",
    "gender": "male",
    "description": "A short marching tunic with chevrons down the sleeves and a dagged hem, a rope-tensioned tabor slung "
                   "on a broad strap at the left hip and a pair of drumsticks thrust through the strap across the chest.",
    "tags": ["martial", "whimsical"],
    "covers_waist": True,
}

S = 34240


def build(g):
    b = body(g, "P", "weave", S)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", S + 1, rows=(0, 10), cuff="A2")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        for y0 in (2, 5):                                                  # chevrons down the outer sleeve
            outer.set(0, y0 + 1, "A2"), outer.set(1, y0, "A3"), outer.set(2, y0, "A3"), outer.set(3, y0 + 1, "A2")
    baldric(g, "right", "L", 2, rows=10)
    belt = g.piece("belt", "TORSO", (-4.6, 9.8, -2.6), (9, 1, 5), inflate=.07)
    solid(belt, "L", "leather", S + 2, 1, edge=False)
    belt.front.set(1, 0, "M3")
    # Drumsticks thrust crosswise through the strap on the chest.
    for i, (x, rz) in enumerate(((-1.4, 30), (-.6, -18))):
        stick = g.piece(f"drumstick_{i}", "TORSO", (-.5, -2.5, -.5), (1, 5, 1), pivot=(x, 3.4, -2.75), rotation=(0, 0, rz))
        solid(stick, "L", "plain", S + 3 + i, 3, edge=False)
        stick.strip.hline(0, stick.strip.w - 1, 0, "S4")                   # knobbed heads
        stick.top.fill("S4")
    # The tabor: a wooden shell, skin heads, rims and a zig-zag tension rope.
    shell = hanging(g, "tabor_shell", 1.8, 9.8, (4, 4, 3), "A", 2, "plain", S + 5, top=10.2)
    for face in shell.sides:
        face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 3, "L1")   # hoops
        for x in range(face.w):
            face.set(x, 1 + x % 2, "S4")                                   # zig-zag tension rope
    shell.top.fill("S4"), shell.bottom.fill("S2")                          # skin heads
    shell.top.set(1, 1, "S3")
    hook = hanging(g, "tabor_hook", 2.8, 9.2, (1, 1, 1), "M", 3, "smooth", S + 6, top=10.2, dz=-1.0)
    hook.front.fill("M4")
    for face in flaps(g, "tunic_skirt", 3, "P", "weave", S + 7, top=10.8):
        for x in range(0, 9, 2):
            face.set(x, 2, "P0")                                           # dagged hem
        face.hline(0, 8, 1, "A2")
