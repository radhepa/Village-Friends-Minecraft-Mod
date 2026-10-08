"""Crossbowwoman's Windlass Jerkin: a buff jerkin with a leather yoke, a spanned crossbow slung on her back, a
windlass at her right hip and a case of bolts at her left."""
from kit import sleeves
from kit_female import girdle
from kit_f04 import Rod, front_prop
from paint import fabric, k, line, solid, strip_fabric

META = {
    "name": "Crossbowwoman's Windlass Jerkin",
    "gender": "female",
    "description": "A buff jerkin with a stitched leather yoke, a spanned crossbow slung across her back, a windlass "
                   "on the right hip and a case of bolts on the left.",
    "tags": ["martial", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "twill", 54001, 2)
    fabric(b.top, "P", "twill", 54001, 3), fabric(b.bottom, "P", "twill", 54001, 1)
    for x, y in [(3, 0), (4, 0), (4, 1)]:
        b.front.set(x, y, "S3")                                    # the shirt at the throat
    b.front.set(3, 1, "S2")
    b.front.vline(4, 2, 11, "P1")                                  # the jerkin's closing edge
    b.front.vline(5, 2, 11, "P3")
    for y in (3, 5, 7):
        b.front.set(3, y, "L3")                                    # horn toggles
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "P1")
    b.back.vline(3, 3, 11, "P1")
    # Shirt sleeves under short jerkin caps.
    sleeves(g, "S", "weave", 54002, base=3, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "twill", 54003, 2, 0, 2)
        fabric(arm.top, "P", "twill", 54003, 3)
        arm.strip.hline(0, 15, 2, "P1")
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4"), arm.strip.hline(0, 15, 11, "S3")
        arm.front.vline(2, 4, 8, "S2")
    # Leather yoke over the shoulders where the sling rides, and the sling itself.
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "L", "leather", 54004, 2, 0, 0, face.w, 2)
        face.hline(0, face.w - 1, 2, "L1")
    fabric(j.top, "L", "leather", 54004, 3)
    for x in (3, 4):
        j.front.clear(x, 0)
    j.front.set(3, 1, "L1"), j.front.set(4, 1, "L1")
    for x in range(0, 8, 2):
        j.front.set(x, 1, "L3"), j.back.set(x, 1, "L3")           # stitching along the yoke
    line(j.front, 0, 2, 6, 9, "L2"), line(j.front, 1, 2, 7, 9, "L1")
    line(j.back, 7, 2, 1, 9, "L2"), line(j.back, 6, 2, 0, 9, "L1")
    girdle(g, "belt", 8.2, role="L", height=2)
    # Windlass on the right hip: a cord drum between two cheeks, the crank folded down beside it.
    drum = front_prop(g, "windlass_drum", -2.9, (3, 3, 2), drop=1.0)
    solid(drum, "K", "smooth", 54005, 2, edge=False)
    for face in drum.sides:
        face.hline(0, face.w - 1, 0, "K3")
        face.hline(0, face.w - 1, 1, "S3"), face.hline(0, face.w - 1, 2, "S2")   # cord wound on the drum
    drum.front.set(1, 0, "M3")                                     # the hanging hook
    crank = front_prop(g, "windlass_crank", -.9, (2, 1, 1), drop=1.0, z=-2.85)
    solid(crank, "M", "smooth", 54006, 2, edge=False)
    crank.front.set(0, 0, "M3")
    handle = front_prop(g, "windlass_handle", -.4, (1, 3, 1), drop=1.0, z=-2.85)
    solid(handle, "L", "smooth", 54007, 3, edge=False)
    handle.front.set(0, 0, "M3"), handle.front.set(0, 2, "L2")
    # Bolt case on the left hip, three fletched bolts standing up out of it.
    case = front_prop(g, "bolt_case", 2.5, (3, 5, 2), drop=1.2)
    solid(case, "L", "leather", 54008, 2)
    for face in case.sides:
        face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 3, "M2")
    case.front.set(1, 1, "M3")
    for i, x in enumerate((1.7, 2.6, 3.4)):
        bolt = front_prop(g, f"bolt_{i}", x, (1, 2, 1), drop=-.8, z=-2.85)
        solid(bolt, "A" if i != 1 else "S", "plain", 54009 + i, 3, edge=False)
        bolt.strip.hline(0, bolt.strip.w - 1, 0, "A4" if i != 1 else "S4")
    # The crossbow slung across her back, butt up by the right shoulder blade, stirrup down by the left hip,
    # spanned so the string runs back to the nut in a V.
    rod = Rod(g, (-2.4, 1.4), (1.8, 11.6))
    stock = rod.piece("crossbow_stock", 0, (1, 10, 1))
    solid(stock, "L", "smooth", 54010, 2, edge=False)
    stock.back.vline(0, 0, 9, "L3")
    stock.back.set(0, 3, "M3"), stock.back.set(0, 4, "K1")        # the nut and trigger slot
    butt = rod.piece("crossbow_butt", 0, (2, 3, 1))
    solid(butt, "L", "smooth", 54011, 2, edge=False)
    butt.back.hline(0, 1, 0, "L3"), butt.back.set(1, 2, "L1")
    lever = rod.piece("crossbow_lever", 2, (1, 4, 1), dx=-1.0, dz=-.2)
    solid(lever, "M", "smooth", 54012, 2, edge=False)              # the long trigger bar under the stock
    prod = rod.piece("crossbow_prod", 8.4, (8, 1, 1))
    solid(prod, "M", "smooth", 54013, 2, edge=False)
    for f in (prod.back, prod.front):
        f.hline(1, 6, 0, "M3"), f.set(3, 0, "M4"), f.set(4, 0, "M4")
        f.set(0, 0, "M1"), f.set(7, 0, "M1")
    binding = rod.piece("crossbow_binding", 8.1, (2, 2, 1), dz=-.1, inflate=.1)
    solid(binding, "S", "plain", 54014, 3, edge=False)             # cord lashing the prod to the stock
    stirrup = rod.piece("crossbow_stirrup", 9.4, (2, 2, 1))
    solid(stirrup, "M", "smooth", 54015, 2, edge=False)
    for f in (stirrup.back, stirrup.front):
        f.set(0, 1, "M3"), f.set(1, 1, "M3"), f.set(0, 0, "M1"), f.set(1, 0, "M1")
    nut = rod.at(3.6)
    for side, dx in (("right", -3.6), ("left", 3.6)):
        tip = rod.at(8.6, dx)
        cord = Rod(g, nut, tip, z=rod.z - .4)
        piece = cord.piece(f"crossbow_string_{side}", 0, (1, int(round(cord.length)), 1))
        for f in piece.faces:
            f.fill("S4")
        piece.back.set(0, 0, "S3")
    # Sling strap from the butt over the shoulder is painted on the yoke; a leather loop holds the stock.
    loop = rod.piece("crossbow_sling_loop", 5.5, (2, 1, 2), dz=-.2, inflate=.05)
    solid(loop, "L", "leather", 54016, 1, edge=False)
    loop.back.set(0, 0, k("M", 3))
