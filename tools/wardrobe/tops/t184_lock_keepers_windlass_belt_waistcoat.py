"""Lock Keeper's Windlass-Belt Waistcoat: a collarless buttoned waistcoat with flapped hip pockets over a full-sleeved
shirt, a broad belt carrying the iron windlass crank for the sluices and a ring of paddle keys."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk
from paint import fabric

META = {
    "name": "Lock Keeper's Windlass-Belt Waistcoat",
    "gender": "male",
    "description": "A collarless buttoned waistcoat with flapped hip pockets over a full-sleeved shirt, a broad belt "
                   "carrying the iron windlass crank for the sluices and a ring of paddle keys.",
    "tags": ["casual", "work"],
    "covers_waist": True,
}

CRANK = (2.4, 9.0, -3.4)     # the crank's socket end rests in the belt here; its pieces share the hinge
KEYS = (-2.6, 10.2, -3.4)


def build(g):
    b = body(g, "S", "weave", 33520, base=3)
    neckline(b.front, "round", "S", base=3)
    # The waistcoat: front panels in the main cloth, the back in plain lining, buttoned down the middle.
    f = b.front
    fabric(f, "P", "twill", 33521, 2, 0, 1, 8, 11)
    f.vline(0, 0, 11, "S3"), f.vline(7, 0, 11, "S3")                    # shirt showing at the armholes
    f.set(1, 1, "P3"), f.set(6, 1, "P3"), f.set(2, 1, "S3"), f.set(5, 1, "S3")
    f.vline(3, 2, 11, "P1"), f.vline(4, 2, 11, "P3")
    for y in range(3, 11, 2):
        f.set(4, y, "M3")
    for face in (b.right, b.left):
        fabric(face, "P", "twill", 33522, 2, 0, 3, face.w, 9)
    fabric(b.back, "S", "plain", 33523, 1, 0, 3, 8, 9)
    b.back.hline(1, 6, 7, "L1"), b.back.set(4, 7, "M2")                 # the back strap and buckle
    sleeves(g, "S", "weave", 33524, base=3, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm").strip
        arm.hline(0, 15, 8, "S2"), arm.hline(0, 15, 9, "S4"), arm.hline(0, 15, 10, "S2")   # gathered cuffs
        arm.set(5, 3, "S2"), arm.set(6, 4, "S2")
    for i, x in enumerate((-2.4, 2.4)):                                  # flapped hip pockets
        flap = blk(g, f"pocket_flap_{i}", (x, 7.6, -2.55), (3, 1, 1), "P", 3, "twill", 33525 + i, edge=False)
        flap.front.set(1, 0, "M3")
    belt(g, "broad_belt", 9.2, height=2)
    # The windlass: an iron crank thrust through the belt, its square socket down and wooden grip up.
    shaft = blk(g, "windlass_shaft", CRANK, (1, 3, 1), "M", 1, "smooth", 33527, origin=(-.5, -1.0, -.5),
                motion="flap_front")
    shaft.strip.hline(0, shaft.strip.w - 1, 0, "M3")
    socket = blk(g, "windlass_socket", CRANK, (2, 2, 1), "M", 1, "smooth", 33528, origin=(-1, 2.0, -.5),
                 motion="flap_front")
    socket.bottom.fill("K0"), socket.bottom.set(0, 0, "M2")
    arm_ = blk(g, "windlass_arm", CRANK, (3, 1, 1), "M", 2, "smooth", 33529, origin=(-2.5, -2.0, -.5),
               motion="flap_front")
    arm_.top.fill("M3")
    grip = blk(g, "windlass_grip", CRANK, (1, 2, 1), "L", 3, "plain", 33530, origin=(-2.5, -3.0, -.5),
               motion="flap_front")
    grip.top.fill("L4")
    # A ring of paddle keys on the right hip.
    ring = blk(g, "key_ring", KEYS, (2, 1, 1), "M", 2, "smooth", 33531, origin=(-1, 0, -.5), motion="flap_front",
               edge=False)
    ring.front.set(0, 0, "M3")
    for i, (x, h) in enumerate(((-1.0, 3), (.1, 2))):
        key = blk(g, f"paddle_key_{i}", KEYS, (1, h, 1), "M", 3, "smooth", 33532 + i, origin=(x, 1.0, -.5),
                  motion="flap_front")
        key.strip.hline(0, key.strip.w - 1, h - 1, "M1")
    for face in flaps(g, "waistcoat_points", 2, "P", "twill", 33534, top=11.0):
        face.set(4, 1, "P0"), face.set(3, 1, "P1"), face.set(5, 1, "P1")
