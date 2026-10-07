"""Leatherworker's Awl Apron: a laced bodice under a short pocketed tool apron bristling with awls and a thread spool."""
from kit_female import bodice, chemise, lacing, over_panel
from paint import solid

META = {
    "name": "Leatherworker's Awl Apron",
    "gender": "female",
    "description": "A laced bodice under a short leather tool apron whose pockets bristle with awls, punches and a thread spool.",
    "tags": ["work", "apron"],
    "covers_waist": True,
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 14401, neckline="square", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "L2"), arm.strip.hline(0, 15, 10, "S2")
    b = bodice(g, "P", "twill", 14402, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "tight", lace="L3", under="P0", eyelet="M3")
    face = over_panel(g, "tool_apron", 6, "L", "leather", 14403, width=9, top=9.0)
    face.hline(0, 8, 2, "L1"), face.vline(3, 2, 5, "L1"), face.vline(6, 2, 5, "L1")
    face.hline(0, 8, 5, "L1")
    for i, (x, key, h) in enumerate(((-2.6, "M", 3), (-2.0, "L", 2), (.6, "M", 3), (1.4, "M", 2))):
        tool = g.piece(f"tool_{i}", "TORSO", (-.5, 2 - h, -.4), (1, h, 1), pivot=(x, 9.0, -3.25), motion="flap_front")
        solid(tool, key, "smooth", 14404 + i, 3, edge=False)
        tool.top.fill("L3" if key == "M" else "M3")
    spool = g.piece("thread_spool", "TORSO", (-1, 1, -.6), (2, 2, 1), pivot=(3.2, 9.0, -3.25), motion="flap_front",
                    inflate=.06)
    solid(spool, "S", "plain", 14408, 3)
    spool.front.hline(0, 1, 0, "L3"), spool.front.hline(0, 1, 1, "A2")
