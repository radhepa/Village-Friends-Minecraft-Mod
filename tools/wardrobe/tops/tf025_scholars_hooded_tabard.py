"""Scholar's Hooded Tabard: a sleeveless academic tabard with a shoulder cape and liripipe hood over a fitted kirtle."""
from kit import body, sleeves
from kit_female import buttons, girdle, hood_down, mantle, neck, over_flaps
from paint import fabric, strip_fabric

META = {
    "name": "Scholar's Hooded Tabard",
    "gender": "female",
    "description": "An open-sided academic tabard with a shoulder cape and a liripipe hood, over a buttoned kirtle.",
    "tags": ["scholarly", "robe"],
}


def build(g):
    b = body(g, "S", "weave", 12501, base=2)
    neck(b.front, "round", "S", 2)
    sleeves(g, "S", "weave", 12502, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for y in (6, 8, 10):
            arm.front.set(2, y, "M3")                                # buttoned forearms
    j = g.part("jacket")
    for face in (j.front, j.back):
        fabric(face, "P", "weave", 12503, 2, 1, 0, 6, 12)
        face.vline(1, 0, 11, "P1"), face.vline(6, 0, 11, "P1")
    fabric(j.top, "P", "weave", 12503, 3, 1, 0, 6, 4)
    buttons(j.front, 4, 4, 11, "P0", step=2, placket=None)
    cape = mantle(g, "shoulder_cape", "P", "weave", 12504, 2, height=3, width=11, depth=6, y=-.8)
    for face in cape.sides:
        face.hline(0, face.w - 1, 2, "A2")
    hood_down(g, "hood", "P", "weave", 12505, 2, lining="A2", point=7)
    girdle(g, "girdle", 8.0, role="L", base=1, height=1)
    f, bk = over_flaps(g, "tabard", 12, "P", "weave", 12506, width=6, top=9.0)
    for face in (f, bk):
        face.vline(0, 0, 11, "P1"), face.vline(5, 0, 11, "P1")
        face.hline(0, 5, 11, "A2")
