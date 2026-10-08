"""Tinker's Pot-Clanking Coat: a patched road coat with a kettle, a frying pan and a ladle clanking on the back."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk
from kit_m07 import baldric, disc, hang, outer, patch, ring_marks, stick
from paint import solid

META = {
    "name": "Tinker's Pot-Clanking Coat",
    "gender": "male",
    "description": "A tinker's road coat patched in odd cloths and mismatched buttons, a rope over the shoulder hung with a kettle, a frying pan and a ladle that clank on his back.",
    "tags": ["rugged", "work", "whimsical"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 37000)
    neckline(b.front, "round", "P")
    b.front.vline(4, 2, 11, "P0")                                        # front opening
    for y, key in ((3, "M3"), (6, "L3"), (9, "A3")):                    # three odd buttons
        b.front.set(3, y, key)
    patch(b.front, 5, 5, 3, 3, "S2")
    patch(b.front, 0, 7, 3, 3, "A2")
    patch(b.back, 4, 7, 3, 3, "S2")
    sleeves(g, "P", "weave", 37001, rows=(0, 10), cuff="P1")
    for side, fill in (("right", "S2"), ("left", "L2")):
        patch(outer(g.part(f"{side}_arm"), side), 0, 4, 4, 3, fill, "K1")   # elbow patches
    jacket = g.part("jacket")
    baldric(jacket.front, jacket.back, from_left=True, key="S2", edge="S1")  # the rope the pots hang on
    belt(g, "belt", 9.4, height=1)

    # The kettle rides high on the back, lid knob and spout and all.
    kettle = blk(g, "kettle", (1.0, 1.6, 4.0), (3, 3, 3), "M", 2, "smooth", 37002)
    for face in kettle.sides:
        face.hline(0, 2, 0, "M3"), face.set(1, 1, "M4")
    kettle.bottom.fill("K1")
    blk(g, "kettle_knob", (1.0, .6, 4.0), (1, 1, 1), "M", 3, "smooth", 37003, edge=False)
    spout = g.piece("kettle_spout", "TORSO", (0, -.5, -.5), (2, 1, 1), pivot=(-.5, 3.4, 4.0), rotation=(0, 0, 30))
    solid(spout, "M", "smooth", 37004, 2, edge=False)
    # The black iron frying pan hangs below it, handle down to the right hip.
    for box in disc(g, "frying_pan", (-1.2, 6.6, 2.85), 5, "K", 2, seed=37005):
        ring_marks(box.back, 2.5, 2.5, 2.0, "K3", ox=0 if box.w == 5 else 1, oy=1 if box.w == 5 else 0)
        box.back.set(box.w // 2, box.h // 2, "K1")
    stick(g, "pan_handle", (-3.0, 10.0, 2.85), 4, "K", 2, rotation=(0, 0, 40), seed=37006)
    # A long ladle swinging off the rope on the other side.
    stick(g, "ladle_haft", (2.7, 5.0, 2.8), 5, "M", 3, centered=False, seed=37007, motion="sway")
    bowl = g.piece("ladle_bowl", "TORSO", (-1, 5, -1), (2, 1, 2), pivot=(2.7, 5.0, 2.8), motion="sway")
    solid(bowl, "M", "smooth", 37008, 2, edge=False)
    # A tin cup clinks at the left hip.
    cup = hang(g, "tin_cup", (2.9, 9.9, -3.0), (2, 2, 2), "M", 3, "smooth", 37009)
    cup.top.fill("M0"), cup.front.hline(0, 1, 0, "M4")
    front, back = flaps(g, "coat_skirt", 5, "P", "weave", 37010, top=10.8, slit=True)
    for face in (front, back):
        face.hline(0, 8, 4, "P1")
    patch(front, 1, 1, 3, 3, "L3")                                # a leather patch on the skirt
