"""Scribe's Penner-Hung Kirtle: a spiral-laced kirtle with elbow-length sleeves over the chemise's
gathered forearms, and the scribe's tools on a cord at the right hip: a long penner case with quills
showing at its mouth and a horn inkpot, with a small penknife at the left."""
from kit import body, sleeves
from kit_female import arm_rings, girdle, lacing, neck
from kit_f05 import dangle
from paint import solid

META = {
    "name": "Scribe's Penner-Hung Kirtle",
    "gender": "female",
    "description": "A spiral-laced kirtle with elbow sleeves over linen forearms, a penner of quills and a horn inkpot hung at the hip.",
    "tags": ["scholarly", "casual"],
}


def build(g):
    b = body(g, "P", "twill", 55381, base=2)
    neck(b.front, "scoop", "P", 2, edge="S4")
    lacing(b.front, 3, 2, 8, "spiral", lace="L3", under="P1", eyelet="M3")
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P1"), face.vline(6, 2, 11, "P1")
    for arm in sleeves(g, "P", "twill", 55382, base=2, rows=(0, 11)):
        for y in range(6, 12):
            arm.strip.hline(0, 15, y, "S3")                            # the chemise's linen forearm
        for x in range(1, 16, 2):
            arm.strip.vline(x, 7, 10, "S2")
        arm.strip.hline(0, 15, 11, "S4")
    for box in arm_rings(g, "sleeve_edge", 3.4, 1, 5, inflate=.08):
        solid(box, "P", "twill", 55383, 3, edge=False)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "A2")
    girdle(g, "girdle", 8.2, role="L", base=1, height=1, buckle="M")
    # The penner: a long leather pen case capped in metal, quill tips at its mouth.
    cord = dangle(g, "penner_cord", -2.4, -.6, (3, 1, 1), "L", 2, "plain", top=9.0, seed=55384, edge=False)
    cord.front.set(1, 0, "L3")
    penner = dangle(g, "penner", -3.2, 1.4, (1, 6, 1), "L", 2, "leather", top=9.0, seed=55385, edge=False)
    for face in penner.sides:
        face.set(0, 0, "M3"), face.set(0, 5, "M2"), face.set(0, 3, "L1")
    quills = dangle(g, "penner_quills", -3.2, .4, (1, 1, 1), "S", 4, "plain", top=9.0, seed=55386, edge=False)
    quills.top.fill("S4"), quills.front.fill("S3")
    # The horn inkpot beside it, its stopper dark with ink.
    horn = dangle(g, "inkhorn", -1.6, 1.4, (2, 3, 1), "L", 3, "smooth", top=9.0, seed=55387, edge=False)
    for face in horn.sides:
        face.hline(0, face.w - 1, 0, "L4")
        face.set(face.w - 1, face.h - 1, "L2")
    stopper = dangle(g, "inkhorn_stopper", -1.6, .4, (1, 1, 1), "K", 2, "plain", top=9.0, seed=55388, edge=False)
    stopper.top.fill("K1")
    # A penknife in its little sheath at the left hip.
    knife = dangle(g, "penknife", 2.6, -.2, (1, 3, 1), "L", 1, "leather", top=9.0, seed=55389, edge=False)
    knife.front.set(0, 0, "M4")
