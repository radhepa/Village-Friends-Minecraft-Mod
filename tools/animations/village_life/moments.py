"""Moments: more small things anyone does while standing around the village."""
from kit import clip, ARMS_CROSSED, HAND_TO_CHEST, HANDS_ON_HIPS, SHIELD_EYES


@clip("crack_knuckles", "Cracks knuckles", weight=1.1, require=["adult"], mirror="never",
      boost={"smith": 2, "guard": 1.5, "personality:pragmatic": 2, "morning": 1.5}, length=3.4)
def _(c):
    c.key(0.45, ra=(-68, -40, 0), la=(-68, -40, 0), head=(8, 0, 0), look=(0, .4))
    c.key(0.8, ra=(-64, -40, 0), la=(-64, -40, 0), waist=(3, 0, 0))
    c.key(1.15, ra=(-92, -20, 0), la=(-92, -20, 0), ra_pos=(0, 0, -1), la_pos=(0, 0, -1), waist=(-3, 0, 0),
          head=(-6, 0, 0), lid=.6, look=(0, 0))
    c.wobble(1.2, 1.75, 6, "ra", 3, base=(-92, -20, 0))
    c.wobble(1.2, 1.75, 6, "la", 3, base=(-92, -20, 0))
    c.key(2.05, ra=(-34, 0, 10), la=(-34, 0, 10), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), head=(2, 0, 0), lid=0)
    c.wobble(2.1, 2.8, 7, "ra", 7, base=(-24, 0, 10), axis=2)
    c.wobble(2.1, 2.8, 7, "la", 7, base=(-24, 0, 10), axis=2)


@clip("check_fingernails", "Checks fingernails", weight=1.1, require=["adult"],
      boost={"personality:meticulous": 3, "job:tailor": 2, "job:painter": 1.5}, length=4.4)
def _(c):
    c.key(0.5, ra=(-78, -34, 0), head=(16, -6, 0), look=(-.1, .6))
    c.key(1.3, ra=(-80, -32, 0), head=(18, -8, 2))
    c.key(1.75, ra=(-88, 4, 6), head=(8, 6, -6), waist=(-3, 0, 0), look=(.3, .3))
    c.key(2.35, ra=(-86, 6, 6), head=(9, 8, -8))
    c.key(2.7, **HAND_TO_CHEST, head=(14, -4, 0), waist=(0, 0, 0), look=(0, .6))
    c.wobble(2.75, 3.25, 6, "ra", 8, base=(-58, -50, 0), axis=1)
    c.key(3.55, ra=(-80, -32, 0), head=(16, -6, 0), lid=.3, look=(-.1, .6))
    c.key(3.85, lid=0)


@clip("adjust_collar", "Adjusts collar", weight=1.1, require=["adult"], mirror="never",
      boost={"personality:meticulous": 2, "job:tailor": 2, "job:tavern_keeper": 1.5, "evening": 1.5}, length=3.6)
def _(c):
    c.key(0.45, ra=(-100, -40, 0), la=(-100, -40, 0), head=(-4, 0, 0))
    c.key(0.75, ra=(-86, -22, 8), la=(-86, -22, 8), head=(-14, 0, 0), lid=.3)
    c.key(1.0, ra=(-101, -40, 0), la=(-101, -40, 0), head=(-8, 0, 0))
    c.key(1.25, ra=(-86, -22, 8), la=(-86, -22, 8), head=(-16, 0, 0))
    c.key(1.55, head=(-10, 10, 0))
    c.key(1.85, head=(-10, -10, 0))
    c.key(2.2, ra=(-50, -40, 0), la=(-50, -40, 0), head=(-3, 0, 0), lid=0)
    c.key(2.7, ra=(-24, -16, 0), la=(-24, -16, 0), head=(-8, 0, 0), waist=(-3, 0, 0), lid=.25)


@clip("tuck_hair", "Tucks hair behind an ear", weight=1.0,
      boost={"personality:gentle": 2.5, "personality:imaginative": 1.5, "personality:reserved": 1.5}, length=3.2)
def _(c):
    c.key(0.5, ra=(-140, -20, 0), head=(4, 6, -6), look=(.1, .2))
    c.key(0.85, ra=(-150, 6, 14), head=(6, 8, -8))
    c.key(1.1, ra=(-148, 10, 18))
    c.key(1.6, ra=(-40, 0, 6), head=(8, -10, 4), look=(-.5, .4), lid=.35)
    c.key(2.5, head=(6, -6, 3), look=(-.2, .2), lid=.2)


@clip("brush_off_shoulder", "Brushes off a shoulder", weight=1.0,
      boost={"personality:playful": 2.5, "personality:adventurous": 1.5, "job:nitwit": 2}, length=3.0)
def _(c):
    c.key(0.4, ra=(-96, -66, 0), head=(10, -26, 0), look=(-.5, .4))
    c.cycle(0.4, 1.2, .4, dict(ra=(-96, -66, 0)), dict(ra=(-72, -38, 0)))
    c.key(1.45, ra=(-60, -20, 10))
    c.key(1.85, ra=(-20, 0, 6), head=(-10, 6, 0), waist=(-3, 0, 0), look=(.2, -.1), lid=.45)
    c.key(2.5, head=(-8, 4, 0), lid=.4)


@clip("lean_on_wall", "Leans back against a wall", weight=1.2, require=["adult"], mirror="free",
      boost={"personality:reserved": 2, "personality:pragmatic": 1.5, "evening": 1.5, "job:nitwit": 1.5}, length=6.4,
      blend=(.5, .6))
def _(c):
    lean = dict(root=(-8, 0, 0), **ARMS_CROSSED, rl=(-6, 0, -20), ll=(0, 0, 3))
    c.key(0.8, **lean, head=(4, 0, 0), lid=.3)
    c.key(2.3, head=(2, 16, 0), look=(.4, 0))
    c.key(3.6, head=(4, -12, 0), look=(-.3, .1))
    c.cycle(4.0, 4.9, .45, dict(rl=(-12, 0, -20)), dict(rl=(-6, 0, -20)), end_on="b")
    c.key(5.6, **lean, head=(4, 0, 0), look=(0, 0), lid=.3)


@clip("stomach_growls", "Stomach growls", weight=1.0, boost={"evening": 2, "morning": 1.5, "child": 1.5}, length=3.6)
def _(c):
    c.key(0.35, waist=(6, 0, 0), root_pos=(0, .4, 0), ra=(-30, -40, 0), head=(14, 0, 0), look=(0, .7))
    c.key(0.65, waist=(2, 0, 0), root_pos=(0, 0, 0), ra=(-34, -48, 0), head=(22, 0, 0), look=(0, .9))
    c.cycle(0.9, 2.1, .6, dict(ra=(-38, -50, 0)), dict(ra=(-30, -42, 0)))
    c.key(2.25, waist=(5, 0, 0), root_pos=(0, .4, 0), head=(24, 0, 0))
    c.key(2.5, waist=(1, 0, 0), root_pos=(0, 0, 0), head=(16, -10, -8), look=(-.5, .5), lid=.4)
    c.key(3.05, ra=(-34, -48, 0), head=(18, 6, -6), look=(.2, .6), lid=.45)


@clip("scratch_back", "Scratches an itch on the back", weight=1.0, boost={"job:nitwit": 2, "personality:playful": 1.5}, length=3.8)
def _(c):
    c.key(0.5, ra=(20, 0, -20), la=(-6, 0, 10), waist=(0, 14, 0), head=(4, 24, 0), look=(.6, .2))
    c.key(0.9, ra=(26, 0, -34), la=(-12, 0, 18), waist=(-5, 18, -6), head=(-2, 30, -4), root_pos=(0, -.5, 0), lid=.5)
    c.wobble(1.0, 2.2, 5, "ra", 7, base=(26, 0, -34))
    c.key(2.4, head=(-8, 20, 0), lid=.9, look=(.3, 0))
    c.key(2.9, ra=(10, 0, 2), la=(0, 0, 4), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(6, 0, 0), lid=.3, look=(0, 0))


@clip("swat_a_bee", "Swats away a bee", weight=1.0, mirror="free", avoid=["rain", "cold", "night"],
      boost={"day": 2, "job:farmer": 2, "job:shepherd": 1.5, "child": 1.5}, length=3.0)
def _(c):
    c.key(0.3, head=(-8, 22, 0), waist=(-3, 0, -4), look=(.7, -.4), lid=0)
    c.key(0.45, ra=(-120, -30, 0), la=(-60, -20, 0), head=(-6, -14, 6), waist=(-6, 0, 6), look=(.5, -.2))
    c.cycle(0.55, 1.65, .32, dict(ra=(-138, 20, 24), la=(-118, -40, 0), head=(-4, -16, 8), root_pos=(0, -.4, 0)),
            dict(ra=(-96, -44, 0), la=(-140, 22, 24), head=(-6, 14, -6), root_pos=(0, 0, 0)))
    c.key(1.9, ra=(-70, 0, 20), la=(-70, 0, 20), head=(-10, 18, 0), waist=(-4, 0, 0), look=(.7, -.3), lid=.2)
    c.key(2.2, head=(-8, -16, 0), look=(-.7, -.3))
    c.key(2.55, ra=(0, 0, 0), la=(0, 0, 0), head=(4, 0, 0), waist=(0, 0, 0), look=(0, 0), lid=.4)


@clip("rub_itchy_nose", "Rubs an itchy nose", weight=1.1, boost={"cold": 2, "morning": 1.5}, length=2.6)
def _(c):
    c.key(0.25, head=(-4, 0, 3), lid=.3)
    c.key(0.45, ra=(-117, -40, 0), head=(-6, 0, 3), lid=.55)
    c.wobble(0.5, 1.4, 6, "ra", 9, base=(-117, -40, 0), axis=1)
    c.key(1.55, head=(-10, 0, 0), lid=.75)
    c.key(1.7, head=(2, 0, 0), lid=.3)
    c.key(1.95, ra=(-24, -8, 4), head=(4, 0, -3), lid=0)


@clip("blow_hair_strand", "Blows a hair strand off the face", weight=1.0, mirror="free",
      boost={"personality:playful": 2, "personality:pragmatic": 1.5, "job:farmer": 1.5}, length=3.4)
def _(c):
    c.key(0.4, head=(6, 0, 0), look=(.1, -.8))
    c.key(0.6, head=(8, 0, 0))
    c.key(0.75, head=(-14, 0, -4), root_pos=(0, -.3, 0), lid=.4, look=(0, -.9))
    c.key(1.1, head=(-6, 0, -2), root_pos=(0, 0, 0), lid=0, look=(.1, -.6))
    c.key(1.4, head=(6, 0, 0), look=(.1, -.8))
    c.key(1.6, head=(9, 0, 0), waist=(2, 0, 0))
    c.key(1.75, head=(-20, 0, -6), waist=(-4, 0, 0), root_pos=(0, -.4, 0), lid=.5, look=(0, -.9))
    c.key(2.05, head=(-4, 0, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), lid=0, look=(0, -.4))
    c.rest(2.1, "ra")
    c.key(2.35, ra=(-150, 10, 16), head=(2, 6, 0))
    c.key(2.6, ra=(-140, 30, 30), head=(0, 4, 0), lid=.35, look=(0, 0))
    c.key(2.95, ra=(-20, 0, 8))


@clip("roll_shoulders", "Rolls the shoulders", weight=1.1, mirror="never",
      boost={"smith": 2, "guard": 1.5, "job:mason": 2, "job:carpenter": 2, "job:farmer": 1.5, "morning": 1.5}, length=3.6)
def _(c):
    fwd = dict(ra_pos=(0, -.4, -1.8), la_pos=(0, -.4, -1.8), ra=(-8, 0, 3), la=(-8, 0, 3), waist=(3, 0, 0))
    up = dict(ra_pos=(0, -2.2, 0), la_pos=(0, -2.2, 0), ra=(-2, 0, 4), la=(-2, 0, 4), waist=(0, 0, 0))
    back = dict(ra_pos=(0, -1, 1.8), la_pos=(0, -1, 1.8), ra=(8, 0, 3), la=(8, 0, 3), waist=(-4, 0, 0))
    down = dict(ra_pos=(0, .4, .3), la_pos=(0, .4, .3), ra=(2, 0, 2), la=(2, 0, 2), waist=(-1, 0, 0))
    for i, pose in enumerate((fwd, up, back, down, fwd, up, back, down)):
        c.key(0.35 + i * .22, **pose)
    c.hold(0.35, 2.0, head=(-4, 0, 0), lid=.45)
    c.key(2.25, ra_pos=(0, -1.4, 0), la_pos=(0, .2, 0), head=(-2, 0, -8))
    c.key(2.6, ra_pos=(0, .2, 0), la_pos=(0, -1.4, 0), head=(-2, 0, 8))
    c.key(2.95, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), waist=(0, 0, 0), head=(2, 0, 0), lid=0)


@clip("touch_toes", "Touches toes", weight=0.9, mirror="never", avoid=["rain"],
      boost={"morning": 3, "personality:adventurous": 1.5, "guard": 1.5}, length=4.6)
def _(c):
    c.key(0.6, ra=(-10, 0, 150), la=(-10, 0, 150), waist=(-6, 0, 0), head=(-12, 0, 0), lid=.4)
    c.key(1.3, ra=(-76, 0, 4), la=(-76, 0, 4), waist=(74, 0, 0), head=(18, 0, 0), lid=.7)
    c.key(1.7, waist=(82, 0, 0), ra=(-80, 0, 4), la=(-80, 0, 4))
    c.key(2.0, waist=(74, 0, 0))
    c.key(2.35, waist=(84, 0, 0), ra=(-82, 0, 4), la=(-82, 0, 4))
    c.key(3.2, ra=(-6, 0, 8), la=(-6, 0, 8), waist=(-6, 0, 0), head=(-10, 0, 0), lid=.3)
    c.key(3.7, waist=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("squint_at_sun", "Squints at the sun", weight=1.1, avoid=["night", "rain"], boost={"day": 2, "morning": 1.5},
      length=3.6)
def _(c):
    c.key(0.5, head=(-26, 10, 0), look=(.2, -.8), lid=.55)
    c.key(0.8, head=(-28, 10, 0), lid=.85)
    c.key(1.05, head=(6, -14, 6), look=(-.2, .3), lid=1)
    c.rest(1.0, "ra")
    c.key(1.4, **SHIELD_EYES, head=(-4, 0, 0), lid=.5)
    c.key(1.8, head=(-20, 8, 0), look=(.2, -.7), lid=.65)
    c.key(2.5, **SHIELD_EYES, head=(-18, 12, 0), lid=.6)
    c.key(2.9, ra=(-30, -10, 4), head=(4, 0, 0), look=(0, 0), lid=.9)
    c.key(3.1, lid=0)


@clip("daydream", "Daydreams", weight=1.1, mirror="never",
      boost={"personality:imaginative": 3, "personality:gentle": 2, "personality:thoughtful": 1.5, "evening": 1.5}, length=6.0,
      blend=(.5, .5))
def _(c):
    dream = dict(ra=(-104, -44, 0), la=(-104, -44, 0), head=(-6, 8, 9), look=(.3, -.5), lid=.5)
    c.key(0.8, **dream)
    c.cycle(1.0, 4.6, 2.4, dict(root=(0, 0, 2.5)), dict(root=(0, 0, -2.5)))
    c.key(4.4, **dream)
    c.key(4.75, ra=(-80, -30, 0), la=(-80, -30, 0), head=(2, 0, 0), look=(0, 0), lid=0)
    c.key(5.2, ra=(-10, 0, 4), la=(-10, 0, 4))


@clip("deep_sigh", "Deep sigh", weight=1.0, mirror="never",
      boost={"evening": 2, "rain": 1.5, "personality:thoughtful": 1.5, "personality:reserved": 1.5}, length=3.2)
def _(c):
    c.key(0.9, ra_pos=(0, -1.6, 0), la_pos=(0, -1.6, 0), head=(-10, 0, 0), waist=(-4, 0, 0), lid=.3)
    c.key(1.2, ra_pos=(0, -1.7, 0), la_pos=(0, -1.7, 0), head=(-11, 0, 0))
    c.key(1.75, ra_pos=(0, .6, 0), la_pos=(0, .6, 0), ra=(4, 0, -2), la=(4, 0, -2), head=(16, 0, 3), waist=(6, 0, 0), lid=.7)
    c.key(2.4, ra_pos=(0, .4, 0), la_pos=(0, .4, 0), head=(12, 0, 2), waist=(4, 0, 0), lid=.5)


@clip("hiccups", "Has the hiccups", weight=1.0, mirror="free", boost={"evening": 1.5, "job:tavern_keeper": 2, "child": 1.5},
      length=4.2)
def _(c):
    for t in (0.6, 1.65, 2.55, 3.3):
        c.key(t - .08, root_pos=(0, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), body=(0, 0, 0))
        c.key(t, root_pos=(0, -.9, 0), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), body=(-4, 0, 0))
        c.key(t + .2, root_pos=(0, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), body=(0, 0, 0))
    c.key(0.52, head=(0, 0, 0), lid=0)
    c.key(0.62, head=(-10, 0, 0), lid=0, look=(0, 0))
    c.key(1.0, head=(8, 0, 4), look=(0, .4), lid=.2)
    c.key(1.57, head=(8, 0, 4))
    c.key(1.67, head=(-8, 0, 2), look=(.4, 0))
    c.rest(1.6, "ra")
    c.key(1.95, **HAND_TO_CHEST, head=(4, 0, 0), look=(0, .2))
    c.key(2.47, head=(4, 0, 0))
    c.key(2.57, head=(-10, 0, -4), lid=.1)
    c.key(2.9, head=(-6, 0, -6), look=(0, -.7), lid=.45)
    c.key(3.22, head=(-6, 0, -6))
    c.key(3.32, head=(-14, 0, -6))
    c.key(3.65, **HAND_TO_CHEST, head=(4, 0, -3), look=(0, .3), lid=.3)


@clip("finger_in_ear", "Wiggles a finger in an ear", weight=0.9, boost={"job:nitwit": 3, "child": 1.5, "personality:playful": 1.5},
      length=3.4)
def _(c):
    c.key(0.5, ra=(-140, 14, 18), head=(0, 0, -10), look=(.3, 0), lid=.3)
    c.wobble(0.6, 1.6, 7, "ra", 5, base=(-140, 14, 18), axis=1)
    c.key(1.6, head=(0, 0, -12), lid=.75)
    c.key(2.0, ra=(-82, -24, 0), head=(18, 0, 0), look=(0, .7), lid=0)
    c.key(2.4, ra=(-84, -22, 0), head=(20, 0, 3))
    c.key(2.6, ra=(-60, 30, 30), head=(4, 0, 0), look=(0, 0))
    c.key(2.9, ra=(-10, 0, 6))


@clip("check_boot_sole", "Checks a boot sole", weight=1.0, avoid=["night"],
      boost={"rain": 2, "job:farmer": 2, "job:shepherd": 1.5, "personality:meticulous": 1.5}, length=3.8)
def _(c):
    c.key(0.5, rl=(14, 0, 4), waist=(4, 16, 0), head=(14, 36, 0), look=(.7, .6), ra=(10, 0, 10), la=(-14, 0, 14))
    c.key(1.0, rl=(42, 0, 6), waist=(6, 22, -4), head=(22, 52, -6), root=(0, 0, -2), ra=(26, 0, 8), la=(-22, 0, 20))
    c.key(1.9, rl=(44, 0, 6), head=(24, 56, -8), lid=.3)
    c.key(2.15, head=(18, 46, -4), lid=.5)
    c.key(2.4, rl=(40, 0, 6), lid=.2)
    c.key(2.9, rl=(0, 0, 0), waist=(0, 0, 0), head=(4, 0, 0), root=(0, 0, 0), ra=(0, 0, 0), la=(0, 0, 0), look=(0, 0), lid=0)


@clip("stamp_mud_off", "Stamps mud off the boots", weight=1.0, mirror="free",
      boost={"rain": 3, "job:farmer": 2, "job:shepherd": 1.5, "morning": 1.5}, length=3.2)
def _(c):
    c.key(0.3, head=(18, 0, 0), look=(0, .8), waist=(4, 0, 0))
    for t, leg in ((0.55, "rl"), (0.95, "rl"), (1.4, "ll")):
        c.key(t - .2, **{leg: (0, 0, 2)}, root_pos=(0, 0, 0))
        c.key(t - .05, **{leg: (-34, 0, 4)}, ra=(-10, 0, 14), la=(-10, 0, 14))
        c.key(t + .05, **{leg: (0, 0, 2)}, root_pos=(0, .5, 0), ra=(-2, 0, 8), la=(-2, 0, 8))
        c.key(t + .2, root_pos=(0, 0, 0))
    c.key(1.9, rl=(0, 0, 2), head=(20, 6, 0))
    c.key(2.2, rl=(16, 0, 4), head=(22, 10, 0), look=(.2, .8))
    c.key(2.45, rl=(0, 0, 2), head=(14, 0, 0))
    c.key(2.7, head=(4, 0, 0), waist=(0, 0, 0), look=(0, .2))


@clip("twirl_hair", "Twirls a lock of hair", weight=1.0,
      boost={"personality:imaginative": 2, "personality:gentle": 2, "personality:playful": 1.5, "child": 1.5}, length=4.6,
      blend=(.4, .5))
def _(c):
    c.key(0.6, ra=(-128, 6, 14), head=(2, 8, -8), look=(.4, -.5), lid=.3)
    for i in range(10):
        t = 0.8 + i * .28
        c.key(t, ra=[(-134, 6, 14), (-128, 12, 18), (-122, 6, 14), (-128, 0, 10)][i % 4])
    c.cycle(0.8, 3.6, 2.0, dict(root=(0, 0, 2), head=(2, 10, -9)), dict(root=(0, 0, -1), head=(0, 4, -6)))
    c.key(3.9, ra=(-50, 4, 8), head=(2, 0, -2), look=(0, 0), lid=0)


@clip("fan_self", "Fans self on a hot day", weight=1.1, avoid=["cold", "night", "rain"],
      boost={"day": 2.5, "job:cook": 2, "smith": 1.5, "job:tavern_keeper": 1.5}, length=3.8)
def _(c):
    c.key(0.45, ra=(-100, -40, 0), la=HANDS_ON_HIPS["la"], head=(-10, 0, 4), lid=.5)
    c.cycle(0.55, 2.75, .28, dict(ra=(-102, -46, 0)), dict(ra=(-96, -4, 12)))
    c.hold(0.6, 2.7, head=(-12, 0, 5), lid=.55, look=(0, -.3))
    c.key(3.05, ra=(-20, 0, 6), la=(0, 0, 0), head=(6, 0, 0), lid=.3, look=(0, 0))
    c.key(3.3, lid=0)


@clip("cough_into_elbow", "Coughs into an elbow", weight=0.9, boost={"cold": 2.5, "rain": 1.5, "night": 1.5}, length=2.8)
def _(c):
    c.key(0.35, ra=(-104, -66, 0), head=(6, 8, 0), lid=.3)
    for t in (0.6, 1.0, 1.35):
        c.key(t - .05, waist=(0, 0, 0), head=(6, 8, 0), root_pos=(0, 0, 0))
        c.key(t + .07, waist=(10, 0, 0), head=(20, 12, 0), root_pos=(0, .3, 0), lid=.8)
    c.key(1.65, waist=(2, 0, 0), head=(8, 6, 0), root_pos=(0, 0, 0), lid=.4)
    c.key(1.95, ra=(-58, -50, 0), head=(-4, 0, 0), waist=(0, 0, 0), lid=.2)
    c.key(2.3, ra=(-20, -10, 4))


@clip("arm_circles", "Arm circles", weight=1.0, mirror="never", avoid=["rain"],
      boost={"morning": 3, "guard": 2, "personality:adventurous": 1.5, "child": 1.5}, length=4.8)
def _(c):
    ring = [(-26, 0, 86), (0, 0, 104), (26, 0, 86), (0, 0, 68)]
    c.key(0.5, ra=(0, 0, 86), la=(0, 0, 86), head=(-4, 0, 0), lid=.2)
    t = 0.7
    for i in range(8):
        c.key(t, ra=ring[i % 4], la=ring[i % 4])
        t += .17
    for i in range(8):
        c.key(t, ra=ring[-i % 4], la=ring[-i % 4])
        t += .17
    c.key(t, ra=(0, 0, 86), la=(0, 0, 86))
    c.key(t + .5, ra=(-4, 0, 6), la=(-4, 0, 6), head=(2, 0, 0), lid=0)


@clip("shuffle_feet", "Shuffles feet restlessly", weight=1.1, mirror="free",
      boost={"personality:reserved": 1.5, "personality:playful": 1.5, "child": 2, "cold": 1.5}, length=4.0)
def _(c):
    c.key(0.35, head=(10, 0, 0), look=(0, .5))
    steps = ((0.5, "rl", (-22, 8, 4), (0, 0, 3)), (0.95, "ll", (-20, -6, 4), (0, 0, -3)),
             (1.35, "rl", (-16, 18, 5), (0, 0, 2.5)), (1.9, "ll", (-24, 14, 4), (0, 0, -3.5)),
             (2.7, "rl", (16, 6, 3), (0, 0, 2)), (3.05, "ll", (-14, 0, 3), (0, 0, -2)))
    for t, leg, lift, sway in steps:
        c.key(t - .15, **{leg: (0, 0, 0)}, root=(0, 0, 0))
        c.key(t, **{leg: lift}, root=sway, root_pos=(0, -.3, 0))
        c.key(t + .18, **{leg: (0, lift[1] * .5, 0)}, root=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(2.3, head=(14, 6, 0), look=(.2, .7))
    c.key(3.3, head=(6, -4, 0), look=(-.2, .3))
    c.rest(3.5, "rl", "ll")


@clip("drum_fingers", "Drums fingers on a folded arm", weight=1.1,
      boost={"personality:pragmatic": 2, "personality:meticulous": 1.5, "job:scholar": 1.5, "job:librarian": 1.5}, length=4.6)
def _(c):
    folded = dict(ra=(-64, -46, -6), la=(-56, -40, -6))
    c.key(0.5, **folded, head=(2, -10, 0), look=(-.3, 0), lid=.25)
    for start in (0.8, 1.45, 2.9):
        for i in range(4):
            t = start + i * .1
            c.key(t, ra=(-70, -46, -6))
            c.key(t + .05, ra=(-62, -46, -6))
        c.key(start + .45, ra=(-64, -46, -6))
    c.key(2.0, head=(-8, 6, 4), look=(.3, -.7), lid=.35)
    c.key(2.55, head=(-6, 10, 4), look=(.4, -.6))
    c.key(2.8, head=(4, -6, 0), look=(-.2, .1), lid=.3)
    c.key(3.6, **folded, head=(4, -2, -3), lid=.4)
    c.key(4.0, ra=(-30, -20, 0), la=(-28, -16, 0), lid=.1)
    c.key(4.3, look=(0, 0))


@clip("wave_to_neighbor", "Waves to a neighbor across the way", weight=1.2, mirror="free",
      boost={"personality:warmhearted": 2.5, "personality:playful": 1.5, "social": 1.5, "morning": 1.5}, length=3.8)
def _(c):
    c.key(0.3, head=(-4, 30, 0), look=(.7, -.1), lid=0)
    c.key(0.55, head=(-8, 44, -4), waist=(0, 10, 0), root=(0, 8, 0), root_pos=(0, -.4, 0), look=(.8, -.2))
    c.key(0.8, ra=(-30, 10, 134), root_pos=(0, 0, 0), lid=.3)
    c.cycle(0.95, 2.4, .4, dict(ra=(-30, 10, 152), head=(-6, 46, -6)), dict(ra=(-30, 10, 120), head=(-8, 44, -2)))
    c.key(2.6, ra=(-26, 6, 100), head=(4, 42, -4), lid=.4)
    c.key(2.8, head=(-4, 42, -4))
    c.key(3.1, ra=(-6, 0, 10), head=(0, 18, 0), waist=(0, 0, 0), root=(0, 0, 0), look=(.3, 0), lid=.2)
    c.key(3.4, look=(0, 0), lid=0)


@clip("catch_falling_leaf", "Catches a falling leaf", weight=1.0, mirror="free", avoid=["rain", "night"],
      boost={"personality:curious": 2, "personality:imaginative": 1.5, "personality:playful": 1.5, "child": 2, "day": 1.5},
      length=5.2)
def _(c):
    c.key(0.4, head=(-24, 14, 0), look=(.4, -.8))
    c.key(0.9, head=(-14, -6, 0), look=(-.4, -.5))
    c.key(1.4, head=(-2, 10, 0), look=(.4, -.2))
    c.key(1.7, ra=(-40, -4, 4), la=(-16, 0, 6))
    c.key(1.95, ra=(-34, 0, 6), head=(10, -2, 0), look=(-.1, .3), lid=0)
    c.key(2.1, ra=(-84, -26, 0), waist=(8, 0, 0), head=(16, 0, 0), root_pos=(0, .4, 0), look=(0, .6))
    c.key(2.45, ra=(-82, -24, 0), waist=(4, 0, 0), root_pos=(0, 0, 0), la=(0, 0, 0))
    c.key(2.9, ra=(-76, -22, 0), waist=(0, 0, 0), head=(18, -6, -4), look=(-.2, .7), lid=.3)
    c.key(3.4, ra=(-88, -6, 8), head=(10, 4, -10), look=(.1, .5), lid=.4)
    c.key(3.95, ra=(-74, 18, 28), head=(-6, 12, 0), look=(.5, -.3), lid=.3)
    c.key(4.6, ra=(-10, 0, 6), head=(2, 0, 0), look=(0, 0), lid=0)


@clip("balance_on_one_leg", "Balances on one leg", weight=0.9, mirror="free", avoid=["rain"],
      boost={"child": 2, "personality:playful": 2, "personality:adventurous": 1.5, "morning": 1.5}, length=5.6)
def _(c):
    c.key(0.5, ra=(0, 0, 82), la=(0, 0, 82), head=(6, 0, 0), look=(0, .4), lid=.2)
    c.key(0.9, ll=(-34, 0, 8), root=(0, 0, -2))
    c.key(1.3, root=(0, 0, -5), ra=(0, 0, 68), la=(0, 0, 100), waist=(0, 0, 4), head=(4, 0, 6))
    c.key(1.7, root=(0, 0, 1), ra=(0, 0, 98), la=(0, 0, 70), waist=(0, 0, -3), head=(4, 0, -4))
    c.key(2.1, root=(0, 0, -3), ra=(0, 0, 80), la=(0, 0, 90), waist=(0, 0, 1), head=(5, 0, 2))
    c.key(2.6, root=(0, 0, 4), ra=(-20, 0, 124), la=(10, 0, 48), waist=(0, 0, -8), head=(0, 0, -10), ll=(-20, 0, 22),
          look=(.4, -.2), lid=0)
    c.key(2.95, root=(0, 0, -5), ra=(10, 0, 58), la=(-20, 0, 120), waist=(0, 0, 8), head=(2, 0, 10), ll=(-30, 0, 6))
    c.key(3.35, root=(0, 0, -2), ra=(0, 0, 82), la=(0, 0, 82), waist=(0, 0, 0), head=(4, 0, 0), ll=(-34, 0, 8), look=(0, .2),
          lid=.25)
    c.key(3.9, head=(-6, 0, 0), look=(0, 0), lid=.45)
    c.key(4.3, ll=(0, 0, 0), root=(0, 0, 0))
    c.key(4.7, **HANDS_ON_HIPS, head=(-8, 0, -4), lid=.4)
    c.key(5.1, lid=0)


@clip("count_the_clouds", "Points up and counts the clouds", weight=1.1, mirror="free", avoid=["rain", "night"],
      boost={"personality:imaginative": 2.5, "child": 2, "personality:curious": 1.5, "day": 1.5}, length=5.8)
def _(c):
    c.key(0.5, head=(-30, 0, 0), waist=(-4, 0, 0), look=(0, -.8))
    c.key(0.9, ra=(-150, 0, -4), la=(-40, -24, 0), head=(-32, -10, 0), look=(-.3, -.8))
    clouds = (((-150, 0, -4), (-32, -10, 0), (-.3, -.8)), ((-158, 0, -12), (-34, 4, 0), (0, -.8)),
              ((-146, 10, -26), (-30, 16, -4), (.4, -.8)), ((-132, 16, -40), (-26, 24, -4), (.6, -.7)))
    for i, (arm, head, look) in enumerate(clouds):
        t = 1.15 + i * .7
        c.key(t - .2, ra=arm, head=head, look=look, la=(-40, -24, 0))
        c.key(t, ra=(arm[0] - 8, arm[1], arm[2]), head=(head[0] + 5, head[1], head[2]), la=(-48, -24, 0))
        c.key(t + .15, ra=arm, head=head, la=(-40, -24, 0))
    c.key(3.9, ra=(-124, 10, -20), head=(-24, 6, 8), look=(.1, -.6), lid=.4)
    c.key(4.5, ra=(-40, 0, 6), la=(-30, -10, 0), head=(-10, 0, 0), waist=(0, 0, 0), look=(0, -.3), lid=.3)
    c.key(5.1, look=(0, 0), lid=0)
