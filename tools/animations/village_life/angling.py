"""Angling: fishermen (and residents whose hobby is fishing) fishing for real from a dock or the water's edge.

The server runs the fishing in phases and syncs the current one; the client plays an "angling" clip whose require
includes angling:<phase>, picks another clip from the same phase whenever one ends (so the long wait loops through
its variants) and cross-fades when the phase changes, the way the pet clips follow play:<phase>. The server's order
is cast, wait (10-40 s), bite, reel, then catch or lost, a short pause, and cast again.

During cast, wait, bite, reel and lost the resident holds a fishing rod in the RIGHT hand; during catch, the fish.
So no clip mirrors (the rod never changes hands) and every clip animates the item arm (items "override"). A standing
arm holding something already pitches -18 degrees (vanilla's held-item pose), so the rod arm is written with held()
as the total angle it reaches. Vanilla draws the rod pointing about 10 degrees above square to the arm, so the waiting
pose (the arm 28 degrees forward) leaves the rod tip out over the water about 38 degrees up. Clips start and end at
rest, which is the vanilla held-item pose, so the rod only dips a few degrees between one clip and the next. When the
waist leans, rod() takes the lean back off the arm so the rod stays where it was.
"""
from kit import clip

ITEM = -18                 # vanilla's held-item pose for a standing arm
ROD_PITCH, ROD_YAW = -28, -5   # the waiting rod: arm a little forward and in, tip out over the water


def held(pitch, yaw=0, roll=0):
    """The item arm as the total angle it reaches, on top of the held-item pose."""
    return (pitch - ITEM, yaw, roll)


def rod(pitch=ROD_PITCH, yaw=ROD_YAW, lean=0, turn=0):
    """The rod arm at a pitch (and yaw) measured against the ground, whatever the waist is doing.

    lean and turn are the waist's pitch and yaw at the same moment; the arm takes them back off."""
    return held(pitch - lean, yaw - turn)


def angling(phase, id, name, length, weight=1, **options):
    return clip(f"angling_{id}", name, trigger="angling", length=length, weight=weight,
                require=[f"angling:{phase}"], mirror="never", items="override", **options)


WATCH = dict(head=(14, 0, 0), look=(0, .4))       # eyes on the float
HIP = (14, 0, 26)                                 # free hand on the hip
GRIP = (-54, -56, 0)                              # free hand across to the rod, just above the right fist
STAGGER = dict(rl=(-6, 0, 3), ll=(7, 0, 3))      # braced, one foot ahead


# -- cast --------------------------------------------------------------------------------------

@angling("cast", "cast_overhead", "Casts the line overhead", 1.7, weight=3, blend=(.15, .3))
def _(c):
    c.key(0.38, ra=rod(-126, -2, lean=-8, turn=8), la=(-28, 0, 14), waist=(-8, 8, 0), head=(-8, 4, 0),
          look=(0, -.3), root_pos=(0, 0, .3))
    c.key(0.52, ra=rod(-132, -2, lean=-9, turn=8), waist=(-9, 8, 0))
    c.key(0.74, ra=rod(-48, -6, lean=10, turn=-6), la=(-10, 0, 10), waist=(10, -6, 0), head=(2, -2, 0),
          look=(0, 0), root_pos=(0, 0, -.4))
    c.key(0.9, ra=rod(-36, -6, lean=8, turn=-4), waist=(8, -4, 0))
    c.key(1.15, ra=rod(-32, -6, lean=4), waist=(4, 0, 0), head=(-4, 0, 0), look=(0, -.2), root_pos=(0, 0, -.1))
    c.key(1.4, ra=rod(lean=2), waist=(2, 0, 0), **WATCH)


@angling("cast", "cast_sidearm", "Flicks a sidearm cast", 1.6, weight=2, blend=(.15, .3))
def _(c):
    c.key(0.36, ra=rod(-48, 52, turn=20), la=(-18, 0, 18), waist=(0, 20, 0), head=(2, 8, 0), look=(.3, .2))
    c.key(0.54, ra=rod(-50, 62, turn=24), waist=(-2, 24, 0), head=(2, 12, 0))
    c.key(0.78, ra=rod(-40, -16, lean=6, turn=-10), la=(-24, -8, 10), waist=(6, -10, 0), head=(2, -4, 0),
          look=(0, 0), root_pos=(0, 0, -.3))
    c.key(0.96, ra=rod(-32, -9, lean=4, turn=-4), waist=(4, -4, 0))
    c.key(1.25, ra=rod(lean=2), la=(-6, 0, 6), waist=(2, 0, 0), root_pos=(0, 0, 0), **WATCH)


# -- wait --------------------------------------------------------------------------------------
# Low energy: the free (left) arm and the head move, the rod arm holds still.

@angling("wait", "wait_still", "Waits for a bite", 6.5, weight=3, blend=(.5, .5))
def _(c):
    c.key(0.7, ra=rod(lean=2), waist=(2, 0, 0), head=(14, 2, 0), look=(0, .4))
    c.key(2.0, root=(0, 0, 1.6), waist=(2, 2, -2), ra=rod(lean=2, turn=2), rl=(-3, 6, 2), ll=(0, 0, -1),
          head=(15, 0, 3))
    c.key(3.0, head=(15, -2, 3), lid=.3)
    c.key(3.5, lid=.05)
    c.key(4.6, root=(0, 0, 0), waist=(2, 0, 0), ra=rod(lean=2), rl=(0, 0, 0), ll=(0, 0, 0), head=(14, 2, 0))
    c.key(5.2, head=(14, -1, -1), look=(-.1, .4), lid=0)
    c.key(5.9, ra=rod(lean=2), waist=(2, 0, 0), head=(13, 0, 0), look=(0, .35))


@angling("wait", "wait_look_around", "Glances along the bank", 5.6, weight=2, blend=(.45, .5))
def _(c):
    c.key(0.6, ra=rod(), **WATCH)
    c.key(1.5, head=(2, -32, -2), look=(-.5, 0))
    c.key(2.5, head=(0, -38, -3), look=(-.6, .1))
    c.key(3.6, head=(3, 30, 2), look=(.5, 0))
    c.key(4.4, head=(1, 34, 3), look=(.6, .05))
    c.key(5.1, ra=rod(), **WATCH)


@angling("wait", "wait_scratch_head", "Tugs the hat and scratches the head", 4.8, weight=1.5, blend=(.4, .45))
def _(c):
    c.key(0.6, ra=rod(), head=(12, 0, 0), look=(0, .35))
    c.key(1.1, la=(-150, -30, 0), head=(6, 0, 0), look=(0, .1))
    c.key(1.32, la=(-156, -28, 0), head=(9, 0, 0))
    c.key(1.55, la=(-150, -30, 0), head=(7, 0, 0))
    c.key(2.0, la=(-164, 0, 14), head=(4, -8, 10), look=(-.2, -.4))
    c.wobble(2.1, 3.3, 5, "la", 7, base=(-164, 0, 14), axis=1)
    c.key(3.4, head=(6, -10, 12))
    c.key(3.95, la=(-40, 0, 6), head=(12, 0, 0), look=(0, .35))
    c.key(4.35, ra=rod(), la=(0, 0, 0), head=(12, 0, 0))


@angling("wait", "wait_stretch", "Stretches the free arm", 5.0, weight=1, boost={"morning": 2}, blend=(.4, .45))
def _(c):
    c.key(0.6, ra=rod(), head=(12, 0, 0), look=(0, .35))
    c.key(1.2, la=(-36, 0, 70), head=(4, 0, 0), look=(0, 0))
    c.key(1.9, la=(-12, 0, 152), head=(-16, 0, -4), waist=(-4, 0, -3), ra=rod(lean=-4), root_pos=(0, -.6, 0), lid=.75)
    c.key(2.7, la=(-10, 0, 160), head=(-20, 0, -6), waist=(-5, 0, -4), ra=rod(lean=-5), root_pos=(0, -.8, 0), lid=.85)
    c.key(3.3, la=(-8, 0, 58), head=(8, 0, 0), waist=(0, 0, 0), ra=rod(), root_pos=(0, 0, 0), lid=.2)
    c.key(3.9, la=(0, 0, 6), head=(12, 0, 0), look=(0, .35), lid=0)
    c.key(4.4, ra=rod(), la=(0, 0, 0))


@angling("wait", "wait_yawn", "Yawns over the water", 4.4, weight=1, boost={"morning": 2, "evening": 2, "night": 3},
         blend=(.4, .45))
def _(c):
    c.key(0.6, ra=rod(), head=(10, 0, 0), look=(0, .3))
    c.key(1.1, head=(-10, 0, -4), la=(-88, -30, 0), waist=(-3, 0, 0), ra=rod(lean=-3), lid=.5)
    c.key(1.6, head=(-20, 0, -6), la=(-113, -40, 0), waist=(-5, 0, 0), ra=rod(lean=-5), lid=1)
    c.key(2.4, head=(-22, 0, -6), la=(-115, -42, 0), lid=1)
    c.key(2.9, head=(8, 0, 0), la=(-18, 0, 6), waist=(1, 0, 0), ra=rod(lean=1), lid=.4)
    c.key(3.2, head=(10, 7, 0), lid=.25)
    c.key(3.45, head=(10, -6, 0))
    c.key(3.7, head=(12, 0, 0), look=(0, .35), la=(0, 0, 0), waist=(0, 0, 0), lid=0)
    c.key(3.95, ra=rod())


@angling("wait", "wait_tap_foot", "Taps a foot while waiting", 4.2, weight=1.5, blend=(.4, .45))
def _(c):
    c.key(0.5, ra=rod(), la=HIP, head=(12, -4, 0), look=(0, .35))
    c.cycle(0.7, 3.2, .4, dict(ll=(-13, 0, 3), head=(11, -4, 1)), dict(ll=(-1, 0, 3), head=(13, -4, -1)), end_on="b")
    c.key(3.5, la=(4, 0, 8), head=(13, 0, 0))
    c.key(3.75, ra=rod(), la=(0, 0, 0), ll=(0, 0, 0))


@angling("wait", "wait_jig", "Jiggles the rod tip to tempt a fish", 4.6, weight=2, blend=(.4, .45))
def _(c):
    lean = 3
    c.key(0.5, ra=rod(lean=lean), waist=(lean, 0, 0), head=(16, 0, 0), look=(0, .45))
    c.wobble(0.9, 1.9, 4, "ra", 3, base=rod(lean=lean), axis=0)
    c.key(2.2, head=(17, 0, 4), lid=.2)
    c.wobble(2.5, 3.4, 3, "ra", 4, base=rod(lean=lean), axis=0)
    c.key(3.7, head=(16, 0, 0), lid=0)
    c.key(4.0, ra=rod(lean=lean), waist=(lean, 0, 0), head=(14, 0, 0), look=(0, .4))


# -- bite --------------------------------------------------------------------------------------

@angling("bite", "bite_jolt", "Jolts at a bite", 1.0, weight=2, blend=(.06, .2))
def _(c):
    c.key(0.12, ra=rod(-46, -8), la=(-34, 0, 22), head=(4, 0, 0), look=(0, .5), root_pos=(0, -.6, 0))
    c.key(0.24, root_pos=(0, 0, 0))
    c.key(0.42, ra=rod(-44, -14, lean=14), la=GRIP, waist=(14, 0, 0), head=(16, 0, 0), look=(0, .6),
          root_pos=(0, 0, -.4), **STAGGER)
    c.key(0.8, ra=rod(-42, -14, lean=16), la=GRIP, waist=(16, 0, 0), head=(18, 0, 0))


@angling("bite", "bite_grip", "Leans in and grips the rod with both hands", 1.2, weight=1, blend=(.12, .2))
def _(c):
    # The fish tugs the rod tip down twice; they hold on and pull it back up.
    c.key(0.18, ra=rod(-40, -14, lean=10), la=GRIP, waist=(10, 0, 0), head=(14, 0, 0), look=(0, .6), **STAGGER)
    c.key(0.36, ra=rod(-30, -14, lean=14), waist=(14, 0, 0), head=(17, 0, 0), root_pos=(0, 0, -.4))
    c.key(0.56, ra=rod(-44, -14, lean=11), waist=(11, 0, 0))
    c.key(0.74, ra=rod(-32, -14, lean=14), waist=(14, 0, 0), head=(17, 0, 0))
    c.key(0.98, ra=rod(-42, -14, lean=11), la=GRIP, waist=(11, 0, 0), head=(15, 0, 0), root_pos=(0, 0, -.2))


# -- reel --------------------------------------------------------------------------------------

def crank(c, start, end, step, base=GRIP):
    """The free hand winding the reel: small circles beside the right fist."""
    p, y, r = base
    loop = [(p - 6, y, r), (p, y + 7, r), (p + 6, y, r), (p, y - 6, r)]
    t, i = start, 0
    while t < end - 1e-6:
        c.key(t, la=loop[i % 4])
        t, i = t + step, i + 1
    c.key(end, la=base)


@angling("reel", "reel_haul", "Hauls back and reels in", 3.6, weight=2, blend=(.2, .35))
def _(c):
    c.key(0.3, ra=rod(-66, -14, lean=-8), la=GRIP, waist=(-8, 0, 0), head=(4, 0, 0), look=(0, .2), **STAGGER)
    # Pump: haul the rod tip up while leaning back, then drop it forward and wind in the slack.
    c.key(0.8, ra=rod(-84, -12, lean=-14), waist=(-14, 0, 0), head=(-2, 0, 0), look=(0, 0),
          rl=(10, 0, 3), ll=(4, 0, 3), root_pos=(0, 0, .4))
    c.key(1.2, rl=(-2, 0, 3), ll=(7, 0, 3))
    c.key(1.5, ra=rod(-62, -14, lean=-4), waist=(-4, 0, 0), head=(6, 0, 0), look=(0, .3), root_pos=(0, 0, .2))
    crank(c, 0.95, 1.5, .09)
    c.key(2.1, ra=rod(-84, -12, lean=-14), waist=(-14, 0, 0), head=(-2, 0, 0), look=(0, 0),
          rl=(-6, 0, 3), ll=(14, 0, 3), root_pos=(0, 0, .6))
    c.key(2.5, ll=(7, 0, 3))
    c.key(2.8, ra=rod(-64, -14, lean=-5), waist=(-5, 0, 0), head=(6, 0, 0), look=(0, .3), root_pos=(0, 0, .3))
    crank(c, 2.25, 3.0, .09)
    c.key(3.25, ra=rod(-48, -10, lean=-2), waist=(-2, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0))


@angling("reel", "reel_crank", "Cranks the reel with the rod tip high", 3.0, weight=2, blend=(.2, .35))
def _(c):
    lean = -10
    c.key(0.3, ra=rod(-70, -14, lean=lean), la=GRIP, waist=(lean, 0, 0), head=(6, 0, 0), look=(0, .4), **STAGGER)
    crank(c, 0.4, 2.6, .08)
    c.key(0.9, root=(0, 0, 2), head=(6, 4, -2), ra=rod(-73, -14, lean=lean))
    c.key(1.5, root=(0, 0, -2), head=(7, -4, 2), ra=rod(-67, -14, lean=lean), lid=.3)
    c.key(2.1, root=(0, 0, 1.5), head=(6, 3, -2), ra=rod(-72, -14, lean=lean))
    c.key(2.6, ra=rod(-68, -14, lean=lean), root=(0, 0, 0), waist=(lean, 0, 0), head=(6, 0, 0), lid=0, **STAGGER)


@angling("reel", "reel_fight", "Fights the fish side to side", 3.8, weight=1.5, blend=(.2, .35))
def _(c):
    lean = -8
    c.key(0.3, ra=rod(-72, -14, lean=lean), la=GRIP, waist=(lean, 0, 0), head=(6, 0, 0), look=(0, .3), **STAGGER)
    # The fish runs to their left, then to their right; the rod follows and they step after it.
    c.key(0.9, ra=rod(-70, -14, lean=lean, turn=-12), waist=(lean, -12, 0), head=(8, -14, 0), look=(-.4, .3),
          rl=(-2, 0, 6), ll=(6, 0, 2), lid=.3)
    crank(c, 1.0, 1.5, .1)
    c.key(1.7, ra=rod(-78, -14, lean=-12), waist=(-12, 0, 0), head=(2, 0, 0), look=(0, .1), **STAGGER)
    c.key(2.4, ra=rod(-70, -14, lean=lean, turn=12), waist=(lean, 12, 0), head=(8, 14, 0), look=(.4, .3),
          rl=(6, 0, 2), ll=(-2, 0, 6))
    crank(c, 2.5, 3.0, .1)
    c.key(3.3, ra=rod(-64, -14, lean=-6), waist=(-6, 0, 0), head=(6, 0, 0), look=(0, .3), lid=0,
          rl=(0, 0, 0), ll=(0, 0, 0))


# -- catch: the fish in the right hand ---------------------------------------------------------

@angling("catch", "catch_admire", "Holds the catch up and admires it", 2.6, weight=2, blend=(.25, .35))
def _(c):
    # Held up beside the face rather than in front of it, so the resident turns to look at it.
    c.key(0.5, ra=held(-104, 12, 0), la=(-8, 0, 8), head=(-8, 18, 0), look=(.4, -.3))
    c.key(0.95, ra=held(-106, 16, 0), head=(-9, 20, 8), lid=.25)
    c.key(1.35, ra=held(-102, 8, 0), head=(-7, 14, -4))
    c.key(1.6, head=(2, 14, 0), lid=.4)
    c.key(1.8, head=(-7, 14, 0))
    c.key(2.0, head=(1, 12, 0), lid=.35)
    c.key(2.25, ra=held(-70, 0, 0), head=(4, 4, 0), lid=.2, look=(0, 0))


@angling("catch", "catch_show_off", "Shows off the catch", 2.8, weight=1.5, blend=(.25, .35))
def _(c):
    c.key(0.4, ra=held(-150, 8, 8), la=(-10, 0, 26), head=(-16, 0, 0), look=(0, -.5), root_pos=(0, -.7, 0), lid=.2)
    c.key(0.7, root_pos=(0, 0, 0))
    c.key(1.15, ra=held(-146, 10, 8), la=HIP, waist=(0, 18, 0), head=(-6, 20, 0), look=(.5, 0), lid=.3)
    c.key(1.8, ra=held(-146, 6, 8), waist=(0, -14, 0), head=(-6, -18, 0), look=(-.5, 0))
    c.key(2.2, ra=held(-100, -10, 0), waist=(0, 0, 0), head=(4, 0, 0), look=(0, 0), lid=.4)
    c.key(2.45, head=(-2, 0, 0), la=(4, 0, 10))


@angling("catch", "catch_weigh", "Weighs the catch in hand and nods", 2.4, weight=1.5, blend=(.25, .35))
def _(c):
    # In front of the right shoulder, bobbed a few times to feel the weight.
    c.key(0.4, ra=held(-70, 8, 0), head=(16, 12, 0), look=(.3, .4))
    c.key(0.62, ra=held(-80, 8, 0))
    c.key(0.8, ra=held(-66, 8, 0))
    c.key(0.98, ra=held(-78, 8, 0))
    c.key(1.15, ra=held(-70, 8, 0), lid=.3)
    c.key(1.4, head=(24, 10, 0))
    c.key(1.6, head=(11, 10, 0))
    c.key(1.8, head=(22, 10, 0), lid=.4)
    c.key(2.05, ra=held(-50, 0, 0), head=(6, 2, 0), lid=.2, look=(0, .1))


# -- lost: the line goes slack -----------------------------------------------------------------

@angling("lost", "lost_slump", "Slumps as the line goes slack", 2.3, weight=1, blend=(.2, .35))
def _(c):
    c.key(0.3, ra=rod(-52, -8), head=(-4, 0, 0), look=(0, -.2), la=(-12, 0, 8))
    c.key(0.8, ra=rod(-16, -6, lean=14), waist=(14, 0, 0), head=(22, 0, 0), look=(0, .5), la=(0, 0, 0),
          root_pos=(0, .3, 0), lid=.3)
    c.key(1.1, head=(21, 12, 0), lid=.45)
    c.key(1.35, head=(21, -12, 0))
    c.key(1.6, head=(21, 9, 0))
    c.key(1.85, ra=rod(-18, -6, lean=12), waist=(12, 0, 0), head=(20, 0, 0), lid=.55)


@angling("lost", "lost_shrug", "Shrugs off the one that got away", 2.0, weight=1, blend=(.2, .35))
def _(c):
    c.key(0.3, ra=rod(-36, -6), head=(8, 10, 0), look=(.2, .3))
    c.key(0.65, ra=rod(-30, -6), la=(-26, 16, 18), la_pos=(0, -1.4, 0), ra_pos=(0, -1.2, 0), head=(4, 0, 10),
          waist=(-2, 0, 0), look=(0, 0))
    c.key(1.15, la_pos=(0, -1.5, 0), ra_pos=(0, -1.3, 0), head=(4, 0, 11))
    c.key(1.55, ra=rod(), la=(0, 0, 2), la_pos=(0, .3, 0), ra_pos=(0, 0, 0), head=(12, 0, 4), waist=(0, 0, 0), lid=.4)
    c.key(1.75, la_pos=(0, 0, 0), head=(13, -4, 0), lid=.2)
