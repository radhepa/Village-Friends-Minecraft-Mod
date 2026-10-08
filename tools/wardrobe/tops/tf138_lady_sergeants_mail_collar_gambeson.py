"""Lady Sergeant's Mail-Collar Gambeson: a row-quilted gambeson buttoned off-centre, a ring-mail cape over the
shoulders, a sergeant's sash and a flanged mace hung at the right hip."""
from kit import sleeves
from kit_female import girdle, mail, mantle, over_flaps
from kit_f04 import front_prop, quilt_rows
from paint import fabric, line, solid, strip_fabric

META = {
    "name": "Lady Sergeant's Mail-Collar Gambeson",
    "gender": "female",
    "description": "A row-quilted gambeson buttoned off-centre, a ring-mail cape over the shoulders, a sergeant's "
                   "sash and a flanged mace hung at the hip.",
    "tags": ["martial", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "plain", 54081, 2)
    fabric(b.top, "P", "plain", 54081, 3), fabric(b.bottom, "P", "plain", 54081, 1)
    for face in b.sides:
        quilt_rows(face, "P", 2, 2, y0=2)
    b.front.vline(5, 1, 11, "P0"), b.front.vline(6, 1, 11, "P3")     # the off-centre closing edge
    for y in (3, 5, 7, 9):
        b.front.set(6, y, "M3")                                       # buttons
    sleeves(g, "P", "plain", 54082, base=2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        quilt_rows(arm.strip, "P", 2, 2, y0=3, y1=9)
        arm.strip.hline(0, 15, 10, "L2"), arm.strip.hline(0, 15, 11, "L1")
    # The sergeant's sash, from the left shoulder to the right hip, under the mail.
    j = g.part("jacket")
    for dx, key in ((0, "A3"), (1, "A2")):
        line(j.front, 7 - dx, 0, 0, 7 - dx, key)
    line(j.back, 0, 0, 7, 7, "A2"), line(j.back, 1, 0, 7, 6, "A3")
    cape = mantle(g, "mail_cape", "M", "smooth", 54083, 2, height=3, width=17, depth=6, y=-1.0)
    for face in cape.sides:
        mail(face, "M", 2)
        face.hline(0, face.w - 1, face.h - 1, "L2")                  # the leather edge the rings are laced to
    fabric(cape.top, "M", "smooth", 54084, 3)
    cape.front.hline(7, 9, 0, "L3")                                   # the throat strap
    cape.front.set(8, 1, "M4")
    girdle(g, "belt", 8.2, role="L", height=1)
    f, bk = over_flaps(g, "gambeson_skirt", 4, "P", "plain", 54085, width=10, top=9.0)
    for face in (f, bk):
        quilt_rows(face, "P", 2, 2, y0=1)
        face.hline(0, face.w - 1, 3, "P0")
    f.vline(7, 0, 3, "P0")
    # A flanged mace hung head-down from a ring at the right hip, in front of the gambeson skirt.
    haft = front_prop(g, "mace_haft", -3.3, (1, 5, 1), drop=.2, z=-3.25)
    solid(haft, "L", "smooth", 54086, 2, edge=False)
    haft.front.vline(0, 0, 4, "L3"), haft.front.set(0, 0, "M3")
    head = front_prop(g, "mace_head", -3.3, (2, 3, 2), drop=5.0, z=-2.95)
    solid(head, "M", "smooth", 54087, 2)
    for face in head.sides:
        face.vline(0, 0, 2, "M4"), face.vline(1, 0, 2, "M1")          # flanges
    head.bottom.fill("M3")
