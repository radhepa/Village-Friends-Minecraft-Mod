"""Outlaw's Hooded Greenwood Tunic: a greenwood tunic with its hood thrown back, a dagged hood-cape and dagged hem, a bracer and a belt knife."""
from kit import SIDES, belt, body, flaps, neckline, sleeves
from kit_male import arm_blk, blk, hood_down, lacing, shoulder_cape
from paint import k, solid

META = {
    "name": "Outlaw's Hooded Greenwood Tunic",
    "gender": "male",
    "description": "A weathered greenwood tunic with its russet hood thrown back, the hood's shoulder cape and the tunic's hem both cut into leaf-like dags, a laced leather bracer on the bow arm and a long knife at the belt.",
    "tags": ["rugged", "relaxed", "casual"],
    "covers_waist": True,
}


def dag(g, pid, pivot, length, base, seed, motion="none", origin=(-.5, 0, -.5), role="P"):
    """One hanging tongue of a dagged edge: a lit top, a darker point."""
    box = g.piece(pid, "TORSO", origin, (1, length, 1), pivot=pivot, motion=motion)
    solid(box, role, "plain", seed, base, edge=False)
    box.strip.hline(0, box.strip.w - 1, length - 1, k(role, base - 1))
    return box


def build(g):
    b = body(g, "P", "weave", 37280)
    neckline(b.front, "laced", "P")
    sleeves(g, "P", "weave", 37281, rows=(0, 10), cuff="P1")
    # A laced leather bracer on the left (bow) forearm.
    bracer = arm_blk(g, "left_bracer", "left", 5.4, (5, 3, 5), "L", 2, "leather", 37282)
    lacing(bracer.left, 1, 0, 2, "L4", "L1")
    for face in bracer.sides:
        face.hline(0, face.w - 1, 0, "L3")
    # The hood thrown back and its short cape over the shoulders, both edged with dags.
    cape = shoulder_cape(g, "hood_cape", "S", "weave", 37283, base=1, length=2, width=10, depth=6, y=-.6)
    for face in cape.sides:
        face.hline(0, face.w - 1, 1, "S0")
    hood = hood_down(g, "S", "weave", 37284, base=1, width=7, y=-.6, z=3.2, tilt=18, lining="S0")
    hood.back.set(3, 2, "S0")
    for i, x in enumerate((-3.5, -1.5, .5, 2.5)):
        dag(g, f"cape_dag_{i}", (x + .5, 1.3, -3.0), 2, 1, 37285 + i, role="S")
    belt(g, "belt", 9.5, height=1)
    # A long knife in a sheath slung at the right hip.
    sheath = blk(g, "knife_sheath", (-2.6, 9.6, -3.0), (1, 4, 1), "L", 1, "leather", 37293, rotation=(0, 0, 14),
                 motion="flap_front")
    sheath.strip.hline(0, 3, 3, "M2")
    grip = blk(g, "knife_grip", (-2.6, 9.6, -3.0), (1, 2, 1), "L", 3, "plain", 37294, rotation=(0, 0, 14),
               origin=(-.5, -2, -.5), motion="flap_front", edge=False)
    grip.strip.hline(0, 3, 1, "M3")
    # The tunic hem and its row of dags, swinging with the stride.
    for face in flaps(g, "tunic_hem", 3, "P", "weave", 37295, top=10.6):
        face.hline(0, 8, 2, k("P", 1))
    for i, x in enumerate((-3.5, -1.5, .5, 2.5)):
        dag(g, f"hem_dag_front_{i}", (0, 10.6, -2.85), 2, 2, 37296 + i, "flap_front", (x, 3, 0))
        dag(g, f"hem_dag_back_{i}", (0, 10.6, 1.85), 2, 2, 37300 + i, "flap_back", (x, 3, 0))
