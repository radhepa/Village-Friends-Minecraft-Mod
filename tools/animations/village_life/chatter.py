"""Chatter: more ways for neighbors to talk and listen to each other."""
from kit import clip, ARMS_CROSSED, HANDS_BEHIND, HANDS_ON_HIPS, HAND_TO_CHEST, HAND_TO_MOUTH

# -- speaking ------------------------------------------------------------------------------------


@clip("chat_gossip", "Gossips behind a hand", trigger="chat_speak", weight=2, boost={"personality:playful": 1.5}, length=3.2)
def _(c):
    c.key(0.35, head=(0, -26, 0), look=(-.7, 0))
    c.key(0.7, head=(0, 20, 0), look=(.7, 0))
    c.key(0.75, ra=(-60, -10, 8))
    c.key(1.0, ra=(-108, -14, 14), waist=(12, 0, 0), root_pos=(0, 0, -.6), head=(4, 0, -10), look=(0, 0), lid=.35)
    c.wobble(1.05, 2.25, 5, "head", 3, base=(4, 0, -10), axis=0)
    c.key(2.3, ra=(-106, -14, 14), waist=(11, 0, 0), lid=.35)
    c.key(2.7, ra=(-30, 0, 6), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("chat_act_it_out", "Acts it out", trigger="chat_speak", weight=1.5, mirror="free",
      boost={"personality:adventurous": 2, "personality:playful": 1.5}, length=3.0)
def _(c):
    c.key(0.25, root_pos=(0, .4, 0), waist=(4, 0, 0))
    c.key(0.6, ra=(-150, 10, 30), la=(-140, -40, 10), waist=(-6, 22, 0), head=(-8, 12, 0), root_pos=(0, -.3, 0), lid=.2)
    c.key(0.85, ra=(-40, -50, 0), la=(-50, 10, 0), waist=(14, -24, 0), head=(6, -12, 0), root_pos=(0, .5, 0), lid=.5)
    c.key(1.3, ra=(-36, -52, 0), la=(-46, 12, 0), waist=(15, -26, 0), root_pos=(0, .4, 0))
    c.key(1.8, ra=(-44, 18, 18), la=(-44, 18, 18), waist=(-2, 0, 0), head=(-6, 0, 0), root_pos=(0, 0, 0), lid=.3)
    c.key(2.4, ra=(-20, 6, 8), la=(-20, 6, 8), head=(0, 0, 0), lid=0)


@clip("chat_complain", "Complains with hands on hips", trigger="chat_speak", weight=1.5,
      boost={"personality:pragmatic": 2, "personality:steadfast": 1.5}, length=3.4)
def _(c):
    c.hold(0.45, 1.6, **HANDS_ON_HIPS)
    c.key(0.45, waist=(-4, 0, 0), head=(-6, 0, 0), lid=.35)
    c.cycle(0.7, 1.7, .5, dict(head=(4, 14, -4)), dict(head=(4, -14, 4)))
    c.key(1.9, ra=(-56, 26, 22), head=(6, 0, 0), waist=(6, 0, 0))
    c.key(2.15, ra=(-48, 30, 26), head=(4, 0, 0))
    c.key(2.55, **HANDS_ON_HIPS, head=(-4, 0, 0), waist=(-3, 0, 0), lid=.35)


@clip("chat_laugh_at_own_joke", "Laughs at own joke", trigger="chat_speak", weight=1.5,
      boost={"personality:playful": 2, "job:nitwit": 2}, length=3.1)
def _(c):
    c.key(0.4, ra=(-64, 22, 18), head=(4, 0, -4), waist=(4, 0, 0))
    c.key(0.75, ra=(-70, 26, 20), head=(-14, 0, 0), waist=(-8, 0, 0), lid=.75)
    c.key(1.05, ra=(-30, -34, 0), la=(-30, -34, 0), waist=(16, 0, 0), head=(12, 0, 0), lid=.9)
    c.wobble(1.05, 2.0, 7, "root_pos", .4, axis=1, decay=.5)
    c.key(1.7, waist=(14, 0, 0), head=(10, 0, 0))
    c.key(2.1, ra=(-84, 4, 0), la=(-20, -20, 0), waist=(2, 0, 0), head=(-4, 0, 0), lid=.5)
    c.key(2.5, ra=(-82, 6, 0), lid=.4)


@clip("chat_draw_in_air", "Draws a shape in the air", trigger="chat_speak", weight=1.5,
      boost={"personality:imaginative": 2, "job:cartographer": 2, "job:mason": 1.5, "job:carpenter": 1.5}, length=3.3)
def _(c):
    c.key(0.4, ra=(-118, 10, 0), head=(-4, 4, 0), look=(.2, -.6))
    for i, (p, y) in enumerate(((-112, 26), (-100, 32), (-86, 26), (-80, 10), (-86, -6), (-100, -12), (-114, -6), (-118, 10))):
        c.key(0.6 + i * .2, ra=(p, y, 0), look=(y / 40, (p + 100) / 30))
    c.key(2.3, ra=(-62, 24, 18), head=(4, 0, -4), look=(0, 0))
    c.key(2.7, ra=(-58, 26, 20), head=(0, 0, 0))


@clip("chat_pat_shoulder", "Pats their shoulder", trigger="chat_speak", weight=1.5,
      boost={"personality:warmhearted": 2, "personality:gentle": 1.5}, length=2.8)
def _(c):
    c.key(0.5, ra=(-84, -4, 0), waist=(8, 0, 0), root_pos=(0, 0, -.6), head=(4, 0, -6), lid=.3)
    c.cycle(0.6, 1.6, .4, dict(ra=(-94, -4, 0)), dict(ra=(-82, -4, 0)), end_on="b")
    c.key(1.9, ra=(-84, -4, 0), head=(10, 0, -6))
    c.key(2.25, ra=(-36, 0, 6), waist=(0, 0, 0), root_pos=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("chat_fish_this_big", "The fish was THIS big", trigger="chat_speak", weight=1.5, mirror="never",
      boost={"job:fisherman": 4, "personality:reserved": 1.5, "personality:adventurous": 1.5}, length=3.3)
def _(c):
    c.key(0.4, ra=(-64, -24, 0), la=(-64, -24, 0), head=(10, 0, 0), look=(0, .4))
    c.hold(0.75, 1.0, ra=(-66, -4, 4), la=(-66, -4, 4), head=(8, 0, 0))
    c.hold(1.3, 1.55, ra=(-70, 22, 12), la=(-70, 22, 12), head=(4, 0, 0), root_pos=(0, -.4, 0), look=(0, .2))
    c.key(1.95, ra=(-74, 54, 22), la=(-74, 54, 22), head=(-6, 0, 0), waist=(-4, 0, 0), root_pos=(0, -1, 0), look=(0, 0), lid=.2)
    c.key(2.6, ra=(-72, 56, 24), la=(-72, 56, 24), root_pos=(0, 0, 0), waist=(-3, 0, 0), lid=.1)


@clip("chat_rant", "Rants and waves the arms", trigger="chat_speak", weight=1, mirror="never",
      boost={"personality:protective": 1.5, "personality:pragmatic": 1.5}, length=3.4)
def _(c):
    c.key(0.3, ra=(-60, 10, 20), la=(-60, 10, 20), waist=(6, 0, 0), head=(4, 0, 0), lid=.4)
    c.cycle(0.45, 1.95, .6, dict(ra=(-110, 10, 70), la=(-44, 10, 24), head=(6, -12, 5), root=(0, 0, -2)),
            dict(ra=(-44, 10, 24), la=(-110, 10, 70), head=(6, 12, -5), root=(0, 0, 2)))
    c.key(2.3, ra=(-24, 0, 128), la=(-24, 0, 128), waist=(-4, 0, 0), head=(-12, 0, 0), root=(0, 0, 0), lid=.55)
    c.key(2.75, ra=(-8, 0, 22), la=(-8, 0, 22), waist=(8, 0, 0), head=(10, 0, 0), lid=.5)


@clip("chat_confide", "Confides with a sigh", trigger="chat_speak", weight=1.5,
      boost={"personality:gentle": 2, "personality:thoughtful": 1.5, "evening": 1.5}, length=3.6)
def _(c):
    c.key(0.5, **HAND_TO_CHEST, head=(-6, 0, 0), root_pos=(0, -.4, 0), lid=.2)
    c.key(1.2, head=(18, 0, -6), waist=(6, 0, 0), root_pos=(0, .4, 0), ra_pos=(0, .5, 0), la_pos=(0, .5, 0), lid=.7, look=(0, .5))
    c.key(1.9, head=(16, -8, -8))
    c.key(2.4, head=(14, 8, -6))
    c.key(2.9, ra=(-56, -48, 0), head=(8, 0, -4), lid=.4, look=(0, .2))


@clip("chat_bounce_excited", "Bounces with excitement", trigger="chat_speak", weight=1.5, mirror="never",
      boost={"child": 2, "personality:playful": 2, "personality:curious": 1.5}, length=2.8)
def _(c):
    c.key(0.3, ra=(-64, -30, 0), la=(-64, -30, 0), head=(-6, 0, 0), lid=.45)
    c.cycle(0.35, 2.05, .34, dict(root_pos=(0, -1.6, 0), ra=(-74, -26, 0), la=(-74, -26, 0), head=(-8, 0, 0)),
            dict(root_pos=(0, 0, 0), ra=(-60, -32, 0), la=(-60, -32, 0), head=(-3, 0, 0)), end_on="b")
    c.key(2.35, ra=(-40, -20, 0), la=(-40, -20, 0), head=(-2, 0, 0), lid=.2)


# -- listening -----------------------------------------------------------------------------------


@clip("listen_chin_in_hand", "Listens with chin in hand", trigger="chat_listen", weight=2,
      boost={"personality:thoughtful": 2, "personality:curious": 1.5, "job:scholar": 1.5, "job:librarian": 1.5}, length=3.8)
def _(c):
    c.hold(0.55, 3.1, ra=(-100, -36, 0), la=(-44, -52, 0))
    c.key(0.55, head=(8, 0, -10), waist=(4, 0, 0), look=(0, -.3))
    c.key(1.5, head=(12, 0, -11), lid=.25)
    c.key(1.85, head=(7, 0, -10), lid=0)
    c.key(2.45, head=(9, 0, -12), lid=0)
    c.key(2.6, lid=.6)
    c.key(2.8, head=(8, 0, -11), waist=(4, 0, 0), lid=0)


@clip("listen_skeptical", "Squints skeptically", trigger="chat_listen", weight=1.5, require=["adult"],
      boost={"personality:pragmatic": 2, "personality:meticulous": 2, "personality:reserved": 1.5}, length=3.4)
def _(c):
    c.key(0.5, **ARMS_CROSSED, head=(-10, -10, -6), waist=(-4, 0, 0), lid=.5, look=(.4, 0))
    c.key(1.4, head=(-12, -14, -8), root=(0, 0, -2), lid=.55, look=(.5, 0))
    c.key(2.0, head=(-8, -6, 6), lid=.6, look=(.3, 0))
    c.key(2.8, **ARMS_CROSSED, head=(-8, -8, 4), waist=(-3, 0, 0), root=(0, 0, 0), lid=.5)


@clip("listen_lean_in", "Leans in curiously", trigger="chat_listen", weight=2,
      boost={"personality:curious": 2.5, "child": 1.5}, length=3.3)
def _(c):
    c.key(0.5, **HANDS_BEHIND, waist=(14, 0, 0), root_pos=(0, 0, -.7), head=(-6, 0, 10), look=(0, -.2))
    c.key(1.3, head=(-4, 4, 12))
    c.key(1.55, head=(5, 4, 12))
    c.key(1.8, head=(-4, 4, 12))
    c.key(2.7, **HANDS_BEHIND, waist=(12, 0, 0), root_pos=(0, 0, -.6), head=(-4, 2, 8), look=(0, -.2))


@clip("listen_knee_slap", "Slaps a knee laughing", trigger="chat_listen", weight=1.5, mirror="free",
      boost={"personality:playful": 2, "job:nitwit": 2}, length=2.8)
def _(c):
    c.key(0.3, waist=(-8, 0, 0), head=(-14, 0, 0), ra=(-70, 0, 12), la=(-24, -24, 0), lid=.75)
    c.key(0.55, waist=(18, 0, 0), head=(8, 0, 0), ra=(-14, 0, 6), rl=(-16, 0, 0), lid=.9)
    c.key(0.8, waist=(12, 0, 0), ra=(-62, 0, 12), rl=(-4, 0, 0))
    c.key(1.05, waist=(18, 0, 0), ra=(-14, 0, 6), rl=(-16, 0, 0))
    c.wobble(1.1, 2.0, 7, "root_pos", .35, axis=1, decay=.5)
    c.key(1.45, waist=(6, 0, 0), head=(-6, 0, 0), ra=(-30, 0, 10), rl=(0, 0, 0))
    c.key(2.2, waist=(0, 0, 0), head=(-2, 0, 0), ra=(-10, 0, 6), la=(-10, -10, 0), lid=.4)


@clip("listen_go_on", "Rolls a hand: go on", trigger="chat_listen", weight=1.5,
      boost={"personality:curious": 2, "personality:adventurous": 1.5}, length=2.7)
def _(c):
    c.key(0.35, ra=(-50, 12, 12), head=(-4, 0, 6), waist=(4, 0, 0))
    for i in range(3):
        t = 0.5 + i * .5
        c.key(t, ra=(-76, 14, 12), head=(6, 0, 6))
        c.key(t + .125, ra=(-62, 32, 16))
        c.key(t + .25, ra=(-46, 14, 12), head=(-2, 0, 6))
        c.key(t + .375, ra=(-60, -4, 8))
    c.key(2.15, ra=(-40, 10, 10), head=(0, 0, 4), waist=(0, 0, 0))


@clip("listen_stifle_yawn", "Stifles a yawn", trigger="chat_listen", weight=1,
      boost={"evening": 2, "night": 3, "morning": 1.5}, length=2.9)
def _(c):
    c.key(0.35, head=(-4, -10, 0), lid=.4)
    c.key(0.6, **HAND_TO_MOUTH, head=(-10, -16, 4), waist=(-3, 0, 0), lid=.85)
    c.key(1.3, ra=(-115, -42, 0), head=(-12, -18, 5), lid=1)
    c.key(1.6, ra=(-40, -10, 0), head=(2, 0, 0), waist=(0, 0, 0), lid=0)
    c.wobble(1.65, 2.05, 6, "head", 5, base=(2, 0, 0), axis=1)
    c.key(1.8, lid=.75)
    c.key(1.95, lid=0)


@clip("listen_wince", "Winces in sympathy", trigger="chat_listen", weight=1.5, mirror="free",
      boost={"personality:gentle": 2, "personality:warmhearted": 1.5}, length=2.6)
def _(c):
    c.key(0.25, head=(6, -18, -10), waist=(-6, 0, 0), ra=(-36, -30, 0), la=(-36, -30, 0),
          ra_pos=(0, -.8, 0), la_pos=(0, -.8, 0), root_pos=(0, 0, .5), lid=1)
    c.key(0.9, head=(8, -20, -12), lid=1)
    c.key(1.2, head=(4, -8, -6), ra_pos=(0, -.3, 0), la_pos=(0, -.3, 0), root_pos=(0, 0, .2), lid=.5)
    c.key(1.5, head=(6, 8, 8), lid=.45)
    c.key(1.85, head=(6, -6, 8), ra=(-30, -26, 0), la=(-30, -26, 0), waist=(-2, 0, 0))
    c.key(2.1, head=(5, 2, 6), lid=.3)


@clip("listen_clasp_delighted", "Clasps hands in delight", trigger="chat_listen", weight=1.5, mirror="never",
      boost={"personality:warmhearted": 2, "personality:imaginative": 1.5, "child": 1.5}, length=2.9)
def _(c):
    c.key(0.25, ra=(-66, -6, 10), la=(-66, -6, 10), head=(-6, 0, 0), lid=.2)
    c.key(0.42, ra=(-84, -40, 0), la=(-84, -40, 0), root_pos=(0, -.9, 0), head=(-8, 0, 0), lid=.65)
    c.key(0.65, root_pos=(0, 0, 0), head=(-6, 0, 10))
    c.key(1.15, head=(-6, 0, -10), root=(0, 0, -2))
    c.key(1.65, head=(-6, 0, 10), root=(0, 0, 2))
    c.key(2.3, ra=(-82, -40, 0), la=(-82, -40, 0), head=(-4, 0, 4), root=(0, 0, 0), lid=.5)


@clip("listen_tsk_tsk", "Tsk-tsks", trigger="chat_listen", weight=1.5, mirror="free",
      boost={"personality:steadfast": 2, "personality:meticulous": 1.5, "personality:protective": 1.5}, length=3.2)
def _(c):
    c.key(0.45, ra=(-30, -34, 0), la=(-28, -32, 0), head=(10, 0, 0), lid=.45, look=(0, .3))
    c.cycle(0.6, 2.2, .8, dict(head=(10, 16, 0)), dict(head=(10, -16, 0)))
    c.key(2.5, ra=(-28, -32, 0), la=(-26, -30, 0), head=(6, 0, 0), lid=.35, look=(0, .1))


@clip("listen_puzzled", "Scratches head in puzzlement", trigger="chat_listen", weight=1.5,
      boost={"job:nitwit": 2, "personality:curious": 1.5, "child": 1.5}, length=3.1)
def _(c):
    c.key(0.4, head=(4, 0, 14), lid=.3, look=(.3, -.3))
    c.key(0.75, ra=(-176, 8, 24), la=(14, 0, 26))
    c.wobble(0.8, 1.9, 5, "ra", 8, base=(-176, 8, 24), axis=0)
    c.key(1.9, head=(6, 0, 16), lid=.35)
    c.key(2.2, head=(2, 0, -12), look=(-.3, -.4), lid=.2)
    c.key(2.45, ra=(-50, 0, 10), la=(4, 0, 10))
