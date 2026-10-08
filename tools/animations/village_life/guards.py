"""Guards: knights work with the sword they carry, archers with their bow.

Every clip here animates the item arm (items="override") so the held vanilla sword or bow follows the hand, and none
mirror: the weapon stays in the main hand whichever hand a resident gestures with. Two clips only play while guards
muster at the bell during a raid (routine:defend); the scanning clips are favored when a night-watch squad pauses.
"""
from kit import clip

DAY = {"day": 2, "morning": 1.3}
KNIGHT = ["adult", "job:knight", "holding"]
ARCHER = ["adult", "job:archer", "holding"]
RAID = ["routine:defend"]  # mustered at the bell: no chores or practice
WATCH = {"routine:night_watch": 4, "night": 1.5}

# Knight: the sword's grip sits across the fist, so pitch alone tips the blade (-32 is a middle guard, point raised
# toward a foe's face) and a half roll of the forearm turns it point-down.
MIDDLE_GUARD = dict(ra=(-32, -12, 0), la=(-60, -62, 0))
STAGGER = dict(rl=(-12, 0, 4), ll=(10, 0, 4))


@clip("rest_on_the_pommel", "Rests both hands on the pommel", weight=4, require=KNIGHT, boost=WATCH, items="override",
      mirror="never", length=6.8)
def _(c):
    c.key(0.45, ra=(-60, 8, 0), head=(6, 0, 0))
    c.key(0.8, ra=(-71, 18, -90))
    c.key(1.15, ra=(-99, 19, -180), la=(-82, -42, 0), waist=(5, 0, 0), head=(6, 0, 0), rl=(0, 0, 5), ll=(0, 0, 5))
    c.key(1.5, la=(-80, -40, 0), lid=.2)
    c.key(2.5, head=(2, 24, 0), look=(.5, 0))
    c.key(3.1, ra_pos=(0, -.7, 0), la_pos=(0, -.7, 0))
    c.key(3.6, ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(4.1, head=(2, -24, 0), look=(-.5, 0))
    c.key(5.0, head=(6, 0, 0), look=(0, 0), lid=.2)
    c.key(5.35, ra=(-99, 19, -180), la=(-80, -40, 0), waist=(5, 0, 0), rl=(0, 0, 5), ll=(0, 0, 5), lid=0)
    c.key(5.7, ra=(-71, 18, -90), la=(-30, -10, 0))
    c.key(6.05, ra=(-60, 8, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0))


@clip("whet_the_sword", "Whets the sword with a stone", weight=4, require=KNIGHT, avoid=RAID, boost=DAY, items="override",
      mirror="never", length=5.8)
def _(c):
    edge = dict(ra=(-22, -34, 15), waist=(6, 0, 0), head=(18, -8, 0), look=(-.2, .5))
    c.key(0.5, **edge, la=(-58, -58, 0))
    for t in (0.9, 1.5, 2.1, 2.7):
        c.key(t, la=(-59, -56, 0), head=(18, -6, 0), look=(-.1, .5))
        c.key(t + .32, la=(-72, -22, 0), head=(17, -14, 0), look=(-.4, .4))
    c.key(3.35, la=(-60, -54, 0), head=(18, -8, 0))
    c.key(3.8, ra=(-40, -30, 15), la=(-30, -10, 0), head=(4, -10, 0), lid=.35, look=(-.3, 0))
    c.key(4.3, ra=(-42, -26, 12), head=(2, -12, 4))
    c.key(4.7, ra=(-22, -34, 15), la=(-70, -30, 0), head=(16, -10, 0), lid=0, look=(-.2, .4))
    c.wobble(4.75, 5.15, 5, "la", 3, base=(-70, -30, 0), axis=1)


@clip("check_for_nicks", "Checks the blade for nicks", weight=3, require=KNIGHT, avoid=RAID, items="override",
      mirror="never", length=5.6)
def _(c):
    c.key(0.4, ra=(-48, 6, 40), head=(4, 0, 0))
    c.key(0.8, ra=(-78, 10, 81), waist=(-2, 0, 0), head=(2, 14, 0), lid=.35, look=(.4, 0))
    c.key(2.2, head=(4, -22, 0), look=(-.5, .1))
    c.key(2.6, ra=(-66, 10, 81), head=(2, -10, 0), lid=.15)
    c.key(3.0, ra=(-90, 10, 81), head=(2, 4, 0), look=(0, .1))
    c.key(3.35, ra=(-78, 10, 81), la=(-104, -35, -7), head=(4, -6, 0), lid=.4, look=(-.2, .2))
    c.wobble(3.45, 4.05, 4, "la", 4, base=(-104, -35, -7), axis=1)
    c.key(4.3, la=(-30, -10, 0), head=(12, -4, 0), lid=0, look=(0, 0))
    c.key(4.55, head=(4, -2, 0))
    c.key(4.85, ra=(-48, 6, 40), la=(0, 0, 0), waist=(0, 0, 0))


@clip("flourish_to_guard", "Salutes with the sword into a high guard", weight=3, require=KNIGHT, avoid=["night"] + RAID,
      boost=DAY, items="override", mirror="never", length=5.2)
def _(c):
    c.key(0.5, ra=(-84, -18, 0), head=(-2, 0, 0), waist=(-2, 0, 0))
    c.key(1.2, ra=(-86, -18, 0), head=(4, 0, 0), lid=.3)
    c.key(1.6, ra=(22, -14, 48), head=(6, -10, 0), waist=(4, -8, 0), lid=0, look=(.3, .3), **STAGGER)
    c.key(1.9, ra=(20, -14, 46))
    c.key(2.4, ra=(-131, 11, -8), la=(-50, -36, 0), waist=(2, 8, 0), head=(-2, 4, 0), look=(0, 0), root_pos=(0, .5, 0))
    c.key(2.65, ra=(-128, 11, -8), root_pos=(0, .8, 0))
    c.key(3.6, ra=(-132, 12, -8), la=(-52, -38, 0), waist=(2, 6, 0), head=(-2, 2, 0), root_pos=(0, .5, 0), lid=.2)
    c.key(4.1, ra=(-60, 0, 8), la=(-10, 0, 0), waist=(0, 0, 0), head=(8, 0, 0), root_pos=(0, 0, 0), lid=0,
          rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(4.5, ra=(-30, 0, 6), head=(2, 0, 0))


@clip("hold_the_line", "Holds the line with sword raised", weight=40, require=KNIGHT + ["routine:defend"],
      items="override", mirror="never", length=7.2)
def _(c):
    c.key(0.5, **MIDDLE_GUARD, **STAGGER, waist=(4, 0, 0), head=(-2, 0, 0), root_pos=(0, .5, 0), lid=.2)
    c.key(1.3, waist=(4, 6, -3), head=(-2, 22, 0), look=(.5, 0))
    c.key(1.7, head=(-2, 26, 0))
    c.key(2.5, waist=(4, -6, 3), head=(-2, -24, 0), look=(-.5, 0), root_pos=(0, .7, 0))
    c.key(2.75, head=(-4, -28, 0), ra=(-40, -12, 0), lid=.35)
    c.key(3.6, head=(-4, -26, 0), ra=(-40, -12, 0), lid=.35)
    c.key(4.1, waist=(4, 0, 0), head=(-2, 0, 0), ra=(-32, -12, 0), look=(0, 0), root_pos=(0, .5, 0), lid=.2)
    c.key(4.5, ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0))
    c.key(4.9, ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(5.6, waist=(4, 4, 2), head=(-2, 14, 0), look=(.3, 0))
    c.key(6.4, **MIDDLE_GUARD, **STAGGER, waist=(4, 0, 0), head=(-2, 0, 0), root_pos=(0, .5, 0), look=(0, 0), lid=.2)


# Archer: the bow's limbs stand across the fist, so an arm raised level holds it upright (the draw) and an arm at
# the side carries it level; rolling the raised arm lays it flat.
BOW_UP = dict(ra=(-62, -10, 0))
LOW_READY = dict(ra=(-27, -10, 0), la=(-62, -70, 0))
FEET_APART = dict(rl=(-8, 0, 5), ll=(8, 0, 5))


@clip("hold_the_draw", "Holds a full draw on the horizon", weight=4, require=ARCHER, avoid=RAID, boost=DAY,
      items="override", mirror="never", length=5.0)
def _(c):
    c.key(0.5, ra=(-60, -6, 0), la=(-70, -30, 0), head=(2, 0, 0), waist=(0, -6, 0))
    c.key(1.1, ra=(-74, 6, 0), la=(-100, -50, 0), waist=(0, -12, 0), head=(0, 12, 0), lid=.45, look=(.15, 0))
    c.wobble(1.3, 2.0, 3, "ra", 1.5, base=(-74, 6, 0))
    c.key(2.5, ra=(-80, 6, 0), la=(-104, -50, 0), head=(-4, 12, 0))
    c.key(3.0, ra=(-80, 6, 0), la=(-104, -50, 0), head=(-4, 12, 0), lid=.45)
    c.key(3.4, la=(-92, -66, 0), head=(0, 10, 0), lid=0, look=(0, 0))
    c.key(3.9, ra=(-40, -6, 0), la=(-40, -30, 0), waist=(0, 0, 0), head=(6, 0, 0))
    c.key(4.4, ra=(-18, 0, 0), la=(-10, 0, 0), head=(2, 0, 0))


@clip("scan_the_dark", "Shades the eyes and scans the dark", weight=4, require=ARCHER, boost={"routine:night_watch": 4, "night": 2},
      items="override", mirror="never", length=6.6)
def _(c):
    shade = dict(la=(-146, -50, 0))
    c.key(0.5, **shade, ra=(12, 0, 5), head=(-4, 0, 0), waist=(4, 0, 0), lid=.3)
    c.key(1.7, head=(-4, 26, 0), look=(.5, 0))
    c.key(3.2, head=(-4, -24, 0), look=(-.5, 0))
    c.key(3.8, head=(-2, -14, 0), waist=(8, -6, 0), ra=(-14, 0, 5), lid=.5, look=(-.3, 0))
    c.key(4.6, head=(-2, -16, 0), waist=(8, -6, 0), ra=(-14, 0, 5), lid=.5)
    c.key(5.0, **shade, head=(4, 0, 0), waist=(2, 0, 0), ra=(12, 0, 5), lid=0, look=(0, 0))
    c.key(5.4, la=(-30, -10, 0), ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0))
    c.key(5.9, ra=(0, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(0, 0, 0))


@clip("flex_the_limb", "Flexes the bow limb", weight=3, require=ARCHER, avoid=RAID, boost=DAY, items="override",
      mirror="never", length=5.8)
def _(c):
    c.key(0.5, **BOW_UP, la=(-83, -36, 0), head=(10, 0, 0), look=(0, .3))
    c.key(1.0, la=(-119, -42, 0), head=(-4, 0, 0), look=(0, -.4))
    c.cycle(1.2, 2.4, .6, dict(ra=(-62, -10, 0), la=(-119, -42, 0)), dict(ra=(-54, -10, 0), la=(-113, -40, 0)))
    c.key(2.8, ra=(-80, -10, -90), la=(-60, -20, 0), head=(-2, 18, 6), lid=.5, look=(.4, 0))
    c.key(3.8, ra=(-80, -10, -90), head=(-2, 20, 6), lid=.5)
    c.key(4.3, **BOW_UP, head=(10, 0, 0), lid=0, look=(0, 0))
    c.key(4.6, head=(4, 0, 0))
    c.key(5.0, ra=(-30, -6, 0), la=(0, 0, 0))


@clip("wax_the_bowstring", "Waxes the bowstring", weight=3, require=ARCHER, avoid=RAID, boost=DAY, items="override",
      mirror="never", length=5.6)
def _(c):
    c.key(0.45, ra=(-56, -14, 0), la=(-79, -48, 0), head=(16, -4, 0), look=(-.1, .4))
    c.cycle(0.8, 3.2, .6, dict(la=(-66, -52, 0), head=(20, -4, 0)), dict(la=(-94, -45, 0), head=(10, -4, 0)))
    c.key(3.5, la=(-79, -48, 0), head=(16, -6, 0), lid=.2)
    c.wobble(3.55, 4.05, 6, "la", 3, base=(-79, -48, 0))
    c.key(4.4, la=(-20, 0, 0), head=(8, -2, 0), lid=0, look=(0, .2))
    c.key(4.8, ra=(-30, -6, 0), head=(4, 0, 0))


@clip("arrow_on_the_string", "Waits with an arrow on the string", weight=40, require=ARCHER + ["routine:defend"],
      items="override", mirror="never", length=7.2)
def _(c):
    c.key(0.5, **LOW_READY, **FEET_APART, waist=(4, -6, 0), head=(0, 4, 0), root_pos=(0, .4, 0), lid=.2)
    c.key(1.3, head=(0, 24, 0), look=(.5, 0))
    c.key(2.2, head=(0, -26, 0), waist=(4, -8, 0), look=(-.5, 0))
    c.key(2.45, head=(-2, -18, 0), look=(-.3, 0), lid=.35)
    c.key(2.9, ra=(-58, -6, 0), la=(-85, -61, 0), waist=(2, -14, 0), head=(-2, -6, 0), lid=.45, look=(0, 0))
    c.key(3.7, ra=(-58, -6, 0), la=(-85, -61, 0), waist=(2, -14, 0), head=(-2, -6, 0), lid=.45)
    c.key(4.2, **LOW_READY, waist=(4, -6, 0), head=(0, 4, 0), lid=.2)
    c.key(4.6, ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0))
    c.key(5.0, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(0, 18, 0), look=(.4, 0))
    c.key(6.4, **LOW_READY, **FEET_APART, waist=(4, -6, 0), head=(0, 4, 0), root_pos=(0, .4, 0), look=(0, 0), lid=.2)
