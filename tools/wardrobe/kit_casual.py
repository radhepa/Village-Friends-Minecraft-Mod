"""Supreme casual: plain everyday basics for the men's wardrobe (tees, tunics, polos, shirts,
chinos, slacks and jeans).

Everything paints key colors only. A plain tee has no color of its own: a module picks a role and
shade (primary, secondary, accent, ink, leather or denim) and the outfit's palette does the rest,
so one plain cut in five roles gives five differently colored shirts in every palette.
"""
from __future__ import annotations

from kit import SIDES, arm_bone, arm_x, belt, leg_bone, leg_ring
from paint import fabric, k, solid, strip_fabric


# -- tops ------------------------------------------------------------------------------------
def shirt_body(g, role: str, base: int = 2, texture: str = "plain", seed: int = 0, hem: bool = True):
    """The torso of a tee or shirt, softly rounded at the sides; `hem` adds an untucked lip."""
    body = g.part("body")
    strip_fabric(body, role, texture, seed, base)
    fabric(body.top, role, texture, seed, base + 1)
    fabric(body.bottom, role, texture, seed + 1, base - 1)
    for face in (body.right, body.left):
        face.vline(0 if face is body.right else face.w - 1, 1, 11, k(role, base - 1))
    if hem:
        jacket = g.part("jacket")
        for face in jacket.sides:
            fabric(face, role, texture, seed + 2, base, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, k(role, base - 1))
        jacket.bottom.fill(k(role, base - 1))
    return body


def crew_neck(body, role: str, base: int = 2, rib: str | None = None):
    """A round ribbed neckline; `rib` colors the band (a ringer's contrast trim)."""
    band = rib or k(role, base - 1)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, band), f.set(5, 0, band), f.set(3, 1, band), f.set(4, 1, band)
    body.back.hline(2, 5, 0, band)


def v_neck(body, role: str, base: int = 2, rib: str | None = None):
    band = rib or k(role, base - 1)
    f = body.front
    for x, y in ((2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (4, 2)):
        f.clear(x, y)
    for x, y in ((1, 0), (2, 1), (3, 2), (6, 0), (5, 1), (4, 3), (3, 3)):
        f.set(x, y, band)
    body.back.hline(2, 5, 0, band)


def placket(face, role: str, base: int = 2, y0: int = 1, y1: int = 11, x: int = 4, buttons=(3, 6, 9), button: str = "S4"):
    """A button stand down the front: a lit edge, a shaded seam and buttons."""
    for y in range(y0, y1 + 1):
        face.set(x, y, k(role, base + 1))
        face.set(x - 1, y, k(role, base - 1) if y % 2 else face.get(x - 1, y))
    for y in buttons:
        if y0 <= y <= y1:
            face.set(x, y, button)


def chest_pocket(face, role: str, base: int = 2, x0: int = 5, y0: int = 3, flap: bool = False, snap: str | None = None):
    """A small patch pocket: lit top edge, shaded sides and bottom."""
    face.hline(x0, x0 + 2, y0, k(role, base + 1))
    for y in (y0 + 1, y0 + 2):
        face.set(x0, y, k(role, base - 1)), face.set(x0 + 2, y, k(role, base - 1))
    face.hline(x0, x0 + 2, y0 + 3, k(role, base - 1))
    if flap:
        face.hline(x0, x0 + 2, y0 + 1, k(role, base))
        face.set(x0 + 1, y0 + 1, snap or k(role, base + 1))


def short_sleeves(g, role: str, base: int = 2, texture: str = "plain", seed: int = 0, length: int = 4,
                  band: str | None = None):
    """Short sleeves with a little volume: the overlay ends one row above the base so the hem lifts."""
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, role, texture, seed + (side == "left"), base, 0, length - 1)
        fabric(arm.top, role, texture, seed, base + 1)
        arm.strip.hline(0, arm.strip.w - 1, length - 1, k(role, base - 1))
        sleeve = g.part(f"{side}_sleeve")
        strip_fabric(sleeve, role, texture, seed + 3, base, 0, length - 2)
        fabric(sleeve.top, role, texture, seed, base + 1)
        sleeve.strip.hline(0, sleeve.strip.w - 1, length - 2, band or k(role, base - 1))


def long_sleeves(g, role: str, base: int = 2, texture: str = "plain", seed: int = 0, cuff: str | None = None, end: int = 10):
    """Full sleeves to the wrist (row `end`), with a cuff band; the hand stays bare."""
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, role, texture, seed + (side == "left"), base, 0, end)
        fabric(arm.top, role, texture, seed, base + 1)
        arm.strip.hline(0, arm.strip.w - 1, end, cuff or k(role, base - 1))
        arm.strip.hline(0, arm.strip.w - 1, end - 1, k(role, base))
        arm.front.vline(0, 1, end - 1, k(role, base - 1))   # a soft fold down the inner arm


def rolled_cuffs(g, role: str, base: int = 3, y: float = 4.2):
    """Sleeves pushed up to the forearm: a rolled ring around each arm."""
    for side in SIDES:
        ring = g.piece(f"{side}_sleeve_roll", arm_bone(side), (arm_x(side) - .45, y, -2.45), (5, 2, 5))
        solid(ring, role, "plain", 7 + (side == "left"), base)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 1))
            face.hline(0, face.w - 1, 1, k(role, base - 1))


def collar_points(g, role: str, base: int = 3, spread: float = 18, button: str | None = None, y: float = -.2):
    """Two turned-down collar points lying on the chest (polo, oxford and camp collars)."""
    for side, x in (("right", -2.2), ("left", 2.2)):
        tab = g.piece(f"{side}_collar_point", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(x, y, -2.15),
                      rotation=(0, 0, spread if side == "right" else -spread))
        solid(tab, role, "plain", 3, base, edge=False)
        tab.front.set(0 if side == "left" else 1, 1, k(role, base - 1))
        if button:
            tab.front.set(1 if side == "left" else 0, 1, button)


def plain_tee(g, role: str, base: int = 2, seed: int = 0, texture: str = "plain"):
    body = shirt_body(g, role, base, texture, seed)
    crew_neck(body, role, base)
    short_sleeves(g, role, base, texture, seed + 7)
    return body


def plain_tunic(g, role: str, base: int = 2, seed: int = 0, texture: str = "weave"):
    """A plain long-sleeved pullover tunic: slit neck, hem to the hip."""
    body = shirt_body(g, role, base, texture, seed)
    f = body.front
    f.clear(3, 0), f.clear(4, 0), f.clear(4, 1)
    f.set(2, 0, k(role, base - 1)), f.set(5, 0, k(role, base - 1)), f.set(3, 1, k(role, base - 1))
    f.vline(4, 2, 3, k(role, base - 1))
    body.back.hline(2, 5, 0, k(role, base - 1))
    long_sleeves(g, role, base, texture, seed + 7)
    for name, z, motion, face_name in (("front", -2.85, "flap_front", "front"), ("back", 1.85, "flap_back", "back")):
        panel = g.piece(f"hem_{name}", "TORSO", (-4.5, 0, 0), (9, 2, 1), pivot=(0, 11.4, z), motion=motion)
        solid(panel, role, texture, seed + 9 + (name == "back"), base, edge=False)
        getattr(panel, face_name).hline(0, 8, 1, k(role, base - 1))
    return body


# -- bottoms ---------------------------------------------------------------------------------
def trousers(g, role: str, base: int = 2, texture: str = "twill", seed: int = 0, end: int = 9, crease: bool = False,
             loops: bool = True, overlay: bool = False):
    """Plain long trousers to row `end`: waistband, belt loops, fly and soft inseam shading."""
    legs = []
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, texture, seed + (side == "left"), base, 0, end)
        fabric(leg.top, role, texture, seed, base)
        inner = leg.left if side == "right" else leg.right
        inner.vline(1, 0, end, k(role, base - 1))
        if crease:
            leg.front.vline(1 if side == "right" else 2, 1, end, k(role, base + 1))
            leg.back.vline(2 if side == "right" else 1, 2, end, k(role, base + 1))
        if overlay:   # roomy legs: the pants overlay stands off the leg
            pants = g.part(f"{side}_pants")
            strip_fabric(pants, role, texture, seed + 5 + (side == "left"), base, 0, end)
            inner_p = pants.left if side == "right" else pants.right
            inner_p.vline(1, 0, end, k(role, base - 1))
            pants.strip.hline(0, pants.strip.w - 1, end, k(role, base - 1))
        legs.append(leg)
    body = g.part("body")
    strip_fabric(body, role, texture, seed + 9, base, 9, 11)
    fabric(body.bottom, role, texture, seed + 10, base - 1)
    for face in body.sides:
        face.hline(0, face.w - 1, 9, k(role, base + 1))
    if loops:
        for x in (1, 6):
            body.front.vline(x, 9, 10, k(role, base - 1))
        for x in (1, 4, 6):
            body.back.vline(x, 9, 10, k(role, base - 1))
    body.front.vline(4, 10, 11, k(role, base - 1))   # fly
    return legs, body


def jeans(g, role: str = "D", base: int = 2, seed: int = 0, end: int = 9, stitch: str = "M3", fade: int = 0,
          overlay: bool = False):
    """Five-pocket jeans: curved front pockets, coin pocket, rivets, back pockets, contrast stitching.
    fade 1-2 lightens the thighs and knees for a worn wash."""
    legs, body = trousers(g, role, base, "twill", seed, end, overlay=overlay)
    f = body.front
    f.set(1, 11, stitch), f.set(6, 11, stitch)   # rivets at the pocket corners
    f.set(5, 10, k(role, base - 1)), f.set(6, 10, k(role, base - 1))   # coin pocket
    for side, leg in zip(SIDES, legs):
        front, back = leg.front, leg.back
        if side == "right":
            front.set(0, 1, stitch), front.set(1, 0, stitch)
        else:
            front.set(3, 1, stitch), front.set(2, 0, stitch)
        # Back patch pocket.
        bx = 1 if side == "right" else 0
        back.hline(bx, bx + 2, 0, stitch)
        for y in (1, 2):
            back.set(bx, y, k(role, base - 1)), back.set(bx + 2, y, k(role, base - 1))
        back.set(bx + 1, 3, k(role, base - 1))
        # Outer seam, then the hem.
        outer = leg.right if side == "right" else leg.left
        outer.vline(2, 1, end, k(role, base - 1))
        leg.strip.hline(0, leg.strip.w - 1, end, k(role, base - 1))
        if fade:   # worn wash: whiskered upper thigh and a pale patch over each knee
            lit, pale = k(role, base + 1), k(role, base + fade)
            cx = 1 if side == "right" else 2
            for y in range(1, 4):
                front.set(cx, y, lit)
            front.set(cx, 2, pale)
            for x, y in ((1, 5), (2, 5), (1, 6), (2, 6), (cx, 4), (cx, 7)):
                front.set(x, y, pale if (x, y) in ((1, 5), (2, 5), (1, 6), (2, 6)) else lit)
    return legs, body


def shoes(g, style: str = "leather", top: int = 10):
    """Plain everyday shoes: leather lace-ups, dark shoes, canvas pumps with a pale sole, or ankle boots."""
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        upper, sole = {"leather": ("L", "K1"), "dark": ("K", "K0"), "canvas": ("S", "S4"), "boot": ("L", "K1")}[style]
        base = 3 if style == "canvas" else 2
        start = top - 2 if style == "boot" else top
        strip_fabric(leg, upper, "smooth", 71, base - 1, start, 11)
        for face in pants.sides:
            fabric(face, upper, "smooth", 72, base, 0, start, face.w, 12 - start)
            face.hline(0, face.w - 1, start, k(upper, base + 1))
            face.hline(0, face.w - 1, 11, sole)
        for y in range(start, 11, 2):   # laces up the front
            pants.front.set(1, y, k(upper, base - 1)), pants.front.set(2, y, k(upper, base - 1))
        leg.bottom.fill(sole), pants.bottom.fill("K0" if style != "canvas" else "S2")


def rolled_hems(g, role: str, base: int = 3, y: float = 8.6, texture: str = "twill", inflate: float = .05):
    """Turned-up cuffs above the shoes."""
    rings = leg_ring(g, "hem_roll", y, role, base, size=(5, 2, 5), texture=texture, inflate=inflate)
    for ring in rings:
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 1))
            face.hline(0, face.w - 1, 1, k(role, base - 1))
    return rings


def stacked_hems(g, role: str, base: int = 2, texture: str = "twill"):
    """Baggy legs that pile up over the shoes: two loose rings standing off the shin."""
    for prefix, y, inflate in (("hem_stack_upper", 6.0, .3), ("hem_stack", 8.0, .45)):
        for ring in leg_ring(g, prefix, y, role, base, size=(4, 2, 4), texture=texture, inflate=inflate):
            for face in ring.sides:   # soft folds: a crease or two, no hard bands
                face.set(1, 1, k(role, base - 1)), face.set(2, 0, k(role, base - 1))


def leather_belt(g, role: str = "L", base: int = 2, buckle: str = "M"):
    """A plain belt through the loops; tops that cover the waist hide it."""
    return belt(g, "waist_belt", 9.4, role=role, base=base, height=1, buckle=buckle, inflate=.04)


def side_pocket(g, side: str, role: str, base: int = 2, y: float = 3.2, texture: str = "twill", flap: str | None = None):
    """A bellows cargo pocket on the outer thigh."""
    x = -2.55 if side == "right" else 1.55
    box = g.piece(f"{side}_cargo_pocket", leg_bone(side), (0, 0, -1.5), (1, 3, 3), pivot=(x, y, 0))
    solid(box, role, texture, 61 + (side == "left"), base)
    face = box.right if side == "right" else box.left
    face.hline(0, face.w - 1, 0, flap or k(role, base + 1))
    face.set(1, 0, "M3")
    return box
