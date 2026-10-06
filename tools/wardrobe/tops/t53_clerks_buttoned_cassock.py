"""Clerk's Buttoned Cassock: a dark cassock closed by a long run of small buttons, a short shoulder cape and a sash."""
from kit import body, collar, sleeves
from kit_male import buttons, sash, shoulder_cape

META = {
    "name": "Clerk's Buttoned Cassock",
    "gender": "male",
    "description": "A parish clerk's dark cassock buttoned from collar to hem, a short buttoned shoulder cape and a sash with a long tail.",
    "tags": ["holy", "robe", "scholarly"],
    "locked_to": "b53_cassock_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "smooth", 5301, base=1)
    b.front.vline(4, 0, 11, "P0")
    buttons(b.front, 3, 1, 11, 1, "M3")
    sleeves(g, "P", "smooth", 5302, base=1, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P0")
        arm.front.set(1, 10, "M3"), arm.front.set(2, 10, "M3")
    stand = collar(g, "stand_collar", "P", "smooth", base=1, height=1, y=-.6)
    stand.front.set(4, 0, "S4"), stand.front.set(3, 0, "P0"), stand.front.set(5, 0, "P0")
    cape = shoulder_cape(g, "pellegrina", "P", "smooth", 5303, base=1, length=3, width=11)
    cape.front.vline(5, 0, 2, "P0")
    buttons(cape.front, 6, 0, 2, 1, "M3")
    sash(g, "fascia", "A", y=8.8, height=2, texture="smooth", seed=5304, tails=((2.6, 0),), tail_len=6)
