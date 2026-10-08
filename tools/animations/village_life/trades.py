"""Trades: three more work motions for each vanilla profession."""
from kit import clip

DAY = {"day": 2, "morning": 1.3}


@clip("polish_a_breastplate", "Polishes a breastplate", weight=4, require=["adult", "job:armorer"], boost=DAY, length=5.2)
def _(c):
    c.key(0.45, la=(-90, -26, 0), ra=(-90, -30, 0), head=(8, 0, 0), head_pos=(0, 0, -.6), lid=.6, look=(0, .3))
    c.key(0.9, la=(-60, -22, 0), ra=(-70, -24, 0), waist=(8, 0, 0), head=(18, 0, 0), head_pos=(0, 0, 0), lid=0,
          look=(0, .6))
    t = 1.05
    while t < 3.4:
        for pose in ((-82, -24, 0), (-72, -12, 4), (-60, -22, 0), (-72, -36, -2)):
            c.key(t, ra=pose)
            t += .19
    c.key(3.0, head=(18, -4, 0), look=(-.2, .6))
    c.key(3.85, la=(-98, -24, 0), ra=(-96, -28, 0), waist=(0, 0, 0), head=(2, 0, 9), lid=.3, look=(0, 0))
    c.key(4.45, la=(-96, -20, 0), ra=(-94, -24, 0), head=(4, 0, -6), lid=.2)


@clip("tap_rivets", "Taps in rivets", weight=4, require=["adult", "job:armorer"], avoid=["night"], boost=DAY,
      items="override", length=4.8)
def _(c):
    c.key(0.4, la=(-50, -18, 0), ra=(-72, -14, 4), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .7))
    for start, yaw, head_yaw, look_x in ((0.6, -14, 0, 0), (1.6, -24, -6, -.3), (2.6, -6, 5, .25)):
        c.key(start - .15, la=(-50, yaw - 6, 0), head=(22, head_yaw, 0), look=(look_x, .7))
        for i in range(3):
            c.key(start + i * .26, ra=(-86, yaw, 4))
            c.key(start + i * .26 + .13, ra=(-62, yaw, 4))
    c.key(3.55, la=(-86, -28, 0), ra=(-40, -10, 4), waist=(4, 0, 0), head=(8, -6, 7), lid=.35, look=(-.2, .2))
    c.key(4.2, la=(-84, -24, 0), head=(14, -4, 0), lid=.1)


@clip("quench_in_trough", "Quenches a piece in the trough", weight=4, require=["adult", "job:armorer"], avoid=["night"],
      boost=DAY, items="override", mirror="never", length=5.6)
def _(c):
    c.key(0.5, ra=(-60, -8, 0), la=(-60, -22, 0), waist=(14, 12, 0), head=(14, 14, 0), look=(.3, .5))
    c.key(1.1, ra=(-86, -8, 0), la=(-86, -22, 0), waist=(2, 8, 0), head=(6, 8, 0), lid=.3)
    c.key(1.7, ra=(-82, -8, 0), la=(-82, -22, 0), waist=(4, -22, 0), root=(0, -8, 0), head=(12, -18, 0), look=(-.3, .5))
    c.key(2.05, ra=(-34, -8, 0), la=(-34, -22, 0), waist=(26, -20, 0), head=(24, -16, 0), root_pos=(0, .3, 0), lid=.2)
    c.key(2.4, ra=(-44, -8, 0), la=(-44, -22, 0), waist=(-8, -14, 0), head=(-14, 2, -9), root_pos=(0, 0, 0), lid=.85,
          look=(.3, 0))
    c.wobble(2.5, 3.3, 4, "la", 10, base=(-112, -34, 0), axis=1)
    c.key(3.3, head=(-12, 6, -10), waist=(-6, -14, 0), lid=.8)
    c.key(3.75, ra=(-88, -8, 0), la=(-88, -22, 0), waist=(2, -10, 0), head=(10, -8, 0), lid=0, look=(0, .3))
    c.key(4.4, ra=(-90, -8, 0), la=(-90, -22, 0), head=(8, -6, 8), root=(0, -6, 0))


@clip("turn_the_grindstone", "Grinds a blade on the treadle wheel", weight=4, require=["adult", "job:toolsmith"],
      avoid=["night"], boost=DAY, length=5.4)
def _(c):
    c.key(0.45, ra=(-64, -16, 0), la=(-64, -26, 0), waist=(12, 0, 0), head=(20, 0, 0), look=(0, .6))
    c.cycle(0.6, 3.6, .7, dict(rl=(-22, 0, 2)), dict(rl=(-3, 0, 2)), end_on="b")
    c.cycle(0.8, 3.4, 1.3, dict(ra=(-66, -10, 0), la=(-66, -20, 0)), dict(ra=(-61, -22, 0), la=(-61, -32, 0)))
    c.key(1.8, head=(22, -3, 0), lid=.35)
    c.key(3.0, head=(20, 3, 0), lid=.3)
    c.key(3.95, ra=(-104, -26, 0), la=(-24, 0, 6), waist=(0, 0, 0), head=(0, -6, 8), lid=.5, look=(-.2, 0))
    c.key(4.6, ra=(-100, -30, 0), head=(2, -6, -6), lid=.4)


@clip("file_an_edge", "Files an edge", weight=4, require=["adult", "job:toolsmith"], boost=DAY, items="override",
      mirror="never", length=5.0)
def _(c):
    c.key(0.4, ra=(-46, -24, 0), la=(-50, -16, 0), waist=(10, 0, 0), head=(22, 0, 0), look=(0, .7))
    for push in (0.7, 1.45, 2.2, 2.95):
        c.key(push, ra=(-46, -24, 0), la=(-50, -16, 0), waist=(10, 0, 0), root_pos=(0, 0, 0))
        c.key(push + .35, ra=(-72, -16, 0), la=(-76, -8, 0), waist=(20, 0, 0), root_pos=(0, 0, -.35))
    c.rest(3.35, "head_pos", "lid")
    c.key(3.7, ra=(-50, -24, 0), la=(-54, -16, 0), waist=(12, 0, 0), root_pos=(0, 0, 0), head=(16, 0, 0),
          head_pos=(0, .4, -.6), lid=.7)
    c.key(4.05, ra=(-58, -42, 0), la=(-60, -26, 0), head=(24, -4, 3), head_pos=(0, 0, 0), lid=.1, look=(-.2, .8))
    c.key(4.5, ra=(-60, -14, 0), head=(24, 3, 3), look=(.2, .8))


@clip("test_tool_heft", "Tests a tool's heft", weight=3, require=["adult", "job:toolsmith"], boost=DAY, items="override",
      length=5.0)
def _(c):
    c.key(0.4, ra=(-40, 0, 6), head=(12, 2, 0), look=(.1, .4))
    c.cycle(0.55, 1.4, .34, dict(ra=(-48, 0, 6)), dict(ra=(-34, 0, 6)))
    c.key(1.7, ra=(-124, 4, 8), la=(-16, 0, 12), waist=(-4, 6, 0), head=(4, 0, 0), look=(0, .2))
    c.key(1.95, ra=(-42, -14, 4), waist=(10, -4, 0), head=(12, 0, 0))
    c.key(2.4, ra=(-120, 4, 8), waist=(-4, 6, 0), head=(4, 0, 0))
    c.key(2.65, ra=(-42, -14, 4), waist=(10, -4, 0), head=(12, 0, 0))
    c.rest(2.7, "lid")
    c.key(3.1, ra=(-100, -34, 0), la=(-94, -20, 0), waist=(0, 0, 0), head=(4, -6, 0), lid=.3, look=(-.2, .1))
    c.wobble(3.2, 3.9, 2, "ra", 12, base=(-100, -34, 0), axis=2)
    c.key(4.15, head=(14, -4, 0), lid=0)
    c.key(4.45, ra=(-60, -10, 4), la=(-20, 0, 6), head=(4, 0, 0))


@clip("sight_down_a_blade", "Sights down a blade", weight=4, require=["adult", "job:weaponsmith"], boost=DAY, length=5.0)
def _(c):
    c.key(0.5, ra=(-104, -32, 0), head=(-16, 0, 6), lid=.5, look=(0, -.6))
    c.key(1.2, ra=(-104, -30, 14), head=(-18, 3, -5), look=(.15, -.65))
    c.key(1.7, ra=(-104, -34, -10), head=(-16, -2, 7))
    c.rest(1.8, "la", "waist")
    c.key(2.3, ra=(-94, -16, 0), la=(-96, -4, 0), head=(4, -6, 12), waist=(4, 0, 0), lid=.55, look=(.3, 0))
    c.key(3.1, head=(5, -8, 14), waist=(6, 0, 0), root_pos=(0, .2, 0))
    c.key(3.7, ra=(-62, -30, 0), la=(-60, -30, 0), waist=(2, 0, 0), head=(16, 0, 0), root_pos=(0, 0, 0), lid=0,
          look=(0, .5))
    c.key(4.0, head=(8, 0, 0))
    c.key(4.3, head=(16, 0, 0))


@clip("whetstone_strokes", "Whets a blade", weight=4, require=["adult", "job:weaponsmith"], boost=DAY, length=4.8)
def _(c):
    c.key(0.4, la=(-72, -18, 0), ra=(-58, -36, 0), head=(18, -4, 0), look=(-.1, .5))
    for i, t in enumerate((0.6, 1.15, 1.7, 2.25, 2.8)):
        c.key(t, ra=(-60, -38 if i % 2 else -32, 0), head=(20, -5, 0), look=(-.15, .55))
        c.key(t + .26, ra=(-104, -2 if i % 2 else -14, 10), head=(14, 2, 0), look=(.1, .3))
    c.key(3.45, ra=(-76, -44, 0), head=(22, -6, 0), lid=.3, look=(-.2, .7))
    c.key(3.85, ra=(-82, -28, 0), head=(16, -3, 0), lid=.1)
    c.key(4.25, la=(-70, -18, 0), head=(20, -3, 0))


@clip("pump_the_bellows", "Pumps the bellows", weight=4, require=["adult", "job:weaponsmith"], boost=DAY, mirror="never",
      length=5.4)
def _(c):
    c.key(0.45, ra=(-84, -18, 0), la=(-84, -18, 0), head=(8, 8, 0), look=(.3, .3))
    c.cycle(0.65, 3.65, 1.0,
            dict(ra=(-88, -18, 0), la=(-88, -18, 0), waist=(-4, 0, 0), root_pos=(0, 0, 0), head=(6, 8, 0)),
            dict(ra=(-40, -18, 0), la=(-40, -18, 0), waist=(22, 0, 0), root_pos=(0, .4, 0), head=(16, 8, 0)))
    c.rest(3.65, "lid")
    c.key(4.1, ra=(-20, 0, 8), la=(-20, 0, 8), waist=(6, 14, 0), root_pos=(0, 0, 0), head=(14, 20, 0), lid=.45,
          look=(.5, .4))
    c.key(4.7, head=(12, 22, 7), lid=.4)


@clip("chisel_stone", "Chisels stone", weight=4, require=["adult", "job:mason"], avoid=["night"], boost=DAY,
      items="override", length=5.0)
def _(c):
    c.key(0.45, la=(-58, -18, 0), ra=(-96, -14, 4), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .7))
    for start, taps, yaw in ((0.7, 4, -16), (2.35, 3, -26)):
        for i in range(taps):
            c.key(start + i * .32, ra=(-106, yaw + 2, 4))
            c.key(start + i * .32 + .2, ra=(-64, yaw, 4), root_pos=(0, .15, 0))
            c.key(start + i * .32 + .28, root_pos=(0, 0, 0))
    c.key(2.15, la=(-56, -28, 0), head=(22, -4, 0), look=(-.2, .7))
    c.rest(3.4, "head_pos", "lid")
    c.key(3.65, ra=(-62, -26, 4), head=(18, -2, 0), head_pos=(0, .4, -.8), lid=.8)
    c.key(4.0, ra=(-62, -42, 0), head_pos=(0, 0, 0), lid=0)
    c.key(4.35, ra=(-60, -4, 4), head=(22, 2, 0), look=(.2, .7))


@clip("lay_a_brick", "Trowels mortar and sets a brick", weight=4, require=["adult", "job:mason"], avoid=["night"],
      boost=DAY, items="override", length=5.6)
def _(c):
    c.key(0.5, ra=(-28, 18, 10), la=(-20, 0, 6), waist=(24, 10, 0), head=(24, 8, 0), look=(.3, .7))
    c.key(0.85, ra=(-62, -10, 0), waist=(12, 0, 0), head=(22, 0, 0), look=(0, .7))
    c.key(1.1, ra=(-56, -38, 0), look=(-.3, .7))
    c.key(1.4, ra=(-58, 6, 6), look=(.3, .7))
    c.key(1.7, ra=(-56, -34, 0), look=(-.2, .7))
    c.key(2.1, la=(-40, -10, 10), ra=(-30, 0, 6), waist=(16, -12, 0), head=(20, -10, 0), look=(-.3, .6))
    c.key(2.6, la=(-58, -24, 0), ra=(-60, -22, 0), waist=(16, 0, 0), head=(24, 0, 0), look=(0, .7))
    c.cycle(2.85, 3.35, .25, dict(ra=(-80, -24, 0)), dict(ra=(-60, -24, 0)), end_on="b")
    c.key(3.6, ra=(-58, -40, 0), la=(-30, 0, 6))
    c.key(3.9, ra=(-58, 0, 4))
    c.key(4.35, ra=(-30, 0, 6), la=(-10, 0, 8), waist=(-2, 0, 0), head=(8, 0, 6), lid=.3, look=(0, .3))
    c.key(4.95, head=(8, 4, -4))


@clip("check_plumb_line", "Checks a plumb line", weight=3, require=["adult", "job:mason"], boost=DAY, length=5.2)
def _(c):
    c.key(0.5, ra=(-130, -12, 0), head=(-6, 0, 0), look=(0, -.3))
    c.key(1.0, ra=(-128, -10, 0), head=(-2, -6, 10), lid=.55, look=(-.2, -.1))
    c.wobble(1.1, 2.3, 2, "ra", 3, base=(-128, -10, 0), axis=1, decay=.6)
    c.key(2.7, waist=(0, -4, -6), head=(0, -8, 14), lid=.6)
    c.key(3.35, waist=(0, 0, 0), head=(8, -4, 4), lid=0, look=(0, .2))
    c.rest(3.4, "la")
    c.key(3.8, ra=(-62, -30, 0), la=(-60, -30, 0), head=(16, 0, 0), look=(0, .6))
    c.cycle(3.9, 4.5, .3, dict(ra=(-70, -24, 0)), dict(ra=(-58, -34, 0)))


@clip("broadcast_seeds", "Broadcasts seed", weight=4, require=["adult", "job:farmer"], avoid=["night"], boost=DAY,
      length=5.2)
def _(c):
    c.key(0.4, la=(-30, -30, 0))
    for t in (0.5, 1.7, 2.9):
        c.key(t, ra=(-30, -48, 0), waist=(6, -14, 0), head=(10, -8, 0), look=(-.2, .4))
        c.key(t + .45, ra=(-78, 40, 34), waist=(-2, 16, 0), head=(2, 18, 0), look=(.4, 0))
        c.key(t + .8, ra=(-62, 42, 40), waist=(0, 14, 0))
    c.key(4.0, la=(-30, -30, 0))
    c.key(4.15, ra=(-146, -50, 0), waist=(-2, 8, 0), head=(-4, 12, 0), look=(.3, 0))
    c.key(4.7, ra=(-146, -50, 0), head=(-4, 4, 0), look=(.1, 0))


@clip("harvest_with_sickle", "Harvests with a sickle", weight=4, require=["adult", "job:farmer"], avoid=["night"],
      boost=DAY, items="override", length=5.4)
def _(c):
    c.key(0.5, waist=(34, 0, 0), head=(6, 0, 0), la=(-56, -12, 0), ra=(-50, 30, 16), look=(0, .6))
    for t in (0.95, 1.85, 2.75):
        c.key(t - .25, la=(-62, -8, 0), ra=(-48, 36, 20), waist=(32, 10, 0))
        c.key(t, ra=(-56, -40, 0), waist=(36, -10, 0), root_pos=(0, .15, 0))
        c.key(t + .3, la=(-74, -20, 0), root_pos=(0, 0, 0))
    c.key(3.75, waist=(-8, 0, 0), ra=(26, 0, -10), la=(-60, -20, 0), head=(-10, 0, 0), lid=.5, look=(0, 0))
    c.key(4.45, waist=(-4, 0, 0), head=(-4, 14, 0), lid=0, look=(.4, 0))


@clip("hoist_a_sack", "Hoists a sack onto the shoulder", weight=4, require=["adult", "job:farmer"], avoid=["night"],
      boost=DAY, length=5.8)
def _(c):
    c.key(0.6, waist=(52, 0, 0), head=(6, 0, 0), ra=(-50, -8, 8), la=(-50, -8, 8), root_pos=(0, .3, 0), look=(0, .5))
    c.key(1.05, ra=(-46, -12, 6), la=(-46, -12, 6), lid=.4)
    c.key(1.6, waist=(8, 0, 0), ra=(-100, -30, 0), la=(-100, -30, 0), head=(-6, 0, 0), root_pos=(0, -.4, 0), lid=.6)
    c.key(2.0, ra=(-166, -4, 6), la=(-118, -60, 0), waist=(0, 0, 0), head=(4, -8, 12), root=(0, 0, 3),
          root_pos=(0, 0, 0), lid=.2)
    c.key(2.35, root_pos=(0, .35, 0))
    c.key(2.6, root_pos=(0, 0, 0))
    c.cycle(3.0, 3.7, .35, dict(la=(-126, -62, 0)), dict(la=(-112, -56, 0)))
    c.key(3.9, ra=(-166, -4, 6), head=(2, -6, 10), root=(0, 0, 3))
    c.key(4.4, ra=(-96, -28, 0), la=(-96, -28, 0), waist=(10, 0, 0), head=(6, 0, 0), root=(0, 0, 0))
    c.key(4.95, ra=(-54, -10, 6), la=(-54, -10, 6), waist=(34, 0, 0), head=(10, 0, 0), lid=0)


@clip("mend_a_net", "Mends a net", weight=4, require=["adult", "job:fisherman"], boost=DAY, mirror="never", length=5.4)
def _(c):
    c.key(0.45, ra=(-74, -36, 0), la=(-74, -36, 0), head=(22, 0, 0), look=(0, .7))
    for t, pitch, head in ((0.7, -74, 22), (1.9, -66, 26), (3.1, -82, 18)):
        c.key(t, ra=(pitch, -36, 0), la=(pitch, -36, 0), head=(head, 0, 0))
        c.wobble(t + .05, t + .6, 5, "ra", 6, base=(pitch, -36, 0))
        c.wobble(t + .05, t + .6, 4, "la", 4, base=(pitch, -36, 0), axis=1)
        c.key(t + .78, ra=(pitch + 4, 8, 14), la=(pitch + 4, 8, 14), head=(head - 4, 0, 0))
        c.key(t + 1.0, ra=(pitch, -36, 0), la=(pitch, -36, 0))
    c.key(4.3, ra=(-104, 4, 12), la=(-104, 4, 12), head=(-4, 0, 0), lid=.3, look=(0, -.1))
    c.key(4.8, head=(-4, 6, 4), look=(.2, -.1))


@clip("reel_in_a_catch", "Reels in a catch", weight=4, require=["adult", "job:fisherman"], length=6.0)
def _(c):
    c.key(0.45, la=(-112, -14, 0), ra=(-70, -30, 0), head=(6, 0, 0), look=(0, -.2))
    crank = [(-76, -30, 0), (-70, -22, 4), (-64, -30, 0), (-70, -38, -2)]
    t = 0.6
    while t < 1.7:
        for pose in crank:
            c.key(t, ra=pose)
            t += .12
    c.rest(1.75, "waist", "root_pos")
    c.key(1.95, la=(-88, -14, 0), waist=(12, 0, 0), root_pos=(0, 0, -.5), head=(14, 0, 0), look=(0, .2))
    c.key(2.3, la=(-130, -10, 0), waist=(-10, 0, 0), root_pos=(0, 0, .4), head=(-6, 0, 0), look=(0, -.4))
    c.cycle(2.5, 3.9, .5, dict(root=(0, 0, 3), la=(-126, -6, 0)), dict(root=(0, 0, -3), la=(-134, -16, 0)))
    t = 2.45
    while t < 3.8:
        for pose in crank:
            c.key(t, ra=pose)
            t += .08
    c.rest(4.2, "lid")
    c.key(4.15, la=(-150, -6, 0), ra=(-140, -12, 0), waist=(-6, 0, 0), root_pos=(0, 0, 0), head=(-14, 4, 0),
          look=(.2, -.6))
    c.key(4.7, la=(-56, -10, 0), ra=(-108, -22, 0), waist=(0, 0, 0), head=(2, 0, 8), lid=.35, look=(0, 0))
    c.key(5.2, head=(2, 0, -6), lid=.3)


@clip("untangle_a_line", "Untangles a line", weight=3, require=["adult", "job:fisherman"], mirror="never", length=5.0)
def _(c):
    c.key(0.45, ra=(-80, -38, 0), la=(-80, -38, 0), head=(22, 0, 0), look=(0, .7))
    c.wobble(0.6, 1.5, 5, "ra", 5, base=(-80, -38, 0))
    c.wobble(0.6, 1.5, 4, "la", 5, base=(-80, -38, 0), axis=1)
    c.rest(1.5, "lid")
    c.key(1.75, ra=(-130, -20, 0), head=(4, 0, 6), lid=.3, look=(.2, -.3))
    c.wobble(2.0, 2.6, 5, "ra", 10, base=(-128, -20, 0), axis=1)
    c.key(2.6, head=(4, 0, -6))
    c.key(2.9, ra=(-96, -36, 0), la=(-96, -32, 0), head=(14, 0, 0), lid=.45, look=(0, .4))
    c.wobble(3.0, 3.6, 5, "ra", 4, base=(-96, -36, 0))
    c.rest(3.6, "root_pos")
    c.key(3.85, ra=(-80, 14, 16), la=(-80, 14, 16), head=(-6, 0, 0), lid=0, look=(0, 0), root_pos=(0, -.4, 0))
    c.key(4.3, ra=(-56, 0, 10), la=(-56, 0, 10), head=(4, 0, 0), lid=.45, root_pos=(0, 0, 0))


@clip("shear_a_sheep", "Shears a sheep", weight=4, require=["adult", "job:shepherd"], avoid=["night", "rain"], boost=DAY,
      items="override", length=5.4)
def _(c):
    c.key(0.6, waist=(40, 0, 0), head=(8, 0, 0), la=(-58, -14, 0), ra=(-56, -26, 0), look=(0, .6))
    t, i = 0.8, 0
    while t < 3.3:
        c.key(t, ra=(-56 + (5 if i % 2 else -5), -26 + i * 1.3, 0))
        t, i = t + .18, i + 1
    c.key(2.1, la=(-60, -4, 4), waist=(42, 8, 0), head=(8, 4, 0), look=(.2, .6))
    c.key(3.2, la=(-58, 2, 6), waist=(40, 12, 0))
    c.key(3.75, waist=(2, 0, 0), la=(-104, -24, 0), ra=(-30, 0, 8), head=(0, -4, 0), lid=.2, look=(-.2, 0))
    c.key(4.4, head=(2, -6, 8), lid=.3)


@clip("call_the_flock", "Calls the flock", weight=4, require=["adult", "job:shepherd"], avoid=["night"], mirror="never",
      length=4.8)
def _(c):
    c.key(0.4, head=(-4, 0, 0), waist=(-4, 0, 0), root_pos=(0, -.2, 0))
    c.key(0.7, ra=(-112, -40, 0), la=(-112, -40, 0), head=(-10, 0, 0), waist=(4, 0, 0), root_pos=(0, 0, 0))
    for t in (0.95, 1.6):
        c.key(t, head=(-15, 0, 0), waist=(9, 0, 0))
        c.key(t + .35, head=(-8, 0, 0), waist=(2, 0, 0))
    c.key(2.35, waist=(4, 18, 0), head=(-12, 10, 0), look=(.3, 0))
    c.key(2.65, head=(-16, 10, 0), waist=(9, 18, 0))
    c.key(3.0, head=(-9, 10, 0), waist=(2, 18, 0))
    c.key(3.5, ra=(-146, -50, 0), la=(0, 0, 0), waist=(0, 8, 0), head=(-4, 14, 0), lid=.3, look=(.4, 0))
    c.key(4.2, head=(-4, 18, 0), lid=.25)


@clip("lean_on_crook", "Leans on a crook", weight=3, require=["adult", "job:shepherd"], mirror="never", blend=(.5, .6),
      length=6.4)
def _(c):
    c.key(0.7, ra=(-58, -34, 0), la=(-62, -30, 0), root=(4, 0, 0), head=(-2, 0, 0), lid=.3)
    c.cycle(1.0, 5.0, 2.0, dict(root=(4, 0, 2), head=(-2, 6, -3)), dict(root=(4, 0, -2), head=(-2, -6, 3)))
    c.key(1.5, look=(.4, 0)).key(3.0, look=(-.4, 0)).key(4.4, look=(0, 0))
    c.key(3.3, rl=(0, 6, 4)).key(5.2, rl=(0, 6, 4))
    c.key(5.2, ra=(-58, -34, 0), la=(-62, -30, 0), head=(8, 0, 0), lid=.5)
    c.key(5.55, head=(-2, 0, 0))


@clip("stretch_a_hide", "Stretches a hide", weight=4, require=["adult", "job:leatherworker"], boost=DAY, mirror="never",
      length=5.0)
def _(c):
    c.key(0.45, ra=(-70, -26, 0), la=(-70, -26, 0), head=(16, 0, 0), look=(0, .5))
    c.cycle(0.9, 1.9, .4, dict(ra=(-70, 32, 24), la=(-70, 32, 24), waist=(-6, 0, 0), root_pos=(0, 0, .3), lid=.4),
            dict(ra=(-70, 22, 18), la=(-70, 22, 18), waist=(-3, 0, 0), root_pos=(0, 0, .1), lid=.3))
    c.key(2.2, ra=(-96, -20, 0), la=(-96, -20, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(6, 0, 0), lid=0)
    c.cycle(2.6, 3.4, .4, dict(ra=(-96, 30, 22), la=(-96, 30, 22), waist=(-8, 0, 0), lid=.45),
            dict(ra=(-96, 22, 16), la=(-96, 22, 16), waist=(-4, 0, 0), lid=.35))
    c.key(3.75, ra=(-60, 20, 16), la=(-60, 20, 16), waist=(4, 0, 0), head=(18, 0, 0), lid=0, look=(0, .6))
    c.key(4.3, ra=(-60, -30, 0), head=(18, -4, 0), look=(-.2, .6))


@clip("punch_with_awl", "Punches holes with an awl", weight=4, require=["adult", "job:leatherworker"], boost=DAY,
      items="override", length=5.2)
def _(c):
    c.key(0.45, la=(-50, -20, 0), ra=(-84, -30, 0), waist=(14, 0, 0), head=(24, 0, 0), look=(-.2, .8))
    for t, yaw, lx in ((0.7, -30, -.2), (1.5, -22, -.07), (2.3, -14, .07), (3.1, -6, .2)):
        c.key(t, ra=(-84, yaw, 0), look=(lx, .8))
        c.key(t + .25, ra=(-58, yaw, 0), waist=(20, 0, 0), root_pos=(0, .35, 0), lid=.3)
        c.key(t + .42, ra=(-58, yaw, 8))
        c.key(t + .52, ra=(-58, yaw, -6))
        c.key(t + .7, ra=(-84, yaw, 0), waist=(14, 0, 0), root_pos=(0, 0, 0), lid=0)
    c.key(3.95, la=(-96, -26, 0), ra=(-40, -10, 4), waist=(4, 0, 0), head=(6, -6, 0), lid=.35, look=(-.2, 0))
    c.key(4.5, head=(8, -2, 8))


@clip("burnish_an_edge", "Burnishes an edge", weight=4, require=["adult", "job:leatherworker"], boost=DAY, length=4.4)
def _(c):
    c.key(0.4, la=(-62, -20, 0), ra=(-64, -30, 0), waist=(6, 0, 0), head=(22, 0, 0), look=(0, .7))
    c.wobble(0.55, 2.0, 6, "ra", 14, base=(-64, -30, 0), axis=1)
    c.rest(2.0, "head_pos", "lid")
    c.key(2.2, head=(16, 0, 0), head_pos=(0, .3, -.7), lid=.7)
    c.key(2.5, head=(22, 0, 0), head_pos=(0, 0, 0), lid=0)
    c.wobble(2.55, 3.4, 6, "ra", 14, base=(-64, -30, 0), axis=1)
    c.key(3.6, ra=(-66, -44, 0), head=(24, -3, 4), lid=.2, look=(-.2, .8))
    c.key(3.95, ra=(-66, -14, 0), head=(24, 3, 4), look=(.2, .8))


@clip("hone_on_a_steel", "Hones a knife on a steel", weight=4, require=["adult", "job:butcher"], boost=DAY, length=5.0)
def _(c):
    c.key(0.4, la=(-72, -30, 0), ra=(-96, -8, 8), waist=(4, 0, 0), head=(16, -4, 0), look=(-.1, .5))
    for i, t in enumerate((0.6, 0.98, 1.36, 1.74, 2.12, 2.5)):
        far = i % 2 == 0
        c.key(t, ra=(-106, -8 if far else -24, 12 if far else 0), head=(15, -3, 0))
        c.key(t + .22, ra=(-66, -36 if far else -46, 4 if far else -4), head=(18, -5, 0))
    c.wobble(0.6, 2.75, 3, "la", 3, base=(-72, -30, 0))
    c.rest(2.8, "lid")
    c.key(3.15, ra=(-120, -26, 0), la=(-20, 0, 6), waist=(0, 0, 0), head=(-4, -6, 9), lid=.5, look=(-.2, -.3))
    c.key(3.6, ra=(-118, -30, 6), head=(-4, -8, -6), look=(-.3, -.3))
    c.key(4.0, la=(-100, -40, 0), ra=(-98, -26, 0), head=(10, -4, 0), lid=.2, look=(-.1, .4))
    c.wobble(4.05, 4.4, 4, "la", 4, base=(-100, -40, 0), axis=1)
    c.key(4.55, ra=(-70, -20, 0), head=(6, 0, 6), lid=0)


@clip("cleave_a_joint", "Cleaves a joint", weight=4, require=["adult", "job:butcher"], avoid=["night"], boost=DAY,
      items="override", length=5.4)
def _(c):
    c.key(0.4, la=(-50, -14, 0), ra=(-62, -12, 0), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .7))
    for up, hit in ((0.85, 1.05), (1.85, 2.05), (2.7, 2.88)):
        c.key(up, ra=(-172, -8, 6), waist=(-2, 0, 0), head=(14, 0, 0), root_pos=(0, -.25, 0), lid=0)
        c.key(hit, ra=(-46, -12, 0), waist=(24, 0, 0), head=(24, 0, 0), root_pos=(0, .5, 0), lid=.45)
        c.key(hit + .22, ra=(-52, -12, 0), waist=(18, 0, 0), root_pos=(0, .15, 0), lid=0)
    c.wobble(3.1, 3.4, 4, "ra", 6, base=(-52, -12, 0))
    c.key(3.6, la=(-86, -22, 0), ra=(-40, -10, 4), waist=(8, 0, 0), root_pos=(0, 0, 0), head=(12, -6, 6), look=(-.2, .4))
    c.key(4.0, la=(-86, -30, -10), head=(12, -8, -6), look=(-.3, .4))
    c.key(4.4, la=(-30, 0, 6), ra=(-16, -26, 0), waist=(2, 0, 0), head=(8, 0, 0), look=(0, .2))
    c.key(4.75, ra=(-12, 4, 10), head=(6, 0, 5))


@clip("wrap_a_parcel", "Wraps and ties a parcel", weight=3, require=["adult", "job:butcher"], boost=DAY, mirror="never",
      length=5.6)
def _(c):
    c.key(0.4, ra=(-60, -24, 0), la=(-60, -24, 0), waist=(10, 0, 0), head=(22, 0, 0), look=(0, .7))
    c.key(0.75, ra=(-50, 22, 14), look=(.3, .7))
    c.key(1.1, ra=(-72, -42, 0), look=(-.1, .7))
    c.key(1.3, ra=(-62, -30, 0))
    c.key(1.55, la=(-50, 22, 14), look=(-.3, .7))
    c.key(1.9, la=(-72, -42, 0), look=(.1, .7))
    c.key(2.1, la=(-62, -30, 0), root_pos=(0, 0, 0))
    c.key(2.25, ra=(-58, -28, 0), la=(-58, -28, 0), root_pos=(0, .25, 0), look=(0, .7))
    c.key(2.45, ra=(-70, -36, 0), la=(-70, -36, 0), root_pos=(0, 0, 0))
    c.cycle(2.6, 3.3, .35, dict(ra=(-80, -38, 0), la=(-62, -34, 0)), dict(ra=(-62, -34, 0), la=(-80, -38, 0)))
    c.key(3.5, ra=(-68, 22, 16), la=(-68, 22, 16), waist=(6, 0, 0), head=(18, 0, 0), lid=.35)
    c.key(3.65, ra=(-68, 8, 8), la=(-68, 8, 8), lid=.1)
    c.key(3.85, ra=(-68, 26, 18), la=(-68, 26, 18), lid=.4)
    c.key(4.15, ra=(-62, -24, 0), la=(-62, -24, 0), waist=(10, 0, 0), head=(20, 0, 0), lid=0)
    c.key(4.3, ra=(-50, -24, 0), la=(-50, -24, 0))
    c.key(4.45, ra=(-62, -24, 0), la=(-62, -24, 0))
    c.key(4.6, ra=(-50, -24, 0), la=(-50, -24, 0))
    c.key(4.9, head=(6, 0, 6), look=(0, 0), lid=.2)


@clip("unroll_a_map", "Unrolls a map and studies it", weight=4, require=["adult", "job:cartographer"], boost=DAY,
      mirror="never", length=6.2)
def _(c):
    c.key(0.4, ra=(-76, -42, 0), la=(-76, -42, 0), head=(14, 0, 0), look=(0, .5))
    c.key(0.9, ra=(-70, 26, 20), la=(-70, 26, 20), waist=(4, 0, 0), head=(18, 0, 0), lid=.2)
    c.key(1.15, ra=(-66, 30, 24), la=(-66, 30, 24))
    c.key(1.7, head=(20, -14, 0), look=(-.5, .6))
    c.key(2.5, head=(22, 12, 0), look=(.5, .7))
    c.key(3.1, head=(18, 4, 0), look=(.2, .4), lid=.2)
    c.key(3.5, ra=(-66, 30, 24), waist=(10, 0, 0), head=(24, 6, 0), lid=.45, look=(.2, .7))
    c.key(3.75, ra=(-60, -12, 0))
    c.key(3.9, ra=(-52, -12, 0))
    c.key(4.05, ra=(-60, -12, 0))
    c.key(4.2, ra=(-52, -12, 0))
    c.key(4.5, ra=(-66, 30, 24), waist=(4, 0, 0), head=(10, 0, 0), lid=0, look=(0, .3))
    c.key(4.75, head=(16, 0, 0))
    c.key(5.4, ra=(-76, -42, 0), la=(-76, -42, 0), waist=(0, 0, 0), head=(10, 0, 0), look=(0, .4))


@clip("walk_the_dividers", "Walks dividers across a chart", weight=4, require=["adult", "job:cartographer"], boost=DAY,
      length=5.4)
def _(c):
    c.key(0.45, la=(-50, -8, 6), ra=(-62, 6, 6), waist=(14, 0, 0), head=(24, 2, 0), look=(.3, .8))
    yaw, t = 6, 0.7
    for i in range(6):
        c.key(t, ra=(-70, yaw - 4, 8 if i % 2 else -8))
        yaw -= 9
        c.key(t + .18, ra=(-60, yaw, 0), head=(24, yaw * .3, 0), look=(yaw / 70 + .2, .8))
        t += .38
    c.key(3.2, la=(-104, -42, 0), waist=(4, 0, 0), head=(2, -6, 6), lid=.4, look=(.2, -.3))
    c.key(3.6, head=(2, -6, -4), look=(-.2, -.3))
    c.key(4.0, la=(-50, -8, 6), ra=(-60, -30, 0), waist=(14, 0, 0), head=(22, -4, 0), lid=0, look=(-.1, .7))
    c.wobble(4.05, 4.65, 6, "ra", 5, base=(-60, -30, 0), axis=1)


@clip("take_a_bearing", "Takes a compass bearing", weight=4, require=["adult", "job:cartographer"], avoid=["night"],
      boost=DAY, mirror="free", length=6.4)
def _(c):
    c.key(0.45, ra=(-64, -34, 0), la=(-64, -34, 0), head=(22, 0, 0), look=(0, .7))
    c.key(1.0, root=(0, -6, 0), head=(24, 0, 0))
    c.key(2.2, root=(0, -26, 0), head=(20, 2, 0), lid=.3)
    c.key(2.6, head=(-2, 4, 0), look=(.1, -.1), lid=.35)
    c.key(3.1, head=(-2, 8, 0), look=(.3, -.1))
    c.key(3.45, head=(22, 0, 0), look=(0, .7), lid=0)
    c.key(3.9, root=(0, -32, 0), head=(23, 0, 0))
    c.key(4.3, ra=(-90, 6, 0), la=(-60, -32, 0), head=(-2, 4, 0), look=(.1, 0))
    c.key(4.8, ra=(-90, 6, 0), head=(4, 4, 6), lid=.25)
    c.key(5.3, ra=(-64, -34, 0), root=(0, -16, 0), head=(14, 0, 0), lid=0, look=(0, .5))


@clip("shelve_a_book_high", "Shelves a book up high", weight=4, require=["adult", "job:librarian"], boost=DAY, length=5.6)
def _(c):
    c.key(0.4, ra=(-62, -30, 0), head=(-10, 0, 0), look=(0, -.4))
    c.key(0.9, ra=(-150, -8, 4), la=(-110, 8, 8), head=(-22, 0, 0), waist=(-4, 0, 0), root_pos=(0, -.8, 0), look=(0, -.7))
    c.key(1.3, ra=(-162, -4, 4), root_pos=(0, -1.1, -.2), lid=.3)
    c.key(1.6, ra=(-168, -4, 4), la=(-114, 8, 8), root_pos=(0, -1.2, -.4))
    c.key(1.8, ra=(-160, -4, 4), root_pos=(0, -1.1, -.3))
    c.key(1.95, ra=(-169, -4, 4), root_pos=(0, -1.2, -.45))
    c.key(2.4, ra=(-120, 4, 8), la=(-40, 0, 6), waist=(-2, 0, 0), root_pos=(0, 0, 0), head=(-18, 0, 0), lid=0)
    c.key(2.9, ra=(-108, 4, 8), head=(-16, -12, 0), look=(-.5, -.6))
    c.key(3.7, head=(-16, 12, 0), look=(.5, -.6))
    c.key(4.2, ra=(-40, 0, 8), la=(-10, 0, 6), waist=(0, 0, 0), head=(-12, 2, 6), lid=.25, look=(.1, -.5))
    c.key(4.55, head=(-4, 0, 6))
    c.key(4.8, head=(2, 0, 0), lid=0, look=(0, 0))


@clip("dust_the_shelves", "Dusts the shelves", weight=4, require=["adult", "job:librarian"], boost=DAY, length=6.0)
def _(c):
    c.key(0.4, ra=(-136, 12, 10), head=(-14, 6, 0), look=(.2, -.5))
    c.wobble(0.5, 1.4, 5, "ra", 16, base=(-136, 12, 10), axis=1)
    c.key(1.7, ra=(-100, 4, 8), head=(-2, 2, 0), look=(.1, 0))
    c.wobble(1.8, 2.6, 5, "ra", 16, base=(-100, 4, 8), axis=1)
    c.key(2.9, ra=(-70, 6, 8), waist=(22, 0, 0), head=(14, 4, 0), look=(.1, .5))
    c.wobble(3.0, 3.6, 5, "ra", 14, base=(-70, 6, 8), axis=1)
    c.key(3.9, ra=(-60, 0, 8), la=(-20, 0, 6), waist=(-6, 0, 0), head=(-18, 0, 0), lid=.6, look=(0, -.3))
    c.key(4.15, ra=(-56, 0, 8), la=(-104, -40, 0), waist=(-10, 0, 0), head=(-24, 0, 0), lid=.85)
    c.key(4.3, waist=(20, 0, 0), head=(24, 0, 0), root_pos=(0, .3, 0), lid=1)
    c.key(4.6, ra=(-40, 0, 8), la=(-108, -42, 0), waist=(6, 0, 0), head=(8, 0, 0), root_pos=(0, 0, 0), lid=.4)
    c.wobble(4.7, 5.2, 4, "head", 8, base=(8, 0, 0), axis=1)
    c.key(5.4, la=(-30, 0, 6), lid=.2)


@clip("sort_a_stack", "Sorts a stack of books", weight=3, require=["adult", "job:librarian"], boost=DAY, mirror="free",
      length=6.0)
def _(c):
    for t, lean in ((0.4, 0), (2.0, 4), (3.5, 0)):
        c.key(t + .1, ra=(-50, -16, 0), la=(-50, -16, 0), waist=(16, 20, 0), head=(18, 14, 0), root_pos=(0, .2, 0),
              lid=0, look=(.4, .6))
        c.key(t + .45, ra=(-84, -32, 0), la=(-84, -32, 0), waist=(4, 0, 0), head=(14, 0, lean), root_pos=(0, 0, 0),
              lid=.3, look=(0, .5))
        c.key(t + .9, waist=(4, 0, 0), head=(16, 0, -lean))
        c.key(t + 1.25, ra=(-50, -16, 0), la=(-50, -16, 0), waist=(16, -20, 0), head=(18, -14, 0), root_pos=(0, .2, 0),
              lid=0, look=(-.4, .6))
    c.key(2.9, head=(12, -6, 8), lid=.5, look=(-.2, .3))
    c.key(5.0, ra=(-56, 22, 14), la=(-56, 22, 14), waist=(10, -16, 0), head=(16, -12, 0), root_pos=(0, 0, 0))
    c.key(5.15, ra=(-56, -18, 0), la=(-56, -18, 0))
    c.key(5.3, ra=(-56, 16, 10), la=(-56, 16, 10))
    c.key(5.45, ra=(-56, -18, 0), la=(-56, -18, 0), head=(10, -6, 4))


@clip("raise_a_blessing", "Raises a hand in blessing", weight=4, require=["adult", "job:cleric"], length=4.8)
def _(c):
    c.key(0.5, la=(-58, -50, 0), head=(6, 0, 0), lid=.3)
    c.key(1.0, ra=(-134, 6, 14), la=(-58, -50, 0), head=(-6, 0, 4), waist=(-3, 0, 0), lid=.75, look=(0, -.2))
    c.key(1.5, ra=(-138, 6, 16), head=(-8, 0, 6))
    c.key(1.9, ra=(-104, 4, 12))
    c.key(2.3, ra=(-120, -24, 4))
    c.key(2.6, ra=(-118, 18, 18))
    c.key(3.0, ra=(-134, 6, 14), head=(-6, 0, 4), lid=.6)
    c.key(3.5, ra=(-70, -30, 0), la=(-58, -50, 0), waist=(10, 0, 0), head=(22, 0, 0), lid=1)
    c.key(4.1, ra=(-40, -10, 4), waist=(2, 0, 0), head=(6, 0, 0), lid=.2, look=(0, 0))


@clip("swing_a_censer", "Swings a censer", weight=4, require=["adult", "job:cleric"], boost=DAY, length=6.4)
def _(c):
    c.key(0.45, ra=(-30, -6, 8), la=(-58, -50, 0), head=(8, 0, 0), lid=.45, look=(0, .3))
    c.cycle(0.7, 2.5, 1.2, dict(ra=(-72, -6, 8), root=(0, 0, 2)), dict(ra=(-20, -6, 8), root=(0, 0, -2)))
    c.key(2.7, waist=(2, -16, 0), head=(8, -10, 0), look=(-.3, .3))
    c.cycle(2.8, 4.0, 1.2, dict(ra=(-72, -24, 4), root=(0, 0, 2)), dict(ra=(-20, -24, 4), root=(0, 0, -2)), end_on="b")
    c.rest(4.0, "root")
    c.key(4.4, ra=(-100, -30, 0), waist=(4, 0, 0), head=(12, -6, 0), head_pos=(0, 0, -.6), lid=.3, look=(-.2, .5))
    c.key(4.7, head=(10, -6, 0), head_pos=(0, 0, 0), lid=.6)
    c.key(5.1, head=(12, -6, 0), head_pos=(0, 0, -.6), lid=.3)
    c.key(5.5, ra=(-34, -6, 8), waist=(0, 0, 0), head=(6, 0, 4), head_pos=(0, 0, 0), lid=.4, look=(0, .2))


@clip("ring_a_handbell", "Rings a handbell", weight=4, require=["adult", "job:cleric"], avoid=["night"], boost=DAY,
      length=4.8)
def _(c):
    c.key(0.4, ra=(-96, -6, 12), head=(-4, 0, 0), look=(0, -.1))
    c.cycle(0.55, 1.55, .3, dict(ra=(-118, -6, 12)), dict(ra=(-86, -6, 12)))
    c.key(1.55, waist=(-4, 0, 0), head=(-8, -18, 0), root=(0, -10, 0), lid=.2, look=(-.4, -.1))
    c.cycle(1.75, 2.75, .3, dict(ra=(-122, -2, 14)), dict(ra=(-88, -2, 14)))
    c.key(2.75, waist=(-4, 0, 0), head=(-8, 16, 0), root=(0, 8, 0), look=(.4, -.1))
    c.key(3.1, ra=(-100, -18, 8), la=(-98, -44, 0), waist=(0, 0, 0), head=(4, 4, 10), root=(0, 0, 0), lid=.45,
          look=(.3, -.3))
    c.key(3.7, head=(4, 6, 12), lid=.5)
    c.key(4.15, ra=(-50, -14, 4), la=(-20, 0, 6), head=(2, 0, 0), lid=0, look=(0, 0))


@clip("fletch_an_arrow", "Fletches an arrow", weight=4, require=["adult", "job:fletcher"], boost=DAY, length=5.8)
def _(c):
    c.key(0.45, la=(-80, -34, 0), ra=(-70, -10, 4), waist=(6, 0, 0), head=(22, 0, 0), head_pos=(0, 0, -.5), lid=.3,
          look=(0, .6))
    for t, roll in ((0.7, 0), (1.75, 12), (2.8, -12)):
        c.key(t, ra=(-88, -18, 0), la=(-80, -34, roll), look=(.1, .6))
        c.key(t + .2, ra=(-82, -22, 0))
        c.wobble(t + .25, t + .55, 7, "ra", 3, base=(-82, -22, 0))
        c.key(t + .7, ra=(-84, -10, 0), look=(.2, .6))
        c.key(t + .9, ra=(-84, -32, 0), look=(-.1, .6))
    c.rest(3.75, "head_pos")
    c.key(4.0, la=(-104, -18, 0), ra=(-30, 0, 6), waist=(0, 0, 0), head=(2, -6, 8), lid=.45, look=(-.2, -.1))
    c.wobble(4.1, 4.7, 3, "la", 14, base=(-104, -18, 0), axis=2)
    c.key(4.85, head=(4, -4, -4), lid=.2)
    c.key(5.2, la=(-80, -30, 0), head=(14, 0, 0), lid=0, look=(0, .4))


@clip("roll_an_arrow_true", "Rolls an arrow to check it is true", weight=3, require=["adult", "job:fletcher"], boost=DAY,
      length=5.6)
def _(c):
    c.key(0.45, ra=(-54, -18, 0), la=(-30, 0, 6), waist=(22, 0, 0), head=(26, -10, 8), root_pos=(0, .3, 0),
          look=(-.3, .6))
    c.cycle(0.65, 2.25, .55, dict(ra=(-48, -18, 0)), dict(ra=(-66, -14, 0)))
    c.key(1.3, head=(28, -14, 10), lid=.4, look=(-.5, .6))
    c.key(2.25, head=(26, -10, 8), lid=.3)
    c.key(2.7, ra=(-118, -10, 0), la=(-112, -22, 0), waist=(0, 0, 0), head=(-12, 0, 6), root_pos=(0, 0, 0), lid=.6,
          look=(.1, -.5))
    c.wobble(2.8, 3.6, 3, "ra", 10, base=(-118, -10, 0), axis=2)
    c.key(3.75, head=(-12, 4, -4), lid=.65)
    c.key(4.1, ra=(-110, -14, 0), la=(-104, -24, 0), head=(-6, 0, 0), lid=.2, look=(0, -.3))
    c.key(4.4, head=(2, 0, 0))
    c.key(4.7, ra=(-60, -20, 0), la=(-30, 0, 6), head=(-2, 0, 0), lid=0, look=(0, 0))


@clip("string_a_bow", "Strings a bow braced against the foot", weight=4, require=["adult", "job:fletcher"], boost=DAY,
      length=6.4)
def _(c):
    c.key(0.5, rl=(-14, 0, 4), la=(-40, -8, 0), ra=(-62, -14, 0), waist=(20, 0, 0), head=(20, 0, 0), look=(0, .6))
    c.key(1.2, la=(-30, -6, 0), ra=(-100, -10, 0), waist=(26, 0, 0), root_pos=(0, .4, 0), head=(14, 0, 0), lid=.5,
          look=(0, .2))
    c.key(1.4, ra=(-104, -8, 0), lid=.7)
    c.key(1.55, la=(-44, -8, 0), ra=(-66, 10, 10), waist=(16, 0, 0), root_pos=(0, 0, 0), head=(10, 0, 0), lid=0)
    c.key(1.9, ra=(-62, -14, 0), waist=(20, 0, 0), head=(18, 0, 6), look=(0, .5))
    c.key(2.7, la=(-28, -6, 0), ra=(-108, -10, 0), waist=(28, 0, 0), root_pos=(0, .5, 0), head=(14, 0, 0), lid=.6,
          look=(0, .2))
    c.key(2.95, ra=(-112, -12, 0), lid=.8)
    c.key(3.15, ra=(-108, -14, 0), la=(-36, -6, 0), root_pos=(0, .2, 0), lid=.3)
    c.key(3.55, rl=(0, 0, 0), la=(-96, -6, 0), ra=(-84, -16, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(6, -4, 0),
          lid=.3, look=(0, 0))
    c.key(3.85, ra=(-82, 18, 10), lid=.4)
    c.key(4.0, ra=(-84, -16, 0))
    c.wobble(4.0, 4.4, 5, "la", 4, base=(-96, -6, 0), axis=2)
    c.key(4.5, ra=(-30, 0, 6), head=(4, -8, 8), lid=.5, look=(-.2, 0))
    c.key(5.1, la=(-96, -6, 0), head=(6, -6, -4), lid=.3)
    c.key(5.5, la=(-40, -6, 4), head=(6, 0, 0), lid=0)
