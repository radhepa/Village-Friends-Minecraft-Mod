"""Belted Sleeveless Overtunic: a square-necked overtunic with deep-cut armholes, a broad buckled belt and pouch, its slit hem over a longer undertunic."""
from kit import SIDES, belt, body, neckline, sleeves
from kit_male import blk
from paint import k, solid

META = {
    "name": "Belted Sleeveless Overtunic",
    "gender": "male",
    "description": "A square-necked sleeveless overtunic cut away deep at the armholes, girt with a broad buckled belt and a small pouch, its front-slit hem stopping short to show a longer undertunic.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}


def build(g):
    under = body(g, "S", "weave", 40500, base=3)
    neckline(under.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 40501, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "S2"), arm.strip.hline(0, arm.strip.w - 1, 10, "S4")
    over = body(g, "P", "weave", 40502, layer="jacket")
    f, bk = over.front, over.back
    # Square neck, edged.
    for x in range(2, 6):
        f.clear(x, 0), f.clear(x, 1)
    f.hline(2, 5, 2, "P3"), f.vline(1, 0, 1, "P3"), f.vline(6, 0, 1, "P1")
    bk.hline(2, 5, 0, "P1")
    # Deep armholes: the overtunic is cut away at the shoulders and down the sides.
    for face in (f, bk):
        for y in range(0, 5):
            face.clear(0, y), face.clear(7, y)
        face.set(1, 4, "P1"), face.set(6, 4, "P1")
        face.set(0, 5, "P1"), face.set(7, 5, "P1")
    for face in (over.right, over.left):
        for y in range(0, 6):
            face.hline(0, face.w - 1, y, None)
    f.vline(4, 3, 8, "P1")                                                # front seam
    # Broad belt with a squared buckle, a hanging tongue and a small pouch.
    wide = belt(g, "belt", 8.8, height=2, buckle="M")
    tongue = g.piece("belt_tongue", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(1.3, 10.4, -2.75), rotation=(0, 0, -4))
    solid(tongue, "L", "leather", 40503, 2, edge=False)
    tongue.front.set(0, 2, "M3")
    pouch = blk(g, "belt_pouch", (-2.5, 10.6, -3.4), (2, 3, 1), "L", 2, "leather", 40504, motion="flap_front")
    pouch.front.hline(0, 1, 0, "L3"), pouch.front.set(1, 1, "M3")
    # The undertunic's longer hem, behind the overtunic's slit skirt.
    for name, z, motion, face_name in (("front", -2.80, "flap_front", "front"), ("back", 1.80, "flap_back", "back")):
        hem = g.piece(f"undertunic_{name}", "TORSO", (-4, 0, 0), (8, 6, 1), pivot=(0, 11.2, z), motion=motion)
        solid(hem, "S", "weave", 40505 + (name == "back"), 3)
        getattr(hem, face_name).hline(0, 7, 5, "S1")
    for name, z, motion, face_name in (("front", -2.85, "flap_front", "front"), ("back", 1.85, "flap_back", "back")):
        skirt = g.piece(f"overtunic_{name}", "TORSO", (-4.5, 0, 0), (9, 4, 1), pivot=(0, 11.2, z), motion=motion)
        solid(skirt, "P", "weave", 40507 + (name == "back"), 2)
        face = getattr(skirt, face_name)
        face.hline(0, 8, 0, k("P", 3))
        face.hline(0, 8, 3, "P1")
        if name == "front":
            face.vline(4, 1, 3, "P0")                                     # the riding slit
