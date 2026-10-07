"""Everyday idles: what anyone does while standing around the village."""
from kit import clip, ARMS_CROSSED, HANDS_BEHIND, HANDS_ON_HIPS, HAND_TO_MOUTH, HAND_TO_CHEST


@clip("look_around", "Looks around", weight=5, mirror="free", length=4.6)
def _(c):
    c.key(0.55, head=(0, 36, 3), waist=(0, 6, 0), look=(.6, 0))
    c.key(1.45, head=(2, 40, 3), waist=(0, 7, 0), look=(.75, .1))
    c.key(2.05, head=(-3, -6, -1), waist=(0, 0, 0), look=(0, 0))
    c.key(2.7, head=(-2, -38, -3), waist=(0, -6, 0), look=(-.7, 0))
    c.key(3.6, head=(1, -34, -2), waist=(0, -5, 0), look=(-.6, .15))


@clip("weight_shift", "Shifts weight", weight=4, mirror="free", length=5.2, blend=(.6, .8))
def _(c):
    shift = dict(root=(0, 0, 2.2), waist=(0, 4, -3.5), head=(0, -4, 2), ra=(0, 0, 5), la=(0, 0, -1),
                 rl=(-4, 8, 3), ll=(0, 0, -1))
    c.key(1.0, **shift)
    c.key(3.9, **{**shift, "head": (2, -8, 3), "waist": (0, 6, -3)})


@clip("stretch_up", "Big stretch", weight=3, require=["adult"], avoid=["rain"], boost={"morning": 4, "evening": 1.5},
      mirror="never", length=4.0)
def _(c):
    # Raised through the sides: roll lifts a hanging arm outward and up into a V overhead.
    c.key(0.5, ra=(-40, 0, 70), la=(-40, 0, 70), waist=(-2, 0, 0), head=(-6, 0, 0))
    c.key(1.1, ra=(-14, 0, 150), la=(-14, 0, 150), waist=(-10, 0, 0), head=(-22, 0, 0), root_pos=(0, -.8, 0), lid=.7)
    c.key(1.9, ra=(-10, 0, 160), la=(-10, 0, 160), waist=(-13, 0, 0), head=(-27, 0, 0), root_pos=(0, -1.1, 0), lid=.85)
    c.key(2.25, waist=(-12, 0, 5))
    c.key(2.55, waist=(-11, 0, -5))
    c.key(3.1, ra=(-8, 0, 54), la=(-8, 0, 54), waist=(3, 0, 0), head=(6, 0, 0), root_pos=(0, 0, 0), lid=0)


@clip("yawn", "Yawns", weight=2, boost={"morning": 3, "evening": 3, "night": 4}, length=3.4)
def _(c):
    c.key(0.5, head=(-12, 0, 4), ra=(-88, -30, 0), waist=(-3, 0, 0), lid=.5)
    c.key(1.0, head=(-22, 0, 6), **HAND_TO_MOUTH, la=(-8, 0, 14), waist=(-6, 0, 0), lid=1)
    c.key(1.9, head=(-24, 0, 6), ra=(-115, -42, 0), lid=1)
    c.key(2.5, head=(7, 0, 0), ra=(-18, 0, 6), la=(0, 0, 4), waist=(3, 0, 0), lid=.4)


@clip("scratch_head", "Scratches head", weight=3, boost={"personality:curious": 2, "personality:thoughtful": 2, "job:nitwit": 3},
      length=3.0)
def _(c):
    # Overhead, roll tips the arm inward so the hand rests on the head.
    c.key(0.55, ra=(-164, 0, 14), head=(4, 8, -10), look=(.2, -.5))
    c.wobble(0.7, 2.0, 5, "ra", 7, base=(-164, 0, 14), axis=1)
    c.key(2.0, head=(6, 10, -12))
    c.key(2.45, ra=(-58, 0, 4), head=(1, 2, -4), look=(0, 0))


@clip("arms_crossed", "Crosses arms", weight=3, require=["adult"],
      boost={"personality:reserved": 3, "personality:pragmatic": 3, "personality:protective": 2}, length=5.6)
def _(c):
    c.key(0.5, **ARMS_CROSSED, waist=(-3, 0, 0), head=(-4, 0, 0))
    c.key(1.8, head=(-3, 4, 0), rl=(0, 0, 3))
    c.cycle(2.0, 2.9, .3, dict(rl=(-12, 0, 3)), dict(rl=(0, 0, 3)), end_on="b")
    c.key(3.6, head=(-2, -14, 2), look=(-.4, 0))
    c.key(4.7, **ARMS_CROSSED, head=(-4, -10, 1), look=(-.2, 0))


@clip("hands_on_hips", "Hands on hips", weight=2, require=["adult"],
      boost={"personality:steadfast": 3, "personality:protective": 3, "job:knight": 2, "job:farmer": 1.5}, length=5.0)
def _(c):
    c.key(0.6, **HANDS_ON_HIPS, waist=(-5, 0, 0), head=(-6, 12, 0), rl=(0, 0, 4), ll=(0, 0, 4))
    c.key(2.5, head=(-4, -14, 0), waist=(-5, -4, 0))
    c.key(4.2, **HANDS_ON_HIPS, head=(-6, 0, 0), waist=(-4, 0, 0))


@clip("rock_on_heels", "Rocks on heels", weight=3, require=["adult"], mirror="never",
      boost={"personality:thoughtful": 2, "personality:gentle": 2, "personality:meticulous": 2, "job:librarian": 2, "job:scholar": 2},
      length=5.2)
def _(c):
    c.key(0.6, **HANDS_BEHIND, head=(-3, 0, 0))
    for i, t in enumerate((1.0, 1.8, 2.6, 3.4)):
        forward = i % 2 == 0
        c.key(t, root=(3, 0, 0) if forward else (-2.4, 0, 0), root_pos=(0, -.5, 0) if forward else (0, 0, 0),
              head=(-5, 0, 0) if forward else (-1, 0, 0))
    c.key(4.2, root=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(4.6, **HANDS_BEHIND)


@clip("hum_a_tune", "Hums a tune", weight=2, mirror="free",
      boost={"personality:playful": 5, "personality:warmhearted": 2, "personality:gentle": 2, "job:bard": 4, "child": 2}, length=6.0)
def _(c):
    a = dict(root=(0, 0, 3), head=(3, 4, -7), ra=(-10, 0, 8), la=(6, 0, 4), waist=(0, 4, 0))
    b = dict(root=(0, 0, -3), head=(3, -4, 7), ra=(6, 0, 4), la=(-10, 0, 8), waist=(0, -4, 0))
    c.cycle(0.45, 5.4, 1.5, a, b)
    c.hold(0.6, 5.2, lid=.35)


@clip("dust_off", "Dusts off sleeves", weight=2, require=["adult"], boost={"personality:meticulous": 4, "job:tailor": 3}, length=3.4)
def _(c):
    c.key(0.4, la=(-52, 10, 0), ra=(-58, -46, 0), head=(18, -12, 0), look=(-.3, .6))
    c.cycle(0.5, 1.6, .34, dict(ra=(-62, -48, 0)), dict(ra=(-50, -26, 0)))
    c.key(1.95, ra=(-52, 10, 0), la=(-58, -46, 0), head=(18, 12, 0), look=(.3, .6))
    c.cycle(2.05, 2.95, .34, dict(la=(-62, -48, 0)), dict(la=(-50, -26, 0)))


@clip("neck_roll", "Rolls neck", weight=2, mirror="free", boost={"morning": 2, "job:armorer": 2, "job:toolsmith": 2, "job:weaponsmith": 2},
      length=3.2)
def _(c):
    c.key(0.4, head=(16, 0, 0), lid=.3)
    c.key(0.9, head=(4, 0, 17), ra_pos=(0, -1, 0), la_pos=(0, -1, 0), lid=.6)
    c.key(1.4, head=(-15, 0, 0), ra_pos=(0, -.4, 0), la_pos=(0, -.4, 0))
    c.key(1.9, head=(4, 0, -17), ra_pos=(0, -1, 0), la_pos=(0, -1, 0))
    c.key(2.35, head=(10, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid=0)


@clip("wipe_brow", "Wipes brow", weight=2, require=["adult"], avoid=["night", "rain", "cold"],
      boost={"day": 2, "job:farmer": 3, "job:armorer": 2, "job:toolsmith": 2, "job:weaponsmith": 2, "job:mason": 2, "job:carpenter": 2},
      length=2.8)
def _(c):
    c.key(0.5, ra=(-152, -32, 0), head=(-6, 0, 0), lid=.5)
    c.key(1.05, ra=(-146, 12, 10), head=(-4, 6, 0))
    c.key(1.45, ra=(-92, 22, 24))
    c.key(2.0, ra=(-10, 0, 8), waist=(4, 0, 0), head=(9, 0, 0), lid=.2)


@clip("rub_hands", "Rubs hands together", weight=2, boost={"cold": 5, "rain": 2, "night": 2, "personality:warmhearted": 1.5},
      mirror="never", length=3.0)
def _(c):
    c.key(0.4, ra=(-58, -34, 0), la=(-58, -34, 0), head=(10, 0, 0), look=(0, .5))
    c.cycle(0.5, 1.9, .3, dict(ra=(-63, -30, 0), la=(-53, -38, 0)), dict(ra=(-53, -38, 0), la=(-63, -30, 0)))
    c.key(2.2, ra=(-102, -38, 0), la=(-102, -38, 0), head=(-4, 0, 0), lid=.5, look=(0, 0))
    c.key(2.55, ra=(-96, -36, 0), la=(-96, -36, 0))


@clip("kick_pebble", "Kicks a pebble", weight=2, boost={"personality:playful": 3, "personality:adventurous": 2, "child": 2}, length=2.9)
def _(c):
    c.key(0.4, head=(22, 0, 0), look=(0, .8), rl=(4, 0, 0))
    c.key(0.9, rl=(20, 0, 0), ra=(-12, 0, 6), la=(8, 0, 6))
    c.key(1.1, rl=(-44, 0, 0), ra=(14, 0, 4), la=(-16, 0, 4), waist=(-4, 0, 0))
    c.key(1.35, rl=(-30, 0, 0))
    c.key(1.8, rl=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(4, -12, 0), look=(-.3, 0))
    c.key(2.3, head=(2, -16, 0))


@clip("sneeze", "Sneezes", weight=.6, mirror="free", length=2.4)
def _(c):
    c.key(0.25, head=(-6, 0, 0), lid=.3)
    c.key(0.9, head=(-24, 0, 0), waist=(-8, 0, 0), root_pos=(0, -.5, 0), lid=.8)
    c.key(1.15, head=(-27, 0, 0), ra=(-100, -40, 0))
    c.key(1.32, head=(26, 0, 0), waist=(16, 0, 0), ra=(-112, -40, 0), root_pos=(0, .3, 0), lid=1)
    c.key(1.5, head=(16, 0, 0), waist=(8, 0, 0))
    c.key(2.0, head=(0, 0, 5), waist=(0, 0, 0), ra=(-10, 0, 4), root_pos=(0, 0, 0), lid=0)


@clip("pat_pockets", "Pats pockets", weight=1.5, require=["adult"], boost={"personality:meticulous": 1.5, "job:nitwit": 2},
      mirror="never", length=3.6)
def _(c):
    c.key(0.4, ra=(6, 0, 11), la=(6, 0, 11), head=(18, 0, 0), look=(0, .6))
    c.cycle(0.5, 1.3, .26, dict(ra=(6, 0, 11), la=(6, 0, 4)), dict(ra=(6, 0, 4), la=(6, 0, 11)))
    c.key(1.55, head=(12, -20, 0), la=(-20, 0, 6), look=(-.4, .5))
    c.key(2.0, ra=(-32, -22, 0), head=(8, 0, 0), look=(0, .3))
    c.key(2.45, ra=(-58, -50, 0), la=(0, 0, 4), waist=(4, 0, 0), head=(-6, 0, 0), lid=.45, look=(0, 0))
    c.key(3.0, **HAND_TO_CHEST, head=(-2, 0, 0), lid=.2)


@clip("shrug", "Shrugs", weight=1.5, mirror="free", length=2.4, also={"talk_shrug": "talk"})
def _(c):
    c.key(0.45, ra_pos=(0, -1.4, 0), la_pos=(0, -1.4, 0), ra=(-26, 16, 18), la=(-26, 16, 18), head=(4, 0, 10), waist=(-2, 0, 0))
    c.key(1.1, ra_pos=(0, -1.5, 0), la_pos=(0, -1.5, 0), head=(4, 0, 11))
    c.key(1.6, ra_pos=(0, .4, 0), la_pos=(0, .4, 0), ra=(0, 0, 2), la=(0, 0, 2), head=(10, 0, 4), waist=(4, 0, 0), lid=.4)


@clip("side_stretch", "Side stretch", weight=2, require=["adult"], boost={"morning": 3}, avoid=["rain"], mirror="free", length=4.4)
def _(c):
    c.key(0.6, ra=(-175, 0, 18), la=(8, 0, -6), waist=(0, 0, 13), head=(0, 0, 7), lid=.5)
    c.key(1.6, ra=(-178, 0, 30), waist=(0, 0, 20), head=(0, 0, 12), lid=.7)
    c.key(2.2, ra=(-60, 0, 20), la=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0), lid=.2)
    c.key(2.9, la=(-175, 0, 18), ra=(8, 0, -6), waist=(0, 0, -13), head=(0, 0, -7), lid=.5)
    c.key(3.6, la=(-178, 0, 30), waist=(0, 0, -20), head=(0, 0, -12), lid=.7)
    c.key(4.0, la=(-60, 0, 20), ra=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("tap_foot", "Taps foot", weight=1.5, require=["adult"], boost={"personality:pragmatic": 2, "job:tavern_keeper": 1.5}, length=3.4)
def _(c):
    c.key(0.4, **HANDS_ON_HIPS, head=(-2, -12, 0), look=(-.3, 0))
    c.cycle(0.6, 2.7, .34, dict(rl=(-13, 0, 4)), dict(rl=(-1, 0, 4)), end_on="b")
    c.key(2.9, **HANDS_ON_HIPS, head=(2, 0, 0), look=(0, 0))


@clip("watch_the_sky", "Watches the sky", weight=1.5, mirror="free", boost={"night": 4, "evening": 2}, length=4.6)
def _(c):
    c.key(0.7, head=(-36, 10, 0), waist=(-6, 0, 0), look=(.2, -.8), **HANDS_BEHIND)
    c.key(2.2, head=(-33, -12, 0), look=(-.3, -.8))
    c.key(3.5, head=(-30, -6, 0), look=(-.1, -.7), **HANDS_BEHIND)
