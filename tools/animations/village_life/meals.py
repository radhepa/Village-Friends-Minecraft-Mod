"""Meals: residents eating a real dish at home, standing, at breakfast, lunch and supper (and a slice of cake at a
birthday party).

While a resident eats, the synced meal state tags them dining:eat and food:<kind> (stew, pie, bread, platter, tart,
cider: a drink in a bottle) and the dish is drawn in their RIGHT hand (left-handed residents mirror these clips and
use the left), so the eating clips use mirror "hand" and items "override" and the right arm carries the dish: held
at chest height while the free hand spoons or picks at it in mime, or lifted to the mouth for a bite or a sip.
A standing arm holding something already pitches -18 degrees (vanilla's held-item pose), so the dish arm is written
with held() as the total angle it reaches. For a few seconds after the meal (dining:done) the empty bowl or bottle
stays in hand, so the after-meal clips keep items and use only the free hand.

Seated diners at the tavern only ever pick clips that require "seated" (the Tavern pack's dining clips); every clip
here also avoids "seated" to say so. Weights are high so a standing diner plays these most of the time while the
food is in hand (everyday idles weigh about 150 in all, three times that during a birthday party).
"""
from kit import clip

ITEM = -18  # vanilla's held-item pose for a standing arm


def held(pitch, yaw=0, roll=0):
    """The arm holding the dish, as the total angle it reaches, on top of the held-item pose."""
    return (pitch - ITEM, yaw, roll)


HOLD = dict(mirror="hand", items="override")
STANDING = ["seated"]
PARTY = {"routine:party": 2}           # cake time: outweigh the party clips, which are boosted fivefold
EAT = ["dining:eat"]
DONE = ["dining:done"]

BOWL = held(-66, -26, 0)               # a bowl held at chest height
LOW = held(-46, -14, 0)                # the dish lowered again before the clip lets go
BITE = held(-104, -40, 0)              # something held in the hand, at the mouth
TO_MOUTH = (-113, -40, 0)              # the free hand (a spoon, a morsel) at the mouth
SPOON_IN = (-80, -36, 0)               # the free hand above the bowl
FREE_LOW = (-26, -8, 0)


def chew(c, start, end, base=(6, 0, 0), lid=0.0):
    """Small nods of the head while chewing."""
    t, up = start, True
    while t < end - 1e-6:
        p, y, r = base
        c.key(t, head=(p - 2 if up else p + 1.5, y, r), lid=lid)
        t += .2
        up = not up
    c.key(end, head=base, lid=lid)


# -- stew ----------------------------------------------------------------------------------------


@clip("spoon_up_stew", "Spoons up stew and blows on it", weight=200, require=EAT + ["food:stew"], avoid=STANDING,
      boost=PARTY, length=6.4, **HOLD)
def _(c):
    c.key(0.5, ra=BOWL, la=SPOON_IN, head=(16, -4, 0), look=(0, .6))
    c.key(0.8, la=(-74, -34, 0))
    c.key(1.05, la=(-82, -38, 0))
    c.key(1.45, la=(-100, -38, 0), head=(6, 0, 0), look=(0, .4))
    for t in (1.7, 2.15):
        c.key(t, head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.45)
        c.key(t + .25, head=(6, 0, 0), head_pos=(0, 0, -.1), lid=.2)
    c.key(2.7, la=TO_MOUTH, head=(-2, 0, 0), head_pos=(0, 0, 0), lid=.5, look=(0, .2))
    c.key(3.0, la=SPOON_IN, head=(12, 0, 0), lid=.2, look=(0, .5))
    chew(c, 3.1, 3.7, base=(12, 0, 0), lid=.2)
    c.key(3.95, la=(-82, -38, 0), head=(16, -4, 0), look=(0, .6), lid=0)
    c.key(4.35, la=TO_MOUTH, head=(-2, 0, 0), look=(0, .2), lid=.4)
    c.key(4.65, la=SPOON_IN, head=(8, 0, 4), lid=.5)
    chew(c, 4.75, 5.35, base=(8, 0, 4), lid=.5)
    c.key(5.85, ra=LOW, la=FREE_LOW, head=(4, 0, 2), lid=.2, look=(0, .2))


@clip("sip_from_the_bowl", "Sips broth from the bowl", weight=150, require=EAT + ["food:stew"], avoid=STANDING,
      boost=PARTY, length=4.8, **HOLD)
def _(c):
    under = (-64, -34, 0)              # the free hand cradling the bowl from below
    c.key(0.5, ra=BOWL, la=under, head=(14, 0, 0), look=(0, .6))
    c.key(1.0, ra=held(-100, -36, 0), la=(-94, -30, 0), head=(-4, 0, 0), lid=.4, look=(0, .2))
    c.key(1.4, ra=held(-110, -34, 0), la=(-104, -28, 0), head=(-12, 0, 0), waist=(-3, 0, 0), lid=.7)
    for t in (1.65, 2.0):
        c.key(t, head=(-14, 0, 0)).key(t + .18, head=(-12, 0, 0))
    c.key(2.5, ra=held(-102, -36, 0), la=(-96, -30, 0), head=(-6, 0, 0), waist=(0, 0, 0), lid=.5)
    c.key(2.9, ra=BOWL, la=under, head=(10, 0, 0), lid=.3, look=(0, .5))
    c.key(3.35, head=(-2, 6, 4), lid=.6, look=(.2, 0))
    c.key(3.8, head=(2, 2, 2), lid=.3)
    c.key(4.25, ra=LOW, la=FREE_LOW, head=(2, 0, 2), lid=.1, look=(0, .2))


# -- bread and pies ------------------------------------------------------------------------------


@clip("tear_off_bread", "Tears off a piece of bread", weight=200, require=EAT + ["food:bread"], avoid=STANDING,
      boost=PARTY, length=5.8, **HOLD)
def _(c):
    c.key(0.5, ra=held(-78, -28, 0), la=(-78, -28, 0), head=(12, 0, 0), look=(0, .5))
    c.key(0.9, ra=held(-80, -26, 0), la=(-80, -26, 0), head=(14, 0, 0))
    c.key(1.1, ra=held(-84, -8, 8), la=(-84, -8, 8), head=(10, 0, 0))
    c.key(1.55, la=TO_MOUTH, ra=held(-62, -14, 0), head=(2, 0, 0), look=(0, .2))
    c.key(1.85, la=(-70, -26, 0), head=(6, 0, 0))
    chew(c, 1.95, 2.75, base=(6, 0, 0), lid=.2)
    c.key(3.1, ra=BITE, la=(-50, -16, 0), head=(0, 0, 0), lid=0, look=(0, .2))
    c.key(3.35, ra=held(-102, -36, 4), head=(8, 8, 0), head_pos=(0, 0, -.4))
    c.key(3.6, ra=held(-90, -30, 0), head=(2, -6, 0), head_pos=(0, 0, 0))
    chew(c, 3.7, 4.7, base=(4, 0, 0), lid=.3)
    c.key(5.2, ra=LOW, la=FREE_LOW, head=(2, 0, 0), lid=0, look=(0, 0))


@clip("bite_a_hand_pie", "Bites into a hand pie", weight=200, require=EAT + ["food:pie"], avoid=STANDING,
      boost=PARTY, length=5.2, **HOLD)
def _(c):
    cupped = (-88, -34, 0)             # the free hand cupped under the chin for crumbs
    c.key(0.5, ra=held(-84, -32, 0), la=(-56, -30, 0), head=(10, 0, 0), look=(0, .5))
    c.key(0.95, ra=BITE, la=cupped, head=(2, 0, 0), look=(0, .2))
    c.key(1.15, head=(8, 0, 0), head_pos=(0, 0, -.5), lid=.4)
    c.key(1.4, ra=held(-90, -34, 0), head=(-2, 0, 0), head_pos=(0, 0, 0))
    chew(c, 1.5, 2.6, base=(2, 0, 0), lid=.2)
    c.key(2.8, ra=held(-82, -30, 0), la=(-60, -30, 0), head=(12, -4, 4), look=(0, .6), lid=0)
    c.key(3.3, ra=BITE, la=cupped, head=(2, 0, 0), look=(0, .2))
    c.key(3.5, head=(8, 0, 0), head_pos=(0, 0, -.5), lid=.4)
    c.key(3.75, ra=held(-88, -32, 0), head=(2, 0, 0), head_pos=(0, 0, 0))
    chew(c, 3.85, 4.45, base=(2, 0, 4), lid=.4)
    c.key(4.7, ra=LOW, la=FREE_LOW, head=(2, 0, 2), lid=.1, look=(0, 0))


# -- platters, tarts and cake ---------------------------------------------------------------------


@clip("pick_at_the_platter", "Picks at a platter", weight=330, require=EAT + ["food:platter"], avoid=STANDING,
      boost=PARTY, length=6.2, **HOLD)
def _(c):
    plate = held(-56, -24, 0)          # the plate held low in front
    reach = (-68, -40, 0)              # the free hand over the plate
    c.key(0.5, ra=plate, la=reach, waist=(6, 0, 0), head=(18, -6, 0), look=(-.2, .7))
    c.key(0.8, la=(-64, -44, 0), head=(18, -8, 0))
    c.key(1.0, la=(-70, -36, 0))
    c.key(1.4, la=TO_MOUTH, waist=(2, 0, 0), head=(0, 0, 0), look=(0, .2))
    c.key(1.7, la=(-50, -22, 0), head=(6, 0, 0))
    chew(c, 1.8, 2.6, base=(6, 0, 0))
    c.key(2.9, la=reach, waist=(6, 0, 0), head=(18, -2, 0), look=(0, .7))
    c.key(3.3, la=(-100, -24, 0), waist=(2, 0, 0), head=(4, 0, -10), look=(0, .3), lid=.3)
    c.key(3.7, la=(-100, -26, 0), head=(4, 0, -12))
    c.key(4.0, la=TO_MOUTH, head=(-2, 0, 0), lid=0, look=(0, .2))
    c.key(4.25, la=(-50, -22, 0), head=(6, 0, 0))
    chew(c, 4.35, 5.15, base=(6, 0, 0), lid=.4)
    c.key(5.3, head=(10, 0, 0), lid=.4)
    c.key(5.7, ra=LOW, la=FREE_LOW, waist=(0, 0, 0), head=(2, 0, 0), look=(0, .2), lid=0)


@clip("nibble_a_slice", "Nibbles a slice of tart", weight=200, require=EAT + ["food:tart"], avoid=STANDING,
      boost=PARTY, length=5.0, **HOLD)
def _(c):
    cupped = (-86, -36, 0)             # the free hand cupped under the slice for crumbs
    c.key(0.5, ra=held(-88, -32, 0), la=(-60, -32, 0), head=(10, 0, 0), look=(0, .5))
    c.key(0.95, ra=BITE, la=cupped, head=(2, 0, 0), look=(0, .2), lid=.2)
    for t in (1.15, 1.45, 1.75):
        c.key(t, head=(6, 0, 0), head_pos=(0, 0, -.4)).key(t + .15, head=(2, 0, 0), head_pos=(0, 0, 0))
    c.key(2.2, ra=held(-90, -32, 0), head=(4, 0, 6), lid=.6, look=(0, .1))
    chew(c, 2.3, 3.1, base=(4, 0, 6), lid=.6)
    c.key(3.4, ra=BITE, head=(2, 0, 0), lid=.2)
    c.key(3.6, head=(6, 0, 0), head_pos=(0, 0, -.4))
    c.key(3.8, ra=held(-90, -32, 0), head=(2, 0, 0), head_pos=(0, 0, 0))
    c.key(4.4, ra=LOW, la=FREE_LOW, head=(2, 0, 2), lid=.2)


# -- cider (a bottle) ----------------------------------------------------------------------------


@clip("swig_of_cider", "Takes a swig of cider", weight=330, require=EAT + ["food:cider"], avoid=STANDING,
      boost=PARTY, length=4.8, **HOLD)
def _(c):
    bottle = held(-78, -26, 0)
    c.key(0.45, ra=bottle, head=(6, 0, 0), look=(0, .3))
    c.key(0.9, ra=held(-108, -36, 0), head=(-8, 0, 0), lid=.5, look=(0, .1))
    c.key(1.3, ra=held(-122, -33, 0), head=(-15, 0, 0), waist=(-4, 0, 0), lid=.8, look=(0, -.2))
    for t in (1.55, 1.85, 2.15):
        c.key(t, head=(-14, 0, 0)).key(t + .15, head=(-16, 0, 0))
    c.key(2.55, ra=held(-110, -36, 0), head=(-8, 0, 0), waist=(-2, 0, 0), lid=.6)
    c.key(2.95, ra=bottle, head=(4, 0, 0), waist=(0, 0, 0), lid=.3, look=(0, .3))
    c.key(3.35, head=(-6, 4, 6), lid=.6, look=(0, 0))
    c.key(3.8, head=(-2, 0, 2), lid=.3)
    c.key(4.25, ra=LOW, head=(0, 0, 0), lid=.1)


# -- anything held in the hand -------------------------------------------------------------------


@clip("take_a_bite", "Takes a hearty bite", weight=150, require=EAT, avoid=STANDING + ["food:stew", "food:platter", "food:cider"],
      boost=PARTY, length=4.4, **HOLD)
def _(c):
    c.key(0.5, ra=held(-76, -28, 0), head=(12, 0, 0), look=(0, .5))
    c.key(1.0, ra=BITE, head=(0, 0, 0), look=(0, .2))
    c.key(1.2, head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.4)
    c.key(1.45, ra=held(-90, -34, 0), head=(4, 0, 0), head_pos=(0, 0, 0))
    chew(c, 1.55, 2.95, base=(4, 0, 0), lid=.2)
    c.key(3.2, head=(-2, 4, 4), lid=.4)
    c.key(3.9, ra=LOW, head=(2, 0, 2), lid=0, look=(0, 0))


@clip("savor_a_mouthful", "Savors a mouthful", weight=150, require=EAT, avoid=STANDING, boost=PARTY, length=5.0, **HOLD)
def _(c):
    c.key(0.5, ra=held(-56, -22, 0), head=(6, 0, 0), lid=.3, look=(0, .3))
    c.key(1.0, waist=(-3, 0, 0), head=(-6, 0, 4), lid=.9, look=(0, 0))
    chew(c, 1.1, 2.3, base=(-6, 0, 4), lid=.9)
    c.key(1.8, la=(-56, -48, 0))
    c.key(2.9, head=(-7, 0, -4), lid=.9)
    c.key(3.3, waist=(0, 0, 0), head=(4, 0, 0), lid=.3, look=(0, .2))
    c.key(3.55, head=(10, 0, 0))
    c.key(3.8, la=FREE_LOW, head=(2, 0, 0), lid=.2)
    c.key(4.4, ra=LOW, head=(0, 0, 0), lid=.1, look=(0, 0))


@clip("child_eager_bites", "Eats in eager little bites", weight=150, require=["child"] + EAT,
      avoid=STANDING + ["food:stew", "food:platter", "food:cider"], boost=PARTY, length=3.8, **HOLD)
def _(c):
    c.key(0.3, ra=held(-80, -28, 0), head=(10, 0, 0), look=(0, .5))
    for t in (0.6, 1.75):
        c.key(t, ra=BITE, head=(0, 0, 0), look=(0, .2))
        c.key(t + .15, head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.4)
        c.key(t + .35, ra=held(-92, -34, 0), head=(2, 0, 0), head_pos=(0, 0, 0), lid=0)
    c.cycle(1.0, 1.6, .4, dict(root_pos=(0, -.5, 0)), dict(root_pos=(0, 0, 0)), end_on="b")
    c.cycle(2.2, 3.0, .4, dict(root=(0, 0, 3), head=(2, 0, -5), la=(-8, 0, 10)),
            dict(root=(0, 0, -3), head=(2, 0, 5), la=(-4, 0, 4)))
    c.key(3.35, ra=LOW, root=(0, 0, 0), head=(0, 0, 0), la=(0, 0, 0), lid=0, look=(0, 0))


# -- after the meal (the empty bowl or bottle still in hand, if there is one) -------------------------
# These keep items: an arm holding the empty bowl stays in vanilla's holding pose and the free hand does the work;
# with nothing left in hand, both hands pat the belly.

BELLY = dict(ra=(-30, -50, 0), la=(-30, -50, 0))


@clip("pat_the_belly", "Pats a full belly", weight=180, require=DONE, avoid=STANDING, boost=PARTY,
      length=4.4)
def _(c):
    c.key(0.5, **BELLY, waist=(-5, 0, 0), head=(-4, 0, 0), lid=.2)
    c.cycle(0.8, 2.4, .4, dict(ra=(-38, -48, 0), la=(-30, -50, 0)), dict(ra=(-30, -50, 0), la=(-38, -48, 0)))
    c.key(1.2, waist=(-8, 0, 0), head=(-10, 0, 4), lid=.6, look=(0, -.3))
    c.key(2.6, **BELLY, waist=(-8, 0, 0), head=(-10, 0, -4), lid=.7)
    c.key(3.2, waist=(-4, 0, 0), head=(2, 0, 0), lid=.4, look=(0, 0))
    c.key(3.5, head=(-3, 0, 0))
    c.key(3.9, ra=(-12, -10, 0), la=(-12, -10, 0), waist=(-1, 0, 0), head=(0, 0, 2), lid=.2)


@clip("wipe_the_mouth_after", "Wipes the mouth with the back of a hand", weight=160, require=DONE, avoid=STANDING,
      boost=PARTY, length=3.8)
def _(c):
    c.key(0.45, head=(6, 0, 0))
    c.key(0.85, la=(-110, -54, 0), head=(2, 8, 0), lid=.3)
    c.key(1.3, la=(-108, -18, 0), head=(2, -8, 0))
    c.key(1.55, la=(-106, -50, 0), head=(2, 4, 0))
    c.key(1.95, la=(-50, -10, 0), head=(4, 0, 0), lid=.2)
    c.key(2.4, waist=(-3, 0, 0), head=(-6, 0, 0), lid=.6)
    c.key(2.8, waist=(0, 0, 0), head=(4, 0, 0), lid=.2)
    c.key(3.3, la=(-8, 0, 0), head=(0, 0, 2), lid=0)
