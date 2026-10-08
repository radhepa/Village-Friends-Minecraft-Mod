"""Net Mender's Cork-Hemmed Skirt: a calf-length wool skirt bordered in netting, with a cord of cork
floats strung along the hem, over laced ankle boots."""
from kit_f03 import net
from kit_female import SKIRT_BACK, SKIRT_FRONT, shoes, skirt
from paint import solid

META = {
    "name": "Net Mender's Cork-Hemmed Skirt",
    "gender": "female",
    "description": "A calf-length wool skirt with a netted border and a cord of cork floats strung along its hem, over laced ankle boots.",
    "tags": ["sea", "work", "skirt"],
}

TOP, LENGTH = 9.8, 10


def build(g):
    s = skirt(g, "P", "weave", 53011, top=TOP, length=LENGTH, flare=6)
    for face in s.faces:
        net(face, "S2", "P1", 4, 0, face.h - 5, face.w, 4, knot="S3", phase=2)
        face.hline(0, face.w - 1, face.h - 6, "S3")
        face.hline(0, face.w - 1, face.h - 1, "L1")                      # the float cord along the hem
    for box in (s.right, s.left):
        for face in (box.front, box.back):
            net(face, "S2", "P1", 4, 0, face.h - 5, face.w, 4, phase=2)
            face.set(0, face.h - 1, "L1")
    # Cork floats strung on the hem cord, riding the stride with their panels.
    for name, z, motion, dz in (("front", SKIRT_FRONT, "flap_front", -.55), ("back", SKIRT_BACK, "flap_back", .55)):
        for i, x in enumerate((-3.5, -0.5, 2.5)):
            cork = g.piece(f"cork_{name}_{i}", "TORSO", (x, LENGTH - 1.6, dz), (1, 1, 1), pivot=(0, TOP, z), motion=motion,
                           inflate=.18)
            solid(cork, "L", "smooth", 53012 + i, 3, edge=False)
            cork.front.set(0, 0, "L4"), cork.back.set(0, 0, "L4")
    shoes(g, "ankle", "L", 2, top=9, accent="S4")
