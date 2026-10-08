"""Lay Sister's Hitched Work Habit: a working habit with the sleeves rolled to the elbow and the front
of its skirt hitched up into the girdle in a bunched roll, so it hangs short in front and full behind;
a wooden dibber and a seed sack ride at the girdle."""
from kit import body, roll, sleeves
from kit_female import girdle, neck, over_panel
from kit_f05 import dangle
from paint import line, solid

META = {
    "name": "Lay Sister's Hitched Work Habit",
    "gender": "female",
    "description": "A work habit with rolled sleeves, its front hitched up into the girdle in a bunched roll, a dibber and seed sack at the waist.",
    "tags": ["holy", "work", "robe"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 55241, base=2)
    neck(b.front, "round", "P", 2, edge="P3")
    for face in (b.front, b.back):
        face.vline(2, 2, 11, "P1"), face.vline(5, 2, 11, "P1")
    sleeves(g, "P", "twill", 55242, base=2, rows=(0, 4))
    roll(g, "P", 2.4, base=3)
    # The habit's back hangs full length; its front is hitched up short.
    back = over_panel(g, "habit_back", 11, "P", "twill", 55243, base=2, width=10, top=9.0, back=True)
    for x in (2, 5, 8):
        back.vline(x, 1, 10, "P1")
    back.hline(0, 9, 10, "P0")
    front = over_panel(g, "habit_front", 3, "P", "twill", 55244, base=2, width=10, top=9.0)
    # Drape folds swagging up to where the cloth is tucked in.
    line(front, 0, 2, 3, 0, "P1"), line(front, 9, 2, 6, 0, "P1")
    front.hline(2, 7, 1, "P3")
    front.hline(0, 9, 2, "P0")
    # The bunched roll of hitched cloth bulging over the girdle.
    bunch = g.piece("hitched_roll", "TORSO", (-4, 0, 0), (8, 2, 2), pivot=(0, 6.2, -3.4), inflate=.1)
    solid(bunch, "P", "twill", 55245, 2, edge=False)
    for face in bunch.sides:
        face.hline(0, face.w - 1, 0, "P3")
        face.hline(0, face.w - 1, 1, "P1")
        for x in range(1, face.w, 3):
            face.set(x, 0, "P2"), face.set(x, 1, "P0")
    bunch.top.fill("P3")
    girdle(g, "girdle", 8.1, role="L", base=1, height=1, buckle="M", wide=True)
    # A wooden dibber pushed through the girdle at the right hip.
    shaft = dangle(g, "dibber_shaft", -3.0, -1.5, (1, 5, 1), "L", 3, "plain", top=9.0, seed=55246, edge=False)
    for face in shaft.sides:
        face.set(0, 4, "L2"), face.set(0, 3, "L4")
    grip = dangle(g, "dibber_grip", -3.0, -2.5, (3, 1, 1), "L", 2, "plain", top=9.0, seed=55247, edge=False)
    grip.front.set(1, 0, "L3")
    # A seed sack tied at the neck, on the left hip.
    sack = dangle(g, "seed_sack", 2.8, -.4, (3, 3, 2), "S", 2, "weave", top=9.0, seed=55248)
    for face in sack.sides:
        face.hline(0, face.w - 1, 0, "S1")
        face.set(1, 2, "S1")
    tie = dangle(g, "seed_sack_tie", 2.8, -1.4, (1, 1, 1), "L", 2, "plain", top=9.0, seed=55249, edge=False)
    tie.top.fill("S3")
