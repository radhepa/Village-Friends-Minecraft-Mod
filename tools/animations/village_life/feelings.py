"""Feelings: more ways to laugh, thank, refuse, cheer, swoon, fume, fret and flinch."""
from kit import clip, ARMS_CROSSED, HANDS_BEHIND, HANDS_ON_HIPS, HAND_TO_CHEST, HAND_TO_MOUTH


@clip("knee_slap_laugh", "Slaps a knee laughing", trigger="laugh", weight=2.5, mirror="free", length=2.6,
      boost={"personality:playful": 2, "personality:adventurous": 1.5})
def _(c):
    c.key(0.25, head=(-14, 0, 0), ra=(-70, 0, 10), lid=.7)
    c.wobble(0.3, 2.0, 6, "root_pos", .4, axis=1, decay=.4)
    for t in (0.55, 1.15):
        c.key(t, waist=(30, 0, 0), head=(-18, 0, 0), ra=(16, 0, 6), la=(-30, -30, 0))
        c.key(t + .32, waist=(18, 0, 0), head=(-12, 0, 0), ra=(-76, 0, 12))
    c.key(1.75, waist=(32, 0, 0), head=(-16, 0, 0), ra=(14, 0, 6))
    c.key(2.1, waist=(4, 0, 0), head=(-4, 0, 0), ra=(-10, 0, 6), la=(-10, -10, 0), lid=.4)


@clip("snort_laugh", "Snorts with laughter", trigger="laugh", weight=2, length=2.4)
def _(c):
    c.key(0.15, head=(-10, 0, 0), lid=.2)
    c.key(0.3, ra=(-120, -40, 0), head=(14, 0, 0), waist=(10, 0, 0), lid=0, look=(0, -.3))
    c.key(0.55, head=(10, 0, 0), look=(.5, 0))
    c.key(0.8, head=(12, 0, 8), lid=.7, look=(0, 0))
    c.wobble(0.85, 1.9, 7, "head", 4, base=(12, 0, 8), axis=0)
    c.wobble(0.85, 1.9, 7, "ra_pos", .4, axis=1)
    c.key(1.95, ra=(-112, -40, 0), waist=(6, 0, 0), lid=.6)


@clip("wheeze_laugh", "Wheezes with laughter", trigger="laugh", weight=2, mirror="never", length=3.0,
      boost={"personality:warmhearted": 1.5})
def _(c):
    knees = dict(ra=(-24, -8, 4), la=(-24, -8, 4))
    c.key(0.35, waist=(34, 0, 0), head=(-26, 0, 0), **knees, lid=.8)
    c.cycle(0.45, 2.3, .4, dict(waist=(30, 0, 0), head=(-28, 0, 0), ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0)),
            dict(waist=(36, 0, 0), head=(-22, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0)))
    c.hold(0.45, 2.3, **knees)
    c.key(2.6, waist=(6, 0, 0), head=(-4, 0, 0), ra=(-6, 0, 4), la=(-6, 0, 4), lid=.4)


@clip("silent_laugh", "Shakes with silent laughter", trigger="laugh", weight=2, mirror="free", length=2.8,
      boost={"personality:reserved": 2, "personality:gentle": 1.5})
def _(c):
    c.key(0.35, ra=(-136, -42, 0), la=(-44, -44, 0), waist=(10, 0, 0), head=(16, 0, -6), lid=1)
    c.wobble(0.4, 2.0, 5, "ra_pos", .6, axis=1)
    c.wobble(0.4, 2.0, 5, "la_pos", .6, axis=1)
    c.wobble(0.4, 2.0, 5, "waist", 3, base=(10, 0, 0), axis=0)
    c.key(2.05, ra=(-136, -42, 0), head=(16, 0, -6), lid=1)
    c.key(2.35, ra=(-112, -34, 0), head=(4, 0, 0), lid=.5)


@clip("point_and_laugh", "Points and laughs", trigger="laugh", weight=2, length=2.5,
      boost={"personality:playful": 2})
def _(c):
    c.key(0.3, ra=(-86, 6, 0), la=(-34, -42, 0), head=(-10, 0, 6), waist=(-8, 0, 0), lid=.6)
    c.wobble(0.35, 1.7, 6, "ra", 5, base=(-86, 6, 0), axis=0)
    c.wobble(0.35, 1.9, 7, "root_pos", .35, axis=1)
    c.key(1.2, waist=(-12, 0, 0), head=(-16, 0, 8))
    c.key(1.9, ra=(-30, 0, 10), la=(-40, -44, 0), waist=(14, 0, 0), head=(8, 0, 0), lid=.7)


@clip("jump_for_joy", "Jumps for joy", trigger="delighted", weight=2.5, mirror="never", length=2.2,
      boost={"personality:playful": 2, "personality:adventurous": 1.5})
def _(c):
    c.key(0.3, root_pos=(0, 2, 0), waist=(16, 0, 0), ra=(30, 0, 12), la=(30, 0, 12), head=(4, 0, 0), lid=.3)
    c.key(0.55, root_pos=(0, -5.2, 0), waist=(-6, 0, 0), ra=(-160, 0, 24), la=(-160, 0, 24), rl=(22, 0, 6),
          ll=(22, 0, 6), head=(-16, 0, 0), lid=.6)
    c.key(0.8, root_pos=(0, 1.2, 0), waist=(10, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(1.0, root_pos=(0, 0, 0), ra=(-80, -10, 10), la=(-80, -10, 10))
    c.key(1.2, ra=(-30, -6, 12), la=(-30, -6, 12), waist=(0, 0, 0), head=(-8, 0, 0))
    c.key(1.6, ra=(-20, 0, 8), la=(-20, 0, 8), head=(-4, 0, 0), lid=.4)


@clip("spin_with_joy", "Spins with joy", trigger="delighted", weight=2, mirror="free", length=2.4, blend=(0, 0),
      boost={"personality:imaginative": 2, "personality:playful": 1.5})
def _(c):
    c.key(0.25, root=(0, -16, 0), ra=(-20, 0, 40), la=(-20, 0, 40), head=(-6, 0, 0), lid=.4)
    c.key(0.65, root=(0, 120, 0), ra=(-14, 0, 96), la=(-14, 0, 96), head=(-14, 0, 0), lid=.7)
    c.key(1.05, root=(0, 260, 0), root_pos=(0, -1.6, 0))
    c.key(1.4, root=(0, 360, 0), root_pos=(0, 0, 0), ra=(-60, 0, 40), la=(-60, 0, 40), head=(-8, 0, 8))
    c.key(1.8, root=(0, 360, 0), ra=(-30, 0, 20), la=(-30, 0, 20), head=(0, 0, 0), lid=.3)
    c.key(2.4, root=(0, 360, 0), ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0), root_pos=(0, 0, 0), lid=0)


@clip("happy_shimmy", "Happy shimmy", trigger="delighted", weight=2, mirror="never", length=2.6,
      boost={"personality:playful": 1.5, "personality:warmhearted": 1.5})
def _(c):
    c.key(0.3, ra=(-40, 0, 26), la=(-40, 0, 26), waist=(-4, 0, 0), head=(-6, 0, 0), lid=.6)
    c.cycle(0.35, 1.95, .2, dict(waist=(-4, 12, 0), ra_pos=(0, 0, -1.2), la_pos=(0, 0, 1.2), head=(-6, 0, 4)),
            dict(waist=(-4, -12, 0), ra_pos=(0, 0, 1.2), la_pos=(0, 0, -1.2), head=(-6, 0, -4)))
    c.cycle(0.35, 1.95, .8, dict(root_pos=(0, .4, 0), root=(0, 0, 3)), dict(root_pos=(0, 0, 0), root=(0, 0, -3)))
    c.key(2.1, ra=(-34, 0, 22), la=(-34, 0, 22), waist=(0, 0, 0), lid=.4)


@clip("gasp_of_joy", "Gasps with joy", trigger="delighted", weight=2.5, mirror="never", length=2.5,
      boost={"personality:gentle": 1.5, "personality:imaginative": 1.5})
def _(c):
    c.key(0.15, root_pos=(0, .6, 0), head=(4, 0, 0))
    c.key(0.35, ra=(-122, -12, 0), la=(-122, -12, 0), head=(-12, 0, 0), waist=(-6, 0, 0), root_pos=(0, -1, 0),
          lid=0, look=(0, -.3))
    c.key(0.6, root_pos=(0, 0, 0), look=(0, 0))
    c.cycle(0.7, 1.7, .5, dict(head=(-8, 0, 9), lid=.5), dict(head=(-8, 0, -9), lid=.6))
    c.key(1.75, ra=(-118, -12, 0), la=(-118, -12, 0), waist=(-4, 0, 0))
    c.key(2.05, ra=(-60, -40, 0), la=(-60, -40, 0), head=(0, 0, 0), waist=(0, 0, 0), lid=.4)


@clip("trophy_raise", "Raises the gift like a trophy", trigger="delighted", weight=2, mirror="never", length=3.0,
      boost={"personality:adventurous": 2, "personality:protective": 1.5})
def _(c):
    c.key(0.35, ra=(-56, -40, 0), la=(-56, -40, 0), head=(16, 0, 0), waist=(6, 0, 0), look=(0, .6))
    c.key(0.75, ra=(-172, -10, 0), la=(-172, -10, 0), head=(-22, 0, 0), waist=(-8, 0, 0), root_pos=(0, -.8, 0),
          look=(0, -.6), lid=.3)
    c.cycle(0.85, 1.9, .5, dict(ra=(-176, -10, 0), la=(-176, -10, 0), root_pos=(0, -1.2, 0)),
            dict(ra=(-160, -10, 0), la=(-160, -10, 0), root_pos=(0, 0, 0)))
    c.key(2.05, head=(-16, 0, 0), look=(0, -.4))
    c.key(2.45, ra=(-60, -34, 0), la=(-60, -34, 0), head=(4, 0, 0), waist=(0, 0, 0), look=(0, 0), lid=.2)


@clip("hand_on_heart_bow", "Bows with a hand on the heart", trigger="thanks", weight=2.5, length=2.7,
      boost={"personality:reserved": 2, "personality:meticulous": 2, "personality:thoughtful": 1.5})
def _(c):
    c.key(0.35, **HAND_TO_CHEST, la=(-16, 14, 30))
    c.key(0.9, waist=(36, 0, 0), head=(16, 0, 0), la=(-24, 24, 48), lid=.6)
    c.key(1.5, waist=(37, 0, 0), head=(17, 0, 0), la=(-22, 24, 50))
    c.key(2.05, waist=(0, 0, 0), head=(-2, 0, 6), ra=(-50, -46, 0), la=(0, 0, 0), lid=.2)


@clip("two_hand_shake", "Two-handed handshake", trigger="thanks", weight=2, mirror="free", length=2.5,
      boost={"personality:warmhearted": 2, "personality:pragmatic": 1.5})
def _(c):
    c.key(0.35, ra=(-78, -6, 0), la=(-70, -30, 0), waist=(10, 0, 0), head=(4, 0, 0), root_pos=(0, 0, -.6))
    c.cycle(0.45, 1.75, .44, dict(ra=(-90, -6, 0), la=(-82, -30, 0), head=(-2, 0, 0)),
            dict(ra=(-70, -6, 0), la=(-62, -30, 0), head=(10, 0, 0)))
    c.hold(0.45, 1.75, lid=.4)
    c.key(2.05, ra=(-30, -10, 0), la=(-20, -10, 0), waist=(0, 0, 0), head=(0, 0, 0), root_pos=(0, 0, 0), lid=.1)


@clip("tip_the_hat", "Tips their hat", trigger="thanks", weight=2, require=["adult"], length=2.1,
      boost={"personality:steadfast": 2, "personality:reserved": 1.5, "personality:pragmatic": 1.5})
def _(c):
    c.key(0.35, ra=(-150, -34, 0), head=(-2, 0, 0))
    c.key(0.65, ra=(-160, -24, 0), ra_pos=(0, -1.4, 0), head=(14, 0, 0), lid=.4)
    c.key(1.1, ra=(-158, -26, 0), ra_pos=(0, -1.2, 0), head=(12, 0, 0))
    c.key(1.35, ra=(-148, -34, 0), ra_pos=(0, 0, 0), head=(0, 0, 0), lid=.1)
    c.key(1.7, ra=(-20, 0, 8))


@clip("you_shouldnt_have", "Says you shouldn't have", trigger="thanks", weight=2.5, length=2.6,
      boost={"personality:gentle": 2, "personality:reserved": 1.5})
def _(c):
    c.key(0.35, ra=(-72, -10, 12), la=(-112, -26, 0), head=(8, -18, 10), look=(-.4, .3), lid=.35)
    c.wobble(0.4, 1.8, 3.5, "ra", 14, base=(-72, -10, 12), axis=0)
    c.cycle(0.4, 1.8, .7, dict(root=(0, 0, 2)), dict(root=(0, 0, -2)))
    c.key(1.9, head=(4, -6, 6), look=(0, 0), la=(-100, -26, 0))
    c.key(2.2, ra=(-20, 0, 6), la=(-20, -10, 0), lid=.2)


@clip("gift_to_heart", "Presses the gift to their heart", trigger="thanks", weight=2, mirror="free", length=2.9,
      boost={"personality:warmhearted": 2, "personality:gentle": 1.5})
def _(c):
    c.key(0.4, ra=(-60, -52, 0), la=(-54, -44, 0), head=(6, 0, 0), lid=.3)
    c.key(1.1, ra_pos=(0, -1, 0), la_pos=(0, -1, 0), head=(-12, 0, 0), waist=(-4, 0, 0), root_pos=(0, -.4, 0), lid=1)
    c.key(1.7, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(8, 0, 10), waist=(2, 0, 0), root_pos=(0, 0, 0), lid=.5)
    c.key(2.0, head=(14, 0, 8))
    c.key(2.3, ra=(-58, -50, 0), la=(-52, -44, 0), head=(4, 0, 4), lid=.3)


@clip("arms_x_refuse", "Crosses arms in an X", trigger="decline", weight=2, mirror="never", length=2.0,
      boost={"personality:pragmatic": 1.5, "personality:steadfast": 1.5})
def _(c):
    c.key(0.15, ra=(-40, 0, 20), la=(-40, 0, 20), head=(4, 0, 0))
    c.key(0.3, ra=(-84, -52, 0), la=(-76, -50, 0), ra_pos=(0, 0, -1), la_pos=(0, 0, -1), waist=(-6, 0, 0), head=(-4, 0, 0), lid=.35)
    c.cycle(0.45, 1.3, .36, dict(head=(-4, 16, 0)), dict(head=(-4, -16, 0)))
    c.hold(0.45, 1.3, ra=(-84, -52, 0), la=(-76, -50, 0))
    c.key(1.55, ra=(-30, -10, 6), la=(-30, -10, 6), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), lid=.1)


@clip("push_it_back", "Pushes it back", trigger="decline", weight=2.5, mirror="never", length=2.1)
def _(c):
    c.key(0.25, ra=(-70, -30, 0), la=(-70, -30, 0), head=(4, 0, 0))
    c.key(0.5, ra=(-86, -6, 4), la=(-86, -6, 4), ra_pos=(0, 0, -1.4), la_pos=(0, 0, -1.4), waist=(-6, 0, 0),
          head=(-2, 16, 0), look=(.4, 0), lid=.35)
    c.key(0.8, ra=(-80, -14, 2), la=(-80, -14, 2), ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(1.0, ra=(-88, -6, 4), la=(-88, -6, 4), ra_pos=(0, 0, -1.2), la_pos=(0, 0, -1.2), head=(0, 20, 0))
    c.key(1.45, ra=(-40, -6, 8), la=(-40, -6, 8), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), head=(2, 6, 0),
          look=(0, 0), lid=.1)


@clip("nose_in_the_air", "Turns up their nose", trigger="decline", weight=2, mirror="free", length=2.5,
      boost={"personality:meticulous": 2, "personality:reserved": 1.5})
def _(c):
    c.key(0.3, la=HANDS_ON_HIPS["la"], head=(-6, -10, 0))
    c.key(0.55, head=(-22, -38, 4), root=(0, -10, 0), lid=.6, look=(-.3, -.2), ra=(-56, 20, 26))
    c.key(0.75, ra=(-36, 44, 44))
    c.key(1.05, ra=(-10, 6, 10))
    c.hold(1.2, 1.9, head=(-20, -40, 4), lid=.65)
    c.key(2.1, la=(0, 0, 0), ra=(0, 0, 0), root=(0, 0, 0))


@clip("not_for_me", "Hands up: not for me", trigger="decline", weight=2, mirror="never", length=2.2)
def _(c):
    c.key(0.3, ra=(-96, 34, 46), la=(-96, 34, 46), waist=(-8, 0, 0), root_pos=(0, 0, .6), head=(-4, 0, 0), lid=.2)
    c.cycle(0.4, 1.4, .4, dict(head=(-4, 12, 0), ra=(-100, 38, 48), la=(-92, 30, 44)),
            dict(head=(-4, -12, 0), ra=(-92, 30, 44), la=(-100, 38, 48)))
    c.key(1.55, ra=(-60, 20, 30), la=(-60, 20, 30), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(2, 0, 0), lid=.1)


@clip("apologetic_shake", "Shakes head apologetically", trigger="decline", weight=2.5, length=2.6,
      boost={"personality:gentle": 2, "personality:warmhearted": 1.5})
def _(c):
    c.key(0.35, **HAND_TO_CHEST, la=(-28, 10, 10), head=(6, 0, 10), waist=(6, 0, 0), look=(0, .3), lid=.4)
    c.cycle(0.45, 1.75, .65, dict(head=(8, 12, 10)), dict(head=(8, -12, 10)))
    c.key(1.95, head=(12, 0, 6), waist=(10, 0, 0), lid=.5)
    c.key(2.2, ra=(-40, -40, 0), la=(-10, 0, 4), head=(4, 0, 2), waist=(0, 0, 0), look=(0, 0), lid=.2)


@clip("hop_and_clap", "Hops and claps", trigger="happy", weight=2.5, mirror="never", length=2.2,
      boost={"personality:playful": 2})
def _(c):
    for t in (0.35, 1.05):
        c.key(t - .15, root_pos=(0, 1, 0), ra=(-40, 16, 30), la=(-40, 16, 30))
        c.key(t + .05, root_pos=(0, -3, 0), ra=(-70, 20, 40), la=(-70, 20, 40), head=(-10, 0, 0))
        c.key(t + .25, root_pos=(0, 0, 0), ra=(-96, -32, 0), la=(-96, -32, 0), head=(-4, 0, 0))
        c.key(t + .4, ra=(-90, -10, 10), la=(-90, -10, 10))
        c.key(t + .5, ra=(-96, -32, 0), la=(-96, -32, 0))
    c.hold(0.2, 1.6, lid=.5)
    c.key(1.8, ra=(-30, -10, 6), la=(-30, -10, 6), head=(0, 0, 0))


@clip("thumbs_up", "Thumbs up", trigger="happy", weight=2, length=1.9,
      boost={"personality:pragmatic": 2, "personality:adventurous": 1.5})
def _(c):
    c.key(0.25, ra=(-60, 0, 20), head=(4, 0, 0))
    c.key(0.45, ra=(-86, 4, 14), ra_pos=(0, 0, -1.2), head=(-4, 0, -8), lid=.5)
    c.key(0.7, ra=(-82, 4, 14), ra_pos=(0, 0, 0), head=(10, 0, -8))
    c.key(0.95, ra=(-88, 4, 14), ra_pos=(0, 0, -1), head=(-2, 0, -8))
    c.key(1.35, ra=(-80, 4, 14), ra_pos=(0, 0, 0), head=(0, 0, -4), lid=.3)


@clip("wiggle_dance", "Wiggle dance", trigger="happy", weight=2, mirror="never", length=2.8,
      boost={"personality:playful": 2, "personality:imaginative": 1.5})
def _(c):
    c.key(0.3, ra=(-40, 0, 24), la=(-40, 0, 24), lid=.5)
    c.cycle(0.35, 2.25, .5, dict(root=(0, 0, 5), waist=(0, 0, -9), head=(-4, 0, 8), ra=(-56, 0, 30), la=(-26, 0, 20),
                                 root_pos=(0, .3, 0)),
            dict(root=(0, 0, -5), waist=(0, 0, 9), head=(-4, 0, -8), ra=(-26, 0, 20), la=(-56, 0, 30),
                 root_pos=(0, 0, 0)))
    c.key(2.4, lid=.3)


@clip("arms_wide_beam", "Beams with arms wide open", trigger="happy", weight=2, mirror="never", length=2.6,
      boost={"personality:warmhearted": 2, "personality:adventurous": 1.5})
def _(c):
    c.key(0.2, ra=(-14, 0, 20), la=(-14, 0, 20), root_pos=(0, .4, 0))
    c.key(0.55, ra=(-34, 20, 80), la=(-34, 20, 80), waist=(-8, 0, 0), head=(-12, 0, 0), root_pos=(0, -.8, 0), lid=.6,
          ra_pos=(0, -.8, 0), la_pos=(0, -.8, 0))
    c.key(1.1, ra=(-36, 22, 84), la=(-36, 22, 84), root=(0, 0, 3), head=(-12, 0, 6), root_pos=(0, 0, 0),
          ra_pos=(0, 0, 0), la_pos=(0, 0, 0))
    c.key(1.6, ra=(-34, 20, 80), la=(-34, 20, 80), root=(0, 0, -3), head=(-10, 0, -6), lid=.65)
    c.key(2.1, ra=(-16, 0, 26), la=(-16, 0, 26), root=(0, 0, 0), waist=(0, 0, 0), head=(-2, 0, 0), lid=.3)


@clip("skip_in_place", "Skips in place", trigger="happy", weight=2, mirror="free", length=2.3,
      boost={"personality:playful": 2})
def _(c):
    for i, t in enumerate((0.3, 0.7, 1.1, 1.5)):
        up, down = ("rl", "ll") if i % 2 == 0 else ("ll", "rl")
        fwd, back = ("la", "ra") if i % 2 == 0 else ("ra", "la")
        c.key(t, root_pos=(0, -2.2, 0), **{up: (-50, 0, 4), down: (6, 0, 0), fwd: (-50, 0, 8), back: (30, 0, 8)},
              head=(-6, 0, 6 if i % 2 else -6))
        c.key(t + .2, root_pos=(0, 0, 0), **{up: (0, 0, 0), down: (0, 0, 0)})
    c.hold(0.3, 1.7, lid=.5)
    c.key(1.95, ra=(0, 0, 0), la=(0, 0, 0), head=(0, 0, 0))


@clip("swoon", "Swoons with hands on cheeks", trigger="love", weight=2.5, mirror="free", length=3.0,
      boost={"personality:imaginative": 2, "personality:gentle": 1.5})
def _(c):
    c.key(0.4, ra=(-124, -14, 0), la=(-112, -10, 0), head=(-4, 0, 14), lid=.6, look=(0, -.4))
    c.key(1.0, root=(0, 0, 5), waist=(-4, 0, 4), head=(-6, 0, 16), lid=.85)
    c.key(1.6, root=(0, 0, -3), waist=(-2, 0, -2), head=(-4, 0, 10))
    c.key(2.2, root=(0, 0, 4), waist=(-4, 0, 4), head=(-6, 0, 16), lid=.9, ra=(-122, -14, 0), la=(-110, -10, 0))
    c.key(2.55, ra=(-50, -30, 0), la=(-46, -30, 0), lid=.4)


@clip("blow_a_kiss", "Blows a kiss", trigger="love", weight=2.5, length=2.3,
      boost={"personality:playful": 2, "personality:warmhearted": 1.5})
def _(c):
    c.key(0.35, **HAND_TO_MOUTH, head=(6, 0, 0), lid=.8)
    c.key(0.7, ra=(-114, -40, 0), head=(8, 0, 4), lid=.9)
    c.key(0.95, ra=(-82, 26, 30), head=(-6, 0, -6), waist=(4, 0, 0), lid=.3)
    c.key(1.4, ra=(-76, 30, 34), head=(-4, 0, -8), lid=.35)
    c.key(1.85, ra=(-20, 0, 8), waist=(0, 0, 0), head=(0, 0, 0), lid=.1)


@clip("heart_flutter", "Heart flutters", trigger="love", weight=2, length=2.5,
      boost={"personality:gentle": 1.5, "personality:warmhearted": 1.5})
def _(c):
    c.key(0.3, ra=(-62, -50, 0), head=(-8, 0, 8), look=(0, -.5), lid=.4)
    c.wobble(0.35, 1.75, 6, "ra", 10, base=(-62, -50, 0), axis=0)
    c.cycle(0.35, 1.75, .7, dict(root=(0, 0, 3), head=(-10, 0, 10)), dict(root=(0, 0, -2), head=(-8, 0, 6)))
    c.hold(0.35, 1.75, lid=.55)
    c.key(2.0, ra=(-56, -48, 0), head=(-2, 0, 4), look=(0, 0), lid=.3)


@clip("dreamy_sigh", "Dreamy sigh", trigger="love", weight=2, mirror="free", length=3.2,
      boost={"personality:thoughtful": 1.5, "personality:imaginative": 1.5})
def _(c):
    c.key(0.45, ra=(-104, -40, 0), la=(-102, -42, 0), head=(-6, 0, 14), look=(.4, -.4), lid=.5)
    c.key(1.0, ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), head=(-12, 0, 14), waist=(-4, 0, 0), lid=.7)
    c.key(1.5, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(-4, 0, 16), waist=(-2, 0, 0), lid=.85)
    c.key(2.3, root=(0, 0, 6), waist=(0, 0, 4), head=(-4, 0, 18), lid=.85)
    c.key(2.75, ra=(-40, -30, 0), la=(-40, -30, 0), root=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 4), look=(0, 0),
          lid=.3)


@clip("shy_toe_twist", "Shy toe twist", trigger="love", weight=2, mirror="free", length=3.2,
      boost={"personality:reserved": 2, "personality:gentle": 1.5})
def _(c):
    c.key(0.4, ra=(-26, -36, 0), la=(-24, -36, 0), head=(16, 0, -8), look=(0, -.5), lid=.3)
    for t, toe, yaw in ((0.7, (-10, 12, 4), 8), (1.1, (-14, 0, 10), 0), (1.5, (-10, -10, 4), -8),
                        (1.9, (-6, 0, -2), 0), (2.3, (-10, 12, 4), 8)):
        c.key(t, rl=toe, root=(0, yaw, 0))
    c.key(1.5, head=(14, 0, 8), look=(0, -.6))
    c.key(2.7, rl=(0, 0, 0), root=(0, 0, 0), ra=(-10, -10, 0), la=(-10, -10, 0), head=(6, 0, -4), look=(0, 0), lid=.1)


@clip("stomp_feet", "Stomps both feet", trigger="angry", weight=2.5, mirror="never", length=2.2, blend=(.12, .4),
      boost={"personality:adventurous": 1.5, "personality:playful": 1.5})
def _(c):
    fists = dict(ra=(14, 0, 10), la=(14, 0, 10))
    c.key(0.2, **fists, head=(10, 0, 0), look=(0, -.4), lid=.45)
    for i, t in enumerate((0.45, 0.85, 1.25, 1.6)):
        leg, other = ("rl", "ll") if i % 2 == 0 else ("ll", "rl")
        c.key(t - .17, **{leg: (-34, 0, 4), other: (0, 0, 0)}, waist=(2, 0, 0), root_pos=(0, -.5, 0), ra=(4, 0, 12),
              la=(4, 0, 12))
        c.key(t, **{leg: (0, 0, 0)}, waist=(12, 0, 0), root_pos=(0, .5, 0), ra=(22, 0, 8), la=(22, 0, 8))
    c.key(1.8, waist=(4, 0, 0), root_pos=(0, 0, 0), **fists)


@clip("rant_flail", "Rants and flails", trigger="angry", weight=2, mirror="never", length=2.6, blend=(.12, .4),
      boost={"personality:imaginative": 1.5, "personality:playful": 1.5})
def _(c):
    c.key(0.25, ra=(-60, 20, 40), la=(-60, 20, 40), waist=(4, 0, 0), lid=.45)
    c.cycle(0.35, 1.85, .44, dict(ra=(-150, 10, 40), la=(-56, 24, 44), head=(-6, 12, 4)),
            dict(ra=(-56, 24, 44), la=(-150, 10, 40), head=(2, -12, -4)))
    c.key(2.05, ra=(-30, 10, 30), la=(-30, 10, 30), head=(8, 0, 0), waist=(0, 0, 0), lid=.3)


@clip("point_and_scold", "Points and scolds", trigger="angry", weight=2.5, length=2.4, blend=(.12, .4),
      boost={"personality:meticulous": 1.5, "personality:protective": 2})
def _(c):
    c.key(0.25, ra=(-88, 0, 0), la=HANDS_ON_HIPS["la"], waist=(8, 0, 0), head=(4, 0, 0), lid=.45)
    for t in (0.5, 0.85, 1.2, 1.55):
        c.key(t, ra=(-92, 0, 0), ra_pos=(0, 0, -1.6), head=(10, 0, 0))
        c.key(t + .17, ra=(-84, 0, 0), ra_pos=(0, 0, 0), head=(2, 0, 0))
    c.key(1.95, ra=(-84, 0, 0), la=HANDS_ON_HIPS["la"], waist=(6, 0, 0), lid=.4)


@clip("cold_shoulder", "Gives the cold shoulder", trigger="angry", weight=2, mirror="free", length=3.0,
      blend=(.12, .4), boost={"personality:reserved": 2, "personality:meticulous": 1.5})
def _(c):
    c.key(0.25, **ARMS_CROSSED)
    c.key(0.55, root=(0, -60, 0), head=(-10, 24, 0), look=(.6, 0), lid=.55)
    c.key(1.2, ra_pos=(0, -1, 0), la_pos=(0, -1, 0), head=(-14, 18, 0))
    c.key(1.5, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(-12, 10, 0), look=(.3, 0))
    c.key(2.2, root=(0, -58, 0), **ARMS_CROSSED, head=(-10, 20, 0), look=(.6, 0), lid=.55)
    c.key(2.65, root=(0, -20, 0))


@clip("fists_tremble", "Shakes with clenched fists", trigger="angry", weight=2, mirror="never", length=2.5,
      blend=(.12, .4), boost={"personality:steadfast": 1.5, "personality:protective": 1.5})
def _(c):
    c.key(0.3, ra=(10, 0, 14), la=(10, 0, 14), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), head=(12, 0, 0),
          look=(0, -.5), lid=.4)
    c.wobble(0.35, 1.7, 10, "root", 1.5, axis=2)
    c.wobble(0.35, 1.7, 9, "ra", 4, base=(10, 0, 14), axis=2)
    c.wobble(0.35, 1.7, 9, "la", 4, base=(10, 0, 14), axis=2)
    c.key(1.7, ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), head=(12, 0, 0))
    c.key(2.0, ra=(4, 0, 6), la=(4, 0, 6), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), head=(-4, 0, 0), look=(0, 0), lid=.6)


@clip("bite_nails", "Bites their nails", trigger="nervous", weight=2.5, length=2.8,
      boost={"personality:thoughtful": 1.5, "personality:reserved": 1.5})
def _(c):
    c.key(0.35, ra=(-114, -40, 0), la=(-40, -50, 0), head=(8, 0, 0), lid=.2)
    c.wobble(0.4, 2.2, 8, "ra_pos", .35, axis=1)
    for t, x in ((0.5, .6), (1.0, -.6), (1.5, .5), (1.9, -.4), (2.2, 0)):
        c.key(t, look=(x, -.1), head=(8, x * 14, 0))
    c.key(2.25, ra=(-112, -40, 0))


@clip("wring_hands", "Wrings their hands", trigger="nervous", weight=2.5, mirror="never", length=2.8)
def _(c):
    c.key(0.35, ra=(-42, -42, 0), la=(-42, -42, 0), ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0), head=(10, 0, 4), lid=.2)
    c.cycle(0.45, 2.15, .5, dict(ra=(-48, -46, 0), la=(-36, -38, 0), ra_pos=(0, -.6, -.5), la_pos=(0, -.6, .3)),
            dict(ra=(-36, -38, 0), la=(-48, -46, 0), ra_pos=(0, -.6, .3), la_pos=(0, -.6, -.5)))
    for t, x in ((0.6, .5), (1.2, -.5), (1.8, .3)):
        c.key(t, look=(x, -.2))
    c.key(2.3, ra=(-30, -30, 0), la=(-30, -30, 0), head=(6, 0, 2), look=(0, 0))


@clip("glance_over_shoulder", "Glances over a shoulder", trigger="nervous", weight=2, mirror="free", length=2.9)
def _(c):
    tucked = dict(ra=(-20, -20, 0), la=(-20, -20, 0), ra_pos=(0, -.6, 0), la_pos=(0, -.6, 0))
    c.key(0.25, **tucked, waist=(6, 0, 0))
    c.key(0.55, waist=(6, 24, 0), head=(4, 60, 0), look=(.8, 0), lid=0)
    c.key(0.95, waist=(6, 26, 0), head=(4, 62, 0))
    c.key(1.15, waist=(6, 0, 0), head=(2, 0, 0), look=(0, 0))
    c.key(1.65, waist=(6, -20, 0), head=(4, -56, 0), look=(-.8, 0))
    c.key(2.0, waist=(6, -22, 0), head=(4, -58, 0))
    c.key(2.25, waist=(4, 0, 0), head=(2, 0, 0), look=(0, 0), **tucked)


@clip("tug_collar", "Tugs at a sweaty collar", trigger="nervous", weight=2.5, length=3.2,
      boost={"personality:meticulous": 1.5, "personality:pragmatic": 1.5})
def _(c):
    c.key(0.3, ra=(-84, -40, 0), la=(-14, -16, 0), head=(-6, 0, 8), look=(.5, 0), lid=.1)
    c.cycle(0.45, 1.65, .36, dict(ra=(-84, -40, 0), ra_pos=(0, 0, 0)), dict(ra=(-92, -34, 6), ra_pos=(0, 0, -1.1)))
    for t, x in ((0.7, .6), (1.15, -.6), (1.55, .4)):
        c.key(t, look=(x, -.1), head=(-8, x * 16, 8))
    c.key(1.85, head=(10, 0, 4), root_pos=(0, .4, 0), lid=.75, look=(0, .2))
    c.key(2.15, ra=(-150, -34, 0), head=(-6, 0, 2), root_pos=(0, 0, 0), lid=.5, look=(0, 0))
    c.key(2.45, ra=(-144, 10, 10), head=(-4, 6, 0))
    c.key(2.75, ra=(-60, 16, 18), la=(0, 0, 0), lid=.2)


@clip("shaky_knees", "Knees knocking", trigger="nervous", weight=2, mirror="never", length=3.0,
      boost={"personality:gentle": 1.5, "personality:reserved": 1.5, "child": 1.5})
def _(c):
    clasp = dict(ra=(-92, -42, 0), la=(-92, -42, 0))
    c.key(0.3, **clasp, ra_pos=(0, -.8, 0), la_pos=(0, -.8, 0), waist=(10, 0, 0), head=(-6, 0, 0), root_pos=(0, .8, 0),
          lid=0, look=(0, -.3))
    c.cycle(0.4, 2.3, .24, dict(rl=(-6, 0, -11), ll=(-6, 0, 3), root=(0, 0, 2)),
            dict(rl=(-6, 0, 3), ll=(-6, 0, -11), root=(0, 0, -2)))
    c.wobble(0.4, 2.3, 9, "ra_pos", .35, base=(0, -.8, 0), axis=1)
    c.wobble(0.4, 2.3, 9, "la_pos", .35, base=(0, -.8, 0), axis=1)
    c.wobble(0.4, 2.3, 11, "head", 2.5, base=(-6, 0, 0), axis=1)
    for t, x in ((0.7, .5), (1.3, -.5), (1.9, .3)):
        c.key(t, look=(x, -.3))
    c.key(2.45, **clasp, waist=(6, 0, 0), root_pos=(0, .3, 0), look=(0, 0))


@clip("clutch_arm", "Clutches a hurt arm", trigger="hurt", weight=2.5, mirror="free", length=1.3, blend=(.04, .3))
def _(c):
    c.key(0.06, la=(-14, 0, 26), waist=(-6, 0, 4), head=(-8, 0, 0), root_pos=(0, 0, .6), lid=1)
    c.key(0.22, ra=(-78, -90, 0), la=(-4, 0, 12), waist=(12, -10, 4), head=(16, -20, 4), root_pos=(0, .4, .2),
          look=(-.5, .4), lid=.85)
    c.key(0.42, ra_pos=(0, -.4, 0), root=(0, 0, 2))
    c.key(0.6, ra=(-80, -92, 0), la=(-2, 0, 10), waist=(10, -10, 4), head=(18, -22, 6), ra_pos=(0, 0, 0), root=(0, 0, -1))
    c.key(0.9, ra=(-56, -66, 0), waist=(6, -6, 2), head=(8, -10, 2), root_pos=(0, 0, 0), root=(0, 0, 0), lid=.5)


@clip("double_over", "Doubles over winded", trigger="hurt", weight=2, mirror="never", length=1.35, blend=(.04, .3))
def _(c):
    belly = dict(ra=(-34, -46, 0), la=(-34, -46, 0))
    c.key(0.05, ra=(-56, -30, 0), la=(-56, -30, 0), waist=(18, 0, 0), head=(-10, 0, 0), root_pos=(0, 0, .8), lid=1)
    c.key(0.2, **belly, waist=(42, 0, 0), head=(-6, 0, 0), root_pos=(0, 1.2, .6), lid=1, look=(0, .4))
    c.key(0.55, **belly, waist=(38, 0, 0), head=(-12, 0, 0), root_pos=(0, 1.0, .4), lid=.9)
    c.key(0.85, ra=(-30, -40, 0), la=(-30, -40, 0), waist=(20, 0, 0), head=(-6, 0, 0), root_pos=(0, .4, 0), lid=.6)


@clip("stubbed_toe_hop", "Hops on one foot clutching a toe", trigger="hurt", weight=1.5, mirror="free", length=1.4,
      blend=(.04, .3), boost={"personality:playful": 1.5, "child": 1.5})
def _(c):
    reach = dict(ra=(-36, -12, 0), la=(-30, -4, 6))
    c.key(0.06, rl=(-30, 0, 0), head=(-14, 0, 0), waist=(-4, 0, 0), lid=1)
    c.key(0.2, rl=(-64, 0, 4), **reach, waist=(28, 0, 0), head=(-12, 0, 0), lid=1)
    for i, t in enumerate((0.3, 0.55, 0.8)):
        c.key(t, root_pos=(0, -2.2, 0), root=(0, 0, 4 if i % 2 else -4), head=(-14, 0, 6 if i % 2 else -6))
        c.key(t + .12, root_pos=(0, 0, 0))
    c.key(0.92, rl=(-58, 0, 4), **reach, waist=(24, 0, 0), lid=.85)
    c.key(1.05, root=(0, 0, 0))
