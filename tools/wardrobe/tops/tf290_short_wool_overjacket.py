"""Short Wool Overjacket: a hip-length wool jacket hooked only at the throat, worn open over a plain kirtle, with turned-back cuffs."""
from kit import body
from kit_female import cuffs, neck, over_panel
from paint import fabric, strip_fabric

META = {
    "name": "Short Wool Overjacket",
    "gender": "female",
    "description": "A boxy hip-length wool jacket hooked only at the throat and worn open over a plain kirtle, with slit pockets and turned-back cuffs.",
    "tags": ["casual", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 60160, base=3)
    neck(b.front, "round", "S", 3)
    b.front.hline(2, 5, 11, "S2")
    j = g.part("jacket")
    strip_fabric(j, "P", "weave", 60161, 2)
    fabric(j.top, "P", "weave", 60162, 3)
    f = j.front
    for y in range(12):
        f.clear(3, y), f.clear(4, y)                                  # worn open down the front
        f.set(2, y, "P3"), f.set(5, y, "P3")                          # the turned facing along each edge
    f.set(1, 0, "P3"), f.set(6, 0, "P3")
    f.set(3, 1, "L2"), f.set(4, 1, "M3")                              # the one hook at the throat
    for x in (1, 6):
        f.vline(x, 4, 11, "P1")
    f.hline(0, 1, 9, "P0"), f.hline(6, 7, 9, "P0")                    # slit pockets
    j.back.vline(3, 1, 11, "P1"), j.back.vline(4, 1, 11, "P3")
    j.back.vline(1, 5, 11, "P1"), j.back.vline(6, 5, 11, "P1")
    for face in (j.right, j.left):
        face.vline(2, 1, 11, "P1")
    # The jacket's short skirts flare over the hips, open at the front.
    for name, x, w in (("hem_front_right", -3.25, 4), ("hem_front_left", 3.25, 4)):
        face = over_panel(g, name, 3, "P", "weave", 60163, 2, width=w, top=9.0, x=x)
        face.hline(0, w - 1, 2, "P1")
        face.vline(0 if x > 0 else w - 1, 0, 2, "P3")
    back = over_panel(g, "hem_back", 3, "P", "weave", 60164, 2, width=10, top=9.0, back=True)
    back.vline(4, 0, 2, "P1"), back.vline(5, 0, 2, "P3")
    back.hline(0, 9, 2, "P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "weave", 60165 + (side == "left"), 2, 0, 11)
        fabric(arm.top, "P", "weave", 60167, 3)
        outer = arm.right if side == "right" else arm.left
        outer.vline(2, 1, 7, "P1")
        arm.strip.hline(0, 15, 11, "S3")
    for cuff in cuffs(g, "S", 6.8, 2, 5, prefix="turned_cuff", texture="weave", base=3):
        for face in cuff.sides:
            face.hline(0, face.w - 1, 1, "S2")
