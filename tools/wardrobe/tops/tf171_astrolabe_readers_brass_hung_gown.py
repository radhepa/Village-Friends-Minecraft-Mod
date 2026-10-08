"""Astrolabe Reader's Brass-Hung Gown: an open-fronted night-blue gown edged in a narrow guard, a brass
astrolabe hung on a chain on the breast, brass dividers at the hip and a leather star-chart case slung
across the back."""
from kit import body, sleeves
from kit_female import OVER_FRONT, girdle, neck, over_panel
from kit_f05 import fixed
from paint import grid, line, solid

META = {
    "name": "Astrolabe Reader's Brass-Hung Gown",
    "gender": "female",
    "description": "An open-fronted gown with a brass astrolabe on a chain at the breast, brass dividers at the hip and a chart case on the back.",
    "tags": ["scholarly", "fancy", "robe"],
    "covers_waist": True,
}

# The astrolabe's face: a rim round a dark plate, the alidade bright across it. g shows the gown behind.
ASTROLABE = ["grrrg", "rddbr", "rdbdr", "rbddr", "grrrg"]


def build(g):
    b = body(g, "P", "velvet", 55301, base=1)
    neck(b.front, "v", "P", 1, edge="A2")
    for face in (b.front, b.back):
        face.vline(1, 3, 11, "P0"), face.vline(6, 3, 11, "P0")
    for arm in sleeves(g, "P", "velvet", 55302, base=1, rows=(0, 11)):
        arm.strip.hline(0, 15, 11, "A2"), arm.strip.hline(0, 15, 10, "P0")
        arm.strip.vline(2, 2, 9, "P2")
    # The chain from the neck to the astrolabe.
    j = g.part("jacket")
    line(j.front, 1, 0, 3, 2, "M3"), line(j.front, 6, 0, 4, 2, "M3")
    disc = fixed(g, "astrolabe", (0, 5.0, -2.6), (5, 5, 1), "M", 3, "smooth", 55303, edge=False)
    grid(disc.front, 0, 0, ASTROLABE, {"g": "P1", "r": "M3", "d": "M1", "b": "M4"})
    grid(disc.back, 0, 0, ASTROLABE, {"g": "P1", "r": "M3", "d": "M2", "b": "M2"})
    shackle = fixed(g, "astrolabe_shackle", (0, 2.1, -2.6), (1, 1, 1), "M", 4, "smooth", 55304, edge=False)
    shackle.front.fill("M3")
    girdle(g, "girdle", 8.2, role="L", base=1, height=1, buckle="M")
    # The gown hangs open: two narrow front panels edged in the guard, and a full back.
    for side, x in (("right", -3.5), ("left", 3.5)):
        f = over_panel(g, f"gown_front_{side}", 12, "P", "velvet", 55305, base=1, width=3, top=9.0, x=x)
        f.vline(2 if side == "right" else 0, 0, 11, "A2")
        f.hline(0, 2, 11, "A2")
    back = over_panel(g, "gown_back", 12, "P", "velvet", 55306, base=1, width=10, top=9.0, back=True)
    for x in (2, 5, 8):
        back.vline(x, 1, 10, "P0")
    back.hline(0, 9, 11, "A2")
    # Brass dividers hanging open from the girdle at the right hip.
    for name, rot in (("dividers_leg_a", 9), ("dividers_leg_b", -9)):
        leg = g.piece(name, "TORSO", (-.5, .8, -.2), (1, 4, 1), pivot=(-2.6, 9.0, OVER_FRONT - .1), rotation=(0, 0, rot),
                      motion="flap_front")
        solid(leg, "M", "smooth", 55307, 3, edge=False)
        for face in leg.sides:
            face.set(0, 3, "M1")
    head = g.piece("dividers_head", "TORSO", (-.5, 0, -.3), (1, 1, 1), pivot=(-2.6, 9.0, OVER_FRONT - .1),
                   motion="flap_front")
    solid(head, "M", "smooth", 55308, 4, edge=False)
    # The star-chart case slung across the back, capped in brass.
    case = g.piece("chart_case", "TORSO", (-1, -4.5, 0), (2, 9, 2), pivot=(0, 5.0, 2.35), rotation=(0, 0, 28))
    solid(case, "L", "leather", 55309, 2)
    for face in case.sides:
        face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 8, "M2")
        face.hline(0, face.w - 1, 4, "L1")
    case.top.fill("M4"), case.bottom.fill("M1")
