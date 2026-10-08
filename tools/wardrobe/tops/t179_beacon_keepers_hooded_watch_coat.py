"""Beacon Keeper's Hooded Watch Coat: a heavy knee-length coat faced with quilting down the front, its deep lined hood
thrown back, soot on the shoulders from the fire basket and a flat oil flask strapped at the belt."""
from kit import belt, body, flaps, pouch, sleeves
from kit_male import blk, hood_down, lozenge, toggles
from paint import fabric

META = {
    "name": "Beacon Keeper's Hooded Watch Coat",
    "gender": "male",
    "description": "A heavy knee-length watch coat faced with quilting down the front, its deep lined hood thrown back, "
                   "soot on the shoulders from the beacon fire and a flat oil flask at the belt.",
    "tags": ["rugged", "sea", "work"],
    "covers_waist": True,
}

FLASK = (2.5, 9.9, -3.4)     # the flask's strap meets the belt here; flask and stopper share the hinge


def build(g):
    b = body(g, "P", "weave", 33320)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    lozenge(f, "A", 2, step=3, rows=range(1, 12))                         # quilted facing, then the coat over it
    fabric(f, "P", "weave", 33326, 2, 0, 1, 2, 11), fabric(f, "P", "weave", 33327, 2, 6, 1, 2, 11)
    f.vline(2, 1, 11, "P3"), f.vline(5, 1, 11, "P1")                    # the coat's front edges
    toggles(f, 3, (3, 6), "L4", "L1")
    for face in b.sides:                                                  # soot on the shoulders
        for x in range(face.w):
            if (x + face.x0) % 3 != 1:
                face.set(x, 0, "K2")
    b.top.hline(0, 7, 0, "K2"), b.top.hline(0, 7, 3, "K2")
    sleeves(g, "P", "weave", 33321, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm").strip
        arm.hline(0, 15, 8, "P3"), arm.hline(0, 15, 9, "P1")             # deep turned cuffs
        for x in range(0, 16, 2):
            arm.set(x, 0, "K2")
    hood = hood_down(g, "P", "weave", 33322, width=8, y=-1.2, z=3.0, tilt=14, lining="A2")
    hood.top.hline(1, 6, 0, "A3")
    hood.back.hline(0, 7, 0, "K2")
    belt(g, "belt", 9.4, height=1)
    # The oil flask: flat and broad-shouldered, a cork stopper, strapped through the belt.
    flask = blk(g, "oil_flask", FLASK, (3, 3, 1), "M", 2, "smooth", 33323, origin=(-1.5, .7, -.5), motion="flap_front")
    flask.front.vline(0, 0, 2, "M3"), flask.front.set(1, 1, "M4")
    flask.front.hline(0, 2, 2, "M1")
    stopper = blk(g, "oil_flask_stopper", FLASK, (1, 1, 1), "L", 3, "plain", 33324, origin=(-.5, -.3, -.5),
                  motion="flap_front", edge=False)
    stopper.top.fill("L4")
    pouch(g, "tinder_pouch", (-2.4, 9.9, -2.9), (2, 2, 1), flap="L3")
    for face in flaps(g, "coat_skirt", 7, "P", "weave", 33325, top=10.8, slit=True, hem="P1"):
        face.vline(3, 0, 5, "P1"), face.vline(5, 0, 5, "P3")
