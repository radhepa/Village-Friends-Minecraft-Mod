"""Miner's Candle Jerkin: a dark buttoned jerkin with a short shoulder cape, crossed hammer-and-pick badge,
a lit candle in an iron holder on the chest strap and a miner's leather seat-apron at the back."""
from kit import body, sleeves
from kit_f07 import prop
from kit_female import cuffs, girdle, mantle, neck, over_panel
from paint import fabric, line

META = {
    "name": "Miner's Candle Jerkin",
    "gender": "female",
    "description": "A dark buttoned jerkin with a short shoulder cape and a hammer-and-pick badge, a lit candle "
                   "in an iron holder on her chest strap and a leather seat-apron at the back.",
    "tags": ["work", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "plain", 57801, base=1)
    neck(b.front, "round", "P", 1, edge="P2")
    for y in range(1, 12):
        b.front.set(3, y, "P0")
    for y in (2, 4, 6, 8, 10):
        b.front.set(4, y, "M3")                                      # a row of pewter buttons
    sleeves(g, "P", "plain", 57802, base=1, rows=(0, 11))
    cuffs(g, "S", y=7.6, h=2, size=5, base=3)
    cape = mantle(g, "shoulder_cape", "P", "plain", 57803, 1, height=3, width=17, depth=6, y=-.7)
    for face in cape.sides:
        face.hline(0, face.w - 1, 2, "P0"), face.hline(0, face.w - 1, 0, "P2")
    # The crossed hammer and pick of the mining trade, stitched on the cape front.
    f = cape.front
    line(f, 10, 0, 12, 2, "M3"), line(f, 12, 0, 10, 2, "M3")
    f.set(10, 0, "M4"), f.set(12, 0, "M2")
    # Chest strap carrying the candle holder.
    j = g.part("jacket")
    line(j.front, 7, 0, 0, 7, "L2")
    line(j.back, 0, 0, 7, 7, "L1")
    fabric(j.front, "L", "leather", 57804, 1, 0, 8, 8, 1)
    holder = prop(g, "candle_holder", "TORSO", (-1, 0, -1.5), (2, 1, 2), pivot=(-2.4, 4.2, -2.4), role="M",
                  texture="smooth", seed=57805, base=2, edge=False)
    holder.top.fill("M3"), holder.front.set(0, 0, "M4")
    candle = prop(g, "candle", "TORSO", (-.5, -2, -1), (1, 2, 1), pivot=(-2.4, 4.2, -2.4), role="S", base=4,
                  seed=57806, edge=False)
    candle.front.set(0, 1, "S3")
    flame = prop(g, "candle_flame", "TORSO", (-.5, -3, -1), (1, 1, 1), pivot=(-2.4, 4.2, -2.4), role="A", base=4,
                 seed=57807, edge=False)
    flame.top.fill("A4"), flame.bottom.fill("A2")
    # The miner's seat-apron: stiff leather hung at the back for sliding down the shafts.
    girdle(g, "apron_belt", 8.0, role="L", base=1, height=1, wide=True)
    seat = over_panel(g, "seat_apron", 7, "L", "leather", 57808, base=2, width=9, top=8.8, back=True)
    seat.vline(0, 0, 6, "L1"), seat.vline(8, 0, 6, "L1"), seat.hline(0, 8, 6, "L1")
    for x in (1, 7):
        seat.set(x, 1, "M3"), seat.set(x, 5, "M3")
