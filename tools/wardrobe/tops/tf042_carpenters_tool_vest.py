"""Carpenter's Tool Vest: a canvas vest with a folding rule in the pocket and a hammer in its loop, over a buttoned shirt."""
from kit import sleeves
from kit_female import chemise, girdle, hanging, neck
from paint import fabric, solid, strip_fabric

META = {
    "name": "Carpenter's Tool Vest",
    "gender": "female",
    "description": "A canvas work vest with a folding rule and pencil in the pocket and a hammer hung in its loop.",
    "tags": ["work", "casual"],
}


def build(g):
    chemise(g, "S", 3, "weave", 14201, neckline="slit", sleeve_rows=(0, 11), gather=False)
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S2"), arm.front.set(2, 10, "M3")
    j = g.part("jacket")
    strip_fabric(j, "P", "twill", 14202, 2, 0, 10)
    fabric(j.top, "P", "twill", 14202, 3)
    neck(j.front, "deep_v", "P", 2)
    j.front.vline(3, 4, 10, "P1")
    for y in (5, 7, 9):
        j.front.set(4, y, "L3")
    j.front.hline(5, 7, 3, "P1"), j.front.vline(5, 3, 6, "P1")       # chest pocket
    j.front.hline(0, 2, 7, "P1"), j.front.vline(2, 7, 10, "P1")     # hip pocket
    for face in j.sides:
        face.hline(0, face.w - 1, 10, "P1")
    rule = g.piece("folding_rule", "TORSO", (-.5, -2, -.5), (1, 3, 1), pivot=(-1.9, 4.6, -2.65), rotation=(0, 0, 8))
    solid(rule, "S", "smooth", 14203, 4)
    rule.front.set(0, 0, "K2"), rule.front.set(0, 2, "K2")
    pencil = g.piece("pencil", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(-2.7, 4.4, -2.65), rotation=(0, 0, -10))
    solid(pencil, "L", "smooth", 14204, 3)
    pencil.top.fill("K1")
    girdle(g, "belt", 8.0, role="L", height=1)
    hanging(g, "hammer_loop", 3.2, 2, role="L", top=9.0)
    handle = g.piece("hammer_handle", "TORSO", (-.5, 2, -.1), (1, 4, 1), pivot=(3.2, 9.0, -3.25), motion="flap_front")
    solid(handle, "L", "smooth", 14205, 3)
    head = g.piece("hammer_head", "TORSO", (-1.5, 6, -.3), (3, 1, 1), pivot=(3.2, 9.0, -3.25), motion="flap_front",
                   inflate=.05)
    solid(head, "M", "smooth", 14206, 2, edge=False)
