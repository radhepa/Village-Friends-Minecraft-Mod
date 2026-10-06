"""Trailblazer Vest: a laced linen shirt with rolled sleeves, a suede vest, satchel strap and kerchief."""
from paint import cap, fabric, grid, k, line, solid, strip_fabric

META = {
    "name": "Trailblazer Vest",
    "gender": "male",
    "description": "Rolled-sleeve linen shirt, pocketed suede vest, crossbody strap and a knotted kerchief.",
    "tags": ["rugged", "casual"],
    "tucked": True,
}


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "S", "weave", 61, 3)
    cap(body, "S", texture="weave", seed=61, base=3)
    f = body.front
    # Laced V-neck.
    for x, y in [(3, 0), (4, 0), (3, 1), (4, 1), (4, 2)]:
        f.clear(x, y)
    f.set(2, 0, "S2"), f.set(5, 0, "S2"), f.set(3, 2, "L2"), f.set(3, 3, "L1"), f.set(4, 3, "S1")
    f.set(2, 1, "S2"), f.set(5, 1, "S2")
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "S2")  # blouse over the waistband

    # Open suede vest on the jacket layer, ending above the belt.
    strip_fabric(jacket, "P", "twill", 62, 2, 0, 9)
    fabric(jacket.top, "P", "twill", 62, 3)
    jf, jb = jacket.front, jacket.back
    for y in range(10):
        for x in (3, 4):
            jf.clear(x, y)
    for y in range(9):
        jf.set(2, y, "P3"), jf.set(5, y, "P1")  # lapel edges catch light / shade
    jf.set(2, 0, None), jf.set(5, 0, None)
    jf.hline(0, 2, 9, "P1"), jf.hline(5, 7, 9, "P1")
    # Pockets with buttoned flaps.
    for x0 in (0, 5):
        jf.hline(x0, x0 + 2, 5, "P0")
        jf.hline(x0, x0 + 2, 4, "P3")
        jf.set(x0 + 1, 5, "M3")
    jf.set(1, 2, "M3")
    jb.vline(3, 0, 9, "P1")
    jb.hline(0, 7, 6, "L2"), jb.set(3, 6, "M3"), jb.set(4, 6, "M1")
    for face in (jacket.right, jacket.left):
        face.vline(1, 0, 9, "P1")

    # Satchel strap: over the wearer's left shoulder, down to the right hip.
    line(jf, 6, 0, 1, 9, "L2")
    line(jf, 7, 0, 2, 9, "L1")
    jf.set(4, 5, "M3")
    line(jb, 1, 0, 6, 9, "L2")
    line(jb, 0, 0, 5, 9, "L1")
    jacket.top.vline(6, 0, 3, "L2"), jacket.top.vline(7, 0, 3, "L1")

    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 63, 3, 0, 4)
        fabric(arm.top, "S", "weave", 63, 4)
        arm.strip.hline(0, arm.strip.w - 1, 5, "X1")
        if side == "left":
            arm.strip.hline(0, arm.strip.w - 1, 9, "L1")  # wrist cord
            arm.front.set(1, 9, "M3")
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        roll = g.piece(f"{side}_sleeve_roll", bone, (ox - .45, 2.0, -2.45), (5, 2, 5))
        solid(roll, "S", "weave", 64, 3)
        for face in roll.sides:
            face.hline(0, face.w - 1, 0, "S4")
            face.hline(0, face.w - 1, 1, "S2")

    # Knotted kerchief: a band around the neck and a short triangular drape.
    band = g.piece("kerchief_band", "TORSO", (-4.5, -.6, -2.6), (9, 1, 5), inflate=.04)
    solid(band, "A", "plain", 65, 2, edge=False)
    for name, w, y in (("kerchief_drape", 4, .4), ("kerchief_tip", 2, 1.4)):
        drape = g.piece(name, "TORSO", (-w / 2, y, -2.95), (w, 1, 1))
        solid(drape, "A", "plain", 66, 2, edge=False)
        drape.front.set(0, 0, "A3")
        drape.front.set(w - 1, 0, "A1")
    knot = g.piece("kerchief_knot", "TORSO", (2.3, -.9, -3.05), (2, 2, 1), rotation=(0, 0, 12))
    solid(knot, "A", "plain", 67, 2)
    knot.front.set(0, 0, "A3")
