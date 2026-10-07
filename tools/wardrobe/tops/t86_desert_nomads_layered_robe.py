"""Desert Nomad's Layered Robe: a pale under-robe beneath an open outer robe, a long scarf over the shoulders and a curved dagger."""
from kit import body, neckline, sleeves
from kit_male import blk, sash
from paint import fabric, solid

META = {
    "name": "Desert Nomad's Layered Robe",
    "gender": "male",
    "description": "A pale under-robe beneath an open, accent-edged outer robe, a long scarf wound over the shoulders and a curved dagger in the sash.",
    "tags": ["robe", "relaxed"],
    "locked_to": "b86_nomads_sirwal",
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 8601, base=3)
    neckline(b.front, "round", "S", base=3)
    outer = body(g, "P", "weave", 8602, layer="jacket")
    for y in range(12):
        outer.front.clear(3, y), outer.front.clear(4, y)
        outer.front.set(2, y, "A2"), outer.front.set(5, y, "A2")
    sleeves(g, "P", "weave", 8603, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        fabric(arm.strip, "S", "weave", 8604, 3, 0, 9, arm.strip.w, 2)       # under-robe at the wrist
        arm.strip.hline(0, arm.strip.w - 1, 8, "A2")
    scarf = g.piece("shoulder_scarf", "TORSO", (-5, -.9, -2.9), (10, 2, 6), inflate=.06)
    solid(scarf, "S", "weave", 8605, 4)
    for face in scarf.sides:
        face.hline(0, face.w - 1, 1, "A2")
    tail = blk(g, "scarf_tail", (-2.6, 1.0, -3.0), (2, 7, 1), "S", 4, "weave", 8606)
    tail.front.hline(0, 1, 5, "A2"), tail.front.hline(0, 1, 6, "S2")
    sash(g, "waist_sash", "A", y=8.8, height=2, seed=8607, tails=((-1.0, 0),), tail_len=4)
    hilt = blk(g, "dagger_hilt", (1.4, 8.0, -3.0), (1, 2, 1), "M", 3, "smooth", 8609)
    hilt.strip.hline(0, hilt.strip.w - 1, 0, "M4")
    sheath = blk(g, "dagger_sheath", (1.4, 10.0, -3.0), (1, 2, 1), "M", 2, "smooth", 8610)
    blk(g, "dagger_curl", (2.0, 11.6, -3.0), (2, 1, 1), "M", 2, "smooth", 8611, edge=False)
    for name, z, motion, face_name in (("robe_front", -2.85, "flap_front", "front"),
                                        ("robe_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 9, 1), pivot=(0, 11.0, z), motion=motion)
        solid(panel, "P", "weave", 8612, 2)
        face = getattr(panel, face_name)
        if face_name == "front":
            fabric(face, "S", "weave", 8613, 3, 3, 0, 3, 9)
            face.vline(2, 0, 8, "A2"), face.vline(6, 0, 8, "A2")
        face.hline(0, 8, 8, "P1")
