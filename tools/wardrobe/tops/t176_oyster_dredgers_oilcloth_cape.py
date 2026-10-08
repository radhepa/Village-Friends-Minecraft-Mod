"""Oyster Dredger's Oilcloth Cape: a thick wool shirt under a short, stiff oilcloth cape buttoned at the throat, an
oyster knife at the belt and a net bag of grey oysters at the hip."""
from kit import belt, body, flaps, neckline, sleeves
from kit_m03 import gloss
from kit_male import blk, shoulder_cape

META = {
    "name": "Oyster Dredger's Oilcloth Cape",
    "gender": "male",
    "description": "A thick wool shirt under a short, stiff oilcloth cape buttoned at the throat, an oyster knife at the "
                   "belt and a net bag of grey oysters swinging at the hip.",
    "tags": ["sea", "work", "rugged"],
    "covers_waist": True,
}

BAG = (2.6, 9.8, -3.9)       # the bag hangs from the belt here; bag and cord share the hinge


def build(g):
    b = body(g, "P", "weave", 33200)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 33201, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "L2")                # cuffs strapped against the wet
    # The cape: stiff oilcloth over the shoulders, a hard crease at each shoulder and a buttoned throat tab.
    cape = shoulder_cape(g, "oilcloth_cape", "S", "smooth", 33202, length=4, width=16, depth=7, y=-.9)
    for face in cape.sides:
        gloss(face, "S", 2, 33203, crease=0)
        face.hline(0, face.w - 1, face.h - 1, "S0")
        face.hline(0, face.w - 1, face.h - 2, "S1")
    gloss(cape.top, "S", 3, 33204, crease=0)
    for face in cape.sides:                                              # the cape's stiff drape folds
        for x in range(2, face.w, 4):
            face.vline(x, 1, face.h - 3, "S1")
    for x in (4, 11):                                                    # stiff folds over the shoulder points
        cape.front.vline(x, 0, 2, "S3"), cape.back.vline(x, 0, 2, "S3")
    cape.front.vline(7, 0, 3, "S0"), cape.front.vline(8, 0, 3, "S1")     # the cape's front opening
    tab = blk(g, "cape_throat_tab", (0, -.6, -3.55), (2, 1, 1), "S", 1, "smooth", 33205, edge=False)
    tab.front.set(0, 0, "M3"), tab.front.set(1, 0, "M3")
    belt(g, "belt", 9.4, height=1)
    # Oyster knife: a short stout blade in a leather sheath, wooden grip up.
    sheath = blk(g, "oyster_knife_sheath", (-2.3, 9.4, -2.9), (1, 3, 1), "L", 1, "leather", 33206)
    sheath.front.set(0, 0, "L3")
    grip = blk(g, "oyster_knife_grip", (-2.3, 8.2, -2.9), (1, 1, 1), "L", 3, "plain", 33207, edge=False)
    grip.top.fill("M3")
    # The net bag of oysters: rough grey shells behind a diamond mesh of cord.
    bag = blk(g, "oyster_bag", BAG, (3, 3, 2), "M", 1, "plain", 33208, origin=(-1.5, .8, -1), motion="flap_front")
    for face in bag.faces:
        for y in range(face.h):
            for x in range(face.w):
                if (x + y) % 2 == 0:
                    face.set(x, y, "L3")                                 # the cord mesh
                else:
                    face.set(x, y, "M2" if (x * 3 + y) % 4 == 1 else "M1")
    cord = blk(g, "oyster_bag_cord", BAG, (1, 1, 1), "L", 2, "plain", 33209, origin=(-.5, -.2, -.5),
               motion="flap_front", edge=False)
    cord.front.set(0, 0, "L3")
    for face in flaps(g, "shirt_hem", 2, "P", "weave", 33210, top=11.0):
        face.hline(0, 8, 1, "P1")
