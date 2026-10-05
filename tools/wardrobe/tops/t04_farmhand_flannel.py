"""Farmhand Flannel: a plaid work shirt, tucked in, sleeves rolled past the elbow."""
from paint import fabric, k, rnd

META = {
    "name": "Farmhand Flannel",
    "description": "Plaid flannel shirt with an open collar, chest pocket and rolled sleeves.",
    "tags": ["simple", "casual"],
    "tucked": True,
}


def plaid(face, seed, x_off=0, y_off=0):
    """Primary flannel with dark crossing bands and a thin accent overcheck."""
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = x + x_off, y + y_off
            band_x, band_y = gx % 5 in (0, 1), gy % 5 in (0, 1)
            if band_x and band_y:
                s = 0
            elif band_x or band_y:
                s = 1
            else:
                s = 2 + (1 if rnd(gx, gy, seed) > .9 else 0)
            key = k("P", s)
            if gx % 5 == 3 and gy % 5 == 3:
                key = "A3"
            elif (gx % 5 == 3 and band_y) or (gy % 5 == 3 and band_x):
                key = "A1"
            face.set(x, y, key)


def build(g):
    body = g.part("body")
    # Continuous plaid around the torso; offsets keep the pattern wrapping across seams.
    plaid(body.strip, 41)
    plaid(body.top, 41, 1, 2)
    plaid(body.bottom, 41, 3, 1)
    f = body.front
    # Open collar showing the throat, with lighter turned-back edges.
    for x, y in [(3, 0), (4, 0), (3, 1), (4, 1)]:
        f.clear(x, y)
    for x, y in [(2, 0), (5, 0), (2, 1), (5, 1), (3, 2), (4, 2)]:
        f.set(x, y, "P3")
    f.set(2, 2, "P1"), f.set(5, 2, "P1")
    # Button placket.
    for y in range(3, 12):
        f.set(4, y, "P3" if y % 3 else "P1")
        f.set(3, y, k("P", 1 if f.get(3, y) in ("P0", "P1") else 2))
    for y in (4, 7, 10):
        f.set(4, y, "S4")
    # Chest pocket on the wearer's left with a button flap.
    for x in (5, 6, 7):
        f.set(x, 3, "P3")
    f.set(6, 4, "S3")
    for y in (4, 5, 6):
        f.set(5, y, "P1" if y > 4 else f.get(5, y))
        f.set(7, y, "P1" if y > 4 else f.get(7, y))
    f.hline(5, 7, 6, "P0")
    # Back yoke seam and soft tuck shadow at the waist.
    b = body.back
    b.hline(0, 7, 2, "P1")
    for face in body.sides:
        for x in range(face.w):
            cur = face.get(x, 11)
            if cur and cur[0] == "P":
                face.set(x, 11, k("P", int(cur[1]) - 1))

    for side, arm_name in (("right", "right_arm"), ("left", "left_arm")):
        arm = g.part(arm_name)
        plaid(arm.top, 13, 2, 0)
        # Shoulder to elbow in plaid; forearms bare below the roll.
        fabric_rows = range(0, 6)
        sub = arm.strip
        for y in fabric_rows:
            for x in range(sub.w):
                gx, gy = x, y
                band_x, band_y = gx % 5 in (0, 1), gy % 5 in (0, 1)
                s = 0 if band_x and band_y else 1 if band_x or band_y else 2
                sub.set(x, y, k("P", s))
        sub.hline(0, sub.w - 1, 5, "X2")
        # A rolled cuff sits on top as a 3D ring (see below).
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        roll = g.piece(f"{side}_sleeve_roll", bone, (ox - .5, 2.6, -2.5), (5, 2, 5))
        for face in roll.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 3 else "A2")
                face.set(x, 1, "P1" if x % 3 else "A1")
        roll.top.fill("P3")
        roll.bottom.fill("P0")

    # Collar points: two small turned-down tabs splayed over the shoulders.
    for side, x in (("right", -3.2), ("left", 1.2)):
        tab = g.piece(f"{side}_collar_point", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(x + 1, -.2, -2.15),
                      rotation=(0, 0, 18 if side == "right" else -18))
        fabric(tab.front, "P", "plain", 3, 3)
        tab.front.set(0 if side == "left" else 1, 1, "P2")
        for face in (tab.right, tab.left, tab.back, tab.top, tab.bottom):
            face.fill("P2")
        tab.bottom.fill("P1")
