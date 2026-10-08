"""Company: more greetings and gestures while talking with you."""
from kit import clip, HANDS_BEHIND, HAND_TO_CHEST, HAND_TO_CHIN, HAND_TO_MOUTH

# -- greetings ---------------------------------------------------------------------------------


@clip("greet_tip_hat", "Tips a hat", trigger="greet", weight=2, require=["adult"],
      boost={"personality:steadfast": 2, "personality:pragmatic": 2}, length=2.2)
def _(c):
    c.key(0.35, ra=(-150, -14, 20), head=(-2, 0, 0))
    c.key(0.6, ra=(-162, -10, 24), ra_pos=(0, -1.5, 0), head=(10, 0, -4), lid=.3)
    c.key(0.95, ra=(-162, -10, 24), ra_pos=(0, -1.5, 0), head=(12, 0, -4))
    c.key(1.2, ra=(-158, -10, 22), ra_pos=(0, 0, 0), head=(2, 0, 0), lid=.15)
    c.key(1.65, ra=(-30, 0, 10))


@clip("greet_curtsy", "Curtsies", trigger="greet", weight=2, require=["adult"], mirror="never",
      boost={"personality:gentle": 3, "personality:warmhearted": 2}, length=2.6)
def _(c):
    c.key(0.35, ra=(-14, 0, 26), la=(-14, 0, 26))
    c.key(0.8, ll=(22, 0, -12), rl=(-10, 0, 4), root_pos=(0, 1.2, 0), waist=(10, 0, 0), head=(16, 0, 6),
          ra=(-16, 0, 30), la=(-16, 0, 30), lid=.5)
    c.key(1.4, ll=(24, 0, -12), rl=(-10, 0, 4), root_pos=(0, 1.3, 0), waist=(12, 0, 0), head=(18, 0, 6))
    c.key(1.95, ll=(0, 0, 0), rl=(0, 0, 0), root_pos=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0),
          ra=(-10, 0, 14), la=(-10, 0, 14), lid=.2)


@clip("greet_brow_salute", "Casual salute", trigger="greet", weight=2, require=["adult"],
      boost={"personality:playful": 3, "personality:adventurous": 3}, length=1.9)
def _(c):
    c.key(0.3, ra=(-145, -30, 10), head=(-4, 0, -6), lid=.3)
    c.key(0.55, ra=(-146, -30, 10))
    c.key(0.75, ra=(-120, 34, 10), head=(-2, 0, -4))
    c.key(1.3, ra=(-40, 10, 14), head=(0, 0, 0), lid=.1)


@clip("greet_hand_on_heart", "Hand on heart", trigger="greet", weight=2, require=["adult"],
      boost={"personality:warmhearted": 2, "personality:gentle": 2, "personality:thoughtful": 2}, length=2.6)
def _(c):
    c.key(0.45, **HAND_TO_CHEST, head=(6, 0, 8), lid=.6)
    c.key(1.1, ra=(-60, -50, 0), head=(12, 0, 10), lid=.75)
    c.key(1.6, ra=(-52, 16, 14), head=(2, 0, 4), lid=.2)
    c.key(2.1, ra=(-26, 8, 8), head=(0, 0, 0))


@clip("greet_arms_open", "Opens arms in welcome", trigger="greet", weight=2, require=["adult"], mirror="never",
      boost={"personality:warmhearted": 4}, length=2.5)
def _(c):
    c.key(0.25, ra=(-12, 0, 10), la=(-12, 0, 10), waist=(4, 0, 0))
    c.key(0.65, ra=(-40, 20, 62), la=(-40, 20, 62), waist=(-6, 0, 0), head=(-8, 0, 0), root_pos=(0, -.4, 0), lid=.5)
    c.key(1.5, ra=(-42, 22, 66), la=(-42, 22, 66), waist=(-5, 0, 0), head=(-6, 0, 4))
    c.key(2.0, ra=(-16, 6, 14), la=(-16, 6, 14), waist=(0, 0, 0), head=(0, 0, 0), root_pos=(0, 0, 0), lid=.1)


@clip("greet_shy_wave", "Small shy wave", trigger="greet", weight=2, require=["adult|child"],
      boost={"personality:reserved": 3, "personality:gentle": 2}, length=2.4)
def _(c):
    c.key(0.4, ra=(-30, 10, 26), la=(-20, -24, 0), head=(12, 0, -10), look=(-.3, .5), lid=.35)
    c.cycle(0.5, 1.7, .32, dict(ra=(-32, 10, 36)), dict(ra=(-28, 10, 16)))
    c.key(1.9, ra=(-6, 0, 6), la=(-14, -18, 0), head=(8, 0, -6), look=(0, .3))


@clip("greet_beckon", "Beckons you over", trigger="greet", weight=1.5, require=["adult"],
      boost={"personality:playful": 2, "personality:warmhearted": 1.5}, length=2.4)
def _(c):
    c.key(0.3, ra=(-58, 6, 4), head=(4, 0, 6), waist=(-2, 0, 0))
    c.cycle(0.4, 1.7, .44, dict(ra=(-100, 0, 6), head=(-2, 0, 6), waist=(-4, 0, 0)),
            dict(ra=(-58, 6, 4), head=(6, 0, 6), waist=(0, 0, 0)))
    c.key(1.95, ra=(-30, 0, 6), head=(0, 0, 0), waist=(0, 0, 0))


@clip("greet_raise_palm", "Raises a palm", trigger="greet", weight=2, require=["adult"],
      boost={"personality:steadfast": 2, "personality:reserved": 1.5}, length=2.0)
def _(c):
    c.key(0.35, ra=(-150, 0, -14), head=(-4, 0, 0))
    c.key(0.7, ra=(-146, 0, -14), head=(8, 0, 0), lid=.25)
    c.key(1.15, ra=(-150, 0, -14), head=(0, 0, 0))
    c.key(1.55, ra=(-40, 4, 10), lid=0)


@clip("greet_flourish_bow", "Bows with a flourish", trigger="greet", weight=1.5, require=["adult"],
      boost={"personality:meticulous": 5, "personality:imaginative": 2}, length=2.8)
def _(c):
    c.key(0.3, ra=(-40, 0, 70), head=(-4, 0, 0))
    c.key(0.55, ra=(-100, 30, 40), **{"la": HANDS_BEHIND["la"]})
    c.key(0.95, ra=(-56, -48, 0), rl=(-14, 0, 0), waist=(40, 0, 0), head=(16, 0, 0), lid=.5)
    c.key(1.65, ra=(-56, -48, 0), rl=(-14, 0, 0), waist=(42, 0, 0), head=(18, 0, 0))
    c.key(2.2, ra=(-20, 0, 10), rl=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0), la=(0, 0, 0), lid=0)


@clip("greet_double_take", "Double-takes and waves", trigger="greet", weight=1.5, require=["adult|child"], mirror="free", length=2.7)
def _(c):
    c.key(0.3, head=(2, -22, 0), look=(-.4, 0))
    c.key(0.55, head=(2, -20, 0))
    c.key(0.7, head=(0, 6, 0), look=(.2, 0))
    c.key(0.88, head=(2, -18, 0), look=(-.3, 0))
    c.key(1.05, head=(-10, 0, 0), look=(0, 0), root_pos=(0, -1.2, 0), waist=(-6, 0, 0), ra=(-30, 0, 40), la=(-20, 0, 20))
    c.key(1.2, root_pos=(0, 0, 0))
    c.key(1.4, ra=(-24, 0, 140), la=(-6, 0, 6), head=(-4, 0, -6), waist=(0, 0, 0), lid=.35)
    c.cycle(1.5, 2.1, .3, dict(ra=(-24, 0, 152)), dict(ra=(-24, 0, 124)))
    c.key(2.3, ra=(-20, 0, 60), head=(0, 0, 0), lid=.1)


@clip("greet_fist_to_chest", "Fist-to-chest salute", trigger="greet", weight=2, require=["adult"],
      boost={"personality:protective": 3, "guard": 3}, length=2.5)
def _(c):
    c.key(0.22, ra=(-30, 0, 46), rl=(-22, 0, 0), head=(-4, 0, 0), **{"la": HANDS_BEHIND["la"]})
    c.key(0.4, ra=(-72, -56, 0), rl=(0, 0, 0), root_pos=(0, .4, .4), waist=(-4, 0, 0), head=(-8, 0, 0), lid=.2)
    c.key(0.52, ra=(-62, -40, 6), root_pos=(0, 0, 0))
    c.key(0.66, ra=(-72, -56, 0), root_pos=(0, .2, .3))
    c.key(0.8, root_pos=(0, 0, 0))
    c.key(1.1, head=(12, 0, 0), lid=.5)
    c.key(1.35, ra=(-72, -56, 0), head=(-6, 0, 0), lid=.2)
    c.key(1.85, ra=(-20, 0, 10), la=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("greet_jump_wave", "Jumps and waves", trigger="greet", weight=3, require=["child"], length=2.6)
def _(c):
    c.key(0.25, ra=(-10, 0, 150), lid=.4)
    c.cycle(0.3, 1.9, .3, dict(ra=(-10, 0, 166)), dict(ra=(-10, 0, 134)))
    for t in (0.5, 1.3):
        c.key(t - .15, root_pos=(0, .8, 0), la=(-10, 0, 10), head=(4, 0, 0))
        c.key(t + .1, root_pos=(0, -4.5, 0), la=(-30, 0, 44), head=(-10, 0, 0), rl=(-10, 0, 4), ll=(6, 0, 4))
        c.key(t + .34, root_pos=(0, 0, 0), la=(-6, 0, 12), head=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(2.15, ra=(-10, 0, 60), lid=.1)


@clip("greet_peek_wave", "Peeks out and waves", trigger="greet", weight=2, require=["child"], length=2.9)
def _(c):
    c.key(0.35, ra=(-128, -42, 0), la=(-128, -42, 0), head=(10, 0, 0), lid=.6)
    c.key(0.9, ra=(-130, -42, 0), la=(-130, -42, 0), head=(12, 0, -8))
    c.key(1.25, ra=(-62, 4, 26), la=(-116, -40, 0), head=(8, 6, -10), look=(.3, .3), lid=.2)
    c.cycle(1.4, 2.2, .3, dict(ra=(-62, 4, 36)), dict(ra=(-62, 4, 18)))
    c.key(2.35, la=(-60, -34, 0), head=(6, 4, -6), look=(.2, .3))


@clip("greet_excited_bounce", "Bounces with excitement", trigger="greet", weight=2.5, require=["child"], mirror="never",
      length=2.2)
def _(c):
    c.key(0.25, ra=(-46, -30, 0), la=(-46, -30, 0), ra_pos=(0, -1, 0), la_pos=(0, -1, 0), head=(-6, 0, 0), lid=.5)
    c.cycle(0.3, 1.7, .26, dict(root_pos=(0, -1.8, 0), head=(-8, 0, 3), ra=(-52, -30, 0), la=(-40, -26, 0)),
            dict(root_pos=(0, .2, 0), head=(-4, 0, -3), ra=(-40, -26, 0), la=(-52, -30, 0)))
    c.key(1.8, root_pos=(0, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid=.3)

# -- talking with you ----------------------------------------------------------------------------


@clip("talk_jab_finger", "Jabs a finger for emphasis", trigger="talk", weight=1.5, length=2.4)
def _(c):
    c.key(0.3, ra=(-112, 6, 6), head=(2, 0, 0), lid=.2)
    for t in (0.55, 1.0, 1.3):
        c.key(t, ra=(-96, 4, 4), head=(8, 0, 0)).key(t + .15, ra=(-114, 6, 6), head=(0, 0, 0))
    c.key(1.85, ra=(-80, 6, 6), head=(2, 0, 0), lid=0)


@clip("talk_hand_on_heart", "Speaks from the heart", trigger="talk", weight=1.5, length=2.8)
def _(c):
    c.key(0.45, **HAND_TO_CHEST, head=(4, 0, 8), lid=.4)
    c.key(0.9, la=(-44, 14, 12), head=(8, 0, 10))
    c.key(1.5, head=(14, 0, 8), lid=.55)
    c.key(1.9, ra=(-58, -50, 0), head=(4, 0, 6), lid=.3)
    c.key(2.25, la=(-30, 8, 6))


@clip("talk_thumb_back", "Thumbs back over the shoulder", trigger="talk", weight=1.5, length=2.3)
def _(c):
    c.key(0.3, ra=(-70, -6, 6), head=(4, 0, 0))
    c.key(0.55, ra=(-158, 8, 20), head=(0, 10, -4), look=(.6, 0))
    for t in (0.72, 1.12):
        c.key(t, ra=(-196, 8, 16), head=(-2, 12, -5)).key(t + .2, ra=(-160, 8, 20), head=(0, 10, -4))
    c.key(1.5, ra=(-150, 8, 20), head=(4, 4, -2), look=(.1, 0), lid=.2)
    c.key(1.85, ra=(-40, 4, 8), head=(0, 0, 0), look=(0, 0), lid=0)


@clip("talk_this_big", "Shows how big it was", trigger="talk", weight=1.5, mirror="never", length=2.8)
def _(c):
    c.key(0.35, ra=(-60, -26, 0), la=(-60, -26, 0), head=(8, 0, 0), look=(0, .5))
    c.key(0.8, ra=(-64, 20, 12), la=(-64, 20, 12), head=(4, 0, 0), look=(0, .3), root_pos=(0, -.3, 0))
    c.key(1.1, ra=(-66, 24, 14), la=(-66, 24, 14), head=(-2, 0, 0), look=(0, 0))
    c.key(1.4, ra=(-64, 10, 8), la=(-64, 10, 8), head=(4, 0, 6), look=(0, .3), lid=.3)
    c.key(1.75, ra=(-68, 30, 16), la=(-68, 30, 16), head=(-6, 0, -2), look=(0, 0), lid=0, root_pos=(0, -.5, 0))
    c.key(2.05, ra=(-68, 30, 16), la=(-68, 30, 16), root_pos=(0, 0, 0))
    c.key(2.4, ra=(-20, 6, 6), la=(-20, 6, 6), head=(0, 0, 0))


@clip("talk_whisper_aside", "Whispers behind a hand", trigger="talk", weight=1.5, length=2.9,
      boost={"personality:playful": 1.5, "personality:curious": 1.5})
def _(c):
    c.key(0.3, ra=(-74, -8, 8), look=(.5, 0))
    c.key(0.5, look=(-.5, 0))
    c.key(0.75, ra=(-108, -12, 18), waist=(12, 0, 0), root_pos=(0, 0, -.6), head=(4, 0, -8), look=(0, .1), lid=.35)
    c.cycle(0.9, 1.6, .24, dict(head=(6, 0, -8)), dict(head=(2, 0, -8)))
    c.key(1.85, ra=(-114, -40, 0), waist=(4, 0, 0), root_pos=(0, 0, 0), head=(4, 0, 4), lid=.55)
    c.key(2.15, ra=(-113, -40, 0), head=(10, 0, 4), lid=.4)
    c.key(2.5, ra=(-30, 0, 6), waist=(0, 0, 0), head=(0, 0, 0), look=(0, 0), lid=0)


@clip("talk_tap_temple", "Taps the temple knowingly", trigger="talk", weight=1.5, length=2.4,
      boost={"personality:thoughtful": 1.5, "personality:pragmatic": 1.5, "personality:imaginative": 1.5})
def _(c):
    c.key(0.35, ra=(-150, -6, 22), head=(0, 0, -8), lid=.3)
    for t in (0.6, 0.95):
        c.key(t, ra=(-143, -8, 24), head=(2, 0, -9)).key(t + .17, ra=(-152, -5, 21), head=(0, 0, -8))
    c.key(1.4, ra=(-150, -6, 22), head=(-4, 0, -10), lid=.45)
    c.key(1.65, ra=(-100, 8, 8), head=(2, 0, -4), lid=.2)
    c.key(2.0, ra=(-40, 6, 8), head=(0, 0, 0), lid=0)


@clip("talk_wave_off", "Waves it off", trigger="talk", weight=1.5, mirror="free", length=2.2,
      boost={"personality:pragmatic": 1.5, "personality:playful": 1.5})
def _(c):
    c.key(0.25, ra=(-78, -22, 4), head=(-4, -4, 4), lid=.3)
    for t in (0.4, 0.8):
        c.key(t, ra=(-62, 36, 22), head=(-6, -10, 7), lid=.55, look=(0, -.6))
        c.key(t + .25, ra=(-80, -18, 4), head=(-4, -8, 6), lid=.5, look=(.1, -.5))
    c.key(1.2, ra=(-60, 38, 24), head=(-5, -10, 7), lid=.55, look=(0, -.6))
    c.key(1.6, ra=(-20, 10, 10), head=(4, 0, 2), lid=.2, look=(0, 0))


@clip("talk_palms_up_why", "Palms up: why?", trigger="talk", weight=1.5, mirror="never", length=2.3)
def _(c):
    c.key(0.25, ra=(-26, 0, 6), la=(-26, 0, 6), head=(4, 0, 0))
    c.key(0.5, ra=(-48, 22, 20), la=(-48, 22, 20), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), waist=(6, 0, 0),
          head=(-6, 0, 6), lid=0)
    c.key(0.72, ra=(-38, 18, 16), la=(-38, 18, 16), head=(-3, 0, 6))
    c.key(0.95, ra=(-52, 24, 22), la=(-52, 24, 22), head=(-8, 0, 8))
    c.key(1.45, ra=(-50, 23, 21), la=(-50, 23, 21), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), waist=(5, 0, 0),
          head=(-7, 0, 8))
    c.key(1.85, ra=(-14, 4, 6), la=(-14, 4, 6), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0))


@clip("talk_rub_chin", "Rubs the chin thoughtfully", trigger="talk", weight=1.5, length=2.8,
      boost={"personality:meticulous": 1.5, "personality:pragmatic": 1.5})
def _(c):
    c.key(0.35, ra=(-104, -42, 0), la=(14, 0, 26), head=(-4, 0, 0), lid=.35)
    c.wobble(0.45, 1.75, 3, "ra", 6, base=(-104, -42, 0), axis=1)
    c.key(0.6, head=(-6, 4, 6), look=(.4, -.3))
    c.key(1.25, head=(-2, -4, -4), look=(-.3, .1), lid=.45)
    c.key(1.75, head=(-2, 0, 0), look=(0, 0), lid=.4)
    c.key(1.95, la=(14, 0, 26), head=(8, 0, 0), lid=.3)
    c.key(2.2, ra=(-40, 0, 6), la=(4, 0, 10), head=(0, 0, 0), lid=.1)


@clip("talk_proud_thumbs", "Proudly thumbs own chest", trigger="talk", weight=1.5, mirror="never", length=2.4,
      boost={"personality:adventurous": 1.5, "personality:steadfast": 1.5})
def _(c):
    c.key(0.3, ra=(-40, -10, 6), la=(-40, -10, 6), waist=(2, 0, 0))
    c.key(0.5, ra=(-62, -30, 0), la=(-62, -30, 0), waist=(-6, 0, 0), head=(-8, 0, 0), root_pos=(0, -.4, 0), lid=.35)
    for t in (0.62, 0.9):
        c.key(t, ra=(-54, -34, 0), la=(-54, -34, 0)).key(t + .14, ra=(-62, -30, 0), la=(-62, -30, 0))
    c.key(1.5, ra=(-61, -30, 0), la=(-61, -30, 0), head=(-10, 0, 5), waist=(-7, 0, 0), lid=.45)
    c.key(1.95, ra=(-18, 4, 6), la=(-18, 4, 6), head=(0, 0, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), lid=0)


@clip("talk_grand_sweep", "Sweeps an arm across the horizon", trigger="talk", weight=1, length=3.0,
      boost={"personality:imaginative": 2.5, "personality:adventurous": 2})
def _(c):
    c.key(0.35, ra=(-88, -40, 0), la=(-30, -20, 0), head=(2, -6, 0), look=(-.4, 0), waist=(2, 0, 0))
    c.key(0.6, ra=(-94, -44, 0), head=(0, -8, 0))
    c.key(1.1, ra=(-106, -6, 6), head=(-4, 0, 0), look=(0, -.2), lid=.2)
    c.key(1.6, ra=(-102, 30, 14), la=(-34, -24, 0), head=(-8, 8, -3), look=(.6, -.2), waist=(-4, 0, 0), lid=.35,
          root=(0, 0, -2))
    c.key(2.1, ra=(-100, 32, 16), head=(-8, 9, -3), lid=.45)
    c.key(2.5, ra=(-30, 6, 8), la=(0, 0, 0), head=(0, 0, 0), look=(0, 0), waist=(0, 0, 0), lid=0, root=(0, 0, 0))


@clip("talk_steepled_fingers", "Steeples the fingers", trigger="talk", weight=1, mirror="never", length=3.0,
      boost={"personality:thoughtful": 2, "personality:meticulous": 1.5, "personality:reserved": 1.5})
def _(c):
    c.key(0.45, ra=(-84, -36, 0), la=(-84, -36, 0), head=(8, 0, 0), look=(0, -.4), lid=.3)
    c.cycle(0.7, 1.9, .34, dict(ra=(-84, -36, 0), la=(-84, -36, 0)), dict(ra=(-84, -29, 0), la=(-84, -29, 0)))
    c.key(2.05, head=(12, 0, 4), lid=.45)
    c.key(2.3, ra=(-70, -30, 0), la=(-70, -30, 0), head=(4, 0, 2), look=(0, 0), lid=.2)


@clip("talk_excited_flap", "Flaps both hands excitedly", trigger="talk", weight=1.2, mirror="never", length=2.2,
      boost={"personality:playful": 2, "personality:curious": 1.5, "child": 2})
def _(c):
    c.key(0.2, ra=(-56, -10, 10), la=(-56, -10, 10), ra_pos=(0, -1, 0), la_pos=(0, -1, 0), head=(-6, 0, 0), lid=.4)
    c.cycle(0.3, 1.5, .2, dict(ra=(-60, -6, 28), la=(-54, -6, 10), root_pos=(0, -.8, 0), head=(-7, 0, 3)),
            dict(ra=(-54, -6, 10), la=(-60, -6, 28), root_pos=(0, .2, 0), head=(-6, 0, -3)))
    c.key(1.75, ra=(-30, 0, 8), la=(-30, 0, 8), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), root_pos=(0, 0, 0), head=(0, 0, 0),
          lid=.2)


@clip("talk_point_you", "Points right at you", trigger="talk", weight=1.5, length=2.2,
      boost={"personality:playful": 1.5, "personality:protective": 1.5})
def _(c):
    c.key(0.25, ra=(-44, -24, 0), waist=(-4, 0, 0), head=(-4, 0, 0), root_pos=(0, 0, .3))
    c.key(0.45, ra=(-92, -6, 0), waist=(8, 0, 0), head=(4, 0, 0), root_pos=(0, 0, -.5))
    c.wobble(0.5, 1.2, 5, "ra", 3, base=(-92, -6, 0), axis=0)
    c.key(1.5, ra=(-88, -6, 0), waist=(6, 0, 0), head=(2, 0, -6), lid=.3, root_pos=(0, 0, -.3))
    c.key(1.8, ra=(-30, 0, 6), waist=(0, 0, 0), head=(0, 0, 0), lid=0, root_pos=(0, 0, 0))
