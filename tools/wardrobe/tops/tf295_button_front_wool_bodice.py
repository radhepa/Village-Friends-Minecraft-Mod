"""Button-Front Wool Bodice: a neat fitted wool bodice buttoned throat to hip, a narrow standing collar and button-cuffed sleeves."""
from kit import SIDES, body
from kit_female import buttons, hanging
from paint import fabric, solid, strip_fabric

META = {
    "name": "Button-Front Wool Bodice",
    "gender": "female",
    "description": "A neat fitted wool bodice with princess seams, buttoned from a narrow standing collar to the hip, button-cuffed sleeves and a needle case on a ribbon.",
    "tags": ["casual", "tailored", "simple"],
}


def build(g):
    b = body(g, "P", "weave", 60360)
    f = b.front
    f.vline(4, 0, 11, "P1")                                            # the buttoned overlap
    buttons(f, 3, 1, 11, "M3", step=2)
    for y in range(2, 12, 2):
        f.set(3, y, "P3")
    for face in (f, b.back):
        face.vline(1, 2, 11, "P1"), face.vline(6, 2, 11, "P1")          # princess seams
        face.vline(2, 3, 11, "P3")
    b.back.vline(3, 0, 11, "P1"), b.back.vline(4, 0, 11, "P3")
    for face in (b.right, b.left):
        face.vline(1, 0, 11, "P1")
    collar = g.piece("standing_collar", "TORSO", (-4.5, -1.0, -2.6), (9, 1, 5), inflate=.08)
    solid(collar, "P", "weave", 60361, 3, edge=False)
    collar.front.set(4, 0, "M3")
    collar.top.fill("P2")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60362 + (side == "left"), 2, 0, 11)
        fabric(arm.top, "P", "weave", 60364, 3)
        outer = arm.right if side == "right" else arm.left
        outer.vline(2, 1, 11, "P1")
        for y in (7, 9, 11):
            outer.set(1, y, "M3")                                      # the buttoned wrist opening
        arm.strip.hline(0, 15, 11, "P1")
        outer.set(1, 11, "M3")
    # A little needle case on a ribbon at the left hip.
    hanging(g, "needle_ribbon", 3.3, 2, role="A", base=2, top=8.6)
    case = g.piece("needle_case", "TORSO", (-.5, 2, -.1), (1, 3, 1), pivot=(3.3, 8.6, -3.25), motion="flap_front")
    solid(case, "L", "smooth", 60365, 2, edge=False)
    case.strip.hline(0, 3, 0, "M3"), case.strip.hline(0, 3, 2, "M2")
    case.bottom.fill("M2")
