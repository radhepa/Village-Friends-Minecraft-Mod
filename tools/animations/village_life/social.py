"""Social: greeting the player, talking with them, and chatting with neighbors."""
from kit import clip, ARMS_CROSSED, HANDS_BEHIND, HAND_TO_CHIN, HAND_TO_CHEST, HAND_TO_MOUTH

# -- greetings (a resident notices you walking up, or a conversation opens) --------------------


@clip("wave_hello", "Waves hello", trigger="greet", weight=4, require=["adult"], boost={"personality:playful": 2, "personality:warmhearted": 2},
      length=2.6)
def _(c):
    c.key(0.38, ra=(-24, 0, 138), head=(-4, 0, -8), lid=.3)
    c.cycle(0.45, 2.0, .36, dict(ra=(-24, 0, 152)), dict(ra=(-24, 0, 122)))
    c.key(2.05, ra=(-20, 0, 60), head=(0, 0, -3), lid=.1)


@clip("bow_politely", "Bows politely", trigger="greet", weight=2, require=["adult"],
      boost={"personality:reserved": 5, "personality:meticulous": 4, "personality:thoughtful": 2}, length=2.5)
def _(c):
    c.key(0.4, **HAND_TO_CHEST)
    c.key(0.85, waist=(30, 0, 0), head=(14, 0, 0), lid=.4)
    c.key(1.35, waist=(31, 0, 0), head=(15, 0, 0))
    c.key(1.85, waist=(0, 0, 0), head=(0, 0, 0), ra=(-40, -40, 0), lid=0)


@clip("tip_a_nod", "Nods hello", trigger="greet", weight=2, require=["adult"],
      boost={"personality:reserved": 3, "personality:pragmatic": 3, "personality:steadfast": 2}, length=1.7)
def _(c):
    c.key(0.35, head=(16, 0, 0), ra=(-40, 0, 36), lid=.3)
    c.key(0.75, head=(-2, 0, 0), ra=(-38, 0, 40))
    c.key(1.2, ra=(-10, 0, 10), lid=0)


@clip("salute", "Salutes", trigger="greet", weight=8, require=["adult", "job:knight|job:archer"], length=2.3)
def _(c):
    c.key(0.25, root_pos=(0, -.5, 0), waist=(-3, 0, 0))
    c.key(0.42, la=(-64, -52, 0), root_pos=(0, 0, 0))
    c.key(0.75, head=(14, 0, 0))
    c.key(1.4, la=(-62, -52, 0), head=(0, 0, 0))


@clip("wave_excitedly", "Waves excitedly", trigger="greet", weight=5, require=["child"], mirror="never", length=2.5)
def _(c):
    c.key(0.3, ra=(-10, 0, 148), la=(-10, 0, 148), root_pos=(0, -1.5, 0), lid=.4)
    c.cycle(0.35, 2.0, .34,
            dict(ra=(-10, 0, 162), la=(-10, 0, 130), root_pos=(0, -2.2, 0)),
            dict(ra=(-10, 0, 130), la=(-10, 0, 162), root_pos=(0, 0, 0)))


# -- talking with the player (the conversation window is open) -----------------------------------


@clip("talk_open_palm", "Explains", trigger="talk", weight=3, length=2.3, also={"chat_explain": "chat_speak"})
def _(c):
    c.key(0.4, ra=(-52, 18, 14), head=(4, 0, -6))
    c.key(0.9, ra=(-44, 10, 10), head=(-2, 0, 4))
    c.key(1.45, ra=(-56, 22, 18), head=(2, 0, -2))


@clip("talk_both_hands", "Gestures with both hands", trigger="talk", weight=2, mirror="never", length=2.5,
      also={"chat_gesture": "chat_speak"})
def _(c):
    c.key(0.4, ra=(-46, 16, 16), la=(-46, 16, 16))
    c.key(0.85, ra=(-56, 24, 24), la=(-50, 20, 20), head=(6, 0, 0))
    c.key(1.3, ra=(-40, 10, 10), la=(-44, 14, 14), head=(-2, 0, 0))
    c.key(1.75, ra=(-52, 22, 20), la=(-52, 22, 20), head=(2, 0, 3))


@clip("talk_point_to_self", "Points to self", trigger="talk", weight=1.5, length=2.1)
def _(c):
    c.key(0.4, **HAND_TO_CHEST, head=(8, 0, 0))
    c.key(0.75, ra=(-62, -48, 0), head=(2, 0, 0))
    c.key(1.1, ra=(-58, -50, 0), head=(9, 0, 0))


@clip("talk_nod", "Nods along", trigger="talk", weight=3, mirror="free", length=1.9, also={"listen_nod": "chat_listen"})
def _(c):
    for t, pitch in ((0.3, 11), (0.6, 0), (0.9, 12), (1.2, 0)):
        c.key(t, head=(pitch, 0, 3))
    c.hold(0.3, 1.3, lid=.2)


@clip("talk_think", "Thinks it over", trigger="talk", weight=2, length=2.9)
def _(c):
    c.key(0.5, **HAND_TO_CHIN, la=(-36, -38, 0), head=(-8, 14, 0), look=(.5, -.6))
    c.key(2.1, ra=(-102, -42, 0), head=(-6, 16, 4), look=(.5, -.5))


@clip("talk_tilt", "Tilts head", trigger="talk", weight=2, mirror="free", length=2.1)
def _(c):
    c.key(0.5, head=(4, 8, 14), ra=(-16, 0, 8), lid=.2)
    c.key(1.4, head=(5, 8, 15))


@clip("talk_count_points", "Counts on fingers", trigger="talk", weight=1.5, length=2.9, also={"chat_count": "chat_speak"})
def _(c):
    c.key(0.4, la=(-62, -20, 0), ra=(-62, -30, 0), head=(10, 0, 0), look=(0, .4))
    for t in (0.8, 1.3, 1.8):
        c.key(t, ra=(-70, -26, 0)).key(t + .2, ra=(-62, -30, 0))
    c.key(2.3, head=(0, 0, 0), look=(0, 0))


# -- chatting with a neighbor (two residents standing together take turns) ----------------------


@clip("chat_tell_a_story", "Tells a story", trigger="chat_speak", weight=3, length=3.1)
def _(c):
    c.key(0.4, ra=(-60, 20, 20), waist=(4, 0, 0))
    c.key(0.6, la=(-40, 16, 12))
    c.key(1.0, ra=(-82, 30, 32), head=(-4, 0, -6))
    c.key(1.5, ra=(-50, 10, 10), la=(-50, 20, 20), head=(2, 0, 2))
    c.key(2.1, ra=(-66, 24, 24), la=(-40, 14, 12))


@clip("chat_point", "Points somewhere", trigger="chat_speak", weight=2, length=2.7)
def _(c):
    c.key(0.5, ra=(-90, 30, 0), head=(0, 30, 0), waist=(0, 8, 0), look=(.6, 0))
    c.key(1.6, ra=(-88, 32, 0), head=(0, 30, 0))
    c.key(2.0, ra=(-40, 10, 10), head=(0, 0, 0), waist=(0, 0, 0), look=(0, 0))


@clip("listen_hands_behind", "Listens politely", trigger="chat_listen", weight=3, mirror="never", length=3.2)
def _(c):
    c.key(0.5, **HANDS_BEHIND, head=(4, 0, 6))
    c.key(1.2, head=(12, 0, 6))
    c.key(1.5, head=(3, 0, 7))
    c.key(2.4, **HANDS_BEHIND, head=(4, 0, -4))


@clip("listen_chuckle", "Chuckles", trigger="chat_listen", weight=2, length=2.3, also={"talk_chuckle": "talk"})
def _(c):
    c.key(0.3, waist=(-6, 0, 0), head=(-10, 0, 4), la=(-30, -30, 0), lid=.6)
    c.wobble(0.3, 1.5, 7, "root_pos", .35, axis=1, decay=.6)
    c.key(1.6, waist=(-2, 0, 0), head=(-2, 0, 2), lid=.3)


@clip("listen_arms_folded", "Listens with arms folded", trigger="chat_listen", weight=2, require=["adult"], length=3.5)
def _(c):
    c.key(0.5, **ARMS_CROSSED, head=(4, 6, 8))
    c.key(1.9, head=(14, 6, 8))
    c.key(2.2, head=(4, 6, 8))
    c.key(2.8, **ARMS_CROSSED, head=(2, 2, 2))


@clip("listen_gasp", "Gasps", trigger="chat_listen", weight=1, length=2.1, also={"talk_gasp": "talk"})
def _(c):
    c.key(0.25, head=(-10, 0, 0), root_pos=(0, -.5, 0), waist=(-4, 0, 0))
    c.key(0.38, **HAND_TO_MOUTH)
    c.key(1.25, ra=(-111, -40, 0), head=(-8, 0, 4), root_pos=(0, 0, 0))
