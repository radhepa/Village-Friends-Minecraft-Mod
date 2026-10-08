"""Chaff-Dusted Breeches: full knee breeches powdered with chaff from the threshing floor, buttoned knee bands, ribbed hose and shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_m01 import outer
from kit_male import flecks, leg_blk, ribbing
from paint import rnd, strip_fabric

META = {
    "name": "Chaff-Dusted Breeches",
    "gender": "male",
    "description": "Full woollen knee breeches powdered pale with chaff from the threshing floor, buttoned knee bands, ribbed hose and plain shoes.",
    "tags": ["work", "simple", "casual"],
}


def chaff(face, seed, rows, dense_from):
    """Chaff: short pale slivers, thicker toward the knee and on the lap."""
    for y in rows:
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            if r < (.11 if y >= dense_from else .04):
                face.set(x, y, "S4" if r < .035 else "S3")
                if r < .015 and x + 1 < face.w:
                    face.set(x + 1, y, "S3")


def build(g):
    legs(g, "P", "weave", 31211, rows=(0, 5), crease=False)
    waistband(g, "P", "weave", 31212)
    footwear(g, "shoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(pants, "P", "weave", 31213 + i, 2, 0, 4)              # full breeches standing off the thigh
        for face in pants.sides:
            face.vline(1, 1, 3, "P1"), face.set(2, 4, "P1")
            face.hline(0, face.w - 1, 0, "P3")
        chaff(pants.strip, 31215 + i, range(0, 5), 2)
        chaff(leg.strip, 31217 + i, range(0, 5), 3)
        ribbing(leg.strip, "S", 3, rows=range(6, 10))                       # ribbed hose
        leg.strip.hline(0, leg.strip.w - 1, 5, "P1")
        flecks(leg.strip, "S4", 31219 + i, .08, rows=range(6, 9))
        band = leg_blk(g, f"{side}_knee_band", side, 4.8, (5, 1, 5), "P", 2, "weave", 31221 + i)
        for face in band.sides:
            face.hline(0, face.w - 1, 0, "P1")
        o = outer(band, side)
        o.set(1, 0, "M3"), o.set(3, 0, "M3")
        for y in (2, 4):
            outer(pants, side).set(2, y, "M3")                               # buttons up the outer knee
    body = g.part("body")
    chaff(body.front, 31223, range(9, 12), 10)
    body.front.set(4, 9, "M3")
