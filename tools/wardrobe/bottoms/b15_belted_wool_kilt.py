"""Belted Wool Kilt: a pleated tartan kilt with a sporran, knee socks with flashes and ghillie shoes."""
from kit import SIDES, belt, footwear, leg_bone, stockings
from paint import solid

META = {
    "name": "Belted Wool Kilt",
    "description": "A pleated tartan kilt, leather sporran, knee socks with garter flashes and laced ghillie shoes.",
    "tags": ["casual", "kilt"],
    "rejects": ["armor"],
}


def tartan(face, ox=0):
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = (x + ox) % 6, y % 6
            band_x, band_y = gx in (0, 1), gy in (0, 1)
            key = "P0" if band_x and band_y else "P1" if band_x or band_y else "P2"
            if (gx == 4 or gy == 4) and not (band_x or band_y):
                key = "A2"
            face.set(x, y, key)


def build(g):
    body = g.part("body")
    for face in body.sides:
        tartan(type(face)(face.layer, face.x0, face.y0 + 9, face.w, 3, face.name))
    for side in SIDES:
        tartan(type(g.part(f"{side}_leg").strip)(g.part(f"{side}_leg").layer, g.part(f"{side}_leg").strip.x0,
                                                  g.part(f"{side}_leg").strip.y0, 16, 4, "strip"))
    stockings(g, "S", (6, 10), base=3)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, leg.strip.w - 1, 6, "S2")
        flash = g.piece(f"{side}_garter_flash", leg_bone(side), (-.5, 0, -.5), (1, 2, 1), pivot=(-1.5 if side == "right" else 1.5, 6.6, -2.4))
        solid(flash, "A", "plain", 1501, 2, edge=False)
    for name, z, motion, face_name in (("kilt_front", -2.85, "flap_front", "front"), ("kilt_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.6, 0, 0), (9, 6, 1), pivot=(0, 10.6, z), motion=motion)
        for face in panel.faces:
            tartan(face, face.x0)
        face = getattr(panel, face_name)
        for x in range(0, 9, 2):
            face.vline(x, 1, 5, "P0")   # pleats
    for name, x in (("kilt_right", -5.0), ("kilt_left", 4.0)):
        side = g.piece(name, "TORSO", (0, 0, -2), (1, 5, 4), pivot=(x, 10.6, 0))
        for face in side.faces:
            tartan(face, face.x0 + 2)
    belt(g, "waist_belt", 10.0)
    sporran = g.piece("sporran", "TORSO", (-1.5, 0, -.5), (3, 3, 1), pivot=(0, 11.4, -3.2), motion="flap_front")
    solid(sporran, "L", "leather", 1502, 2)
    sporran.front.hline(0, 2, 0, "L3"), sporran.front.set(1, 1, "M3"), sporran.front.hline(0, 2, 2, "S3")
    footwear(g, "turnshoe", top=10)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "L4"), pants.front.set(2, 10, "L4")
