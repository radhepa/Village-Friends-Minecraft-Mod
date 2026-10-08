"""Pastimes: two more hobbies for each personality, alongside their signature one."""
from kit import clip, HANDS_ON_HIPS, HAND_TO_CHEST


@clip("knit_a_scarf", "Knits a scarf", weight=3, require=["personality:warmhearted|job:shepherd"], boost={"evening": 1.5, "cold": 2},
      mirror="never", length=5.0)
def _(c):
    work = dict(ra=(-58, -30, 0), la=(-58, -30, 0), head=(22, 0, 0), waist=(4, 0, 0), look=(0, .7))
    c.key(0.45, **work)
    c.cycle(0.6, 2.4, .4, dict(ra=(-65, -35, 0), la=(-55, -26, 0)), dict(ra=(-55, -26, 0), la=(-65, -35, 0)))
    c.key(2.4, head=(22, 0, 0), waist=(4, 0, 0), look=(0, .7))
    c.key(2.85, ra=(-88, -22, 0), la=(-88, -22, 0), head=(2, 0, 0), waist=(0, 0, 0), look=(0, .1), lid=.2)
    c.key(3.25, head=(2, 0, -7), lid=.35)
    c.key(3.6, **work, lid=0)
    c.cycle(3.7, 4.4, .4, dict(ra=(-65, -35, 0), la=(-55, -26, 0)), dict(ra=(-55, -26, 0), la=(-65, -35, 0)))
    c.key(4.4, head=(22, 0, 0), waist=(4, 0, 0))


@clip("feed_the_birds", "Feeds the birds", weight=3, require=["personality:warmhearted"], avoid=["rain", "night"],
      boost={"morning": 2}, length=5.6)
def _(c):
    c.key(0.5, la=(-40, -30, 0), ra=(-30, -10, 0), head=(14, 0, 0), look=(0, .5))
    c.key(0.9, ra=(-46, -32, 0))
    c.key(1.25, ra=(-76, 28, 18), waist=(6, 6, 0), head=(20, 12, 0), look=(.3, .7))
    c.key(1.45, ra=(-64, 32, 22))
    c.key(1.9, ra=(-46, -32, 0), waist=(2, 0, 0), head=(16, 0, 0), look=(0, .5))
    c.key(2.35, ra=(-82, 4, 6), waist=(8, -4, 0), head=(22, -8, 0), look=(-.3, .8))
    c.key(2.55, ra=(-68, 2, 4))
    c.key(3.1, ra=(-26, 0, 6), la=(-36, -28, 0), waist=(0, 0, 0), head=(24, 0, 5), lid=.3, look=(0, .8))
    c.key(3.55, head=(24, 10, -4), look=(.4, .8))
    c.key(3.75, head=(27, 10, -4))
    c.key(4.1, head=(23, -8, 6), look=(-.4, .8))
    c.key(4.3, head=(26, -8, 6))
    c.key(4.9, la=(-30, -20, 0), head=(16, 0, 0), lid=.3, look=(0, .5))


@clip("mull_it_over", "Mulls it over", weight=3, require=["personality:thoughtful|job:scholar"], length=5.2)
def _(c):
    temple = (-150, -26, 0)
    c.key(0.5, ra=temple, la=(-42, -36, 0), head=(-4, -6, 4), look=(-.3, -.4))
    c.key(1.1, head=(-10, -8, 6), look=(.3, -.7), lid=.15)
    c.key(1.8, look=(-.3, -.7))
    c.key(2.3, ra=temple, head=(-10, 4, 6), look=(0, -.6))
    c.cycle(2.45, 3.05, .3, dict(ra=(-144, -26, 0)), dict(ra=(-152, -26, 0)))
    c.key(3.3, ra=temple, head=(0, 0, 0), look=(0, 0), lid=0)
    c.key(3.75, ra=(-70, -34, 0), la=(-42, -36, 0), head=(14, 0, 0), lid=.3)
    c.key(4.1, head=(2, 0, 0))
    c.key(4.45, head=(12, 0, 0), ra=(-40, -20, 0), la=(-30, -20, 0))
    c.key(4.75, head=(2, 0, 0), lid=0)


@clip("read_a_letter", "Reads a letter", weight=3, require=["personality:thoughtful"], avoid=["rain"], mirror="never", length=6.4)
def _(c):
    c.key(0.4, ra=(-56, -34, 0), la=(-56, -34, 0), head=(16, 0, 0), look=(0, .6))
    c.key(0.8, ra=(-60, -8, 4), la=(-60, -8, 4))
    c.key(1.1, ra=(-56, 2, 6), la=(-56, 2, 6), head=(20, 0, 0))
    for i, t in enumerate((1.3, 1.9, 2.5, 3.1)):
        c.key(t, look=(-.4, .5 + i * .08)).key(t + .5, look=(.4, .5 + i * .08))
    c.key(3.7, head=(22, 0, -6), lid=.3)
    c.key(4.1, ra=(-56, 2, 6), la=(-56, 2, 6), head=(20, 0, 0), lid=0, look=(0, .6))
    c.key(4.45, ra=(-58, -34, 0), la=(-56, -34, 0), head=(18, 0, 0))
    c.key(4.7, ra=(-74, -36, 0))
    c.key(4.9, ra=(-56, -36, 0))
    c.key(5.3, **HAND_TO_CHEST, la=(-12, 0, 4), head=(6, 0, 0), look=(0, .2))
    c.key(5.55, ra=(-52, -50, 0))
    c.key(5.8, ra=(-58, -50, 0))


@clip("juggle_three_balls", "Juggles three balls", weight=3, require=["personality:playful|job:bard"], mirror="never", length=4.8)
def _(c):
    c.key(0.4, ra=(-50, -6, 8), la=(-50, -6, 8), head=(-12, 0, 0), look=(0, -.5))
    c.cycle(0.55, 3.15, .5, dict(ra=(-72, -16, 0), la=(-46, 6, 12), head=(-14, 0, 3), look=(.2, -.6)),
            dict(ra=(-46, 6, 12), la=(-72, -16, 0), head=(-14, 0, -3), look=(-.2, -.6)))
    c.key(3.35, ra=(-104, -10, 0), la=(-50, -6, 8), head=(-26, 0, 0), look=(0, -.9))
    c.key(3.7, ra=(-58, -8, 4), head=(-18, 0, 0))
    c.key(3.85, ra=(-54, -8, 4), head=(0, 0, 0), look=(0, 0))
    c.key(4.15, ra=(-40, -10, 6), la=(-20, 0, 30), waist=(14, 0, 0), head=(10, 0, 0), lid=.4)


@clip("dance_a_jig", "Dances a little jig", weight=3, require=["personality:playful"], mirror="free", length=4.2)
def _(c):
    c.key(0.35, **HANDS_ON_HIPS, head=(-4, 0, 0), lid=.3)
    c.cycle(0.5, 3.3, .6, dict(rl=(-44, 0, 10), ll=(6, 0, -2), root=(0, 0, -4), head=(-4, 0, 7)),
            dict(rl=(6, 0, -2), ll=(-44, 0, 10), root=(0, 0, 4), head=(-4, 0, -7)))
    c.cycle(0.5, 3.3, .3, dict(root_pos=(0, 0, 0)), dict(root_pos=(0, -1.4, 0)))
    c.key(3.3, **HANDS_ON_HIPS)
    c.key(3.55, ra=(-150, 0, 40), la=(14, 0, 26), root_pos=(0, -3, 0), rl=(-8, 0, 12), ll=(-8, 0, 12), head=(-8, 0, 0))
    c.key(3.75, root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0))


@clip("peer_through_spyglass", "Peers through a spyglass", weight=3, require=["personality:adventurous|job:cartographer"],
      avoid=["night"], length=5.6)
def _(c):
    c.key(0.4, ra=(-84, -24, 0), la=(-84, -22, 0), head=(6, 0, 0), look=(0, .3))
    c.key(0.8, ra=(-84, 12, 6))
    c.key(1.25, ra=(-118, -36, 0), la=(-110, -12, 0), head=(-2, 0, 0), look=(0, 0), lid=.35)
    c.key(1.6, waist=(-2, -14, 0), head=(-2, -10, 0))
    c.key(2.7, waist=(-2, 14, 0), head=(-2, 10, 0))
    c.key(3.1, waist=(4, 14, 0), head=(-4, 12, 0))
    c.cycle(3.2, 3.9, .35, dict(la=(-110, -12, 0)), dict(la=(-110, -6, 4)))
    c.key(4.1, ra=(-118, -36, 0), waist=(4, 14, 0), head=(-4, 12, 0), lid=.35)
    c.key(4.55, ra=(-84, -24, 0), la=(-84, -22, 0), waist=(0, 0, 0), head=(4, 0, 0), lid=0)
    c.key(4.8, ra=(-84, -22, 0))


@clip("shadowbox", "Shadowboxes", weight=3, require=["personality:adventurous"], length=4.4)
def _(c):
    guard = dict(ra=(-96, -34, 0), la=(-94, -30, 0))
    c.key(0.35, **guard, rl=(10, 0, 4), ll=(-14, 0, 4), root=(0, -14, 0), head=(6, 0, 0), waist=(4, 0, 0), lid=.25)
    c.cycle(0.4, 2.2, .4, dict(root_pos=(0, 0, 0)), dict(root_pos=(0, -.9, 0)))
    for t in (0.75, 1.1):
        c.key(t, la=(-92, 2, 0)).key(t + .15, la=(-94, -30, 0))
    c.key(1.45, ra=(-94, -34, 0), waist=(4, 0, 0))
    c.key(1.6, ra=(-90, -6, 0), waist=(6, -18, 0)).key(1.85, **guard, waist=(4, 0, 0))
    c.key(2.35, waist=(12, 0, 9)).key(2.65, waist=(12, 0, -9)).key(2.9, waist=(4, 0, 0))
    c.key(3.05, la=(-92, 2, 0)).key(3.2, la=(-94, -30, 0))
    c.key(3.35, ra=(-94, -34, 0), waist=(4, 0, 0))
    c.key(3.5, ra=(-90, -6, 0), waist=(6, -18, 0)).key(3.7, **guard, waist=(4, 0, 0))
    c.key(3.9, rl=(10, 0, 4), ll=(-14, 0, 4), root=(0, -14, 0))


@clip("sweep_the_step", "Sweeps the step", weight=3, require=["personality:meticulous"], boost={"morning": 2}, length=5.6)
def _(c):
    c.key(0.45, ra=(-30, 0, 0), la=(-56, -40, 0), waist=(12, 0, 0), head=(20, 0, 0), look=(0, .6))
    c.cycle(0.6, 2.6, .6, dict(ra=(-36, 14, 6), la=(-60, -26, 0), waist=(14, 12, 0), head=(20, 8, 0)),
            dict(ra=(-24, -30, 0), la=(-50, -56, 0), waist=(14, -12, 0), head=(22, -8, 0)))
    c.key(3.0, ra=(-26, 0, 0), la=(-50, -40, 0), waist=(24, 0, 0), head=(26, 0, 0), look=(0, .9), lid=.3)
    c.key(3.4, head=(28, 0, 8), look=(.4, .9))
    c.key(3.75, head=(28, 0, -8), look=(-.4, .9))
    c.key(4.0, ra=(-26, 0, 0), la=(-50, -40, 0), waist=(24, 0, 0), lid=.3)
    c.key(4.2, ra=(-34, 14, 6), la=(-58, -26, 0), waist=(20, 10, 0), head=(24, 6, 0))
    c.key(4.45, ra=(-22, -30, 0), la=(-48, -56, 0), waist=(18, -12, 0), head=(24, -8, 0), lid=0)
    c.key(4.9, ra=(-20, 0, 0), la=(-30, -30, 0), waist=(2, 0, 0), head=(6, 0, 0), look=(0, .2))


@clip("tally_a_list", "Tallies a list", weight=3, require=["personality:meticulous"], length=5.6)
def _(c):
    c.key(0.45, la=(-58, -24, 0), ra=(-64, -36, 0), head=(22, 0, 0), waist=(3, 0, 0), look=(0, .6))
    for i, t in enumerate((0.85, 1.4, 1.95, 2.5)):
        p = -64 + i * 4
        c.key(t, ra=(p, -36, 0), head=(22 + i, 0, 0), look=(-.2, .55 + i * .08))
        c.key(t + .14, ra=(p + 3, -26, 4), head=(25 + i, 0, 0), look=(.2, .55 + i * .08))
        c.key(t + .3, ra=(p, -36, 0), head=(22 + i, 0, 0))
    c.key(3.2, ra=(-102, -42, 0), la=(-58, -24, 0), head=(6, 10, -6), look=(.4, -.4))
    c.cycle(3.35, 3.95, .3, dict(ra=(-102, -42, 0)), dict(ra=(-98, -40, 0)))
    c.key(4.2, ra=(-50, -36, 0), head=(26, 0, 0), look=(0, .8))
    c.key(4.35, ra=(-47, -26, 4)).key(4.5, ra=(-50, -36, 0))
    c.key(4.8, la=(-58, -24, 0), head=(12, 0, 0), lid=.35)
    c.key(5.1, ra=(-30, -20, 0), la=(-40, -20, 0), head=(4, 0, 0))


@clip("split_firewood", "Splits firewood", weight=3, require=["adult", "personality:steadfast|job:carpenter"],
      boost={"cold": 2, "morning": 1.5}, mirror="never", length=5.4)
def _(c):
    stance = dict(rl=(0, 0, 8), ll=(0, 0, 8))
    c.key(0.35, **stance, ra=(-56, -20, 0), la=(-56, -20, 0), waist=(6, 0, 0), head=(16, 0, 0), look=(0, .6))
    for t in (0.6, 2.75):
        c.key(t + .45, ra=(-174, -10, 0), la=(-174, -10, 0), waist=(-8, 0, 0), head=(-2, 0, 0), look=(0, -.1))
        c.key(t + .62, ra=(-176, -10, 0), la=(-176, -10, 0), waist=(-9, 0, 0))
        c.key(t + .8, ra=(-46, -16, 0), la=(-46, -16, 0), waist=(26, 0, 0), head=(22, 0, 0), look=(0, .8), root_pos=(0, 1.2, 0))
        c.key(t + 1.0, root_pos=(0, 0, 0))
        c.cycle(t + 1.1, t + 1.6, .25, dict(ra=(-58, -16, 0), la=(-58, -16, 0), waist=(22, 0, 0)),
                dict(ra=(-46, -16, 0), la=(-46, -16, 0), waist=(26, 0, 0)))
    c.key(2.75, ra=(-30, -6, 0), la=(-56, -20, 0), waist=(30, 0, 0), head=(20, 0, 0))
    c.key(4.75, **stance, ra=(-30, -14, 0), la=(-30, -14, 0), waist=(0, 0, 0), head=(2, 0, 0), look=(0, .2), lid=.35)


@clip("haul_water", "Hauls two buckets of water", weight=3, require=["personality:steadfast|job:farmer"], avoid=["night"],
      mirror="never", length=5.4)
def _(c):
    c.key(0.55, waist=(32, 0, 0), head=(14, 0, 0), ra=(-22, 0, 4), la=(-22, 0, 4), look=(0, .6))
    c.key(0.9, waist=(32, 0, 0), ra=(-22, 0, 4), la=(-22, 0, 4))
    c.key(1.45, waist=(-5, 0, 0), head=(-4, 0, 0), ra=(4, 0, 10), la=(4, 0, 10), lid=.45, look=(0, 0), root_pos=(0, .7, 0))
    c.cycle(1.65, 3.25, .8, dict(rl=(-14, 0, 4), ll=(4, 0, 0), root=(0, 0, -4), ra=(4, 0, 12), la=(4, 0, 8)),
            dict(rl=(4, 0, 0), ll=(-14, 0, 4), root=(0, 0, 4), ra=(4, 0, 8), la=(4, 0, 12)))
    c.key(3.25, waist=(-5, 0, 0), head=(-4, 0, 0), lid=.45, root_pos=(0, .7, 0), rl=(0, 0, 0), ll=(0, 0, 0), root=(0, 0, 0))
    c.key(3.7, waist=(30, 0, 0), head=(12, 0, 0), ra=(-22, 0, 4), la=(-22, 0, 4), lid=0, root_pos=(0, 0, 0))
    c.key(4.15, waist=(-3, 0, 0), head=(-6, 0, 4), ra=(0, 0, 8), la=(0, 0, 8))
    c.cycle(4.25, 4.8, .16, dict(ra=(0, 0, 12), la=(0, 0, 5)), dict(ra=(0, 0, 5), la=(0, 0, 12)))


@clip("sip_tea", "Sips tea", weight=3, require=["personality:reserved"], boost={"evening": 2, "cold": 1.5, "morning": 1.5}, length=6.0)
def _(c):
    saucer, cup = (-50, -30, 0), (-54, -34, 0)
    c.key(0.45, la=saucer, ra=cup, head=(10, 0, 0), look=(0, .5))
    c.key(1.0, ra=(-106, -40, 0), head=(8, 0, 0), look=(0, .4))
    for t in (1.2, 1.5):
        c.key(t, head=(11, 0, 0), lid=.35).key(t + .15, head=(7, 0, 0), lid=.2)
    c.key(2.0, ra=(-122, -40, 0), head=(-10, 0, 0), lid=.7, look=(0, .2))
    c.key(2.6, ra=(-122, -40, 0), head=(-10, 0, 0), lid=.7)
    c.key(2.95, ra=cup, head=(6, 0, 0), lid=.5, look=(0, .4))
    c.key(3.3, root_pos=(0, -.5, 0), head=(2, 0, -6), lid=.5)
    c.key(3.8, root_pos=(0, 0, 0), head=(4, 10, 0), look=(.4, .1), lid=.2)
    c.key(4.0, ra=cup)
    c.key(4.5, ra=(-120, -40, 0), head=(-6, 0, 0), lid=.6, look=(0, .2))
    c.key(4.9, la=saucer, ra=(-120, -40, 0), head=(-6, 0, 0))
    c.key(5.3, ra=cup, head=(8, 0, 0), lid=.2, look=(0, .4))


@clip("skip_a_stone", "Skips a stone", weight=3, require=["personality:reserved|job:fisherman"], avoid=["night"], length=5.6)
def _(c):
    c.key(0.6, waist=(40, 0, 0), head=(20, 0, 0), ra=(-62, -6, 0), la=(-20, 0, 6), look=(0, .7))
    c.key(0.9, ra=(-66, -10, 0))
    c.key(1.3, waist=(4, 0, 0), head=(12, 0, 0), ra=(-60, -30, 0), la=(-10, 0, 6), look=(0, .5))
    c.key(1.45, ra=(-68, -30, 0)).key(1.6, ra=(-58, -30, 0))
    crouch = dict(root_pos=(0, 3, 0), rl=(-28, 0, 4), ll=(-28, 0, 4))
    c.key(1.75, waist=(4, 0, 0), head=(12, 0, 0))
    c.key(2.0, **crouch, waist=(16, 28, 0), ra=(4, 0, 58), la=(-52, -30, 0), head=(10, -18, 0), look=(-.3, .2))
    c.key(2.2, **crouch, waist=(16, 30, 0), ra=(10, 0, 60))
    c.key(2.42, waist=(14, -24, 0), ra=(-74, -30, 8), head=(6, -6, 0))
    c.key(2.6, ra=(-60, -52, 0), waist=(12, -28, 0))
    c.key(2.9, root_pos=(0, 1.2, 0), rl=(-12, 0, 2), ll=(-12, 0, 2), waist=(6, -8, 0), ra=(-30, -20, 0), la=(-30, -20, 0),
          head=(0, -4, 0), look=(0, 0))
    for t, dip in ((3.1, 7), (3.42, 6), (3.68, 4), (3.88, 3), (4.03, 2)):
        c.key(t, head=(dip, -4, 0)).key(t + .1, head=(-1, -4, 0))
    c.key(4.2, root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), waist=(2, 0, 0))
    c.key(4.6, head=(12, 0, 0), lid=.4, ra=(-20, 0, 4), la=(-20, 0, 4))
    c.key(5.0, head=(2, 0, 0), lid=.25)


@clip("shape_clay", "Shapes clay", weight=3, require=["personality:imaginative|job:mason"], mirror="never", length=5.6)
def _(c):
    c.key(0.45, ra=(-46, -20, 0), la=(-46, -20, 0), waist=(14, 0, 0), head=(24, 0, 0), look=(0, .7))
    c.cycle(0.6, 1.8, .5, dict(ra=(-60, -28, 0), la=(-38, -16, 0), waist=(15, 0, 2)),
            dict(ra=(-38, -16, 0), la=(-60, -28, 0), waist=(15, 0, -2)))
    c.cycle(1.95, 2.75, .4, dict(ra=(-46, 2, 6), la=(-46, 2, 6)), dict(ra=(-48, -32, 0), la=(-48, -32, 0)), end_on="b")
    c.key(2.75, waist=(14, 0, 0), head=(24, 0, 0))
    c.key(3.0, ra=(-68, -30, 0), la=(-68, -30, 0), waist=(10, 0, 0), head=(16, 0, 0), look=(0, .4))
    c.cycle(3.15, 3.75, .2, dict(ra=(-72, -36, 0)), dict(ra=(-64, -30, 0)))
    c.key(3.75, la=(-66, -30, 0), head=(18, 0, 4))
    c.key(4.15, ra=(-40, -10, 4), la=(-40, -10, 4), waist=(0, 0, 0), head=(6, 0, -10), lid=.3, look=(0, .3))
    c.key(4.55, head=(10, 0, -12), lid=.4)
    c.key(4.95, head=(4, 0, -6), lid=.2)


@clip("act_out_a_tale", "Acts out a tale", weight=3, require=["personality:imaginative|job:bard"], length=7.4)
def _(c):
    c.key(0.45, ra=(-22, 0, 152), la=(-10, 0, 14), head=(-8, 0, 0), look=(0, -.4), lid=.25)
    c.key(0.75, ra=(-40, 0, 138))
    lunge = dict(rl=(-26, 0, 4), ll=(14, 0, 4), root_pos=(0, 1.2, 0))
    c.key(1.05, ra=(-88, -8, 0), la=(12, 0, 22), waist=(12, -8, 0), head=(4, 0, 0), look=(0, 0), **lunge)
    c.key(1.5, ra=(-90, -8, 0), la=(12, 0, 22), waist=(12, -8, 0), **lunge)
    c.key(1.9, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), lid=0)
    c.key(2.25, ra=(-142, 8, 18), la=(-142, 8, 18), waist=(-8, 0, 0), head=(-6, 0, 0), look=(0, -.2))
    c.key(2.65, ra=(-118, -6, 10), la=(-118, -6, 10), waist=(14, 0, 0), head=(8, 0, 0), lid=.6, look=(0, .1))
    c.cycle(2.85, 3.45, .3, dict(ra=(-98, -22, 0), la=(-84, -22, 0)), dict(ra=(-122, -18, 0), la=(-66, -18, 0)))
    c.wobble(3.45, 3.95, 7, "head", 9, base=(8, 0, 0), axis=1)
    c.key(3.95, ra=(-98, -22, 0), la=(-84, -22, 0), waist=(14, 0, 0), lid=.6)
    c.key(4.4, la=(-92, -26, 0), ra=(-92, -6, 0), head=(0, -10, 0), waist=(0, -8, 0), lid=.45, look=(-.3, 0))
    c.key(5.0, ra=(-93, -2, 0))
    c.key(5.2, ra=(-88, 24, 14), lid=0)
    c.key(5.45, la=(-90, -26, 0), head=(-4, -14, 0), look=(-.5, -.1))
    c.key(6.0, waist=(32, 0, 0), ra=(-58, -50, 0), la=(-24, 0, 50), head=(14, 0, 0), lid=.5, look=(0, .3))
    c.key(6.45, waist=(32, 0, 0), ra=(-58, -50, 0), la=(-24, 0, 50), head=(14, 0, 0), lid=.5)
    c.key(6.85, waist=(0, 0, 0), head=(-2, 0, 0), ra=(-20, 0, 8), la=(-12, 0, 16), lid=.2, look=(0, 0))


@clip("weave_a_basket", "Weaves a basket", weight=3, require=["personality:pragmatic"], boost={"evening": 1.5, "rain": 1.5},
      length=5.6)
def _(c):
    hold = dict(ra=(-46, -26, 0), la=(-42, -22, 0))
    c.key(0.45, **hold, waist=(10, 0, 0), head=(22, 0, 0), look=(0, .7))
    c.cycle(0.65, 2.45, .6, dict(ra=(-60, -6, 8), head=(22, 4, 0), look=(.2, .7)),
            dict(ra=(-36, -36, 0), head=(22, -3, 0), look=(-.1, .75)))
    c.key(2.6, ra=(-66, 22, 18), head=(16, 8, 0), look=(.4, .4))
    c.key(2.75, ra=(-76, 34, 28), head=(12, 10, 0))
    for t in (3.05, 3.55):
        c.key(t, ra=(-38, -42, 0), la=(-52, -2, 6), waist=(10, -6, 0), head=(22, -4, 0), look=(0, .7))
        c.key(t + .3, **hold, waist=(10, 0, 0), head=(22, 0, 0))
    c.cycle(4.0, 4.6, .3, dict(ra=(-58, -8, 6)), dict(ra=(-38, -34, 0)))
    c.key(4.95, ra=(-74, -22, 0), la=(-74, -22, 0), waist=(2, 0, 0), head=(6, 0, -7), look=(0, .2), lid=.25)
    c.key(5.15, head=(6, 0, 6))


@clip("mend_a_fence", "Mends a fence", weight=3, require=["adult", "personality:pragmatic|job:farmer"], avoid=["night", "rain"],
      boost={"morning": 1.5, "day": 1.5}, length=6.0)
def _(c):
    crouch = dict(rl=(-58, 0, 0), ll=(58, 0, 0), root_pos=(0, 5.6, 0), waist=(28, 0, 0))
    c.key(0.4, head=(10, 0, 0), look=(0, .4))
    c.key(0.65, rl=(-30, 0, 0), ll=(30, 0, 0), root_pos=(0, 1.8, 0), waist=(12, 0, 0))
    c.key(0.95, **crouch, la=(-62, -20, 0), ra=(-40, -10, 0), head=(18, 0, 0), look=(0, .6))
    for t in (1.3, 1.75, 2.2):
        c.key(t, ra=(-120, -12, 0), head=(16, 0, 0)).key(t + .17, ra=(-54, -16, 0), head=(20, 0, 0))
        c.key(t + .3, ra=(-62, -16, 0), head=(18, 0, 0))
    c.key(2.75, la=(-104, -6, 12), ra=(-48, -10, 0), head=(6, 0, 0), lid=.85, look=(0, .3))
    c.wobble(2.8, 3.4, 6, "la", 14, base=(-104, -6, 12), axis=2)
    c.key(3.6, la=(-62, -20, 0), head=(18, 0, 0), lid=0, look=(0, .6))
    for t in (3.85, 4.35):
        c.key(t, ra=(-140, -10, 0), waist=(24, 0, 0), head=(14, 0, 0)).key(t + .18, ra=(-52, -16, 0), waist=(30, 0, 0), head=(20, 0, 0))
    c.key(4.75, **crouch, la=(-62, -20, 0), ra=(-40, -10, 0))
    c.cycle(4.85, 5.15, .15, dict(la=(-58, -20, 0)), dict(la=(-66, -20, 0)))
    c.key(5.5, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), ra=(-20, 0, 6), la=(-20, 0, 6), head=(4, 0, 0),
          look=(0, .3))


@clip("peer_through_a_lens", "Peers through a lens", weight=3, require=["personality:curious"], avoid=["night"],
      boost={"day": 1.5}, length=5.4)
def _(c):
    c.key(0.4, ra=(-74, -24, 0), la=(-30, -10, 0), head=(12, 0, 0), look=(0, .4))
    c.key(0.9, ra=(-52, -22, 0), waist=(26, 0, 0), head=(22, 0, 0), lid=.45, look=(0, .7), root_pos=(0, 0, -.6))
    c.key(1.45, ra=(-50, 4, 6), waist=(26, 8, 0), head=(24, 10, 0), look=(.4, .8))
    c.key(2.1, ra=(-54, -40, 0), waist=(26, -8, 0), head=(24, -10, 0), look=(-.4, .8))
    c.key(2.45, waist=(32, -8, 0), head=(26, -10, 0), lid=.6, root_pos=(0, 0, -.8))
    c.wobble(2.55, 3.1, 4, "head", 6, base=(26, -10, 0), axis=2)
    c.key(3.12, ra=(-54, -40, 0), waist=(32, -8, 0), lid=.6, look=(-.4, .8), root_pos=(0, 0, -.8))
    c.key(3.35, ra=(-62, -24, 0), waist=(4, 0, 0), head=(-6, 0, 0), lid=0, look=(0, .1), root_pos=(0, 0, 0))
    c.key(3.8, ra=(-106, -38, 0), head=(0, 0, 6), lid=.5, look=(0, 0))
    c.key(4.4, ra=(-108, -38, 0), head=(0, 4, 8))
    c.key(4.85, ra=(-40, -20, 0), la=(-20, 0, 4), head=(4, 0, 0), lid=0)


@clip("tinker_with_a_gadget", "Tinkers with a gadget", weight=3, require=["personality:curious"], boost={"rain": 1.5, "evening": 1.5},
      mirror="never", length=5.8)
def _(c):
    work = dict(ra=(-64, -30, 0), la=(-64, -30, 0), head=(22, 0, 0), waist=(6, 0, 0), look=(0, .6))
    c.key(0.45, **work)
    c.wobble(0.6, 2.0, 6, "ra", 5, base=(-64, -30, 0))
    c.cycle(0.6, 2.0, .5, dict(la=(-62, -24, 0)), dict(la=(-66, -36, 0)))
    c.key(2.15, ra=(-68, -24, 0), la=(-60, -34, 0), head=(26, 0, 6), waist=(10, 0, 0), lid=.4, look=(0, .7))
    c.key(2.4, ra=(-68, -12, 6)).key(2.6, ra=(-70, -30, 0))
    c.key(2.62, la=(-60, -34, 0), head=(26, 0, 6), waist=(10, 0, 0), lid=.4, look=(0, .7), root_pos=(0, 0, 0))
    c.key(2.75, root_pos=(0, -3.6, 0), ra=(-132, 20, 40), la=(-132, 20, 40), head=(-14, 0, 0), waist=(-8, 0, 0), lid=0, look=(0, -.3))
    c.key(2.95, root_pos=(0, 0, 0), ra=(-120, 14, 34), la=(-120, 14, 34))
    c.key(3.2, ra=(-110, 10, 28), la=(-110, 10, 28), head=(-8, 0, 0), waist=(-4, 0, 0))
    c.key(3.6, **HAND_TO_CHEST, la=(-20, 0, 10), head=(6, 0, 0), waist=(0, 0, 0), look=(0, .6))
    c.key(4.0, ra=(-56, -46, 0), waist=(16, 0, 0), head=(24, 0, -6), look=(0, .9))
    c.key(4.45, **work)
    c.cycle(4.6, 5.2, .3, dict(ra=(-60, -26, 0)), dict(ra=(-68, -32, 0)))
    c.key(5.3, head=(18, 0, 0), look=(0, .5))


@clip("practice_a_stance", "Practices a fighting stance", weight=3, require=["personality:protective"], avoid=["night"],
      boost={"morning": 2}, mirror="free", length=5.4)
def _(c):
    wide = dict(rl=(-6, 0, 16), ll=(-6, 0, 16), root_pos=(0, 1.4, 0))
    c.key(0.4, ra=(16, 0, 4), la=(16, 0, 4), waist=(16, 0, 0), head=(12, 0, 0), lid=.3)
    c.key(0.8, waist=(0, 0, 0), head=(0, 0, 0), lid=0)
    c.key(1.2, **wide, root=(0, 0, 0), ra=(-70, -44, 0), la=(-100, -18, 0), head=(2, 0, 0), lid=.25)
    c.key(1.85, rl=(-20, 0, 6), ll=(14, 0, 6), root_pos=(0, 1.4, 0), root=(0, 38, 0), ra=(-100, -18, 0), la=(-70, -44, 0))
    c.key(2.15, ra=(-162, -22, 0)).key(2.4, ra=(-160, -22, 0)).key(2.7, ra=(-100, -18, 0))
    c.key(3.2, rl=(14, 0, 6), ll=(-20, 0, 6), root=(0, -38, 0), ra=(-70, -44, 0), la=(-100, -18, 0))
    c.key(3.5, la=(-36, 18, 22)).key(3.75, la=(-34, 18, 24)).key(4.0, la=(-100, -18, 0))
    c.key(4.4, **wide, root=(0, 0, 0), ra=(16, 0, 4), la=(16, 0, 4), head=(2, 0, 0))
    c.key(4.8, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), lid=.5, head=(-4, 0, 0))


@clip("keep_watch", "Keeps watch", weight=3, require=["personality:protective"], boost={"evening": 2, "night": 2},
      length=6.4)
def _(c):
    c.key(0.5, la=(14, 0, 26), rl=(0, 0, 6), ll=(0, 0, 6), head=(-2, 0, 0), lid=.2)
    c.key(2.3, root=(0, 28, 0), waist=(0, 8, 0), head=(-2, 18, 0), look=(.5, 0))
    c.key(2.8, waist=(6, 8, 0), head=(-4, 20, 0), lid=.55, look=(.5, -.1))
    c.key(3.05, ra=(-22, -40, 0))
    c.key(3.6, ra=(-22, -40, 0), root=(0, 28, 0), waist=(6, 8, 0), head=(-4, 20, 0), lid=.55)
    c.key(3.95, ra=(0, 0, 0), waist=(0, 8, 0), head=(0, 14, 0), lid=.2, look=(.2, 0))
    c.key(5.2, root=(0, -26, 0), waist=(0, -8, 0), head=(-2, -18, 0), look=(-.5, 0))
    c.key(5.7, root=(0, 0, 0), waist=(0, 0, 0), head=(6, 0, 0), look=(0, .1))
    c.key(5.9, la=(14, 0, 26), rl=(0, 0, 6), ll=(0, 0, 6), head=(0, 0, 0))


@clip("pet_a_cat", "Pets a cat", weight=3, require=["personality:gentle"], boost={"evening": 1.5}, length=6.2)
def _(c):
    squat = dict(rl=(-62, 0, 10), ll=(-62, 0, 10), root_pos=(0, 6, 0), waist=(30, 0, 0))
    c.key(0.4, head=(18, 0, 0), look=(0, .8))
    c.key(1.0, **squat, head=(22, 0, 0), la=(-24, 0, 8), ra=(-20, 0, 6))
    c.key(1.4, ra=(-42, -6, 0), head=(22, 0, 0))
    for t in (1.5, 2.35):
        c.key(t, ra=(-42, -6, 0)).key(t + .6, ra=(-14, -6, 0), head=(24, 0, 4), lid=.3).key(t + .8, ra=(-32, -6, 6))
    c.key(3.2, ra=(-40, -6, 0), head=(22, 0, -10), lid=.65)
    c.key(3.5, ra=(-36, -10, 0), head=(24, 0, -12))
    c.wobble(3.6, 4.3, 7, "ra", 4, base=(-36, -10, 0))
    c.key(4.6, **squat, ra=(-20, 0, 8), la=(-24, 0, 8), head=(22, 0, 8), lid=.3)
    c.key(5.2, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), la=(0, 0, 0), ra=(0, 0, 0), head=(12, 10, 0),
          look=(.4, .7), lid=0)
    c.key(5.6, head=(10, 16, 0), look=(.5, .6))


@clip("water_the_flowers", "Waters the flowers", weight=3, require=["personality:gentle"], avoid=["rain", "night"],
      boost={"morning": 2, "evening": 1.5}, length=6.6)
def _(c):
    carry = dict(ra=(-30, -6, 6), la=(-50, -30, 0), waist=(4, 0, 0), head=(12, 0, 0))
    pour = dict(ra=(-58, -10, 14), la=(-62, -34, 0), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .8))
    c.key(0.5, **carry, root=(0, -14, 0), look=(0, .5))
    c.key(0.95, **pour)
    c.cycle(1.1, 2.1, .5, dict(waist=(14, -6, 0), head=(22, -4, 0)), dict(waist=(14, 6, 0), head=(22, 4, 0)))
    c.key(2.3, **carry, look=(.3, .4))
    c.key(2.55, rl=(0, 0, 14), root=(0, -2, -3), root_pos=(.2, 0, 0))
    c.key(2.8, rl=(0, 0, 0), ll=(0, 0, 10), root=(0, 8, 0), root_pos=(.4, 0, 0))
    c.key(3.05, ll=(0, 0, 0), root=(0, 16, 0))
    c.key(3.35, **pour)
    c.cycle(3.5, 4.5, .5, dict(waist=(14, 6, 0), head=(22, 4, 0)), dict(waist=(14, -6, 0), head=(22, -4, 0)))
    c.key(4.65, ra=(-74, -10, 22), waist=(16, 0, 0), head=(24, 0, 0))
    c.wobble(4.75, 5.2, 6, "ra", 6, base=(-74, -10, 22))
    c.key(5.5, ra=(-24, -4, 6), la=(-30, -16, 0), waist=(2, 0, 0), root=(0, 16, 0), root_pos=(.4, 0, 0), head=(4, 0, -6), lid=.35,
          look=(0, .3))
    c.key(5.95, head=(2, 0, 0), lid=0)
