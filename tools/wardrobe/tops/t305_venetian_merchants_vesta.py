"""Venetian Merchant's Vesta: an ankle-length vesta with full elbow sleeves, a stola over the left shoulder and a purse at the belt."""
from kit import SIDES, belt, body, pouch, sleeves
from kit_male import sleeve_shapes
from kit_m08 import coat_skirt, fringe, hanging_tail

META = {
    "name": "Venetian Merchant's Vesta",
    "gender": "male",
    "description": "A sober ankle-length vesta with full sleeves gathered at the elbow, a narrow stola thrown over the left shoulder to hang front and back, and a leather purse at the belt.",
    "tags": ["fancy", "robe", "tailored"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 38361)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.set(2, 0, "S3"), b.front.set(5, 0, "S3")                       # the shirt's collar edge
    b.front.vline(3, 1, 11, "P1")
    for y in (2, 5, 8):
        b.front.set(4, y, "K1")                                            # hidden hooks
    b.back.vline(4, 3, 11, "P1")
    sleeves(g, "P", "velvet", 38362, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S3")
    for s in sleeve_shapes(g, "comeo_sleeve", "P", 1.4, (5, 6, 6), "velvet", 38363, inflate=.1):
        for face in s.sides:
            face.hline(0, face.w - 1, 0, "P3")
            face.vline(1, 1, 4, "P1"), face.vline(face.w - 2, 2, 4, "P1")     # gathers
            face.hline(0, face.w - 1, 5, "P0")
        s.bottom.fill("P0")
    belt(g, "belt", 9.4, height=1)
    pouch(g, "scarsella", (-2.2, 9.8, -3.4), size=(2, 3, 1), role="L", flap="M3")
    coat_skirt(g, "vesta_skirt", 11, "P", "velvet", 38364, top=10.8)
    # The stola: an upper run from the shoulder and a lower run that follows the skirt.
    for name, pivot, size, motion in (("stola_front", (2.4, 0.0, -2.9), (2, 11, 1), "none"),
                                      ("stola_front_low", (2.4, 10.8, -3.4), (2, 6, 1), "flap_front"),
                                      ("stola_back", (2.4, 0.0, 2.9), (2, 11, 1), "none"),
                                      ("stola_back_low", (2.4, 10.8, 3.4), (2, 6, 1), "flap_back")):
        stola = hanging_tail(g, name, pivot, size, "A", "smooth", 38365, motion=motion)
        for face in (stola.right, stola.left):
            face.fill("A1")                                                # dark selvedges
        if name.endswith("low"):
            for face in (stola.front, stola.back):
                fringe(face, 5, "A3", "A1")
                face.hline(0, 1, 3, "A3")
