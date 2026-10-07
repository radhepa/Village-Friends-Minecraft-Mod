"""Fisher's Oilskin Smock: a stiff oiled smock shining wet, toggled at the throat, its deep hood thrown back, cuffs strapped tight."""
from kit import body, sleeves
from kit_male import hood_down, toggles
from paint import rnd

META = {
    "name": "Fisher's Oilskin Smock",
    "gender": "male",
    "description": "A stiff oiled smock shining with wet, toggled at the throat, its deep hood thrown back and the cuffs strapped tight.",
    "tags": ["sea", "work"],
    "locked_to": "b85_fishers_oilskin_waders",
    "covers_waist": True,
}


def sheen(face, seed=0, rows=None):
    """Oilskin: smooth stiff cloth, a few bright glints of wet and one stiff crease."""
    for y in range(face.h) if rows is None else rows:
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, 8500 + seed)
            face.set(x, y, "P4" if r < .05 else "P3" if r < .12 else "P2")
        if y % 6 == 4:
            face.hline(0, face.w - 1, y, "P1")


def build(g):
    b = body(g, "P", "smooth", 8501)
    for face in b.sides:
        sheen(face)
    b.front.hline(3, 4, 0, None)
    toggles(b.front, 3, (1, 3), "L4", "L1")
    sleeves(g, "P", "smooth", 8502, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        sheen(arm.strip, 2)
        arm.strip.hline(0, arm.strip.w - 1, 9, "L2")                      # cuff straps
        arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
    hood = hood_down(g, "P", "smooth", 8503, width=8, y=-1.0, z=3.0, tilt=12, lining="P0")
    for face in hood.sides:
        sheen(face, 1)
    for name, z, motion, face_name in (("smock_front", -2.85, "flap_front", "front"),
                                        ("smock_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 4, 1), pivot=(0, 11.2, z), motion=motion)
        for face in panel.faces:
            sheen(face, 3)
        getattr(panel, face_name).hline(0, 8, 3, "P0")
