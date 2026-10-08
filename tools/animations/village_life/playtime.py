"""Playtime: more games for the village's children."""
from kit import clip

SQUAT = dict(rl=(-62, 0, 10), ll=(-62, 0, 10), root_pos=(0, 6, 0), waist=(30, 0, 0), head=(26, 0, 0))


@clip("skip_rope", "Skips rope", weight=3, require=["child"], mirror="never", length=4.4)
def _(c):
    c.key(0.3, ra=(-20, 0, 28), la=(-20, 0, 28), look=(0, .3))
    for t in (0.55, 1.0, 1.45, 1.9, 2.35, 2.8):
        c.key(t, root_pos=(0, .6, 0), ra=(4, 0, 26), la=(4, 0, 26), rl=(-6, 0, 2), ll=(-6, 0, 2), head=(4, 0, 0))
        c.key(t + .2, root_pos=(0, -3, 0), ra=(-38, 0, 32), la=(-38, 0, 32), rl=(12, 0, 2), ll=(12, 0, 2), head=(-2, 0, 0))
    c.key(3.2, root_pos=(0, .6, 0), ra=(0, 0, 24), la=(0, 0, 24), rl=(0, 0, 0), ll=(0, 0, 0), lid=.5, head=(8, 0, 0))
    c.key(3.5, root_pos=(0, 0, 0), head=(2, 0, 0))
    c.hold(0.5, 3.0, lid=.25)


@clip("hopscotch", "Plays hopscotch", weight=2.5, require=["child"], mirror="free", length=5.0)
def _(c):
    one = dict(ll=(26, 0, 0), rl=(-4, 0, 0), ra=(-24, 0, 40), la=(-30, 0, 46))
    two = dict(ll=(-2, 0, 12), rl=(-2, 0, 12), ra=(-10, 0, 24), la=(-10, 0, 24))
    c.key(0.4, head=(20, 0, 0), look=(0, .8), root_pos=(0, .6, 0))
    for t, pose in ((0.7, one), (1.2, one), (1.7, two), (2.2, one), (2.7, two), (3.2, one)):
        c.key(t, root_pos=(0, -2.6, 0), waist=(4, 0, 0))
        c.key(t + .22, **pose, root_pos=(0, .5, 0), waist=(8, 0, 0))
    c.key(3.8, ll=(0, 0, 0), rl=(0, 0, 0), ra=(-20, 0, 50), la=(-20, 0, 50), root_pos=(0, 0, 0), head=(-6, 0, 0), lid=.5)
    c.key(4.3, look=(0, 0), waist=(0, 0, 0))


@clip("spin_until_dizzy", "Spins until dizzy", weight=2, require=["child"], mirror="free", length=5.2)
def _(c):
    # One fast turn; 360 degrees wraps back to 0 in the same instant, which looks identical.
    c.key(0.3, root=(0, 0, 0), ra=(-20, 0, 30), la=(-20, 0, 30))
    c.key(0.55, root=(0, -50, 0), head=(-8, 0, 0), lid=.3)
    c.key(0.9, root=(0, 90, 0), ra=(-10, 0, 76), la=(-10, 0, 76))
    c.key(1.2, root=(0, 230, 0))
    c.key(1.5, root=(0, 360, 0), ra=(-10, 0, 70), la=(-10, 0, 70))
    c.key(1.5001, root=(0, 0, 0))
    c.key(1.8, root=(0, 0, 6), head=(6, 0, 14), ra=(-30, 0, 44), la=(-20, 0, 30), rl=(0, 0, 12), lid=.4, look=(.6, -.3))
    c.key(2.2, root=(0, 0, -5), head=(4, 0, -12), look=(-.5, .4))
    c.key(2.6, root=(0, 0, 5), head=(8, 0, 10), look=(.4, .5), ll=(0, 0, 10), rl=(0, 0, 4))
    c.key(3.0, root=(0, 0, -4), head=(4, 0, -9), look=(-.6, -.2))
    c.key(3.4, root=(0, 0, 3), head=(6, 0, 6), look=(.2, -.5))
    c.key(3.8, root=(0, 0, -1), head=(2, 0, -3), look=(0, 0), ra=(-14, 0, 20), la=(-14, 0, 20), lid=.6, ll=(0, 0, 0), rl=(0, 0, 0))
    c.wobble(3.9, 4.6, 5, "head", 5, base=(2, 0, 0), axis=2)


@clip("ride_hobby_horse", "Rides a hobby horse", weight=3, require=["child"], mirror="never", length=4.8)
def _(c):
    reins = dict(ra=(-46, -24, 0), la=(-40, -20, 0))
    c.key(0.35, **reins, waist=(8, 0, 0), head=(-4, 0, 0), lid=.25)
    c.cycle(0.5, 3.8, .44, dict(rl=(-32, 0, 0), ll=(10, 0, 0), root_pos=(0, -1.8, 0), head=(-6, 0, 0)),
            dict(rl=(10, 0, 0), ll=(-32, 0, 0), root_pos=(0, .4, 0), head=(-2, 0, 0)))
    c.cycle(0.5, 1.8, .44, dict(ra=(-52, -24, 0), la=(-46, -20, 0)), dict(ra=(-40, -24, 0), la=(-34, -20, 0)))
    c.key(2.1, ra=(-12, 0, 156), head=(-12, 0, 0), lid=.5)
    c.wobble(2.2, 3.3, 3, "ra", 14, base=(-12, 0, 156), axis=1)
    c.key(3.6, **reins)
    c.key(4.1, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0))


@clip("build_a_sandcastle", "Builds a sandcastle", weight=2.5, require=["child"], mirror="never", length=6.4)
def _(c):
    c.key(0.7, **SQUAT, ra=(-46, -6, 6), la=(-46, -6, 6), look=(0, .8))
    c.cycle(0.9, 2.5, .4, dict(ra=(-58, -8, 6), la=(-58, -8, 6)), dict(ra=(-38, -8, 6), la=(-38, -8, 6)))
    c.key(2.9, ra=(-64, -26, 0), la=(-64, -26, 0), head=(22, 0, 0))
    c.key(3.3, ra=(-80, -24, 0), la=(-80, -24, 0), head=(16, 0, 0), look=(0, .5))
    c.key(3.7, waist=(16, 0, 0), head=(4, 0, 6), ra=(-30, 0, 10), la=(-30, 0, 10), lid=.4, look=(0, .3))
    c.key(4.4, waist=(18, 0, 0), head=(6, 0, -6))
    c.key(4.7, waist=(30, 0, 0), head=(24, 0, 0), ra=(-62, -6, 6), lid=0, look=(0, .8))
    c.key(4.95, ra=(-44, -6, 6))
    c.key(5.2, **SQUAT)


@clip("blow_a_dandelion", "Blows a dandelion", weight=2, require=["child"], length=5.6)
def _(c):
    c.key(0.6, waist=(36, 0, 0), head=(30, 0, 0), ra=(-48, -8, 0), look=(0, .8), root_pos=(0, 1, 0))
    c.key(0.9, ra=(-40, -8, 0))
    c.key(1.1, ra=(-48, -6, 0))
    c.key(1.7, waist=(0, 0, 0), head=(0, 0, 0), ra=(-96, -30, 0), root_pos=(0, 0, 0), look=(0, .2))
    c.key(2.2, head=(-8, 0, 0), root_pos=(0, -.5, 0), lid=.2)
    c.key(2.5, head=(8, 0, 0), root_pos=(0, 0, 0), waist=(4, 0, 0), lid=.6)
    c.key(2.9, head=(6, 0, 0), ra=(-96, -28, 0))
    c.key(3.4, head=(-24, 18, 0), waist=(-2, 0, 0), ra=(-70, -10, 0), look=(.6, -.6), lid=0)
    c.key(4.2, head=(-32, 28, 0), look=(.8, -.8), ra=(-30, 0, 4))
    c.key(4.9, head=(-26, 22, 0), look=(.6, -.7), waist=(0, 0, 0))


@clip("stick_sword_play", "Plays at swords with a stick", weight=3, require=["child"], length=4.6)
def _(c):
    c.key(0.4, ra=(-70, 8, 0), la=(14, 0, 26), rl=(-18, 0, 4), ll=(8, 0, 4), waist=(4, 10, 0), lid=.3, head=(0, -6, 0))
    c.key(0.9, ra=(-162, 20, 0), waist=(-4, 14, 0), head=(-6, -8, 0))
    c.key(1.15, ra=(-40, -34, 0), waist=(10, -12, 0), head=(6, 8, 0))
    c.key(1.6, ra=(-100, -44, 20), waist=(0, -6, 0), head=(-4, 4, 0), root_pos=(0, 0, .4))
    c.key(2.0, ra=(-96, 6, 0), waist=(12, 10, 0), rl=(-34, 0, 4), ll=(14, 0, 4), root_pos=(0, .8, -.6), head=(0, -8, 0))
    c.key(2.4, ra=(-70, 8, 0), waist=(4, 10, 0), rl=(-18, 0, 4), ll=(8, 0, 4), root_pos=(0, 0, 0))
    c.key(2.8, ra=(-96, 6, 0), waist=(12, 10, 0), rl=(-34, 0, 4), root_pos=(0, .8, -.6))
    c.key(3.2, ra=(-170, 0, 12), la=(0, 0, 10), waist=(-6, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, -1, 0), head=(-14, 0, 0), lid=.5)
    c.key(3.8, ra=(-164, 0, 14), root_pos=(0, 0, 0))


@clip("pretend_to_be_a_monster", "Pretends to be a monster", weight=2.5, require=["child"], mirror="never", length=4.4)
def _(c):
    claws = dict(ra=(-118, 14, 30), la=(-118, 14, 30))
    c.key(0.5, **claws, waist=(14, 0, 0), head=(12, 0, 0), root_pos=(0, 1.4, 0), rl=(-14, 0, 10), ll=(-14, 0, 10), lid=.5)
    c.key(1.0, ra=(-150, 20, 40), la=(-150, 20, 40), waist=(-8, 0, 0), head=(-20, 0, 0), root_pos=(0, -1, 0), lid=.3)
    c.wobble(1.1, 1.9, 9, "head", 6, base=(-20, 0, 0), axis=1, decay=.3)
    c.key(2.1, **claws, waist=(10, 0, 0), head=(8, 0, 0), root_pos=(0, 1, 0), lid=.5)
    c.cycle(2.3, 3.6, .65, dict(rl=(-30, 0, 10), root=(0, 0, -5), root_pos=(0, .4, 0)),
            dict(ll=(-30, 0, 10), rl=(-8, 0, 10), root=(0, 0, 5), root_pos=(0, 1.2, 0)))
    c.key(3.8, ll=(0, 0, 0), rl=(0, 0, 0), root=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), head=(-4, 0, 0), lid=.6)


@clip("pat_a_cake", "Plays pat-a-cake", weight=3, require=["child"], mirror="never", length=4.6)
def _(c):
    own = dict(ra=(-64, -36, 0), la=(-64, -36, 0), head=(4, 0, 0))
    pat = dict(ra=(-86, 6, 8), la=(-86, 6, 8), head=(-2, 0, 0))
    cross_r = dict(ra=(-86, -26, 0), la=(-36, 0, 10), waist=(0, -10, 0), head=(0, -6, 0))
    cross_l = dict(la=(-86, -26, 0), ra=(-36, 0, 10), waist=(0, 10, 0), head=(0, 6, 0))
    c.key(0.3, ra=(-60, -10, 8), la=(-60, -10, 8), lid=.3)
    for t, pose in ((0.5, own), (0.8, pat), (1.1, own), (1.4, cross_r), (1.7, own), (2.0, cross_l), (2.3, own), (2.6, pat)):
        c.key(t, **{"waist": (0, 0, 0), **pose})
    c.cycle(2.85, 3.55, .24, dict(ra=(-74, -30, 0), la=(-56, -30, 0), head=(4, 0, 4)),
            dict(ra=(-56, -30, 0), la=(-74, -30, 0), head=(4, 0, -4)))
    c.key(3.8, ra=(-92, 0, 6), la=(-92, 0, 6), waist=(8, 0, 0), head=(-6, 0, 0), root_pos=(0, -1, 0), lid=.6)
    c.key(4.05, waist=(2, 0, 0), root_pos=(0, 0, 0))


@clip("toss_and_catch_ball", "Tosses a ball up and catches it", weight=3, require=["child"], mirror="never", length=5.0)
def _(c):
    cup = dict(ra=(-40, -26, 0), la=(-40, -26, 0))
    c.key(0.4, **cup, head=(10, 0, 0), look=(0, .5))
    c.key(0.7, ra=(-30, -24, 0), la=(-30, -24, 0), root_pos=(0, 1.2, 0))
    c.key(0.95, ra=(-150, -12, 0), la=(-150, -12, 0), root_pos=(0, -.8, 0), head=(-20, 0, 0), look=(0, -.8))
    c.key(1.3, ra=(-128, -18, 0), la=(-128, -18, 0), root_pos=(0, 0, 0), head=(-34, 0, 0))
    c.key(1.65, ra=(-110, -28, 0), la=(-110, -28, 0), head=(-20, 0, 0))
    c.key(1.9, ra=(-64, -30, 0), la=(-64, -30, 0), head=(8, 0, 0), root_pos=(0, 1, 0), look=(0, .4), lid=.2)
    c.key(2.3, ra=(-34, -24, 0), la=(-34, -24, 0), root_pos=(0, 1.4, 0), lid=0)
    c.key(2.55, ra=(-165, -10, 0), la=(-165, -10, 0), root_pos=(0, -2, 0), head=(-24, 0, 0), look=(0, -.9))
    c.key(3.0, ra=(-130, -16, 0), la=(-130, -16, 0), root_pos=(0, 0, 0), head=(-40, 0, 0))
    c.key(3.35, ra=(-118, -30, 0), la=(-118, -30, 0), head=(-26, 0, 0), lid=.3)
    c.key(3.5, ra=(-90, -20, 0), la=(-110, -34, 0), head=(-6, 0, 6), look=(0, .3))
    c.key(3.65, ra=(-108, -34, 0), la=(-86, -18, 0), head=(-4, 0, -6))
    c.key(3.85, ra=(-66, -34, 0), la=(-66, -34, 0), waist=(10, 0, 0), head=(12, 0, 0), look=(0, .6))
    c.key(4.3, waist=(4, 0, 0), head=(6, 0, 0), lid=.5)


@clip("count_for_hide_and_seek", "Counts for hide-and-seek", weight=2.5, require=["child"], mirror="never", length=6.8)
def _(c):
    eyes = dict(ra=(-128, -42, 0), la=(-128, -42, 0))
    c.key(0.4, **eyes, head=(10, 0, 0), waist=(6, 0, 0), lid=1)
    c.cycle(0.6, 3.0, .5, dict(head=(13, 0, 0), rl=(0, 0, 0)), dict(head=(6, 0, 0), rl=(-8, 0, 0)))
    c.key(3.0, **eyes)
    c.key(3.25, ra=(-98, -34, 0), head=(6, 14, 0), waist=(6, 0, -5), lid=0, look=(.8, 0))
    c.key(3.8, head=(4, 18, 0), look=(.8, .2))
    c.key(4.0, **eyes, head=(12, 0, 0), waist=(10, 0, 0), lid=1, look=(0, 0))
    c.cycle(4.15, 4.85, .35, dict(head=(14, 0, 0)), dict(head=(6, 0, 0)))
    c.key(4.8, **eyes)
    c.key(5.0, ra=(-30, 0, 30), la=(-30, 0, 30), head=(-6, 0, 0), waist=(0, 0, 0), root_pos=(0, -1.5, 0), lid=0)
    c.key(5.2, root_pos=(0, 0, 0))
    c.key(5.4, head=(-4, -22, 0), look=(-.7, 0))
    c.key(5.8, head=(-4, 22, 0), look=(.7, 0))
    c.key(6.2, ra=(-10, 0, 14), la=(-10, 0, 14), head=(-2, 6, 0), look=(.3, 0))


@clip("tantrum_stomp", "Throws a stomping tantrum", weight=2, require=["child"], mirror="never", length=4.8)
def _(c):
    c.key(0.25, ra=(10, 0, 14), la=(10, 0, 14), waist=(-4, 0, 0), head=(-8, 0, 0), lid=.5)
    for i, t in enumerate((0.55, 0.95, 1.3, 1.65)):
        leg, other = ("rl", "ll") if i % 2 == 0 else ("ll", "rl")
        c.key(t - .18, **{leg: (-40, 0, 4), other: (0, 0, 0)}, ra=(-12, 0, 18), la=(-12, 0, 18), waist=(0, 0, 0), root_pos=(0, -.6, 0), head=(2, 0, 0))
        c.key(t, **{leg: (0, 0, 0)}, ra=(24, 0, 6), la=(24, 0, 6), waist=(12, 0, 0), root_pos=(0, .8, 0), head=(14, 0, 0))
    c.key(1.85, ra=(20, 0, 12), la=(20, 0, 12), waist=(4, 0, 0), root_pos=(0, 0, 0))
    c.wobble(1.85, 2.4, 5, "head", 16, base=(8, 0, 0), axis=1)
    c.key(2.6, ra=(-64, -46, -6), la=(-56, -40, -6), waist=(-4, 0, 0), head=(-10, -26, 0), root=(0, -14, 0), lid=.55, look=(-.6, 0))
    c.key(3.2, head=(10, -30, 6), look=(.6, .3), lid=.45)
    c.key(3.55, head=(6, -30, 4), rl=(-30, 0, 4))
    c.key(3.75, head=(-14, -34, 0), rl=(0, 0, 0), root_pos=(0, .6, 0), lid=.75, look=(0, 0))
    c.key(4.0, root_pos=(0, 0, 0))
    c.key(4.2, ra=(-64, -46, -6), la=(-56, -40, -6), head=(4, -24, 0), root=(0, -14, 0), lid=.5, waist=(-2, 0, 0))


@clip("measure_my_height", "Measures their height", weight=2.5, require=["child"], length=5.4)
def _(c):
    c.key(0.4, ra=(-150, 0, 12), head=(-4, 0, 0))
    c.key(0.7, ra=(-164, 0, 14), look=(0, -.9))
    c.key(1.3, root_pos=(0, -2.4, 0), waist=(-3, 0, 0), la=(-6, 0, 14), head=(-6, 0, 0))
    c.key(1.7, root_pos=(0, -3, 0), la=(-10, 0, 26), lid=.3)
    c.wobble(1.7, 2.4, 4, "root", 2.5, axis=2)
    c.key(2.4, ra=(-164, 0, 14), la=(-10, 0, 26), root_pos=(0, -3, 0))
    c.key(2.7, root_pos=(0, 0, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(-2, 0, 0), lid=0, look=(0, -.6))
    c.key(3.1, ra=(-140, -4, 0), head=(-2, 10, 0), look=(.4, -.4))
    c.key(3.5, ra=(-140, -4, 0), head=(0, 10, 8), look=(.4, -.3))
    c.key(3.9, ra=(14, 0, 26), la=(14, 0, 26), waist=(-6, 0, 0), head=(-10, 0, 0), root_pos=(0, -.8, 0), lid=.45, look=(0, 0))
    c.key(4.1, root_pos=(0, 0, 0))
    c.key(4.7, ra=(14, 0, 26), la=(14, 0, 26), waist=(-5, 0, 0), head=(-8, 0, 0))


@clip("flap_like_a_bird", "Flaps like a bird", weight=3, require=["child"], mirror="never", length=4.8)
def _(c):
    c.key(0.3, ra=(-6, 0, 40), la=(-6, 0, 40), head=(-6, 0, 0), lid=.3)
    c.cycle(0.5, 2.3, .44, dict(ra=(-6, 0, 96), la=(-6, 0, 96), root_pos=(0, 0, 0), head=(-6, 0, 0)),
            dict(ra=(4, 0, 34), la=(4, 0, 34), root_pos=(0, -2, 0), head=(-2, 0, 0)))
    c.key(2.6, ra=(-4, 0, 80), la=(-4, 0, 80), root=(0, 0, 9), head=(-4, 0, -8))
    c.key(3.0, root=(0, 0, -9), head=(-4, 0, 8))
    c.key(3.3, ra=(28, 0, 24), la=(28, 0, 24), root=(0, 0, 0), waist=(22, 0, 0), head=(8, 0, 0), look=(0, .7), lid=0)
    c.cycle(3.45, 4.05, .25, dict(waist=(30, 0, 0), head=(22, 0, 0)), dict(waist=(22, 0, 0), head=(6, 0, 0)))
    c.key(4.25, waist=(4, 0, 0), head=(-4, 0, 0), ra=(10, 0, 20), la=(10, 0, 20), look=(0, 0))


@clip("make_silly_faces", "Makes silly faces", weight=3, require=["child"], mirror="never", length=5.0)
def _(c):
    c.key(0.4, ra=(-170, 0, 50), la=(-170, 0, 50), head=(0, 0, 0), lid=0)
    c.cycle(0.55, 2.0, .2, dict(ra=(-170, 10, 40), la=(-170, -10, 60)), dict(ra=(-170, -10, 60), la=(-170, 10, 40)))
    c.cycle(0.55, 2.0, .7, dict(head=(0, 0, 16), look=(.8, -.3)), dict(head=(0, 0, -16), look=(-.8, .4)))
    c.key(2.3, ra=(-104, -30, 10), la=(-104, -30, 10), head=(-12, 0, 0), waist=(-4, 0, 0), lid=.6, look=(0, 0))
    c.wobble(2.4, 3.0, 4, "head", 12, base=(-12, 0, 0), axis=1)
    c.key(3.2, ra=(-170, 0, 50), la=(-170, 0, 50), waist=(16, 0, 0), head=(-16, 0, 0), lid=0, look=(0, -.8))
    c.cycle(3.3, 4.0, .2, dict(ra=(-170, 10, 40), la=(-170, -10, 60)), dict(ra=(-170, -10, 60), la=(-170, 10, 40)))
    c.key(4.3, ra=(-113, -40, 0), la=(-104, -36, 0), waist=(8, 0, 0), head=(6, 0, 0), lid=.7, look=(0, 0))
    c.wobble(4.3, 4.6, 6, "root_pos", .4, axis=1)


@clip("march_like_a_soldier", "Marches like a soldier", weight=2.5, require=["child"], length=5.6)
def _(c):
    c.key(0.3, ra=(4, 0, 4), la=(4, 0, 4), head=(-8, 0, 0), waist=(-3, 0, 0), lid=.25)
    for i, t in enumerate((0.55, 1.0, 1.45, 1.9, 2.35, 2.8)):
        leg, other, arm, back = ("rl", "ll", "la", "ra") if i % 2 == 0 else ("ll", "rl", "ra", "la")
        c.key(t, **{leg: (-62, 0, 0), other: (0, 0, 0), arm: (-44, 0, 0), back: (26, 0, 0)}, root_pos=(0, -.8, 0))
        c.key(t + .22, **{leg: (0, 0, 0), arm: (-6, 0, 2), back: (6, 0, 2)}, root_pos=(0, .4, 0))
    c.key(3.25, ra=(2, 0, 2), la=(2, 0, 2), root_pos=(0, 0, 0), head=(-8, 0, 0))
    c.key(3.55, ra=(-145, -30, 10), head=(-10, 0, 0), waist=(-5, 0, 0), lid=.3)
    c.key(4.45, ra=(-146, -30, 10))
    c.key(4.7, ra=(0, 0, 4), head=(-6, 0, 0))
    c.key(5.0, head=(-2, 0, 0), waist=(-2, 0, 0), lid=0)
