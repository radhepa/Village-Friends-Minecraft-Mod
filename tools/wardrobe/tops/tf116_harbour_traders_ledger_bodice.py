"""Harbour Trader's Ledger Bodice: a close double-breasted bodice with a stand collar and ink-spotted
turned cuffs, a clasped ledger thrust under the girdle and a pen case and inkhorn hung at the hip."""
from kit import body, sleeves
from kit_female import girdle, hanging, neck
from paint import fabric, solid

META = {
    "name": "Harbour Trader's Ledger Bodice",
    "gender": "female",
    "description": "A double-breasted trader's bodice with ink-spotted cuffs, a clasped ledger thrust under the girdle and a pen case and inkhorn at the hip.",
    "tags": ["tailored", "scholarly", "slim"],
}

SEED = 53180


def build(g):
    b = body(g, "P", "twill", SEED)
    neck(b.front, "round", "P", 2, edge="P3")
    b.front.vline(5, 1, 11, "P1"), b.front.vline(6, 1, 11, "P3")     # the wrapped front edge
    for y in (2, 4, 6, 9):
        b.front.set(2, y, "M3"), b.front.set(5, y, "M3")             # two rows of buttons
    for face in (b.front, b.back):
        face.hline(0, face.w - 1, 8, "P1")                          # the waist seam
    for face in (b.right, b.left):
        face.vline(2, 0, 11, "P1")
    b.back.vline(3, 0, 7, "P1"), b.back.vline(4, 0, 7, "P3")
    j = g.part("jacket")
    for face in j.sides:                                             # a stand collar
        face.hline(0, face.w - 1, 0, "S3")
    j.front.clear(3, 0), j.front.clear(4, 0)
    fabric(j.top, "S", "plain", SEED + 1, 4, 0, 0, 8, 1)
    sleeves(g, "P", "twill", SEED + 2, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 8, "S4"), arm.strip.hline(0, 15, 9, "S3"), arm.strip.hline(0, 15, 10, "S2")
        arm.front.set(1, 9, "K2"), arm.front.set(2, 10, "K1")         # ink on the cuff
        arm.strip.hline(0, 15, 11, "P1")
    girdle(g, "girdle", 7.6, role="L", base=2, height=1, buckle="M")
    # The ledger, thrust under the girdle at the left front.
    ledger = g.piece("ledger", "TORSO", (-2, -3, -.5), (4, 5, 1), pivot=(1.6, 8.0, -3.0), rotation=(0, 0, -10))
    solid(ledger, "L", "leather", SEED + 3, 3, edge=False)
    for f in (ledger.front,):
        f.hline(0, 3, 0, "L4"), f.vline(0, 0, 4, "L4"), f.hline(0, 3, 4, "L1"), f.vline(3, 0, 4, "L1")
        f.set(1, 1, "A2"), f.set(2, 3, "A2")                         # tooled bosses on the cover
    ledger.top.fill("S4"), ledger.left.fill("S4")                    # page edges
    ledger.left.vline(0, 0, 4, "S3")
    ledger.front.set(3, 2, "M3")                                     # the clasp
    over = g.piece("ledger_girdle", "TORSO", (-2, 0, -.5), (4, 1, 1), pivot=(1.6, 7.6, -3.3), rotation=(0, 0, -10),
                   inflate=.04)
    solid(over, "L", "leather", SEED + 4, 2, edge=False)
    over.front.hline(0, 3, 0, "L3")
    # A pen case and an inkhorn hung from the girdle at the right hip.
    penner = hanging(g, "penner", -3.0, 4, role="L", base=1, top=8.4)
    penner.front.set(0, 0, "M3"), penner.front.set(0, 3, "L3")
    horn = hanging(g, "inkhorn", -2.0, 2, role="K", base=3, top=8.4)
    horn.front.set(0, 0, "M3"), horn.front.set(0, 1, "K2")
