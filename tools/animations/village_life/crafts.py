"""Crafts: three more work motions for each Village Friends profession, the unemployed and nitwits."""
from kit import clip, HAND_TO_CHEST, HAND_TO_MOUTH, HANDS_ON_HIPS

DAY = {"day": 2, "morning": 1.3}
EVENING = {"evening": 2, "day": 1.5}


@clip("saw_the_plank", "Saws a plank", weight=4, require=["adult", "job:carpenter"], avoid=["night"], boost=DAY,
      items="override", length=4.6)
def _(c):
    c.key(0.4, la=(-44, -20, 0), ra=(-52, -8, 0), waist=(16, 8, 0), head=(20, -6, 0), rl=(-10, 0, 0), ll=(8, 0, 0),
          look=(0, .6))
    c.cycle(0.6, 3.2, .64,
            dict(ra=(-76, -6, 0), ra_pos=(0, 0, -2), waist=(20, 3, 0), root_pos=(0, 0, -.3)),
            dict(ra=(-32, -10, 0), ra_pos=(0, 0, 1.5), waist=(14, 11, 0), root_pos=(0, 0, .2)))
    c.key(3.55, ra=(-24, 0, 10), ra_pos=(0, 0, 0), waist=(24, 0, 0), head=(26, 0, -6), lid=.4, look=(0, .8),
          root_pos=(0, 0, 0))
    c.key(4.05, la=(-50, -26, 0), head=(26, 6, 7), rl=(-10, 0, 0), ll=(8, 0, 0))


@clip("measure_hand_spans", "Measures in hand spans", weight=4, require=["adult", "job:carpenter"], boost=DAY, length=5.0)
def _(c):
    c.key(0.45, ra=(-54, -36, 0), la=(-40, -14, 0), waist=(18, 0, 0), head=(22, -10, 0), look=(-.4, .7))
    for i, t in enumerate((0.75, 1.25, 1.75, 2.25, 2.75)):
        yaw = -34 + i * 11
        c.key(t, ra=(-64, yaw + 5, 0), head=(18, -10 + i * 5, 0), look=(-.4 + i * .2, .5))
        c.key(t + .24, ra=(-52, yaw + 9, 0), head=(23, -10 + i * 5, 0), look=(-.4 + i * .2, .75))
    c.key(3.4, ra=(-78, 26, 0), la=(-78, 26, 0), waist=(2, 0, 0), head=(4, 0, 0), look=(0, .3))
    c.key(3.75, head=(9, 0, 0))
    c.key(4.05, head=(1, 0, 0))
    c.key(4.4, ra=(-78, 26, 0), la=(-78, 26, 0), head=(6, 0, 0), lid=.3)


@clip("plane_the_wood", "Planes a board", weight=4, require=["adult", "job:carpenter"], avoid=["night"], boost=DAY,
      items="override", mirror="never", length=5.2)
def _(c):
    back = dict(ra=(-44, -24, 0), la=(-44, -24, 0), ra_pos=(0, 0, 1), la_pos=(0, 0, 1), waist=(12, 0, 0),
                root_pos=(0, 0, .3), head=(18, 0, 0))
    c.key(0.45, **back, rl=(-14, 0, 0), ll=(10, 0, 0), look=(0, .6))
    for t in (0.6, 1.6, 2.6):
        c.key(t, **back)
        c.key(t + .7, ra=(-84, -18, 0), la=(-84, -18, 0), ra_pos=(0, 0, -2.5), la_pos=(0, 0, -2.5), waist=(24, 0, 0),
              root_pos=(0, 0, -.6), head=(22, 0, 0))
    c.key(3.6, **back)
    c.key(4.0, ra=(-54, 0, 10), la=(-30, -10, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(26, 0, 0), root_pos=(0, 0, 0),
          head=(18, 0, 12), lid=.5, look=(0, .4))
    c.key(4.6, head=(18, 0, 14), rl=(-14, 0, 0), ll=(10, 0, 0))


@clip("count_coins", "Counts coins", weight=4, require=["adult", "job:none"], length=5.2)
def _(c):
    c.key(0.45, la=(-58, -22, 0), ra=(-60, -36, 0), head=(24, -4, 0), look=(-.2, .8))
    for i, t in enumerate((0.75, 1.15, 1.55, 1.95, 2.35)):
        c.key(t, ra=(-66, -32, 0), head=(23, -4, 0))
        c.key(t + .18, ra=(-56, -40, 0), head=(26, -4, 0))
    c.key(2.95, la=(-62, -22, 0), ra=(-62, -30, 0), head=(20, -2, 0))
    c.key(3.3, la=(-112, -30, 0), ra=(-110, -40, 0), head=(4, -12, -10), look=(-.4, 0), lid=.3)
    c.wobble(3.35, 3.95, 7, "la", 5, base=(-112, -30, 0), axis=0)
    c.key(4.4, la=(8, 0, 10), ra=(-20, 0, 4), head=(-4, 16, 0), look=(.5, 0), lid=0)
    c.key(4.75, la=(8, 0, 10), head=(-4, -12, 0), look=(-.4, 0))


@clip("sigh_and_slump", "Sighs and slumps", weight=3, require=["adult", "job:none"], mirror="never", length=4.4)
def _(c):
    c.key(0.8, ra_pos=(0, -1, 0), la_pos=(0, -1, 0), head=(-12, 0, 0), waist=(-4, 0, 0), root_pos=(0, -.3, 0), lid=.3,
          look=(0, -.4))
    c.key(1.5, ra_pos=(0, .9, 0), la_pos=(0, .9, 0), ra=(-8, 0, -3), la=(-8, 0, -3), head=(24, 0, 4), waist=(14, 0, 0),
          root_pos=(0, .7, 0), lid=.6, look=(0, .5))
    c.key(2.6, head=(26, 8, 6), look=(.2, .6))
    c.key(3.1, head=(24, -8, 2), look=(-.2, .6))
    c.key(3.5, head=(22, 0, 4), ra_pos=(0, .9, 0), la_pos=(0, .9, 0), waist=(12, 0, 0), root_pos=(0, .6, 0))


@clip("whistle_and_wait", "Whistles while waiting", weight=3, require=["adult", "job:none"], mirror="free", length=5.6)
def _(c):
    pockets = dict(ra=(16, 0, -6), la=(16, 0, -6), ra_pos=(0, -.5, 0), la_pos=(0, -.5, 0))
    c.key(0.5, **pockets, head=(-12, 10, -6), look=(.3, -.5), lid=.15)
    for i, t in enumerate((0.9, 1.7, 2.5, 3.3)):
        side = 1 if i % 2 == 0 else -1
        c.key(t, root_pos=(0, -1.1, 0), root=(3, 0, 2 * side), head=(-14, 14 * side, -8 * side), look=(.45 * side, -.5))
        c.key(t + .4, root_pos=(0, 0, 0), root=(0, 0, 0), head=(-8, 6 * side, -4 * side))
    c.key(4.3, head=(4, -18, 0), look=(-.6, .1))
    c.key(4.8, **pockets, head=(4, -20, 0), look=(-.6, .1))


@clip("marvel_at_hands", "Marvels at their own hands", weight=4, require=["adult", "job:nitwit"], mirror="free", length=5.0)
def _(c):
    c.key(0.5, ra=(-98, -26, 0), la=(-62, -20, 0), head=(10, -6, 0), look=(.2, .3))
    c.key(1.0, ra=(-104, -12, 14), head=(6, 4, -8), look=(.4, .1))
    c.key(1.5, ra=(-100, -34, -6), ra_pos=(0, 0, 1.2), head=(8, -4, 8), look=(.1, .2), lid=0)
    c.key(2.1, ra=(-100, -20, 4), la=(-100, -22, 0), ra_pos=(0, 0, 0), head=(6, 0, 0), look=(0, .2))
    c.wobble(2.2, 3.2, 5, "la", 8, base=(-100, -22, 0), axis=1)
    c.key(2.6, head=(4, 0, -10), look=(-.3, .2))
    c.key(3.3, ra=(-104, -30, 0), la=(-104, -30, 0), head=(10, 0, 0), look=(0, .3))
    c.key(3.75, ra=(-104, 40, 24), la=(-104, 40, 24), head=(-12, 0, 0), waist=(-6, 0, 0), look=(0, -.3), lid=0)
    c.key(4.3, ra=(-106, 42, 26), la=(-106, 42, 26), head=(-10, 0, 7))


@clip("stumble_and_recover", "Stumbles and recovers", weight=3, require=["adult", "job:nitwit"], mirror="free", length=4.0)
def _(c):
    c.key(0.35, head=(10, 0, 0), look=(0, .5))
    c.key(0.6, rl=(-30, 0, 4), ll=(14, 0, 0), waist=(24, 0, 0), root_pos=(0, .5, -.6), ra=(-110, 0, 50), la=(-70, 0, 70),
          head=(-12, 0, 0), look=(0, -.4), lid=0)
    c.cycle(0.8, 1.7, .36, dict(ra=(-150, 0, 40), la=(-60, 0, 80), root=(0, 0, 4), waist=(18, 0, 0)),
            dict(ra=(-70, 0, 80), la=(-150, 0, 40), root=(0, 0, -4), waist=(12, 0, 0)))
    c.key(2.0, rl=(0, 0, 0), ll=(0, 0, 0), waist=(-4, 0, 0), root_pos=(0, 0, 0), root=(0, 0, 0), ra=(-20, 0, 20),
          la=(-20, 0, 20), head=(0, 0, 0), look=(0, 0))
    c.key(2.5, ra=(-46, -40, 0), la=(-20, 0, 6), head=(4, 18, 0), look=(.5, 0))
    c.key(2.9, ra=(-52, -34, 0), head=(4, -20, 0), look=(-.5, 0))
    c.key(3.4, ra=(-58, -50, 0), la=(0, 0, 0), head=(-2, 0, 6), lid=.35, look=(0, 0), waist=(0, 0, 0))


@clip("lose_count", "Loses count on their fingers", weight=4, require=["adult", "job:nitwit"], length=5.4)
def _(c):
    c.key(0.45, la=(-70, -26, 0), ra=(-72, -40, 0), head=(20, -6, 0), look=(-.2, .6))
    for t in (0.75, 1.15, 1.55, 2.45, 2.75):
        c.key(t, ra=(-77, -35, 0), head=(22, -6, 0))
        c.key(t + .18, ra=(-70, -42, 0), head=(18, -6, 0))
    c.key(1.95, head=(12, 0, 10), look=(.3, -.4))
    c.key(2.3, head=(18, -6, 0), look=(-.2, .6))
    c.key(3.15, la=(-60, -20, 0), ra=(-62, -36, 0), head=(8, 0, -10), lid=.3, look=(0, 0))
    c.key(3.55, ra=(-164, 0, 14), la=(-20, 0, 4), head=(4, 8, -10), look=(.2, -.5), lid=0)
    c.wobble(3.65, 4.6, 5, "ra", 7, base=(-164, 0, 14), axis=1)
    c.key(4.95, ra=(-58, 0, 4), head=(2, 4, -4), look=(0, 0))


@clip("shield_block_drill", "Drills shield blocks", weight=4, require=["adult", "job:knight"], avoid=["night"], boost=DAY,
      items="override", length=5.2)
def _(c):
    guard = dict(la=(-84, -34, 0), ra=(-40, 10, 12), waist=(6, -6, 0), head=(4, 0, 0), root_pos=(0, .5, 0))
    c.key(0.45, **guard, rl=(-12, 0, 4), ll=(10, 0, 4), lid=.2)
    c.key(0.9, la=(-152, -30, 0), waist=(8, 0, 0), head=(10, 0, 0), root_pos=(0, .8, 0))
    c.key(1.05, la=(-146, -30, 0), root_pos=(0, 1.1, .4))
    c.key(1.45, **guard)
    c.key(1.9, la=(-40, -20, 14), waist=(18, 0, 0), head=(14, 0, 0), root_pos=(0, 1.4, 0))
    c.key(2.05, root_pos=(0, 1.6, .4))
    c.key(2.45, **guard)
    c.key(2.9, la=(-86, 22, 30), waist=(4, -18, 0), head=(2, -18, 0), look=(-.4, 0))
    c.key(3.05, root_pos=(0, .7, .4))
    c.key(3.4, ra=(-92, -4, 0), ra_pos=(0, 0, -2), la=(-80, -30, 0), waist=(8, 12, 0), head=(2, 8, 0), look=(0, 0),
          root_pos=(0, .5, -.4))
    c.key(3.8, **guard, ra_pos=(0, 0, 0))
    c.key(4.3, la=(-70, -10, 0), ra=(-20, 0, 6), waist=(4, 0, 0), head=(16, -12, 0), root_pos=(0, 0, 0), look=(-.3, .6),
          rl=(-12, 0, 4), ll=(10, 0, 4), lid=0)
    c.key(4.75, la=(-72, -8, 0), head=(16, -14, 4))


@clip("lunge_stretch", "Stretches in lunges", weight=3, require=["adult", "job:knight"], boost=DAY, mirror="never", length=6.2)
def _(c):
    c.key(0.4, **HANDS_ON_HIPS)
    for start, front, back in ((0.6, "rl", "ll"), (3.0, "ll", "rl")):
        c.key(start, **{front: (-32, 0, 0), back: (30, 0, 0)}, root_pos=(0, 1.7, 0), head=(-2, 0, 0))
        for i, t in enumerate((start + .5, start + .9, start + 1.3)):
            deep = i % 2 == 0
            c.key(t, **{front: (-38 if deep else -32, 0, 0), back: (36 if deep else 30, 0, 0)},
                  root_pos=(0, 2.4 if deep else 1.7, 0))
        c.key(start + 1.8, **{front: (0, 0, 0), back: (0, 0, 0)}, root_pos=(0, 0, 0))
    c.key(4.6, **HANDS_ON_HIPS, head=(0, 0, 0))
    c.key(5.0, ra=(-88, -62, 0), la=(-74, -34, 0), head=(0, 10, 0), lid=.4)
    c.key(5.6, ra=(-88, -66, 0), la=(-76, -38, 0), head=(0, 12, 0), lid=.4)


@clip("kneel_and_pledge", "Kneels and pledges", weight=3, require=["adult", "job:knight"], length=6.4)
def _(c):
    c.key(0.45, head=(8, 0, 0), waist=(4, 0, 0))
    c.key(0.8, rl=(-30, 0, 0), ll=(30, 0, 0), root_pos=(0, 1.6, 0), la=(-20, -10, 0))
    c.key(1.2, rl=(-58, 0, 0), ll=(58, 0, 0), root_pos=(0, 5.6, 0), waist=(8, 0, 0), head=(12, 0, 0), la=(-40, -18, 0))
    c.key(1.8, **HAND_TO_CHEST, head=(24, 0, 0), lid=.6)
    c.key(2.1, lid=.9)
    c.key(3.0, head=(26, 0, 0), waist=(10, 0, 0))
    c.key(4.0, head=(24, 0, 0), waist=(8, 0, 0), lid=.9)
    c.key(4.5, head=(-6, 0, 0), waist=(2, 0, 0), lid=0, look=(0, -.2))
    c.key(4.7, rl=(-58, 0, 0), ll=(58, 0, 0), root_pos=(0, 5.6, 0), la=(-40, -18, 0))
    c.key(5.3, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), la=(0, 0, 0), **HAND_TO_CHEST,
          head=(-4, 0, 0))


@clip("test_the_wind", "Tests the wind", weight=4, require=["adult", "job:archer"], avoid=["night"], boost=DAY, length=5.0)
def _(c):
    c.key(0.4, **HAND_TO_MOUTH, head=(2, 0, 0))
    c.key(0.75, ra=(-115, -42, 0), lid=.3)
    c.key(1.15, ra=(-172, 6, 8), head=(-14, 0, 0), look=(.2, -.6), lid=.45)
    c.key(1.8, ra=(-170, 2, 10), head=(-12, 16, 0), look=(.5, -.4))
    c.key(2.5, ra=(-172, 8, 6), head=(-12, -16, 0), look=(-.5, -.4))
    c.key(2.95, head=(-10, 4, 6), lid=.6, look=(0, -.3))
    c.key(3.35, ra=(-92, 28, 0), head=(0, 20, 0), look=(.5, 0), lid=0)
    c.key(3.6, head=(7, 20, 0))
    c.key(3.85, head=(0, 20, 0))
    c.key(4.3, ra=(-90, 28, 0))


@clip("nock_from_quiver", "Nocks an arrow from the quiver", weight=4, require=["adult", "job:archer"], boost=DAY, length=4.8)
def _(c):
    c.key(0.4, la=(-80, -6, 0), head=(2, 0, 0))
    c.key(0.75, ra=(-196, -14, 0), head=(-2, 16, 0), look=(.5, -.2))
    c.key(1.0, ra=(-200, -16, 0), ra_pos=(0, -1, 0))
    c.key(1.3, ra=(-170, -10, 0), ra_pos=(0, 0, 0), head=(-6, 4, 0), look=(.1, -.4))
    c.key(1.7, ra=(-98, -34, 0), la=(-82, -10, 0), head=(10, -8, 0), look=(-.3, .4))
    c.key(2.0, ra=(-86, -42, 0))
    c.wobble(2.05, 2.7, 5, "ra", 4, base=(-86, -42, 0), axis=1)
    c.key(3.1, ra=(-52, -30, 0), la=(-56, -14, 0), head=(4, 0, 0), look=(0, 0))
    c.key(3.4, head=(8, 0, 0))
    c.key(4.2, ra=(-52, -30, 0), la=(-56, -14, 0), head=(2, 0, 0))


@clip("pluck_the_bowstring", "Plucks the bowstring and listens", weight=3, require=["adult", "job:archer"], length=4.6)
def _(c):
    c.key(0.45, la=(-86, -16, 0), ra=(-78, -30, 0), head=(4, 14, 10), look=(-.3, 0))
    for t in (0.85, 2.6):
        c.key(t, ra=(-80, -32, 0))
        c.key(t + .08, ra=(-70, 6, 16), head=(4, 22, 12), lid=.7, look=(-.4, 0))
        c.key(t + .9, ra=(-74, 0, 12), head=(6, 24, 14), lid=.7)
    c.key(2.0, ra=(-128, -26, 0), la=(-92, -14, 0), head=(-6, 4, 0), lid=.2, look=(-.2, -.3))
    c.wobble(2.05, 2.45, 6, "ra", 6, base=(-128, -26, 0), axis=1)
    c.key(2.55, ra=(-80, -32, 0), la=(-86, -16, 0), head=(4, 14, 10), lid=0)
    c.key(3.75, head=(10, 20, 6), lid=.4)
    c.key(4.0, ra=(-60, -10, 6), la=(-70, -12, 0), head=(2, 6, 0), lid=0, look=(0, 0))


@clip("taste_the_spoon", "Tastes from the spoon", weight=4, require=["adult", "job:cook"], boost=DAY, length=5.0)
def _(c):
    c.key(0.4, ra=(-50, -20, 0), la=(-34, -6, 0), waist=(10, 0, 0), head=(18, 0, 0), look=(0, .6))
    c.key(0.8, ra=(-44, -24, 0))
    c.key(1.2, ra=(-100, -36, 0), waist=(2, 0, 0), head=(4, 0, 0), look=(0, .4))
    for t in (1.45, 1.85):
        c.key(t, head=(-3, 0, 0), head_pos=(0, 0, -.5), lid=.3)
        c.key(t + .2, head=(4, 0, 0), head_pos=(0, 0, 0), lid=0)
    c.key(2.4, **HAND_TO_MOUTH, head=(6, 0, 0), lid=.85)
    c.key(2.75, lid=.85)
    c.key(3.0, ra=(-74, -16, 0), la=(-36, -34, 0), head=(-10, 0, 0), lid=0, look=(0, -.3))
    c.cycle(3.25, 4.25, .4, dict(head=(-6, 0, 8), la=(-40, -36, 0), lid=.6), dict(head=(-6, 0, -8), la=(-30, -30, 0), lid=.6))


@clip("pinch_of_salt", "Sprinkles a pinch of salt", weight=4, require=["adult", "job:cook"], boost=DAY, length=4.4)
def _(c):
    c.key(0.4, ra=(-56, -44, 0), la=(14, 0, 26), waist=(6, 0, 0), head=(16, -10, 0), look=(-.3, .6))
    c.key(0.7, ra=(-52, -46, 0))
    c.key(1.15, ra=(-150, 20, -10), waist=(-2, 0, 0), head=(-8, 4, 0), look=(.2, -.5))
    c.wobble(1.25, 2.45, 6, "ra", 5, base=(-150, 20, -10), axis=1)
    c.key(1.9, head=(12, 0, 0), look=(0, .5))
    c.key(2.45, head=(14, 0, 0))
    c.key(2.85, ra=(-108, 40, 40), head=(-6, 10, -6), lid=.4, look=(.3, 0))
    c.key(3.6, ra=(-106, 42, 42), head=(-6, 12, -7), la=(14, 0, 26))


@clip("toss_the_pan", "Tosses the pan", weight=4, require=["adult", "job:cook"], boost=DAY, items="override", length=4.6)
def _(c):
    c.key(0.4, ra=(-60, -10, 0), la=(14, 0, 26), waist=(6, 0, 0), head=(16, 0, 0), look=(0, .6))
    for dip, big in ((0.75, False), (1.75, False), (2.85, True)):
        c.key(dip, ra=(-50, -10, 0), root_pos=(0, .3, 0), head=(18, 0, 0), look=(0, .6))
        c.key(dip + .15, ra=(-88 if big else -80, -10, 0), root_pos=(0, 0, 0), head=(-12 if big else 2, 0, 0),
              look=(0, -.7 if big else -.3), lid=0)
        c.key(dip + (.6 if big else .45), ra=(-54, -10, 0), head=(14, 0, 0), look=(0, .5), root_pos=(0, .4, 0))
        c.key(dip + (.75 if big else .6), ra=(-60, -10, 0), root_pos=(0, 0, 0))
    c.key(3.75, root=(0, 0, 3), head=(16, 0, -6), lid=.5)
    c.key(4.05, ra=(-72, -22, 0), root=(0, 0, 0), head=(20, -4, 4), lid=0, look=(-.1, .7))


@clip("polish_a_mug", "Polishes a mug", weight=4, require=["adult", "job:tavern_keeper"], boost=EVENING, length=5.6)
def _(c):
    c.key(0.45, la=(-74, -28, 0), ra=(-78, -36, 0), head=(14, -4, 0), look=(-.1, .6))
    twist = [(-82, -34, 4), (-78, -28, 0), (-74, -34, -4), (-78, -40, 0)]
    t = 0.6
    while t < 2.5:
        for pose in twist:
            c.key(t, ra=pose)
            t += .15
    c.key(2.95, la=(-132, -22, 0), ra=(-60, -30, 0), head=(-14, -6, 0), lid=.45, look=(-.2, -.6))
    c.key(3.35, la=(-130, -24, 0))
    c.key(3.65, la=(-104, -36, 0), head=(6, 0, 0), head_pos=(0, 0, -.5), lid=.3, look=(0, .2))
    c.key(3.9, head_pos=(0, 0, 0), ra=(-100, -40, 0))
    c.cycle(4.0, 4.6, .2, dict(ra=(-104, -36, 4)), dict(ra=(-96, -42, -4)))
    c.key(4.95, la=(-70, -26, 0), ra=(-40, -10, 0), head=(8, 0, 4), lid=0, look=(0, .2))


@clip("wipe_the_counter", "Wipes the counter", weight=4, require=["adult", "job:tavern_keeper"], boost=EVENING, length=5.0)
def _(c):
    c.key(0.45, la=(-44, -10, 0), ra=(-60, -40, 0), waist=(16, 0, 0), head=(18, 0, 0), look=(0, .6))
    loop = [(-60, -40, 0), (-48, -20, 10), (-56, 8, 20), (-70, -12, 6)]
    t, i = 0.6, 0
    while t < 3.2:
        c.key(t, ra=loop[i % 4], waist=(16, (-6, 0, 6, 0)[i % 4], 0))
        t += .2
        i += 1
    c.key(3.45, ra=(-60, -30, 0), waist=(10, 0, 0))
    c.key(3.75, ra=(-196, -14, 0), la=(-20, 0, 6), waist=(0, 0, 0), head=(2, 10, 0), look=(.3, 0))
    c.key(4.15, **HANDS_ON_HIPS, head=(-2, 10, 0), lid=.3)
    c.key(4.55, head=(-2, -8, 0), look=(-.3, 0))


@clip("balance_a_tray", "Balances a tray overhead", weight=3, require=["adult", "job:tavern_keeper"], boost=EVENING,
      length=5.4)
def _(c):
    c.key(0.5, ra=(-168, 0, -12), la=(-10, 0, 40), head=(-14, 0, 0), look=(.2, -.7))
    c.cycle(0.8, 2.9, .9, dict(ra=(-166, 0, -18), root=(0, 0, 3), la=(-14, 0, 46)),
            dict(ra=(-170, 0, -6), root=(0, 0, -3), la=(-8, 0, 34)))
    c.key(3.15, ra=(-156, 0, -30), root=(0, 0, -6), la=(-30, 0, 72), head=(-16, 0, -8), lid=0, look=(.4, -.8))
    c.key(3.35, ra=(-174, 0, 2), root=(0, 0, 4), la=(-20, 0, 60))
    c.key(3.65, ra=(-168, 0, -12), root=(0, 0, 0), la=(-10, 0, 40), head=(-14, 0, 0))
    c.key(4.2, ra=(-124, -10, 0), la=(-4, 0, 6), head=(2, 0, 0), lid=.5, look=(0, 0))
    c.key(4.7, ra=(-122, -10, 0), lid=.3)


@clip("grind_mortar", "Grinds with mortar and pestle", weight=4, require=["adult", "job:apothecary"], boost=DAY,
      length=5.0)
def _(c):
    c.key(0.4, la=(-52, -26, 0), ra=(-58, -34, 0), waist=(8, 0, 0), head=(22, 0, 0), look=(0, .8))
    grind = [(-62, -30, 0), (-58, -24, 6), (-54, -30, 0), (-58, -40, -4)]
    t, i = 0.55, 0
    while t < 3.0:
        c.key(t, ra=grind[i % 4], ra_pos=(0, .6 if i % 4 == 0 else 0, 0), waist=(10 if i % 4 == 0 else 8, 0, 0))
        t += .16
        i += 1
    c.key(3.3, la=(-74, -30, 0), ra=(-60, -30, 0), ra_pos=(0, 0, 0), waist=(8, 0, 0), head=(24, -6, 6), look=(-.2, .8))
    for t in (3.7, 3.95):
        c.key(t, ra=(-66, -30, 0))
        c.key(t + .12, ra=(-58, -30, 0))
    c.key(4.4, la=(-60, -26, 0), head=(16, 0, 0), lid=.3)


@clip("measure_drops", "Measures drops from a vial", weight=4, require=["adult", "job:apothecary"], boost=DAY, length=5.6)
def _(c):
    c.key(0.5, ra=(-140, -18, 0), la=(-56, -24, 0), head=(-16, 0, 0), look=(.1, -.6), lid=.4)
    c.wobble(1.0, 1.7, 3, "ra", 10, base=(-140, -18, 0), axis=2)
    c.key(2.0, ra=(-84, -34, 0), la=(-62, -24, 0), head=(20, -4, 0), look=(-.1, .7), lid=.3)
    for t in (2.35, 2.85, 3.35):
        c.key(t, ra=(-88, -34, 8), head=(23, -4, 0))
        c.key(t + .2, ra=(-84, -34, 0), head=(20, -4, 0))
    c.key(3.95, la=(-140, -20, 0), ra=(-60, -30, 0), head=(-16, -6, 0), look=(-.1, -.6), lid=.45)
    c.wobble(4.2, 4.8, 3, "la", 8, base=(-140, -20, 0), axis=2)
    c.key(5.0, la=(-136, -20, 0), head=(-12, -6, 4))


@clip("sniff_and_recoil", "Sniffs a potion and recoils", weight=3, require=["adult", "job:apothecary"], length=4.2)
def _(c):
    c.key(0.45, ra=(-104, -38, 0), la=(-60, -20, 0), head=(6, 0, 0))
    c.cycle(0.6, 1.4, .4, dict(la=(-100, -10, 20)), dict(la=(-88, -30, 0)))
    c.key(1.1, head=(8, 0, 0), waist=(4, 0, 0), lid=.4)
    c.key(1.5, ra=(-104, -38, 0), head=(10, 0, 0), root_pos=(0, 0, -.3), lid=.6)
    c.key(1.75, head=(-22, 0, 8), waist=(-10, 0, 0), root_pos=(0, 0, .6), ra=(-72, 28, 24), la=(-113, -40, 0), lid=.9)
    c.wobble(1.9, 2.7, 5, "head", 10, base=(-18, 0, 6), axis=1)
    c.key(3.1, head=(6, 10, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), ra=(-80, 20, 20), la=(-30, 0, 6), lid=.3,
          look=(.4, .3))
    c.key(3.6, ra=(-80, 22, 22), head=(6, 12, 0))


@clip("brush_the_canvas", "Paints broad strokes on a canvas", weight=4, require=["adult", "job:painter"], boost=DAY,
      length=5.4)
def _(c):
    c.key(0.45, ra=(-100, -8, 0), la=(-52, -30, 0), waist=(-3, 0, 0), head=(2, 0, 0), look=(0, .1))
    strokes = [((-132, 22, 14), (-72, -28, 0)), ((-126, -30, 0), (-78, 24, 16)), ((-100, -34, 0), (-100, 30, 14))]
    t = 0.8
    for top, bottom in strokes:
        c.key(t, ra=top, waist=(0, 4, 0), head=(-4, 4, 0), look=(.1, -.3), root_pos=(0, 0, 0))
        c.key(t + .4, ra=bottom, waist=(6, -6, 0), head=(6, -4, 0), look=(-.1, .3), root_pos=(0, 0, -.4))
        t += .75
    c.key(3.1, ra=(-92, 0, 0), ra_pos=(0, 0, 0), waist=(4, 0, 0), head=(2, 0, 0), look=(0, 0))
    for t in (3.25, 3.5):
        c.key(t, ra=(-94, -2, 0), ra_pos=(0, 0, -1.8))
        c.key(t + .12, ra=(-92, 0, 0), ra_pos=(0, 0, 0))
    c.key(3.9, ra=(-48, -10, 0), waist=(-5, 0, 0), root_pos=(0, 0, .5), head=(2, 0, 10), lid=.35, look=(0, 0))
    c.key(4.4, head=(4, 0, -8))
    c.key(4.8, head=(8, 0, -6), lid=.2)


@clip("mix_on_palette", "Mixes colors on a palette", weight=4, require=["adult", "job:painter"], boost=DAY, length=5.2)
def _(c):
    c.key(0.45, la=(-66, -24, 0), ra=(-60, -38, 0), waist=(4, 0, 0), head=(20, -10, 0), look=(-.3, .7))
    swirl = [(-70, -44, 4), (-66, -36, 0), (-62, -44, -4), (-66, -52, 0)]
    t, i = 0.7, 0
    while t < 2.4:
        c.key(t, ra=swirl[i % 4])
        t += .14
        i += 1
    c.key(2.65, ra=(-62, -30, 0), ra_pos=(0, .6, 0))
    c.key(3.0, ra=(-104, 8, 6), ra_pos=(0, 0, 0), head=(-4, 6, 0), lid=.3, look=(.25, -.2))
    c.key(3.35, head=(-4, 6, 8))
    c.key(3.6, head=(4, 6, 0), lid=0)
    c.key(3.95, ra=(-64, -40, 0), head=(20, -10, 0), look=(-.3, .7))
    for t in (4.15, 4.4):
        c.key(t, ra=(-68, -40, 0), ra_pos=(0, .7, 0))
        c.key(t + .12, ra=(-62, -40, 0), ra_pos=(0, 0, 0))


@clip("thumb_measure", "Measures the subject with a thumb", weight=3, require=["adult", "job:painter"], boost=DAY,
      length=5.4)
def _(c):
    c.key(0.5, ra=(-92, -6, 0), la=(14, 0, 26), waist=(-3, 0, 0), head=(4, 6, -10), lid=.45, look=(.15, 0))
    c.key(1.2, ra=(-100, -6, 0), head=(2, 6, -10), look=(.15, -.2))
    c.key(1.7, ra=(-86, -6, 0), head=(6, 6, -10), look=(.15, .2))
    c.key(2.1, ra=(-94, -6, 0), head=(4, 6, -10), look=(.15, 0))
    c.key(2.5, ra=(-56, -26, 0), waist=(8, 0, 0), head=(18, -4, 0), lid=0, look=(0, .6))
    c.key(2.7, ra=(-58, -26, 0), ra_pos=(0, 0, -1.2))
    c.key(2.85, ra=(-56, -26, 0), ra_pos=(0, 0, 0))
    c.key(3.3, ra=(-92, -16, 0), waist=(-4, 0, 0), root_pos=(0, 0, .4), head=(4, 4, -10), lid=.45, look=(0, 0))
    c.key(3.8, ra=(-92, 10, 4), head=(4, 10, -10), look=(.3, 0))
    c.key(4.25, ra=(-92, -14, 0), head=(4, 2, -10), look=(-.1, 0))
    c.key(4.7, ra=(-34, -8, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(9, 0, 0), lid=0, look=(0, 0))


@clip("strum_the_lute", "Strums a lute", weight=4, require=["adult", "job:bard"], boost=EVENING, length=6.0)
def _(c):
    c.key(0.5, la=(-78, 30, 8), ra=(-40, -44, 0), waist=(2, 0, 0), head=(14, -14, -6), look=(-.3, .5))
    c.cycle(0.8, 4.4, .36, dict(ra=(-48, -44, 0)), dict(ra=(-30, -38, 0)))
    c.cycle(0.8, 4.4, 1.6, dict(root=(0, 0, 3), rl=(-8, 0, 0)), dict(root=(0, 0, -3), rl=(0, 0, 0)))
    c.cycle(0.8, 4.4, .8, dict(head=(16, -14, -6)), dict(head=(10, -12, -2)))
    for i, t in enumerate((1.6, 2.4, 3.2, 4.0)):
        c.key(t, la=(-84, 26, 8) if i % 2 == 0 else (-74, 36, 10))
    c.key(4.7, ra=(-74, 12, 34), la=(-86, 30, 10), root=(0, 0, 0), rl=(0, 0, 0), head=(-8, -10, 4), lid=.5,
          look=(0, -.4))
    c.key(5.2, ra=(-70, 14, 36), head=(-6, -10, 6), lid=.6)


@clip("play_the_flute", "Plays a flute", weight=4, require=["adult", "job:bard"], boost=EVENING, length=5.6)
def _(c):
    flute = dict(la=(-110, -46, 0), ra=(-100, 32, 12))
    c.key(0.5, **flute, head=(4, 10, -10), lid=.3, look=(.3, .1))
    c.wobble(0.8, 2.4, 8, "ra", 4, base=(-100, 32, 12), axis=0)
    c.wobble(0.8, 2.4, 6, "la", 3, base=(-110, -46, 0), axis=0)
    c.cycle(0.8, 4.6, 1.8, dict(root=(0, 6, 3), waist=(2, 0, 0)), dict(root=(0, -4, -3), waist=(-2, 0, 0)))
    c.key(2.6, head=(-6, 10, -12), lid=.8, look=(.3, -.2))
    c.wobble(2.6, 3.3, 3, "ra", 3, base=(-104, 32, 12), axis=0)
    c.key(3.4, head=(4, 10, -10), lid=.3, look=(.3, .1))
    c.wobble(3.4, 4.6, 8, "ra", 4, base=(-100, 32, 12), axis=0)
    c.wobble(3.4, 4.6, 6, "la", 3, base=(-110, -46, 0), axis=0)
    c.key(5.0, ra=(-50, -10, 0), la=(-40, -20, 0), head=(4, 0, 0), lid=0, look=(0, 0))


@clip("sing_a_ballad", "Sings a ballad", weight=4, require=["adult", "job:bard"], boost=EVENING, length=6.2)
def _(c):
    c.key(0.5, ra=(-40, -30, 0), waist=(-4, 0, 0), root_pos=(0, -.3, 0), head=(-6, 0, 0))
    c.key(0.9, **HAND_TO_CHEST, la=(-60, 30, 26), root_pos=(0, 0, 0), head=(-16, 6, 4), lid=.6, look=(0, -.4))
    c.cycle(1.2, 3.0, 1.4, dict(root=(0, 0, 3), head=(-16, 6, 6)), dict(root=(0, 0, -3), head=(-16, 2, 0)))
    c.key(2.2, la=(-86, 46, 30))
    c.key(3.2, la=(-142, 30, 40), waist=(-8, 0, 0), head=(-24, -6, 6), root_pos=(0, -.6, 0), lid=.9, look=(0, -.6))
    c.wobble(3.4, 4.0, 6, "head", 2, base=(-24, -6, 6), axis=2)
    c.key(4.4, la=(-50, 20, 10), waist=(6, 0, 0), head=(14, 0, 0), root_pos=(0, 0, 0), lid=.8, look=(0, .4))
    c.key(5.5, **HAND_TO_CHEST, la=(-46, 18, 8), head=(16, 0, 0), lid=.8)


@clip("measure_with_tape", "Measures with a tape", weight=4, require=["adult", "job:tailor"], boost=DAY, mirror="free",
      length=5.8)
def _(c):
    c.key(0.45, ra=(-74, -34, 0), la=(-74, -34, 0), head=(14, 0, 0), look=(0, .5))
    c.key(1.0, ra=(-86, 68, 10), la=(-86, 68, 10), head=(6, 0, 0), look=(0, .2))
    c.key(1.4, head=(8, 24, 0), look=(.6, .2))
    c.key(1.9, head=(8, -24, 0), look=(-.6, .2), lid=.3)
    c.key(2.3, ra=(-88, 70, 10), la=(-88, 70, 10), head=(14, 0, 0), lid=0, look=(0, .3))
    c.key(2.85, ra=(-150, 6, 10), la=(-36, -14, 0), head=(-14, 4, 0), look=(.1, -.6))
    c.key(3.35, ra=(-152, 6, 10), head=(18, -4, 0), look=(0, .7))
    c.key(3.85, ra=(-70, -34, 0), la=(-66, -34, 0), head=(14, 0, 0), look=(0, .5))
    c.cycle(3.95, 4.95, .3, dict(ra=(-78, -34, 0), la=(-60, -34, 0)), dict(ra=(-64, -34, 0), la=(-74, -34, 0)))
    c.key(5.2, head=(10, 0, 4), lid=.3)


@clip("cut_with_shears", "Cuts cloth with shears", weight=4, require=["adult", "job:tailor"], boost=DAY, length=5.6)
def _(c):
    c.key(0.45, la=(-48, -18, 0), ra=(-46, -34, 0), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .7))
    for i in range(11):
        t = 0.7 + i * .22
        c.key(t, ra=(-46 - i * 2.4, -30 + (6 if i % 2 else -2), 0), ra_pos=(0, 0, -i * .2),
              head=(22 - i * .5, 0, 0), waist=(14 + i * .3, 0, 0))
    c.key(3.4, ra=(-118, 14, 12), la=(-118, 14, 12), ra_pos=(0, 0, 0), waist=(0, 0, 0), head=(-8, 0, 0), look=(0, -.4))
    c.key(3.8, head=(-8, 0, 10), lid=.3)
    c.key(4.2, ra=(-108, 14, 12), la=(-108, 14, 12), head=(-6, 0, 4))
    c.key(4.35, ra=(-122, 14, 12), la=(-122, 14, 12), lid=0)
    c.key(4.9, ra=(-50, -20, 0), la=(-50, -20, 0), head=(16, 0, 0), waist=(6, 0, 0), look=(0, .5))


@clip("thread_a_needle", "Threads a needle", weight=3, require=["adult", "job:tailor"], boost=DAY, length=5.4)
def _(c):
    c.key(0.5, la=(-122, -36, 0), ra=(-112, -20, 6), head=(-4, 0, 0), head_pos=(0, 0, -.6), waist=(-2, 0, 0), lid=.5,
          look=(0, -.1))
    c.key(1.0, ra=(-120, -30, 0))
    c.key(1.25, ra=(-122, -34, 0))
    c.key(1.45, ra=(-114, -20, 8), head=(0, 6, 0), lid=.25)
    c.key(1.8, ra=(-110, -44, 0), head=(2, 0, 0))
    c.key(2.1, head=(4, 0, 0), ra=(-108, -44, 0))
    c.key(2.55, ra=(-114, -22, 6), head=(-4, 0, 0), head_pos=(0, 0, -1), waist=(3, 0, 0), lid=.7)
    c.key(3.0, ra=(-118, -28, 2))
    c.key(3.4, ra=(-122, -34, 0))
    c.key(3.75, ra=(-96, 30, 24), head=(-6, 10, 0), head_pos=(0, 0, 0), waist=(0, 0, 0), lid=0, look=(.4, -.1))
    c.key(4.3, ra=(-98, 32, 26), head=(6, 6, 0))
    c.key(4.75, la=(-80, -30, 0), head=(4, 4, 0))


@clip("polish_spectacles", "Polishes spectacles", weight=3, require=["adult", "job:scholar"], boost=DAY, length=6.0)
def _(c):
    c.key(0.45, ra=(-128, -44, 0), head=(2, 0, 0))
    c.key(0.8, ra=(-100, -30, 0), lid=.35)
    c.key(1.2, ra=(-108, -40, 0), la=(-104, -38, 0), head=(6, 0, 0), head_pos=(0, 0, -.4), waist=(2, 0, 0))
    c.key(1.4, head=(10, 0, 0), head_pos=(0, 0, 0))
    rub = [(-74, -34, 4), (-68, -28, 0), (-64, -34, -4), (-68, -40, 0)]
    t, i = 1.7, 0
    while t < 3.1:
        c.key(t, ra=rub[i % 4], la=(-70, -30, 0), head=(18, 0, 0), look=(0, .6), lid=.3)
        t += .13
        i += 1
    c.key(3.4, ra=(-136, -24, 0), la=(-40, -14, 0), head=(-14, 0, 0), waist=(0, 0, 0), look=(0, -.6), lid=.5)
    c.key(3.9, ra=(-134, -20, 8), head=(-14, 0, 6))
    c.key(4.3, ra=(-126, -44, 0), la=(-126, -44, 0), head=(0, 0, 0), look=(0, 0), lid=.3)
    c.key(4.6, lid=.9)
    c.key(4.75, lid=0)
    c.key(4.95, ra=(-30, -10, 0), la=(-20, -6, 0))
    c.key(5.3, head=(6, 0, 0))


@clip("eureka", "Has a eureka moment", weight=4, require=["adult", "job:scholar"], boost=DAY, length=4.6)
def _(c):
    c.key(0.5, ra=(-104, -42, 0), la=(-50, -36, 0), head=(-6, 8, -8), look=(.3, -.6), lid=.2)
    c.wobble(0.9, 1.7, 4, "ra", 4, base=(-104, -42, 0), axis=0)
    c.key(1.7, head=(-6, -4, 6), look=(-.3, -.6))
    c.key(2.0, ra=(-96, -40, 0), la=(-52, -36, 0), waist=(4, 0, 0), head=(6, 0, 0), lid=.4, look=(0, .3))
    c.key(2.2, ra=(-178, 6, 8), la=(-30, 10, 30), head=(-16, 0, 0), waist=(-6, 0, 0), root_pos=(0, -1.2, 0), lid=0,
          look=(0, -.7))
    c.key(2.45, root_pos=(0, 0, 0))
    c.wobble(2.45, 3.0, 4, "ra", 6, base=(-178, 6, 8), axis=0)
    c.key(3.3, ra=(-58, -38, 0), la=(-58, -30, 0), waist=(8, 0, 0), head=(24, 0, 0), look=(0, .8))
    c.wobble(3.4, 4.0, 6, "ra", 7, base=(-58, -38, 0), axis=1)


@clip("read_down_scroll", "Reads down an unrolled scroll", weight=4, require=["adult", "job:scholar"], boost=DAY,
      length=6.4)
def _(c):
    c.key(0.45, ra=(-96, -30, 0), la=(-96, -30, 0), head=(6, 0, 0))
    c.key(0.9, la=(-112, -18, 0), ra=(-50, -22, 0), head=(-6, 0, 0), look=(0, -.4))
    for i in range(6):
        t = 1.2 + i * .38
        c.key(t, head=(-6 + i * 5, -4, 0), look=(-.3, -.4 + i * .2))
        c.key(t + .28, head=(-6 + i * 5, 4, 0), look=(.3, -.4 + i * .2))
    c.key(3.7, ra=(-26, -14, 0), head=(26, 0, 0), look=(0, .8), lid=.3)
    c.key(4.0, head=(30, 0, 0))
    c.key(4.4, ra=(-96, -30, 0), la=(-96, -30, 0), head=(8, 0, 0), look=(0, .2), lid=0)
    c.cycle(4.6, 5.4, .3, dict(ra=(-100, -30, 0), la=(-92, -30, 0)), dict(ra=(-92, -30, 0), la=(-100, -30, 0)))
