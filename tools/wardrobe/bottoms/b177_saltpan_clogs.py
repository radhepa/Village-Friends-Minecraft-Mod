"""Saltpan Clogs: linen trousers rolled to mid-calf and ringed with dried salt tide-marks, bare shins, and chunky
carved wooden clogs with a leather instep strap for standing in the brine."""
from kit import SIDES, legs, waistband
from kit_male import leg_blk, leg_rings
from paint import k

META = {
    "name": "Saltpan Clogs",
    "gender": "male",
    "description": "Linen trousers rolled to mid-calf and ringed with white salt tide-marks, bare shins, and chunky carved "
                   "wooden clogs with a leather instep strap for standing in the brine.",
    "tags": ["work", "relaxed", "sea"],
    "rejects": ["armor"],
}

# Dried brine: a wavy white line around each leg, the high-water mark of the pans.
TIDE = [3, 3, 4, 4, 3, 3, 3, 4, 4, 4, 3, 3, 4, 4, 3, 3]


def build(g):
    legs(g, "P", "weave", 33260, rows=(0, 6), crease=False)
    body = waistband(g, "P", "weave", 33261)
    body.front.set(3, 10, "S3"), body.front.set(4, 10, "S3")             # the drawstring knot
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for x, y in enumerate(TIDE):
            leg.strip.set(x, y, "S4")
            leg.strip.set(x, y + 1, "P1")
        leg.strip.hline(0, 15, 9, "L2")                                   # inside the clog
        for y in (10, 11):
            leg.strip.hline(0, 15, y, "L2")
        leg.bottom.fill("L1")
    for i, ring in enumerate(leg_rings(g, "trouser_roll", 5.4, "P", (5, 2, 5), 2, "weave", 33262, inflate=.1)):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P3")
            for x in range(face.w):
                face.set(x, 1, "S4" if (x + face.x0 + i) % 4 == 0 else "P1")
    for i, side in enumerate(SIDES):
        # The clog: one block of carved wood round the foot, a raised toe and a leather strap over the instep.
        clog = leg_blk(g, f"{side}_clog", side, 9.0, (5, 3, 6), "L", 3, "plain", 33264 + i, dz=-.6, inflate=.05)
        for face in clog.sides:
            for y in range(3):
                for x in range(face.w):
                    face.set(x, y, k("L", 3 if (x + face.x0) % 3 else 2))  # carving marks along the grain
            face.hline(0, face.w - 1, 2, "L1")
        clog.front.hline(0, 4, 0, "L4")
        clog.top.fill("L2")
        for x in range(5):
            clog.top.set(x, 0, "L1")
        clog.bottom.fill("L0")
        strap = leg_blk(g, f"{side}_clog_strap", side, 8.6, (5, 1, 4), "L", 1, "leather", 33266 + i, dz=-.6,
                        inflate=.12)
        strap.front.set(2, 0, "M3")
