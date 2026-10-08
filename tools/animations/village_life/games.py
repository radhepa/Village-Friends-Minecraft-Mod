"""Games the children play together (Playground.java): tag, hide-and-seek, ring-around-the-rosie, follow the
leader and catch, and a bored child tagging along behind a player. These clips use the ``play`` trigger: the
director plays them on the reaction layer whenever a child's part in a game changes, and again each time one
ends while the part lasts, so they keep their upper body while the child runs about.

Tags: ``play:<game>``, ``play:<game>:<role>`` and the full state (``play:follow_the_leader:do:hop``); ``moving``
while the child is on the move. Leader moves must keep the lengths in Games.Move (ticks / 20).
"""
from kit import clip, HANDS_BEHIND, HAND_TO_CHIN, HAND_TO_MOUTH, SHIELD_EYES

SQUAT = dict(rl=(-62, 0, 10), ll=(-62, 0, 10), root_pos=(0, 6, 0), waist=(30, 0, 0), head=(-6, 0, 0))
EYES_COVERED = dict(ra=(-128, -42, 0), la=(-128, -42, 0))
V_ARMS = dict(ra=(-10, 0, 160), la=(-10, 0, 160))


def play(*tags, moving=None, **options):
    """A play clip for children with these tags; ``moving`` True/False requires or avoids being on the move."""
    require = ["child", *tags]
    avoid = list(options.pop("avoid", []))
    if moving is True:
        require.append("moving")
    elif moving is False:
        avoid.append("moving")
    return dict(trigger="play", require=require, avoid=avoid, **options)


# -- tag --------------------------------------------------------------------------------------------

@clip("tag_count", "Counts to three", **play("play:tag:count|play:tag:tagged", length=2.0, weight=3))
def _(c):
    for i, t in enumerate((0.35, 0.95, 1.55)):
        c.key(t, ra=(-104 - i * 6, -12, 4), head=(10, 0, 0), lid=.5)
        c.key(t + .25, ra=(-94 - i * 6, -12, 4), head=(2, 0, 0), lid=.2)
    c.key(1.85, ra=(-40, 0, 10), head=(-6, 0, 0), lid=0)


@clip("tag_chase", "Chases with arms out", **play("play:tag:it", moving=True, length=1.2, weight=3, mirror="free"))
def _(c):
    c.cycle(0.1, 1.1, .5, dict(ra=(-92, 8, 8), la=(-70, 8, 8), head=(-8, 0, 0), waist=(10, 0, 0)),
            dict(ra=(-70, 8, 8), la=(-92, 8, 8), head=(-8, 0, 0), waist=(10, 0, 0)))


@clip("tag_it_wait", "Looks for someone to tag", **play("play:tag:it", moving=False, length=2.2, weight=2))
def _(c):
    crouch = dict(waist=(16, 0, 0), ra=(-50, 30, 40), la=(-50, 30, 40), rl=(-20, 0, 8), ll=(-20, 0, 8), root_pos=(0, 2, 0))
    c.key(0.3, **crouch, head=(-10, 20, 0))
    c.key(1.0, head=(-10, -24, 0))
    c.key(1.6, head=(-10, 18, 0))
    c.key(2.0, **crouch, head=(-6, 0, 0))


@clip("tag_flee", "Runs away squealing", **play("play:tag:run", moving=True, length=1.0, weight=3, mirror="free"))
def _(c):
    c.cycle(0.08, 0.92, .42, dict(ra=(-160, 0, 20), la=(-110, 0, 30), head=(-12, 0, 6)),
            dict(ra=(-110, 0, 30), la=(-160, 0, 20), head=(-12, 0, -6)))
    c.hold(0.1, 0.9, lid=.3)


@clip("tag_taunt", "Can't catch me!", **play("play:tag:run", moving=False, length=2.4, weight=3, mirror="free"))
def _(c):
    ears = dict(ra=(-125, -15, 38), la=(-125, -15, 38))
    c.key(0.25, **ears, head=(0, 0, 8), lid=.4)
    c.wobble(0.3, 1.5, 4, "ra", 10, base=(-125, -15, 38), axis=1)
    c.wobble(0.3, 1.5, 4, "la", 10, base=(-125, -15, 38), axis=1)
    for t, side in ((0.4, 1), (0.9, -1), (1.4, 1)):
        c.key(t, root_pos=(side * .5, -2.5, 0), head=(0, 0, 10 * side), rl=(-10, 0, 10), ll=(-10, 0, 10))
        c.key(t + .22, root_pos=(side * .5, 0, 0))
    c.key(1.8, ra=(-30, 0, 20), la=(-30, 0, 20), root_pos=(0, 0, 0), head=(4, 0, 0), lid=0, rl=(0, 0, 0), ll=(0, 0, 0))


# -- hide-and-seek ----------------------------------------------------------------------------------

@clip("hide_count", "Counts with eyes covered", **play("play:hide_and_seek:count", length=3.2, weight=3, mirror="never"))
def _(c):
    c.key(0.35, **EYES_COVERED, head=(14, 0, 0), lid=1)
    c.cycle(0.5, 2.8, .8, dict(head=(16, 0, 3), rl=(0, 0, 2)), dict(head=(12, 0, -3), rl=(-12, 0, 2)))
    c.hold(0.5, 2.8, lid=1)
    c.key(2.9, **EYES_COVERED, head=(14, 0, 0))


@clip("hide_sneak", "Tiptoes off to hide", **play("play:hide_and_seek:hide", moving=True, length=1.3, weight=3))
def _(c):
    c.cycle(0.1, 1.2, .6, dict(waist=(16, 0, 0), ra=(-48, -10, 16), la=(-36, -10, 16), head=(-14, 14, 0)),
            dict(waist=(16, 0, 0), ra=(-36, -10, 16), la=(-48, -10, 16), head=(-14, -14, 0)))


@clip("hide_hidden", "Giggles in hiding", **play("play:hide_and_seek:hidden", length=3.6, weight=3))
def _(c):
    c.key(0.5, **SQUAT, **HAND_TO_MOUTH, la=(-30, 0, 8), lid=.3)
    c.wobble(0.9, 2.6, 6, "body", 3, axis=2)
    c.key(2.8, **SQUAT, **HAND_TO_MOUTH, lid=.4)
    c.key(3.3, **SQUAT, ra=(-30, 0, 8), lid=0)


@clip("hide_peek", "Peeks out from hiding", **play("play:hide_and_seek:hidden", length=3.0, weight=2, mirror="free"))
def _(c):
    c.key(0.4, **SQUAT, ra=(-26, 0, 6), la=(-26, 0, 6))
    c.key(1.0, waist=(24, 0, -18), head=(-10, 0, -20), look=(-.6, 0), root_pos=(-.5, 6, 0))
    c.key(1.8, waist=(24, 0, -18), head=(-10, 10, -20), look=(-.5, 0))
    c.key(2.3, **SQUAT, look=(0, 0))
    c.key(2.7, **SQUAT)


@clip("hide_seek_scan", "Searches high and low", **play("play:hide_and_seek:seek", length=2.4, weight=3, mirror="hand"))
def _(c):
    c.key(0.3, **SHIELD_EYES, head=(-4, 26, 0))
    c.key(1.1, head=(-4, -26, 0))
    c.key(1.7, head=(6, 10, 0))
    c.key(2.1, **SHIELD_EYES, head=(0, 0, 0))


@clip("hide_seek_peer", "Peers behind things", **play("play:hide_and_seek:seek", moving=False, length=2.6, weight=2, mirror="free"))
def _(c):
    c.key(0.5, waist=(26, 0, 16), head=(-14, -10, 14), ra=(-20, 0, 30), la=(-10, 0, 10), look=(.5, 0))
    c.key(1.3, waist=(26, 0, -16), head=(-14, 10, -14), ra=(-10, 0, 10), la=(-20, 0, 30), look=(-.5, 0))
    c.key(2.0, waist=(10, 0, 0), head=(0, 0, 0), look=(0, 0))


@clip("hide_point", "Found you!", **play("play:hide_and_seek:point", length=1.5, weight=3))
def _(c):
    c.key(0.2, ra=(-90, 0, 0), head=(-6, 0, 0), root_pos=(0, 1, 0), lid=.2)
    c.key(0.45, ra=(-96, 0, 0), root_pos=(0, -3.5, 0), la=(-10, 0, 40))
    c.key(0.75, ra=(-90, 0, 0), root_pos=(0, 0, 0))
    c.wobble(0.8, 1.2, 4, "ra", 6, base=(-90, 0, 0), axis=0)


@clip("hide_found", "Aww found!", **play("play:hide_and_seek:found", length=2.0, weight=3))
def _(c):
    c.key(0.25, ra=(-160, -30, 14), la=(-160, -30, 14), head=(-10, 0, 0), lid=.5)
    c.wobble(0.3, 1.2, 5, "body", 3, axis=2)
    c.key(1.4, ra=(-20, 20, 24), la=(-20, 20, 24), head=(0, 0, 10), lid=.2)
    c.key(1.8, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("hide_home", "Waits at home base", **play("play:hide_and_seek:home", length=3.0, weight=3))
def _(c):
    c.key(0.4, **HANDS_BEHIND)
    c.cycle(0.4, 2.6, .5, dict(root_pos=(0, -.8, 0), rl=(-4, 0, 0), ll=(-4, 0, 0), head=(-4, 8, 0)),
            dict(root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), head=(-4, -8, 0)))
    c.key(2.7, **HANDS_BEHIND)


@clip("hide_won", "Wins hide-and-seek", **play("play:hide_and_seek:won", length=2.2, weight=3, mirror="never"))
def _(c):
    c.key(0.25, **V_ARMS, root_pos=(0, 1, 0), lid=.3)
    for t in (0.45, 1.05):
        c.key(t, root_pos=(0, -4.5, 0), head=(-12, 0, 0))
        c.key(t + .3, root_pos=(0, 0, 0), head=(-4, 0, 0))
    c.key(1.7, ra=(-10, 0, 120), la=(-10, 0, 120))
    c.key(2.0, ra=(0, 0, 0), la=(0, 0, 0), lid=0)


# -- ring-around-the-rosie --------------------------------------------------------------------------

@clip("ring_walk", "Skips round in a ring holding hands", **play("play:ring:walk|play:ring:join", length=1.0, weight=3, mirror="never"))
def _(c):
    hands = dict(ra=(-14, 0, 52), la=(-14, 0, 52))
    c.key(0.1, **hands, lid=.2)
    c.cycle(0.1, 0.9, .5, dict(**hands, root_pos=(0, -1.2, 0), head=(-4, 0, 4)), dict(**hands, root_pos=(0, 0, 0), head=(-2, 0, -4)))
    c.key(0.95, **hands)


@clip("ring_fall", "All fall down!", **play("play:ring:fall", length=3.4, weight=3, mirror="never", blend=(.15, .4)))
def _(c):
    sit = dict(rl=(-84, 0, 12), ll=(-84, 0, 12), root_pos=(0, 6.5, 0), waist=(-14, 0, 0), ra=(28, 0, 26), la=(28, 0, 26))
    c.key(0.3, ra=(-10, 0, 150), la=(-10, 0, 150), root_pos=(0, -1, 0), head=(-10, 0, 0), lid=.3)
    c.key(0.62, **sit, head=(-16, 0, 0), lid=.6)
    c.wobble(0.8, 2.3, 5, "head", 6, base=(-12, 0, 0), axis=2)
    c.key(2.5, **sit, head=(-6, 0, 0), lid=.3)
    c.key(3.0, rl=(-30, 0, 4), ll=(-30, 0, 4), root_pos=(0, 3, 0), waist=(20, 0, 0), ra=(-20, 0, 10), la=(-20, 0, 10), lid=0)


# -- follow the leader ------------------------------------------------------------------------------

@clip("leader_march", "Marches proudly", **play("play:follow_the_leader:lead|play:follow_the_leader:follow", length=1.45, weight=3, mirror="never"))
def _(c):
    c.cycle(0.12, 1.32, 1.2, dict(ra=(-46, 0, 6), la=(40, 0, 6), head=(-8, 0, 0), rl=(-30, 0, 0), ll=(6, 0, 0)),
            dict(ra=(40, 0, 6), la=(-46, 0, 6), head=(-8, 0, 0), rl=(6, 0, 0), ll=(-30, 0, 0)))


@clip("copy_hop", "Bunny hops", **play("play:follow_the_leader:do:hop", length=2.7, weight=1, mirror="never"))
def _(c):
    paws = dict(ra=(-70, -30, 0), la=(-70, -30, 0))
    c.key(0.25, **paws, root_pos=(0, 1.5, 0), rl=(-14, 0, 0), ll=(-14, 0, 0))
    for t in (0.5, 1.05, 1.6):
        c.key(t, root_pos=(0, -5, 0), rl=(6, 0, 0), ll=(6, 0, 0), head=(-6, 0, 0))
        c.key(t + .27, root_pos=(0, 1.5, 0), rl=(-14, 0, 0), ll=(-14, 0, 0), head=(4, 0, 0))
    c.key(2.3, **paws, root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), head=(0, 0, 0))


@clip("copy_star", "Star jumps", **play("play:follow_the_leader:do:star", length=2.8, weight=1, mirror="never"))
def _(c):
    for t in (0.3, 1.0, 1.7):
        c.key(t, **{"ra": (-10, 0, 150), "la": (-10, 0, 150)}, rl=(0, 0, 22), ll=(0, 0, 22), root_pos=(0, -4, 0))
        c.key(t + .35, ra=(0, 0, 8), la=(0, 0, 8), rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(2.5, ra=(0, 0, 0), la=(0, 0, 0))


@clip("copy_spin", "Spins round", **play("play:follow_the_leader:do:spin", length=2.5, weight=1, mirror="never", blend=(0, .3)))
def _(c):
    c.key(0.3, root=(0, 0, 0), ra=(-20, 0, 70), la=(-20, 0, 70))
    c.key(0.8, root=(0, 140, 0))
    c.key(1.3, root=(0, 290, 0))
    c.key(1.6, root=(0, 360, 0), ra=(-10, 0, 40), la=(-10, 0, 40))
    c.key(1.6001, root=(0, 0, 0))
    c.key(2.1, ra=(0, 0, 0), la=(0, 0, 0), head=(-6, 0, 6))


@clip("copy_flap", "Flaps like a bird", **play("play:follow_the_leader:do:flap", length=3.0, weight=1, mirror="never"))
def _(c):
    c.key(0.3, ra=(-10, 0, 40), la=(-10, 0, 40), waist=(10, 0, 0), head=(-10, 0, 0))
    c.cycle(0.4, 2.4, .5, dict(ra=(-10, 0, 100), la=(-10, 0, 100), root_pos=(0, -1.5, 0)), dict(ra=(-10, 0, 30), la=(-10, 0, 30), root_pos=(0, 0, 0)))
    c.key(2.7, ra=(0, 0, 10), la=(0, 0, 10), waist=(0, 0, 0), head=(0, 0, 0))


@clip("copy_stomp", "Stomp stomp clap", **play("play:follow_the_leader:do:stomp", length=2.8, weight=1, mirror="never"))
def _(c):
    clap_open, clap_shut = dict(ra=(-70, 30, 0), la=(-70, 30, 0)), dict(ra=(-74, -26, 0), la=(-74, -26, 0))
    c.key(0.3, rl=(-50, 0, 0), waist=(6, 0, 0), ra=(10, 0, 14), la=(10, 0, 14))
    c.key(0.5, rl=(0, 0, 0), root_pos=(0, .6, 0))
    c.key(0.75, ll=(-50, 0, 0), root_pos=(0, 0, 0))
    c.key(0.95, ll=(0, 0, 0), root_pos=(0, .6, 0))
    c.key(1.2, **clap_open, root_pos=(0, 0, 0))
    c.key(1.35, **clap_shut)
    c.key(1.55, **clap_open)
    c.key(1.7, **clap_shut, head=(-8, 0, 0))
    c.key(2.4, ra=(0, 0, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0))


@clip("copy_salute", "Salutes smartly", **play("play:follow_the_leader:do:salute", length=2.2, weight=1, mirror="never"))
def _(c):
    c.key(0.35, ra=(-140, -58, 0), head=(-6, 0, 0), rl=(0, 0, 0))
    c.key(0.5, root_pos=(0, -1, 0))
    c.key(0.65, root_pos=(0, 0, 0))
    c.hold(0.7, 1.6, ra=(-140, -58, 0), head=(-6, 0, 0))
    c.key(1.95, ra=(0, 0, 0), head=(0, 0, 0))


# -- catch ------------------------------------------------------------------------------------------

@clip("catch_ready", "Ready to catch", **play("play:catch:ready", length=1.6, weight=3, mirror="never"))
def _(c):
    ready = dict(ra=(-42, -16, 10), la=(-42, -16, 10), waist=(10, 0, 0), rl=(-14, 0, 6), ll=(-14, 0, 6))
    c.key(0.25, **ready, root_pos=(0, 1.5, 0))
    c.cycle(0.3, 1.3, .5, dict(root_pos=(0, 1.5, 0)), dict(root_pos=(0, .4, 0)))
    c.key(1.4, **ready, root_pos=(0, 1.5, 0))


@clip("catch_hold", "Holds the ball and picks someone", **play("play:catch:hold", length=2.4, weight=3, mirror="never", items="override"))
def _(c):
    hold = dict(ra=(-52, -26, 0), la=(-52, -32, 0))
    c.key(0.3, **hold, head=(4, 0, 0))
    c.key(1.0, head=(0, 14, 0), ra=(-60, -26, 0), la=(-60, -32, 0))
    c.key(1.7, head=(0, -12, 0))
    c.key(2.1, **hold, head=(0, 0, 0))


@clip("catch_throw", "Throws the ball", **play("play:catch:throw", length=1.4, weight=3, mirror="never", items="override", blend=(.1, .3)))
def _(c):
    # The ball leaves the hand at 0.6 s (Playground.RELEASE ticks).
    c.key(0.15, ra=(-60, -20, 0), la=(-30, 0, 10))
    c.key(0.45, ra=(-168, 0, 12), la=(-60, 10, 10), waist=(-6, -18, 0), head=(-10, 0, 0), rl=(-10, 0, 0))
    c.key(0.6, ra=(-80, 0, 0), waist=(10, 14, 0), head=(-4, 0, 0))
    c.key(0.8, ra=(-34, -26, 0), waist=(14, 10, 0), la=(-20, 0, 10), rl=(0, 0, 0))
    c.key(1.2, ra=(-10, 0, 0), waist=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0))


@clip("catch_catch", "Catches the ball", **play("play:catch:catch", length=1.4, weight=3, mirror="never", items="override"))
def _(c):
    # The ball lands at 1.4 s (Playground.RELEASE + FLIGHT ticks).
    c.key(0.3, ra=(-46, -16, 10), la=(-46, -16, 10), look=(0, -.5), head=(-14, 0, 0), rl=(-14, 0, 6), ll=(-14, 0, 6), root_pos=(0, 1.5, 0))
    c.key(0.9, ra=(-70, -10, 6), la=(-70, -10, 6), head=(-18, 0, 0), look=(0, -.6))
    c.key(1.3, ra=(-84, -18, 0), la=(-84, -18, 0), head=(-4, 0, 0), look=(0, 0))


@clip("catch_fumble", "Fumbles the catch", **play("play:catch:fumble", length=2.4, weight=3, mirror="free"))
def _(c):
    c.key(0.15, ra=(-100, 0, 0), la=(-70, 0, 20), waist=(12, 0, 0))
    c.key(0.4, ra=(-40, 0, 30), la=(-30, 0, 30), head=(24, 30, 0), waist=(20, 0, 0), look=(.5, .5))
    c.key(1.0, ra=(-160, -30, 14), la=(-160, -30, 14), head=(6, 0, 8), waist=(0, 0, 0), look=(0, 0), lid=.5)
    c.wobble(1.1, 1.8, 5, "body", 3, axis=2)
    c.key(2.1, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), lid=0)


# -- curious about a player -------------------------------------------------------------------------

@clip("curious_tiptoe", "Tiptoes after you", **play("play:curious:follow", moving=True, length=1.3, weight=3))
def _(c):
    c.cycle(0.1, 1.2, .6, dict(waist=(14, 0, 0), ra=(-62, -24, 12), la=(-50, -24, 12), head=(-12, 0, 4)),
            dict(waist=(14, 0, 0), ra=(-50, -24, 12), la=(-62, -24, 12), head=(-12, 0, -4)))


@clip("curious_skip", "Skips along behind you", **play("play:curious:follow", moving=True, length=1.2, weight=1.5, mirror="never"))
def _(c):
    c.cycle(0.1, 1.1, 1.0, dict(ra=(-30, 0, 10), la=(24, 0, 10), head=(-6, 0, 6)), dict(ra=(24, 0, 10), la=(-30, 0, 10), head=(-6, 0, -6)))


@clip("curious_watch", "Watches you closely", **play("play:curious:watch", length=3.4, weight=3))
def _(c):
    c.key(0.5, **HANDS_BEHIND, waist=(16, 0, 0), head=(-14, 0, 12))
    c.key(1.6, head=(-14, 0, -10))
    c.key(2.4, head=(-12, 0, 14), lid=.2)
    c.key(3.0, **HANDS_BEHIND, waist=(10, 0, 0), head=(-6, 0, 0), lid=0)


@clip("curious_peer", "Leans in for a better look", **play("play:curious:watch", length=3.0, weight=2))
def _(c):
    c.key(0.5, waist=(30, 0, 0), head=(-34, 0, 0), ra=(-34, -14, 0), la=(-34, -14, 0), rl=(-10, 0, 0), ll=(-10, 0, 0), look=(0, -.3))
    c.key(1.6, head=(-34, 10, 6))
    c.key(2.6, waist=(10, 0, 0), head=(-8, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), look=(0, 0))


@clip("curious_ponder", "Wonders what you're doing", **play("play:curious:watch", moving=False, length=3.2, weight=2))
def _(c):
    c.key(0.5, **HAND_TO_CHIN, la=(-40, -40, 0), head=(-6, 0, 14), look=(.3, -.3))
    c.wobble(0.8, 2.2, 2, "ra", 4, base=(-104, -42, 0), axis=0)
    c.key(2.8, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), look=(0, 0))


@clip("curious_caught", "Acts innocent", **play("play:curious:caught", length=3.0, weight=3, mirror="never"))
def _(c):
    c.key(0.3, **HANDS_BEHIND, head=(-14, 0, 0), look=(0, -.6), lid=.2)
    c.cycle(0.4, 2.6, .8, dict(root_pos=(0, -.6, 0), rl=(-6, 0, 0), ll=(-6, 0, 0), head=(-16, 0, 6)),
            dict(root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0), head=(-12, 0, -6)))
    c.key(2.8, **HANDS_BEHIND, head=(-10, 0, 0), look=(0, -.4))


@clip("curious_caught_sky", "Is suddenly very interested in the sky", **play("play:curious:caught", length=2.8, weight=2))
def _(c):
    c.key(0.35, ra=(-150, -20, 0), head=(-28, 0, 0), look=(0, -.7), la=(10, 0, 8))
    c.wobble(0.5, 1.6, 3, "ra", 8, base=(-150, -20, 0), axis=1)
    c.key(2.0, ra=(-150, -20, 0), head=(-22, 10, 0))
    c.key(2.5, ra=(0, 0, 0), la=(0, 0, 0), head=(-6, 0, 0), look=(0, 0))


@clip("curious_bye", "Waves bye-bye", **play("play:curious:bye", length=2.0, weight=3))
def _(c):
    c.key(0.3, ra=(-10, 0, 150), head=(0, 0, 8), lid=.2)
    c.wobble(0.35, 1.5, 4, "ra", 18, base=(-10, 0, 150), axis=2)
    c.key(1.8, ra=(0, 0, 0), head=(0, 0, 0), lid=0)
