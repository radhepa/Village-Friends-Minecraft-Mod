"""Siege Engineer's Plumb-Line Coat: a piped working coat with dividers in the breast pocket, rolled plans and a plumb bob."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import buttons
from kit_m04 import hanging
from paint import solid

META = {
    "name": "Siege Engineer's Plumb-Line Coat",
    "gender": "male",
    "description": "A sober, piped working coat with a stand collar, brass dividers poking from the breast pocket, rolled "
                   "siege plans thrust through the belt and a brass plumb bob swinging from a cord at the hip.",
    "tags": ["scholarly", "tailored", "work"],
    "covers_waist": True,
}

S = 34480


def build(g):
    b = body(g, "P", "twill", S)
    f = b.front
    f.vline(4, 0, 11, "A2")                                                # piped front edge
    buttons(f, 3, 1, 9, 2, "M3")
    f.rect(5, 2, 3, 3, "P1"), f.hline(5, 7, 2, "A2")                      # breast pocket
    f.set(6, 1, "M3"), f.set(5, 1, "M4"), f.set(7, 1, "M4")               # dividers peeping out
    sleeves(g, "P", "twill", S + 1, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2")
        arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
        arm.front.vline(0, 1, 8, "P1")
    stand = collar(g, "stand_collar", "S", "plain", base=3, height=1, y=-.9)
    stand.front.set(4, 0, "S1")
    belt = g.piece("belt", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.07)
    solid(belt, "L", "leather", S + 2, 1, edge=False)
    belt.front.set(4, 0, "M3")
    # Rolled plans thrust through the belt at the right hip, tied with tape.
    for i, (x, y, n) in enumerate(((-3.0, 7.6, 6), (-2.0, 8.2, 5))):
        roll_ = hanging(g, f"rolled_plan_{i}", x, y, (1, n, 1), "S", 3, "plain", S + 3 + i, top=10.4, dz=-.2 - .4 * i)
        roll_.top.fill("S4")
        roll_.front.set(0, 0, "S4"), roll_.front.set(0, 2, "A2")
        for face in roll_.sides:
            face.set(0, n - 1, "S2")
    # Plumb bob on its cord at the left hip.
    cord = hanging(g, "plumb_cord", 2.6, 10.6, (1, 4, 1), "S", 2, "plain", S + 5, top=10.4, dz=.3)
    cord.front.vline(0, 0, 3, "S3")
    bob = hanging(g, "plumb_bob", 2.6, 14.6, (2, 2, 2), "M", 3, "smooth", S + 6, top=10.4, dz=.8)
    for face in bob.sides:
        face.set(0, 0, "M4"), face.set(1, 1, "M1"), face.set(0, 1, "M2")
    tip = hanging(g, "plumb_tip", 2.6, 16.6, (1, 1, 1), "M", 2, "smooth", S + 7, top=10.4, dz=.3)
    tip.front.fill("M1")
    for face in flaps(g, "coat_skirt", 5, "P", "twill", S + 8, top=10.8, slit=True):
        face.hline(0, 8, 4, "A2")
