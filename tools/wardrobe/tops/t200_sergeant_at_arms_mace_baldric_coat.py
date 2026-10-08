"""Sergeant-at-Arms' Mace-Baldric Coat: a long faced coat with a studded baldric carrying a flanged mace at the hip."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import blk, buttons
from kit_m04 import baldric, hanging
from paint import strip_fabric

META = {
    "name": "Sergeant-at-Arms' Mace-Baldric Coat",
    "gender": "male",
    "description": "A long knee-skirted coat with contrasting facings, cuffs and stand collar, "
                   "and a broad studded baldric from which a flanged iron mace hangs at the left hip.",
    "tags": ["martial", "tailored"],
    "covers_waist": True,
}

S = 34160

def build(g):
    b = body(g, "P", "twill", S)
    f = b.front
    f.vline(3, 0, 11, "A2"), f.vline(4, 0, 11, "A3")                     # facings
    buttons(f, 4, 2, 8, 2, "M3")
    sleeves(g, "P", "twill", S + 1, rows=(0, 10))
    for side in SIDES:
        sl = g.part(f"{side}_sleeve")
        strip_fabric(sl, "A", "plain", S + 2, 2, 7, 10)                    # deep turned-back cuffs
        sl.strip.hline(0, sl.strip.w - 1, 7, "A3"), sl.strip.hline(0, sl.strip.w - 1, 10, "A1")
        sl.front.set(1, 8, "M3")
    stand = collar(g, "stand_collar", "A", "plain", base=2, height=1, y=-.9)
    stand.front.set(4, 0, "M3")
    baldric(g, "right", "L", 2, rows=10, stud="M3", every=3)
    belt = blk(g, "belt", (0, 9.8, 0), (9, 1, 5), "L", 1, "leather", S + 3, inflate=.06, edge=False)
    belt.front.set(1, 0, "M3")
    # The mace, hung head-down by its wrist ring at the left hip.
    ring = hanging(g, "mace_ring", 3.0, 10.2, (1, 1, 1), "M", 3, "smooth", S + 4, top=10.4, dz=.1)
    ring.front.fill("M4")
    shaft = hanging(g, "mace_shaft", 3.0, 11.2, (1, 4, 1), "L", 2, "plain", S + 5, top=10.4, dz=-.1)
    shaft.front.set(0, 0, "L3"), shaft.front.set(0, 1, "L0"), shaft.front.set(0, 2, "L0")    # wrapped grip
    head = hanging(g, "mace_head", 3.0, 15.2, (2, 3, 2), "M", 2, "smooth", S + 6, top=10.4, dz=.4)
    for face in head.sides:
        face.vline(0, 0, 2, "M3"), face.vline(1, 0, 2, "M1")              # flanges
        face.hline(0, 1, 2, "M0")
    head.top.fill("M3")
    front, back = flaps(g, "coat_skirt", 6, "P", "twill", S + 7, top=10.8, slit=True)
    front.vline(3, 1, 5, "A2"), front.vline(4, 1, 5, "A3")
    for face in (front, back):
        face.hline(0, 8, 5, "A2")
