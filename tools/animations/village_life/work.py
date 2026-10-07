"""Work: a trade motion for every profession, practiced through the working day."""
from kit import clip, PRAYER

DAY = {"day": 2, "morning": 1.3}
SMITHS = "job:armorer|job:toolsmith|job:weaponsmith|job:mason|job:carpenter"


@clip("hammer_and_anvil", "Hammers at the anvil", weight=6, require=["adult", SMITHS], avoid=["night"], boost=DAY,
      items="override", length=4.2)
def _(c):
    c.key(0.4, la=(-46, -14, 0), ra=(-60, 0, 4), waist=(12, 0, 0), head=(18, 0, 0), look=(0, .6))
    for strike in (0.82, 1.57, 2.32):
        c.key(strike - .24, ra=(-152, 0, 6), waist=(8, 4, 0), root_pos=(0, 0, 0))
        c.key(strike, ra=(-58, -6, 4), waist=(16, -4, 0), root_pos=(0, .25, 0))
        c.key(strike + .12, ra=(-62, -4, 4), waist=(15, -2, 0), root_pos=(0, 0, 0))
    c.key(2.95, la=(-76, -24, 0), ra=(-22, 0, 6), head=(10, -8, 0), waist=(6, 0, 0), look=(-.2, .2))
    c.key(3.6, la=(-74, -26, 0), head=(8, -12, 4))


@clip("hoe_the_rows", "Hoes the rows", weight=6, require=["adult", "job:farmer"], avoid=["night"], boost=DAY, items="override",
      mirror="never", length=4.2)
def _(c):
    c.key(0.4, ra=(-46, -22, 0), la=(-56, -22, 0), waist=(8, 0, 0), head=(16, 0, 0), look=(0, .6))
    for strike in (0.95, 1.85, 2.75):
        c.key(strike - .3, ra=(-112, -18, 0), la=(-120, -18, 0), waist=(-2, 0, 0))
        c.key(strike, ra=(-34, -22, 0), la=(-42, -22, 0), waist=(18, 0, 0), root_pos=(0, .2, 0))
        c.key(strike + .14, ra=(-40, -22, 0), la=(-48, -22, 0), waist=(16, 0, 0), root_pos=(0, 0, 0))
    c.key(3.4, ra=(-30, -10, 0), la=(-36, -10, 0), waist=(2, 0, 0), head=(0, 0, 0), look=(0, 0))


@clip("write_notes", "Writes notes", weight=6, require=["adult", "job:cartographer|job:librarian|job:scholar"], boost=DAY,
      length=4.8)
def _(c):
    c.key(0.4, la=(-58, -30, 0), ra=(-54, -38, 0), head=(26, 0, 0), look=(0, .8))
    c.wobble(0.6, 2.3, 4, "ra", 6, base=(-54, -38, 0), axis=1)
    c.key(2.7, ra=(-106, -42, 0), head=(4, 0, 7), look=(.4, -.5))
    c.key(3.2, ra=(-104, -40, 0), head=(4, 0, 8))
    c.key(3.5, ra=(-54, -38, 0), head=(26, 0, 0), look=(0, .8))
    c.wobble(3.6, 4.2, 4, "ra", 6, base=(-54, -38, 0), axis=1)


@clip("pray", "Prays", weight=6, require=["adult", "job:cleric"], mirror="never", length=5.6)
def _(c):
    c.key(0.6, **PRAYER, head=(20, 0, 0), waist=(4, 0, 0))
    c.hold(0.8, 4.5, lid=1)
    c.key(3.2, head=(22, 0, 0))
    c.key(4.8, **PRAYER, head=(4, 0, 0), waist=(0, 0, 0), lid=0)


@clip("chop_vegetables", "Chops vegetables", weight=6, require=["adult", "job:butcher|job:cook"], boost=DAY, items="override",
      length=3.8)
def _(c):
    c.key(0.4, la=(-44, -10, 0), ra=(-72, -6, 0), waist=(12, 0, 0), head=(22, 0, 0), look=(0, .7))
    c.cycle(0.6, 2.8, .3, dict(ra=(-76, -6, 0)), dict(ra=(-46, -6, 0)), end_on="b")
    c.key(3.1, ra=(-50, -40, 0), la=(-50, 10, 0), head=(18, 0, 0))


@clip("stir_the_pot", "Stirs the pot", weight=6, require=["adult", "job:cook|job:apothecary|job:tavern_keeper"], boost=DAY,
      items="override", length=4.6)
def _(c):
    c.key(0.4, ra=(-50, -20, 0), la=(-34, -6, 0), waist=(10, 0, 0), head=(18, 0, 0), look=(0, .6))
    stir = [(-56, -30, 0), (-50, -12, 6), (-44, -24, 0), (-50, -36, -4)]
    t = 0.6
    while t < 3.5:
        for pose in stir:
            c.key(t, ra=pose)
            t += .2
    c.key(3.85, ra=(-110, -40, 0), head=(-2, 0, 0), waist=(4, 0, 0), lid=.5, look=(0, 0))
    c.key(4.15, ra=(-80, -30, 0), head=(4, 0, 7), lid=0)


@clip("pour_a_drink", "Pours a drink", weight=6, require=["adult", "job:tavern_keeper"], boost={"evening": 2, "day": 1.5},
      items="override", length=4.2)
def _(c):
    c.key(0.4, ra=(-70, -10, 0), la=(-50, -24, 0), head=(16, 0, 0), look=(0, .5))
    c.key(0.95, ra=(-92, -12, -28), head=(18, -4, 0))
    c.key(2.0, ra=(-94, -12, -32))
    c.key(2.35, ra=(-70, -10, 0))
    c.cycle(2.75, 3.6, .3, dict(ra=(-56, -34, 0)), dict(ra=(-50, -24, 0)))


@clip("stitch_cloth", "Stitches cloth", weight=6, require=["adult", "job:tailor|job:leatherworker|job:shepherd"], boost=DAY,
      length=4.8)
def _(c):
    c.key(0.4, la=(-60, -24, 0), ra=(-60, -34, 0), head=(24, 0, 0), look=(0, .8))
    for pull in (0.85, 1.85, 2.85):
        c.key(pull, ra=(-98, 6, 28), head=(18, 8, 0), look=(.3, .3))
        c.key(pull + .45, ra=(-60, -34, 0), head=(24, 0, 0), look=(0, .8))
    c.key(3.8, la=(-96, -20, 0), ra=(-90, -20, 0), head=(4, 0, 0), look=(0, .1))


@clip("sight_an_arrow", "Sights down an arrow", weight=6, require=["adult", "job:fletcher|job:archer"], boost=DAY, length=4.0)
def _(c):
    c.key(0.45, ra=(-92, -4, 0), la=(-80, -22, 0), head=(0, -2, 0), lid=.45, look=(.15, 0))
    c.key(1.6, ra=(-94, -2, 5))
    c.cycle(2.1, 2.9, .3, dict(la=(-72, -30, 0)), dict(la=(-80, -22, 0)))
    c.key(3.2, head=(10, 0, 0), lid=0, look=(0, 0))


@clip("stand_guard", "Stands guard", weight=6, require=["adult", "job:knight|job:archer"], length=6.2)
def _(c):
    c.key(0.6, rl=(0, 0, 6), ll=(0, 0, 6), la=(8, 0, 9), waist=(-3, 0, 0), head=(-4, 26, 0), look=(.5, 0))
    c.key(2.2, head=(-4, -26, 0), waist=(-3, -6, 0), look=(-.5, 0))
    c.key(3.6, head=(-2, 0, 0), waist=(-3, 0, 0), look=(0, 0))
    c.key(4.3, ra_pos=(0, -1.1, 0), la_pos=(0, -1.1, 0))
    c.key(4.8, ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(5.4, rl=(0, 0, 6), ll=(0, 0, 6), la=(8, 0, 9))


@clip("sword_drill", "Runs a sword drill", weight=4, require=["adult", "job:knight"], avoid=["night"], items="override",
      length=3.8)
def _(c):
    c.key(0.4, ra=(-60, 10, 10), waist=(4, -10, 0), rl=(-12, 0, 4), ll=(10, 0, 4), head=(0, -6, 0))
    c.key(0.8, ra=(-160, -10, 20), waist=(-4, 14, 0))
    c.key(1.0, ra=(-30, -40, -10), waist=(12, -18, 0), head=(6, -8, 0))
    c.key(1.35, ra=(-70, 0, 10), waist=(4, 0, 0), head=(0, 0, 0))
    c.key(1.8, ra=(-92, 0, 0), waist=(6, 0, 0), rl=(-22, 0, 4), root_pos=(0, 0, -.6))
    c.key(2.2, ra=(-60, 10, 10), rl=(-12, 0, 4), root_pos=(0, 0, 0))
    c.key(2.8, ra=(-150, -30, 0), waist=(-2, 0, 0), head=(-4, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(3.2, ra=(-146, -30, 0))


@clip("practice_the_draw", "Practices the draw", weight=4, require=["adult", "job:archer"], avoid=["night"], mirror="never",
      length=3.6)
def _(c):
    c.key(0.45, la=(-90, -28, 0), ra=(-90, -6, 0), head=(0, -10, 0), waist=(0, -8, 0))
    c.key(1.1, ra=(-92, -2, 0), lid=.45)
    c.key(2.1, ra=(-92, -2, 0), lid=.45)
    c.key(2.25, ra=(-88, 22, 12), lid=0)
    c.key(2.9, la=(-30, -10, 0), ra=(-30, 10, 6), head=(6, 0, 0), waist=(0, 0, 0))


@clip("twiddle_thumbs", "Twiddles thumbs", weight=3, require=["adult", "job:none|job:nitwit"], length=4.4)
def _(c):
    c.key(0.45, ra=(-42, -34, 0), la=(-42, -34, 0), head=(6, 0, 0), lid=.2)
    c.wobble(0.6, 2.4, 3, "ra", 4, base=(-42, -34, 0), axis=0)
    c.key(1.2, head=(4, 20, 0), look=(.4, 0))
    c.key(2.4, head=(4, -22, 0), look=(-.4, 0))
    c.key(3.4, head=(-6, 0, 0), look=(0, -.4), la=(-42, -34, 0), ra=(-42, -34, 0))


@clip("silly_dance", "Does a silly dance", weight=3, require=["job:nitwit|child"], mirror="free", length=3.6)
def _(c):
    a = dict(waist=(0, 10, 9), ra=(-150, 0, 30), la=(8, 0, 12), head=(0, -6, -10), root_pos=(0, -1, 0),
             rl=(-14, 0, 6), ll=(0, 0, 2))
    b = dict(waist=(0, -10, -9), ra=(8, 0, 12), la=(-150, 0, 30), head=(0, 6, 10), root_pos=(0, 0, 0),
             rl=(0, 0, 2), ll=(-14, 0, 6))
    c.cycle(0.3, 3.1, .9, a, b)
    c.hold(0.4, 3.0, lid=.4)
