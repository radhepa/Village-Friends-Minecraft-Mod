"""Almoner's Alms-Purse Robe: a knee-length bordered robe, an embroidered alms purse with tassels hanging from the girdle, and a basket of loaves carried on the arm."""
from kit import belt, body, flaps, side_panels, sleeves
from kit_male import arm_blk, embroider
from paint import solid

META = {
    "name": "Almoner's Alms-Purse Robe",
    "gender": "male",
    "description": "The house almoner's knee-length robe with a bordered hem, a big embroidered alms purse swinging from his girdle on tasselled cords, and a wicker basket of round loaves carried on his arm for the poor at the gate.",
    "tags": ["holy", "robe", "simple"],
    "covers_waist": True,
}


def wicker(face, rim_key="L4"):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, "L3" if (x + y) % 2 == 0 else "L1")
    face.hline(0, face.w - 1, 0, rim_key)


def build(g):
    b = body(g, "P", "weave", 35240)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "S3"), f.set(5, 0, "S3"), f.set(3, 1, "S3"), f.set(4, 1, "S2")   # linen shirt at the throat
    f.vline(4, 2, 8, "P1")
    for face in (b.right, b.left):
        face.vline(1 if face is b.right else 2, 3, 11, "P1")
    sleeves(g, "P", "weave", 35241, rows=(0, 10))
    for side in ("right", "left"):
        cuff = arm_blk(g, f"{side}_turned_cuff", side, 7.6, (5, 2, 5), "A", 2, "weave", 35242, inflate=.06)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "A3")
    belt(g, "girdle", 9.4, height=1)
    # The alms purse: an embroidered bag under a brass frame, two tasselled cords below.
    frame = g.piece("purse_frame", "TORSO", (-1.5, 0, -.5), (3, 1, 1), pivot=(-1.4, 10.4, -3.0), motion="flap_front")
    solid(frame, "M", "smooth", 35243, 3, edge=False)
    frame.front.set(1, 0, "M4")
    purse = g.piece("alms_purse", "TORSO", (-1.5, 1, -.5), (3, 3, 1), pivot=(-1.4, 10.4, -3.0), motion="flap_front")
    solid(purse, "A", "plain", 35244, 2)
    pf = purse.front
    pf.set(1, 0, "M3"), pf.set(0, 1, "A3"), pf.set(2, 1, "A3"), pf.set(1, 1, "S4"), pf.set(1, 2, "A3")
    pf.set(0, 2, "A1"), pf.set(2, 2, "A1")
    for i, ox in enumerate((-1.5, .5)):
        tassel = g.piece(f"purse_tassel_{i}", "TORSO", (ox, 4, -.5), (1, 2, 1), pivot=(-1.4, 10.4, -3.0), motion="flap_front")
        solid(tassel, "A", "plain", 35245 + i, 3, edge=False)
        tassel.strip.hline(0, tassel.strip.w - 1, 1, "M3"), tassel.bottom.fill("M2")
    # A basket of loaves carried on the left forearm.
    basket = g.piece("bread_basket", "LEFT_ARM", (-2, 0, -1.5), (4, 2, 3), pivot=(1.0, 7.4, -3.6))
    for face in basket.sides:
        wicker(face)
    basket.top.fill("L2"), basket.bottom.fill("L0")
    for i, (dx, dz) in enumerate(((-.9, -.1), (.9, .2))):
        loaf = g.piece(f"loaf_{i}", "LEFT_ARM", (-1, -1, -1), (2, 1, 2), pivot=(1.0 + dx, 7.4, -3.6 + dz))
        solid(loaf, "L", "plain", 35247 + i, 3, edge=False)
        loaf.top.fill("L4"), loaf.top.set(i, 1 - i, "L2")                   # the baker's slash
    for i, (ox, oy, w, h) in enumerate(((-2, -3, 4, 1), (-2, -2, 1, 2), (1, -2, 1, 2))):   # arched handle
        handle = g.piece(f"basket_handle_{i}", "LEFT_ARM", (ox, oy, -.5), (w, h, 1), pivot=(1.0, 7.4, -2.6))
        solid(handle, "L", "plain", 35249, 3, edge=False)
        handle.top.fill("L4")
    front, back = flaps(g, "robe", 7, "P", "weave", 35250, top=10.6, hem="A2")
    for face in (front, back):
        face.vline(4, 1, 5, "P1")
        embroider(face, 5, "dash", "A3", "A1")
    side_panels(g, "robe_side", 6, "P", "weave", hem="A2", top=10.6)
