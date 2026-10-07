"""Children's play. Positions are adult model pixels; children scale them to their size."""
from kit import clip


@clip("hop_in_place", "Hops", weight=4, require=["child"], mirror="never", length=2.7)
def _(c):
    for i, t in enumerate((0.3, 0.8, 1.3)):
        c.key(t - .1, root_pos=(0, .8, 0), ra=(-10, 0, 10), la=(-10, 0, 10))
        c.key(t + .1, root_pos=(0, -5, 0), ra=(-30, 0, 46), la=(-30, 0, 46), head=(-8, 0, 0))
        c.key(t + .32, root_pos=(0, 0, 0), ra=(-6, 0, 12), la=(-6, 0, 12), head=(2, 0, 0))
    c.hold(0.2, 1.8, lid=.35)


@clip("twirl", "Twirls", weight=3, require=["child"], mirror="free", length=2.6, blend=(0, 0))
def _(c):
    c.key(0.25, root=(0, 20, 0), ra=(-20, 0, 70), la=(-20, 0, 70), head=(-10, 0, 0), lid=.4)
    c.key(0.75, root=(0, 180, 0))
    c.key(1.25, root=(0, 330, 0), ra=(-20, 0, 82), la=(-20, 0, 82))
    c.key(1.5, root=(0, 360, 0), ra=(-10, 0, 40), la=(-10, 0, 40))
    c.key(1.8, root=(0, 360, 4), head=(0, 0, 10))
    c.key(2.1, root=(0, 360, -4), head=(0, 0, -10))
    c.key(2.6, root=(0, 360, 0), head=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), lid=0)


@clip("play_airplane", "Plays airplane", weight=3, require=["child"], mirror="free", length=3.8)
def _(c):
    c.key(0.4, ra=(0, 0, 88), la=(0, 0, 88), head=(-6, 0, 0))
    c.cycle(0.6, 3.2, 1.3, dict(waist=(6, 10, 14), root=(0, 18, 0), head=(-6, 0, -10)),
            dict(waist=(6, -10, -14), root=(0, -18, 0), head=(-6, 0, 10)))
    c.cycle(0.6, 3.2, .4, dict(rl=(-16, 0, 0), ll=(12, 0, 0), root_pos=(0, -.8, 0)),
            dict(rl=(12, 0, 0), ll=(-16, 0, 0), root_pos=(0, 0, 0)))
    c.key(3.3, ra=(0, 0, 70), la=(0, 0, 70), lid=0)
    c.hold(0.6, 3.0, lid=.3)


@clip("peekaboo", "Peekaboo!", weight=2, require=["child"], mirror="never", length=2.9)
def _(c):
    c.key(0.4, ra=(-128, -42, 0), la=(-128, -42, 0), head=(8, 0, 0), lid=1)
    c.key(1.3, ra=(-130, -42, 0), la=(-130, -42, 0), head=(10, 0, 0), lid=1)
    c.key(1.5, ra=(-40, 0, 72), la=(-40, 0, 72), head=(-10, 0, 0), root_pos=(0, -3, 0), lid=0)
    c.key(1.75, root_pos=(0, 0, 0))
    c.key(2.2, ra=(-36, 0, 66), la=(-36, 0, 66), head=(-6, 0, 6))


@clip("watch_a_bug", "Watches a bug", weight=2, require=["child"], length=4.8)
def _(c):
    squat = dict(rl=(-62, 0, 10), ll=(-62, 0, 10), root_pos=(0, 6, 0), waist=(30, 0, 0), head=(26, 0, 0),
                 ra=(-40, 0, 6), la=(-36, 0, 6), look=(0, .9))
    c.key(0.6, **squat)
    for t in (1.5, 2.4):
        c.key(t, ra=(-72, -4, 0)).key(t + .2, ra=(-52, -4, 0))
    c.key(3.1, head=(26, 0, 12), look=(.3, .8))
    c.key(3.8, **squat)


@clip("chase_tag", "Wants to play tag", weight=2, require=["child"], mirror="free", length=2.4)
def _(c):
    c.key(0.3, waist=(10, 0, 0), ra=(-60, 30, 30), la=(-50, 20, 20), rl=(-14, 0, 6), ll=(10, 0, 6), lid=.3)
    c.cycle(0.45, 1.7, .4, dict(root_pos=(0, -1.6, 0), head=(-6, 12, 0)), dict(root_pos=(0, 0, 0), head=(-4, -12, 0)))
    c.key(1.9, waist=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), lid=0)
