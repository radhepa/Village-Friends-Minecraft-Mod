"""Dining: eating, drinking and finishing up at the tavern table.

While a clip that requires dining:eat or dining:drink plays, the dish or mug moves from the table into the
resident's RIGHT hand (left-handed residents mirror the clip and use the left), so every such clip uses
mirror "hand" and items "override", and the right arm carries the dish: up to the mouth for a sip or a
bite, held in front of the chest while the other hand spoons, forks or picks at it in mime. Vanilla's
held-item pose leaves a seated holding arm at the same -36 degrees as the riding pose, so both arms are
written with sat() as the total angle they reach. A mug reaches the mouth at about -100 to -120 with the
arm swung across the body; the head tips back for a gulp.
"""
from kit import clip

RIDE = -36  # the riding pose (and the seated held-item pose) already pitch the arms this far forward


def sat(pitch, yaw=0, roll=0):
    """An arm pose as the total angle it reaches, written relative to the riding pose."""
    return (pitch - RIDE, yaw, roll)


HOLD = dict(mirror="hand", items="override")
SIP = sat(-104, -38, 0)            # mug at the lips
GULP = sat(-124, -34, 0)           # tipped right up
CUPPED = sat(-80, -26, 0)          # held in front of the chest
DISH_UP = sat(-62, -22, 0)         # a bowl or plate lifted just off the table edge
TO_MOUTH = sat(-113, -40, 0)       # the free hand (spoon, fork, a morsel) at the mouth
IN_DISH = sat(-90, -36, 0)         # the free hand dipping into the dish
DRINK = ["seated", "dining:drink"]


# -- drinking --------------------------------------------------------------------------------------


@clip("sip_the_drink", "Sips a drink", weight=9, require=DRINK, length=4.4, **HOLD)
def _(c):
    c.key(0.5, ra=CUPPED, head=(6, 0, 0), look=(0, .4))
    c.key(1.0, ra=SIP, head=(-4, 0, 0), lid=.4, look=(0, .2))
    c.key(1.8, ra=sat(-108, -38, 0), head=(-8, 0, 0), lid=.5)
    c.key(2.3, ra=CUPPED, head=(4, 0, 0), lid=.3, look=(0, .3))
    c.key(2.7, head=(-2, 6, 4), lid=.5, look=(.2, 0))
    c.key(3.3, ra=sat(-70, -20, 0), head=(2, 4, 2), lid=.2)
    c.key(3.9, ra=sat(-44, -8, 0), head=(0, 0, 0), lid=0, look=(0, 0))


@clip("big_gulp", "Takes a big gulp", weight=6, require=DRINK, avoid=["drink:coffee"],
      boost={"personality:adventurous": 1.5, "personality:playful": 1.5, "evening": 1.3}, length=4.8, **HOLD)
def _(c):
    c.key(0.45, ra=CUPPED, head=(4, 0, 0), look=(0, .3))
    c.key(0.9, ra=SIP, head=(-8, 0, 0), waist=(-2, 0, 0), lid=.5)
    c.key(1.3, ra=GULP, head=(-22, 0, 0), waist=(-7, 0, 0), lid=.8, look=(0, -.2))
    for t in (1.55, 1.85, 2.15):
        c.key(t, head=(-20, 0, 0)).key(t + .15, head=(-23, 0, 0))
    c.key(2.55, ra=sat(-120, -34, 0), head=(-20, 0, 0), waist=(-6, 0, 0), lid=.8)
    c.key(2.95, ra=sat(-72, -20, 0), head=(4, 0, 0), waist=(2, 0, 0), lid=.2, look=(0, .2))
    c.key(3.3, la=sat(-110, -50, 0), head=(-4, 8, 0), lid=.6)
    c.key(3.6, la=sat(-106, -18, 0), head=(-4, -6, 0))
    c.key(4.0, la=sat(-50, -10, 0), ra=sat(-56, -14, 0), head=(-6, 0, 4), waist=(0, 0, 0), lid=.5, look=(0, 0))
    c.key(4.4, la=sat(-38), head=(-2, 0, 2), lid=.2)


@clip("blow_on_the_coffee", "Blows on a hot coffee", weight=9, require=DRINK + ["drink:coffee"],
      boost={"morning": 1.5, "cold": 1.5}, length=5.2, **HOLD)
def _(c):
    under = sat(-92, -36, 0)
    c.key(0.5, ra=CUPPED, head=(10, 0, 0), look=(0, .5))
    c.key(1.0, ra=under, head=(12, 0, 0), head_pos=(0, 0, -.3), look=(0, .6))
    for t in (1.3, 1.85, 2.4):
        c.key(t, head=(14, 0, 0), head_pos=(0, 0, -.7), lid=.45)
        c.key(t + .3, head=(11, 0, 0), head_pos=(0, 0, -.2), lid=.2)
    c.key(3.1, ra=SIP, head=(-2, 0, 0), head_pos=(0, 0, 0), lid=.5, look=(0, .2))
    c.key(3.45, ra=sat(-98, -36, 0), head=(-10, 0, 6), lid=.9)
    c.key(3.75, ra=CUPPED, head=(2, 0, -4), lid=.3, look=(0, .3))
    c.key(4.3, ra=sat(-70, -20, 0), head=(4, 6, 0), lid=.4)
    c.key(4.8, ra=sat(-46, -8, 0), lid=.1, look=(0, 0))


@clip("raise_a_toast", "Raises a toast", weight=7, require=DRINK + ["social"],
      boost={"evening": 1.5, "night": 1.5, "personality:warmhearted": 1.5, "personality:playful": 1.5}, length=4.6, **HOLD)
def _(c):
    c.key(0.45, ra=CUPPED, head=(2, 0, 0))
    c.key(0.9, ra=sat(-150, 4, 6), waist=(-4, 0, 0), head=(-10, 0, 0), lid=.3, look=(0, -.4))
    c.key(1.5, ra=sat(-154, 6, 8), head=(-12, 0, -4), lid=.4)
    c.key(1.7, ra=sat(-146, 4, 6))
    c.key(2.2, ra=SIP, waist=(-2, 0, 0), head=(-6, 0, 0), lid=.5, look=(0, .1))
    c.key(2.7, ra=sat(-112, -36, 0), head=(-12, 0, 0), waist=(-4, 0, 0), lid=.7)
    c.key(3.2, ra=CUPPED, head=(2, 0, 0), waist=(0, 0, 0), lid=.3, look=(0, 0))
    c.key(3.6, head=(-4, 0, 6), lid=.5)
    c.key(4.1, ra=sat(-50, -10, 0), head=(0, 0, 2), lid=.1)


@clip("clink_mugs", "Clinks mugs with a tablemate", weight=7, require=DRINK + ["social"],
      boost={"evening": 1.5, "night": 1.5, "personality:playful": 1.5}, length=4.2, **HOLD)
def _(c):
    c.key(0.4, ra=CUPPED, head=(0, 0, 0))
    c.key(0.85, ra=sat(-102, -4, 0), waist=(12, 0, 0), head=(-12, 0, 0), look=(0, -.3), lid=.2)
    c.key(1.05, ra=sat(-102, -4, 0), ra_pos=(0, 0, -1.4), waist=(14, 0, 0))
    c.key(1.2, ra_pos=(0, .4, .4), lid=.5)
    c.key(1.45, ra_pos=(0, 0, 0), waist=(12, 0, 0), head=(-10, 0, 4))
    c.key(1.9, ra=SIP, waist=(0, 0, 0), head=(-6, 0, 0), lid=.5, look=(0, .2))
    c.key(2.6, ra=sat(-110, -38, 0), head=(-12, 0, 0), lid=.7)
    c.key(3.1, ra=CUPPED, head=(2, 0, 0), lid=.2, look=(0, 0))
    c.key(3.7, ra=sat(-48, -8, 0), head=(0, 0, 3))


@clip("swirl_and_peer", "Swirls the drink and peers in", weight=6, require=DRINK,
      boost={"personality:curious": 2, "personality:thoughtful": 1.5, "personality:meticulous": 1.5}, length=5.2, **HOLD)
def _(c):
    c.key(0.5, ra=sat(-84, -28, 0), head=(14, 0, 0), look=(0, .6))
    swirl = [sat(-86, -24, 6), sat(-82, -30, 0), sat(-84, -34, -6), sat(-88, -28, 0)]
    t, i = 0.7, 0
    while t < 2.3:
        c.key(t, ra=swirl[i % 4])
        t += .16
        i += 1
    c.key(2.6, ra=sat(-94, -34, 0), head=(16, 0, -8), head_pos=(0, 0, -.5), lid=.35, look=(0, .7))
    c.key(3.3, head=(18, 0, -10), lid=.4)
    c.key(3.6, ra=SIP, head=(-4, 0, 0), head_pos=(0, 0, 0), lid=.5, look=(0, .2))
    c.key(4.2, ra=CUPPED, head=(4, 0, 4), lid=.2, look=(0, 0))
    c.key(4.7, ra=sat(-48, -8, 0), head=(2, 0, 2))


# -- eating ----------------------------------------------------------------------------------------
EAT = ["seated", "dining:eat"]


def chew(c, start, end, base=(8, 0, 0), lid=0.0):
    """Small nods of the head while chewing."""
    t, up = start, True
    while t < end - 1e-6:
        p, y, r = base
        c.key(t, head=(p - 2 if up else p + 1.5, y, r), lid=lid)
        t += .2
        up = not up
    c.key(end, head=base, lid=lid)


@clip("spoonful_of_stew", "Spoons up stew and blows on it", weight=14, require=EAT + ["food:stew"], length=6.4, **HOLD)
def _(c):
    c.key(0.5, ra=DISH_UP, la=IN_DISH, waist=(6, 0, 0), head=(16, -4, 0), look=(0, .6))
    c.key(0.8, la=sat(-86, -32, 0))
    c.key(1.05, la=sat(-92, -38, 0))
    c.key(1.45, la=sat(-104, -38, 0), head=(8, 0, 0), look=(0, .4))
    for t in (1.7, 2.15):
        c.key(t, head=(10, 0, 0), head_pos=(0, 0, -.6), lid=.45)
        c.key(t + .25, head=(8, 0, 0), head_pos=(0, 0, -.1), lid=.2)
    c.key(2.7, la=TO_MOUTH, head=(-2, 0, 0), head_pos=(0, 0, 0), lid=.5, look=(0, .2))
    c.key(3.0, la=IN_DISH, head=(10, 0, 0), lid=.2, look=(0, .5))
    chew(c, 3.1, 3.7, base=(10, 0, 0), lid=.2)
    c.key(3.95, la=sat(-92, -38, 0), head=(16, -4, 0), look=(0, .6), lid=0)
    c.key(4.35, la=TO_MOUTH, head=(-2, 0, 0), look=(0, .2), lid=.4)
    c.key(4.65, la=IN_DISH, head=(8, 0, 4), lid=.5)
    chew(c, 4.75, 5.35, base=(8, 0, 4), lid=.5)
    c.key(5.85, ra=sat(-50, -14, 0), la=sat(-50, -10, 0), waist=(2, 0, 0), head=(4, 0, 2), lid=.2, look=(0, .2))


@clip("tear_and_bite_bread", "Tears the bread and takes a bite", weight=14, require=EAT + ["food:bread"], length=5.8,
      **HOLD)
def _(c):
    together = dict(ra=sat(-80, -28, 0), la=sat(-80, -28, 0))
    c.key(0.5, **together, head=(12, 0, 0), look=(0, .5))
    c.key(0.9, ra=sat(-82, -26, 0), la=sat(-82, -26, 0), head=(14, 0, 0))
    c.key(1.1, ra=sat(-86, -8, 8), la=sat(-86, -8, 8), head=(10, 0, 0))
    c.key(1.55, la=TO_MOUTH, ra=sat(-64, -14, 0), head=(2, 0, 0), look=(0, .2))
    c.key(1.85, la=sat(-86, -30, 0), head=(6, 0, 0))
    chew(c, 1.95, 2.75, base=(6, 0, 0), lid=.2)
    c.key(3.1, ra=sat(-106, -40, 0), la=sat(-60, -16, 0), head=(0, 0, 0), lid=0, look=(0, .2))
    c.key(3.35, ra=sat(-102, -36, 4), head=(8, 8, 0), head_pos=(0, 0, -.4))
    c.key(3.6, ra=sat(-92, -30, 0), head=(2, -6, 0), head_pos=(0, 0, 0))
    chew(c, 3.7, 4.7, base=(4, 0, 0), lid=.3)
    c.key(5.2, ra=sat(-50, -12, 0), la=sat(-44, -6, 0), head=(2, 0, 0), lid=0, look=(0, 0))


@clip("forkful_of_pie", "Takes a forkful of pie", weight=14, require=EAT + ["food:pie"], length=5.8, **HOLD)
def _(c):
    c.key(0.5, ra=DISH_UP, la=IN_DISH, waist=(6, 0, 0), head=(16, -4, 0), look=(0, .6))
    for t in (0.8, 1.15):
        c.key(t, la=sat(-86, -36, 0)).key(t + .17, la=sat(-92, -36, 0))
    c.key(1.7, la=TO_MOUTH, head=(-2, 0, 0), look=(0, .2), lid=.3)
    c.key(2.0, la=sat(-98, -36, 0), head=(6, 0, 0))
    chew(c, 2.1, 3.1, base=(6, 0, 0), lid=.55)
    c.key(3.3, head=(6, 0, 6), lid=.6)
    c.key(3.65, la=IN_DISH, head=(16, -4, 0), look=(0, .6), lid=0)
    c.key(3.9, la=sat(-92, -38, 0))
    c.key(4.25, la=TO_MOUTH, head=(-2, 0, 0), look=(0, .2), lid=.3)
    c.key(4.55, la=sat(-90, -34, 0), head=(6, 0, 0))
    chew(c, 4.65, 5.15, base=(6, 0, 0), lid=.3)
    c.key(5.4, ra=sat(-50, -14, 0), la=sat(-48, -10, 0), waist=(2, 0, 0), look=(0, .2))


@clip("ploughmans_bites", "Picks at a ploughman's lunch", weight=14, require=EAT + ["food:platter"], length=6.2, **HOLD)
def _(c):
    low = sat(-58, -20, 0)
    c.key(0.5, ra=low, la=sat(-92, -34, 0), waist=(8, 0, 0), head=(18, -6, 0), look=(-.2, .7))
    c.key(0.8, la=sat(-96, -40, 0), head=(18, -8, 0))
    c.key(1.2, la=TO_MOUTH, head=(0, 0, 0), look=(0, .2))
    c.key(1.45, la=sat(-62, -20, 0), head=(6, 0, 0))
    chew(c, 1.55, 2.35, base=(6, 0, 0))
    c.key(2.7, la=sat(-94, -32, 0), head=(18, -2, 0), look=(0, .7))
    c.key(3.1, la=sat(-104, -24, 0), head=(4, 0, -10), look=(0, .3), lid=.3)
    c.key(3.5, la=sat(-104, -26, 0), head=(4, 0, -12))
    c.key(3.8, la=TO_MOUTH, head=(-2, 0, 0), lid=0, look=(0, .2))
    c.key(4.05, la=sat(-62, -20, 0), head=(6, 0, 0))
    chew(c, 4.15, 4.95, base=(6, 0, 0), lid=.4)
    c.key(5.1, head=(10, 0, 0), lid=.4)
    c.key(5.4, head=(2, 0, 0), lid=.3)
    c.key(5.8, ra=sat(-46, -12, 0), la=sat(-46, -10, 0), waist=(2, 0, 0), look=(0, .2), lid=0)


@clip("nibble_a_tart", "Nibbles an apple tart", weight=14, require=EAT + ["food:tart"], length=5.0, **HOLD)
def _(c):
    c.key(0.5, ra=sat(-90, -34, 0), head=(10, 0, 0), look=(0, .5))
    c.key(0.95, ra=sat(-104, -40, 0), head=(2, 0, 0), look=(0, .2), lid=.2)
    for t in (1.15, 1.45, 1.75):
        c.key(t, head=(6, 0, 0), head_pos=(0, 0, -.4)).key(t + .15, head=(2, 0, 0), head_pos=(0, 0, 0))
    c.key(2.2, ra=sat(-90, -32, 0), head=(4, 0, 6), lid=.6, look=(0, .1))
    chew(c, 2.3, 3.1, base=(4, 0, 6), lid=.6)
    c.key(3.4, ra=sat(-104, -40, 0), head=(2, 0, 0), lid=.2)
    c.key(3.6, head=(6, 0, 0), head_pos=(0, 0, -.4))
    c.key(3.8, head=(2, 0, 0), head_pos=(0, 0, 0))
    c.key(4.4, ra=sat(-56, -16, 0), head=(2, 0, 2), lid=.2)


@clip("lift_and_bite", "Takes a hearty mouthful", weight=10, require=EAT, length=4.4, **HOLD)
def _(c):
    c.key(0.5, ra=sat(-74, -28, 0), head=(12, 0, 0), look=(0, .5))
    c.key(1.0, ra=sat(-104, -40, 0), head=(0, 0, 0), look=(0, .2))
    c.key(1.2, head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.4)
    c.key(1.45, ra=sat(-92, -34, 0), head=(4, 0, 0), head_pos=(0, 0, 0))
    chew(c, 1.55, 2.95, base=(4, 0, 0), lid=.2)
    c.key(3.2, head=(-2, 4, 4), lid=.4)
    c.key(3.9, ra=sat(-50, -12, 0), head=(2, 0, 2), lid=0, look=(0, 0))


@clip("savor_it", "Savors a bite with eyes closed", weight=10, require=EAT, length=5.4, **HOLD)
def _(c):
    c.key(0.5, ra=sat(-74, -28, 0), head=(12, 0, 0), look=(0, .5))
    c.key(1.0, ra=sat(-104, -40, 0), head=(0, 0, 0), look=(0, .2))
    c.key(1.2, head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.4)
    c.key(1.5, ra=sat(-70, -24, 0), head=(2, 0, 0), head_pos=(0, 0, 0))
    c.key(2.1, waist=(-6, 0, 0), head=(-12, 0, 6), lid=1, look=(0, -.3))
    c.key(2.8, head=(-12, 0, -6), lid=1)
    c.key(3.5, head=(-10, 0, 6), lid=1)
    c.key(4.0, waist=(0, 0, 0), head=(6, 0, 0), lid=.3, look=(0, .2))
    c.key(4.3, head=(0, 0, 0))
    c.key(4.9, ra=sat(-50, -14, 0), head=(2, 0, 2), lid=.2, look=(0, 0))


@clip("wipe_the_mouth", "Wipes the mouth", weight=6, require=EAT, length=3.8, **HOLD)
def _(c):
    low = sat(-58, -18, 0)
    c.key(0.45, ra=low, head=(6, 0, 0))
    c.key(0.85, la=sat(-110, -54, 0), head=(2, 8, 0), lid=.3)
    c.key(1.3, la=sat(-108, -18, 0), head=(2, -8, 0))
    c.key(1.55, la=sat(-106, -50, 0), head=(2, 4, 0))
    c.key(1.95, la=sat(-50, -10, 0), head=(4, 0, 0), lid=.2)
    c.key(2.4, head=(10, 0, 0), lid=.4)
    c.key(2.7, head=(2, 0, 0), lid=.2)
    c.key(3.3, ra=sat(-46, -10, 0), la=sat(-38), head=(2, 0, 2), lid=0)


# -- done (the empty dish stays on the table) ------------------------------------------------------
DONE = ["seated", "dining:done"]
BELLY = dict(ra=sat(-30, -50, 0), la=sat(-30, -50, 0))


@clip("pat_a_full_belly", "Pats a full belly and leans back", weight=4, require=DONE, mirror="never",
      boost={"personality:warmhearted": 1.5, "personality:playful": 1.5}, length=4.8)
def _(c):
    c.key(0.5, **BELLY, waist=(-6, 0, 0), head=(-4, 0, 0), lid=.2)
    c.cycle(0.8, 2.4, .4, dict(ra=sat(-38, -48, 0), la=sat(-30, -50, 0)), dict(ra=sat(-30, -50, 0), la=sat(-38, -48, 0)))
    c.key(1.2, waist=(-11, 0, 0), head=(-12, 0, 4), lid=.6, look=(0, -.3))
    c.key(2.6, **BELLY, waist=(-12, 0, 0), head=(-12, 0, -4), lid=.7)
    c.key(3.4, waist=(-8, 0, 0), head=(2, 0, 0), lid=.4, look=(0, 0))
    c.key(3.7, head=(-4, 0, 0))
    c.key(4.3, ra=sat(-36), la=sat(-36), waist=(-2, 0, 0), head=(0, 0, 2), lid=.2)


@clip("peer_into_the_empty_mug", "Peers into an empty mug", weight=4, require=DONE,
      boost={"evening": 1.5, "night": 1.5}, length=4.8)
def _(c):
    c.key(0.5, ra=sat(-106, -14, 0), waist=(14, 0, 0), head=(26, 0, 0), look=(0, .8))
    c.wobble(0.9, 1.8, 3, "ra", 7, base=sat(-106, -14, 0), axis=2)
    c.key(2.2, waist=(16, 0, 0), head=(24, 0, -12), head_pos=(0, 0, -.5), lid=.3, look=(0, .9))
    c.key(2.8, ra=sat(-46, -6, 0), waist=(-4, 0, 0), head=(-6, 0, 0), head_pos=(0, 0, 0), ra_pos=(0, .5, 0),
          la_pos=(0, .5, 0), lid=.6, look=(0, -.2))
    c.cycle(3.2, 4.0, .4, dict(head=(-4, 8, 0)), dict(head=(-4, -8, 0)))
    c.key(4.3, ra=sat(-36), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), head=(2, 0, 0), lid=.2, look=(0, 0))


@clip("push_the_plate_away", "Pushes the plate away content", weight=4, require=DONE, mirror="never", length=4.6)
def _(c):
    c.key(0.45, ra=sat(-98, -12, 0), la=sat(-98, -12, 0), waist=(8, 0, 0), head=(12, 0, 0), look=(0, .5))
    c.key(0.9, ra=sat(-106, -6, 0), la=sat(-106, -6, 0), ra_pos=(0, 0, -1.2), la_pos=(0, 0, -1.2), waist=(14, 0, 0))
    c.key(1.2, ra_pos=(0, 0, -1.2), la_pos=(0, 0, -1.2), head=(10, 0, 0), lid=.2)
    c.key(1.7, **BELLY, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(-10, 0, 0), head=(-8, 0, 6), lid=.6, look=(0, -.2))
    c.key(2.6, waist=(-11, 0, 0), head=(-8, 0, -4), lid=.7)
    c.key(3.4, **BELLY, waist=(-8, 0, 0), head=(-4, 0, 0), lid=.4, look=(0, 0))
    c.key(4.0, ra=sat(-36), la=sat(-36), waist=(-2, 0, 0), head=(0, 0, 2), lid=.2)
