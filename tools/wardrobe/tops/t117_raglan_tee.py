"""Raglan Tee: a pale body with contrast three-quarter raglan sleeves."""
from kit_casual import crew_neck, shirt_body
from paint import fabric, strip_fabric

META = {
    "name": "Raglan Tee",
    "gender": "male",
    "description": "A pale tee with contrast three-quarter raglan sleeves running up to the collar.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "S", 3, "plain", 11701)
    crew_neck(body, "S", 3, rib="P2")
    # Raglan seams run from the collar down to the underarm.
    for face in (body.front, body.back):
        for x, y in ((0, 0), (1, 0), (0, 1), (6, 0), (7, 0), (7, 1)):
            face.set(x, y, "P2")
    for face in (body.right, body.left):
        face.hline(0, 3, 0, "P2"), face.hline(0, 3, 1, "P2")
    fabric(body.top, "P", "plain", 11703, 3, 0, 0, 2, 4), fabric(body.top, "P", "plain", 11703, 3, 6, 0, 2, 4)
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "plain", 11702, 2, 0, 7)
        fabric(arm.top, "P", "plain", 11702, 3)
        arm.strip.hline(0, 15, 7, "P1")
        sleeve = g.part(f"{side}_sleeve")
        strip_fabric(sleeve, "P", "plain", 11704, 2, 0, 6)
        sleeve.strip.hline(0, 15, 6, "P1")
        fabric(sleeve.top, "P", "plain", 11704, 3)
