"""Chat: talking across the tavern table, talking with you from the seat, and seated reactions.

The director turns a seated resident's head toward their chat partner, so these clips don't aim the head
sideways. Like every seated clip they never key the legs or root, and arm poses are written with sat() as
the total angle the arm reaches on top of the riding pose (see seated.py).
"""
from kit import clip

RIDE = -36  # vanilla's riding pose pitches both arms this far forward


def sat(pitch, yaw=0, roll=0):
    """An arm pose as the total angle it reaches, written relative to the riding pose."""
    return (pitch - RIDE, yaw, roll)


SEATED = ["seated"]
ON_TABLE = sat(-92, -16, 0)
FOLDED = dict(ra=sat(-64, -46, -6), la=sat(-56, -40, -6))
OPEN_PALM = sat(-62, 18, 14)

# -- speaking --------------------------------------------------------------------------------------


@clip("lean_in_to_tell_it", "Leans in to tell it", trigger="chat_speak", weight=3, require=SEATED,
      boost={"personality:playful": 1.5, "personality:curious": 1.5, "evening": 1.3}, length=3.4)
def _(c):
    c.key(0.4, la=sat(-104, -16, 0), ra=sat(-106, -10, 4), waist=(12, 0, 0), head=(-6, 0, 0), lid=.3)
    for t in (0.7, 1.15, 1.6):
        c.key(t, ra=sat(-114, -8, 6), head=(-4, 0, -4)).key(t + .2, ra=sat(-104, -10, 4), head=(-6, 0, 0))
    c.key(2.2, la=sat(-106, -16, 0), waist=(14, 0, 0), head=(-8, 0, 6), lid=.45)
    c.key(2.7, ra=sat(-50, 10, 10), la=sat(-60, -10, 0), waist=(-2, 0, 0), head=(-4, 0, 0), lid=.2)
    c.key(3.05, head=(-2, 0, 0))


@clip("tell_a_story", "Tells a story with both hands", trigger="chat_speak", weight=3, require=SEATED, mirror="never",
      boost={"personality:imaginative": 2, "personality:adventurous": 1.5}, length=3.6)
def _(c):
    c.key(0.4, ra=sat(-90, 10, 12), la=sat(-88, 10, 12), head=(-4, 0, 0), waist=(4, 0, 0))
    c.key(0.9, ra=sat(-112, 24, 20), la=sat(-88, 6, 10), waist=(0, 6, 0), head=(-8, 0, -4), lid=.2)
    c.key(1.4, ra=sat(-88, 6, 10), la=sat(-110, 24, 20), waist=(0, -6, 0), head=(-6, 0, 4))
    c.key(1.9, ra=sat(-98, 30, 24), la=sat(-98, 30, 24), waist=(-4, 0, 0), head=(-10, 0, 0), lid=.35)
    c.key(2.35, ra=sat(-96, 4, 8), la=sat(-96, 4, 8), waist=(6, 0, 0), head=(2, 0, 0), lid=.1)
    c.key(3.0, ra=sat(-50, 6, 6), la=sat(-50, 6, 6), waist=(0, 0, 0), head=(0, 0, 0))


@clip("story_with_the_mug", "Tells a story waving the mug", trigger="chat_speak", weight=4,
      require=SEATED + ["dining:drink"], boost={"evening": 1.5, "night": 1.5}, mirror="hand", items="override",
      length=3.8)
def _(c):
    c.key(0.4, ra=sat(-92, 10, 10), la=sat(-70, 14, 12), head=(-4, 0, 0))
    c.cycle(0.7, 2.1, .7, dict(ra=sat(-106, 34, 24), la=sat(-78, 18, 14), head=(-8, 0, -4)),
            dict(ra=sat(-92, 10, 10), la=sat(-64, 8, 10), head=(-2, 0, 4)))
    c.key(2.45, ra=sat(-104, -38, 0), head=(-6, 0, 0), lid=.45)
    c.key(2.85, ra=sat(-108, -38, 0), head=(-10, 0, 0), lid=.6)
    c.key(3.2, ra=sat(-74, -20, 0), la=sat(-46, 0, 4), head=(0, 0, 0), lid=.1)


@clip("point_across_the_room", "Points across the room", trigger="chat_speak", weight=2, require=SEATED, mirror="free",
      length=3.2)
def _(c):
    c.key(0.35, ra=sat(-80, 10, 6), head=(0, 6, 0))
    c.key(0.7, ra=sat(-98, 34, 10), waist=(0, 10, 0), head=(-2, 24, 0), look=(.6, 0))
    c.wobble(0.8, 1.5, 4, "ra", 3, base=sat(-98, 34, 10), axis=0)
    c.key(1.7, ra=sat(-96, 32, 10), head=(-2, 20, 0), look=(.5, 0))
    c.key(2.1, ra=sat(-70, 10, 8), waist=(0, 0, 0), head=(-4, 0, 4), look=(0, 0), lid=.3)
    c.key(2.7, ra=sat(-46, 4, 4), head=(0, 0, 0), lid=0)


@clip("count_on_fingers_at_the_table", "Counts on fingers", trigger="chat_speak", weight=2, require=SEATED,
      boost={"personality:meticulous": 2, "personality:pragmatic": 1.5}, length=3.4)
def _(c):
    c.key(0.4, la=sat(-84, -28, 0), ra=sat(-86, -36, 0), head=(10, 0, 0), look=(0, .4))
    for i, t in enumerate((0.7, 1.15, 1.6, 2.05)):
        c.key(t, ra=sat(-92, -36 + i * 4, 0), head=(8, 0, 0))
        c.key(t + .2, ra=sat(-84, -40 + i * 4, 0), head=(12, 0, 0))
    c.key(2.5, ra=sat(-72, 16, 14), la=sat(-60, -14, 0), head=(-4, 0, 4), look=(0, 0), lid=.2)
    c.key(2.95, ra=sat(-50, 8, 8), head=(-2, 0, 2))



@clip("whisper_across_the_table", "Whispers across the table", trigger="chat_speak", weight=2, require=SEATED,
      boost={"personality:playful": 1.5, "personality:curious": 1.5, "night": 1.3}, length=3.4)
def _(c):
    c.key(0.35, head=(0, -14, 0), look=(-.6, 0))
    c.key(0.7, head=(0, 12, 0), look=(.6, 0))
    c.key(1.0, ra=sat(-110, -16, 16), la=sat(-104, -16, 0), waist=(16, 0, 0), head=(2, 0, -8), look=(0, 0), lid=.35)
    c.wobble(1.1, 2.3, 5, "head", 3, base=(2, 0, -8), axis=0)
    c.key(2.4, ra=sat(-108, -16, 16), la=sat(-104, -16, 0), waist=(15, 0, 0), lid=.4)
    c.key(2.9, ra=sat(-50, 0, 6), la=sat(-50, -6, 0), waist=(0, 0, 0), head=(0, 0, 0), lid=0)

# -- listening -------------------------------------------------------------------------------------


@clip("nod_along_at_the_table", "Nods along", trigger="chat_listen", weight=3, require=SEATED, length=3.0)
def _(c):
    c.key(0.35, la=ON_TABLE, head=(2, 0, 0), lid=.15)
    c.cycle(0.5, 2.3, .6, dict(head=(12, 0, 2)), dict(head=(2, 0, -2)))
    c.key(2.4, la=ON_TABLE)
    c.key(2.6, head=(4, 0, 0), lid=.1)


@clip("laugh_and_slap_the_table", "Laughs and slaps the table", trigger="chat_listen", weight=2, require=SEATED,
      mirror="free", boost={"personality:playful": 2, "job:nitwit": 2, "evening": 1.3}, length=3.0)
def _(c):
    c.key(0.3, waist=(-8, 0, 0), head=(-16, 0, 0), ra=sat(-110, -10, 0), lid=.8)
    for t in (0.6, 1.1):
        c.key(t, waist=(12, 0, 0), head=(8, 0, 0), ra=sat(-94, -12, 0), lid=.9)
        c.key(t + .25, waist=(4, 0, 0), head=(-6, 0, 0), ra=sat(-112, -10, 0))
    c.wobble(1.4, 2.2, 6, "waist", 3, base=(2, 0, 0), axis=0, decay=.5)
    c.key(2.4, ra=sat(-50, -6, 0), waist=(0, 0, 0), head=(-2, 0, 0), lid=.4)


@clip("chin_in_hand_listening", "Listens with chin in hand", trigger="chat_listen", weight=2, require=SEATED,
      boost={"personality:thoughtful": 2, "personality:curious": 1.5, "personality:gentle": 1.5}, length=3.8)
def _(c):
    c.hold(0.55, 3.1, ra=sat(-104, -42, 0), la=sat(-96, -26, 0))
    c.key(0.55, waist=(12, 0, 0), head=(6, 0, -10), look=(0, -.2))
    c.key(1.5, head=(10, 0, -11), lid=.25)
    c.key(1.85, head=(6, 0, -10), lid=0)
    c.key(2.45, head=(8, 0, -12))
    c.key(2.6, lid=.6)
    c.key(2.8, waist=(12, 0, 0), head=(7, 0, -11), lid=0)


@clip("lean_back_skeptical", "Leans back skeptical with arms folded", trigger="chat_listen", weight=1.5,
      require=SEATED, boost={"personality:pragmatic": 2, "personality:meticulous": 2, "personality:reserved": 1.5},
      length=3.4)
def _(c):
    c.key(0.5, **FOLDED, waist=(-10, 0, 0), head=(-8, -8, -6), lid=.5, look=(.4, 0))
    c.key(1.4, head=(-10, -12, -8), lid=.55, look=(.5, 0))
    c.key(2.0, head=(-6, -4, 6), lid=.6, look=(.3, 0))
    c.key(2.8, **FOLDED, waist=(-9, 0, 0), head=(-6, -6, 4), lid=.5)



@clip("gasp_at_the_table", "Gasps at the news", trigger="chat_listen", weight=1.5, require=SEATED,
      boost={"personality:gentle": 1.5, "personality:warmhearted": 1.5, "personality:imaginative": 1.5}, length=2.8)
def _(c):
    c.key(0.25, ra=sat(-58, -50, 0), waist=(-8, 0, 0), head=(-10, 0, 0), ra_pos=(0, -.5, 0), lid=0, look=(0, -.2))
    c.key(0.6, ra=sat(-110, -42, 0), waist=(-10, 0, 0), head=(-12, 0, 4))
    c.key(1.5, ra=sat(-112, -42, 0), waist=(-9, 0, 0), head=(-10, 0, 6), lid=.15)
    c.key(1.9, ra=sat(-58, -50, 0), ra_pos=(0, 0, 0), waist=(-2, 0, 0), head=(4, 0, 0), look=(0, 0))
    c.key(2.3, head=(8, 0, -4), lid=.3)


@clip("listen_over_the_mug", "Listens over the mug", trigger="chat_listen", weight=3, require=SEATED + ["dining:drink"],
      boost={"personality:reserved": 1.5, "personality:thoughtful": 1.5}, mirror="hand", items="override", length=3.8)
def _(c):
    c.key(0.45, ra=sat(-80, -26, 0), head=(4, 0, 0), look=(0, .1))
    c.key(0.9, ra=sat(-104, -38, 0), head=(-4, 0, 0), lid=.4)
    c.key(1.4, ra=sat(-106, -38, 0), head=(-6, 0, 0), lid=.45)
    c.key(1.8, ra=sat(-82, -26, 0), head=(6, 0, 0), lid=.1)
    c.key(2.2, head=(12, 0, 2))
    c.key(2.6, ra=sat(-80, -26, 0), head=(3, 0, 0))
    c.key(3.3, ra=sat(-48, -10, 0), head=(5, 0, 0))

# -- talking with you (your conversation window is open) -------------------------------------------


@clip("explain_from_the_seat", "Explains from the seat", trigger="talk", weight=3, require=SEATED, length=2.6)
def _(c):
    c.key(0.4, ra=OPEN_PALM, head=(4, 0, -6))
    c.key(0.9, ra=sat(-54, 10, 10), head=(-2, 0, 4))
    c.key(1.4, ra=sat(-66, 22, 18), la=sat(-50, 8, 8), head=(2, 0, -2))
    c.key(1.9, ra=sat(-56, 14, 12), la=sat(-40, 2, 4), head=(0, 0, 0))


@clip("nod_from_the_seat", "Nods from the seat", trigger="talk", weight=2, require=SEATED, length=2.6)
def _(c):
    c.key(0.3, la=ON_TABLE, head=(2, 0, 0), lid=.15)
    c.cycle(0.45, 1.65, .4, dict(head=(12, 0, 0)), dict(head=(2, 0, 0)))
    c.key(1.8, la=ON_TABLE)
    c.key(2.1, head=(4, 0, 4), lid=.1)


@clip("shrug_in_the_seat", "Shrugs in the seat", trigger="talk", weight=2, require=SEATED, mirror="never", length=2.6)
def _(c):
    c.key(0.3, ra=sat(-44, 10, 10), la=sat(-44, 10, 10), head=(2, 0, 0))
    c.key(0.55, ra=sat(-54, 24, 22), la=sat(-54, 24, 22), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), waist=(-4, 0, 0),
          head=(-6, 0, 8), lid=.2)
    c.key(1.4, ra=sat(-52, 23, 21), la=sat(-52, 23, 21), ra_pos=(0, -1.2, 0), la_pos=(0, -1.2, 0), head=(-7, 0, 9))
    c.key(1.85, ra=sat(-40, 4, 4), la=sat(-40, 4, 4), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0),
          lid=0)


@clip("tap_the_table_for_emphasis", "Taps the table for emphasis", trigger="talk", weight=2, require=SEATED, length=2.6,
      boost={"personality:pragmatic": 1.5, "personality:protective": 1.5, "personality:steadfast": 1.5})
def _(c):
    c.key(0.35, ra=sat(-100, -14, 0), waist=(8, 0, 0), head=(4, 0, 0), lid=.2)
    for t in (0.6, 1.0, 1.4):
        c.key(t, ra=sat(-92, -14, 0), head=(8, 0, 0)).key(t + .18, ra=sat(-102, -14, 0), head=(2, 0, 0))
    c.key(2.0, ra=sat(-56, 6, 8), waist=(0, 0, 0), head=(0, 0, 0), lid=0)


# -- reactions -------------------------------------------------------------------------------------


@clip("wave_from_the_seat", "Waves from the seat", trigger="greet", weight=4, require=["adult"] + SEATED,
      boost={"personality:playful": 1.5, "personality:warmhearted": 1.5}, length=2.6)
def _(c):
    c.key(0.38, ra=sat(-24, 0, 138), head=(-4, 0, -8), lid=.3)
    c.cycle(0.45, 2.0, .36, dict(ra=sat(-24, 0, 152)), dict(ra=sat(-24, 0, 122)))
    c.key(2.1, ra=sat(-30, 0, 50), head=(0, 0, -3), lid=.1)


@clip("nod_hello_from_the_seat", "Nods hello from the seat", trigger="greet", weight=2, require=["adult"] + SEATED,
      boost={"personality:reserved": 3, "personality:pragmatic": 2, "personality:steadfast": 2}, length=2.6)
def _(c):
    c.key(0.4, head=(14, 0, 0), ra=sat(-50, 0, 24), lid=.3)
    c.key(0.9, head=(-2, 0, 0), ra=sat(-48, 0, 28))
    c.key(1.3, head=(6, 0, -4), lid=.2)
    c.key(1.9, ra=sat(-38, 0, 8), head=(0, 0, 0), lid=0)


@clip("raise_the_mug_to_you", "Raises the mug to you", trigger="greet", weight=6,
      require=["adult"] + SEATED + ["dining:drink"], mirror="hand", items="override", length=2.8)
def _(c):
    c.key(0.35, ra=sat(-100, -6, 4), head=(-2, 0, 0))
    c.key(0.7, ra=sat(-132, 6, 8), head=(-6, 0, -4), lid=.3)
    c.key(1.2, ra=sat(-134, 6, 8), head=(10, 0, -4), lid=.45)
    c.key(1.55, head=(-2, 0, -2), lid=.2)
    c.key(2.0, ra=sat(-80, -24, 0), head=(0, 0, 0), lid=0)


@clip("belly_laugh_at_the_table", "Belly laughs and slaps the table", trigger="laugh", weight=4, require=SEATED,
      mirror="free", length=3.0)
def _(c):
    c.key(0.25, waist=(-12, 0, 0), head=(-18, 0, 0), ra=sat(-60, -20, 0), la=sat(-60, -20, 0), lid=.75)
    c.wobble(0.3, 1.0, 7, "waist", 2.5, base=(-12, 0, 0), axis=0)
    for t in (1.15, 1.6):
        c.key(t, waist=(14, 0, 0), head=(8, 0, 0), ra=sat(-94, -14, 0), la=sat(-94, -14, 0), lid=.9)
        c.key(t + .22, waist=(6, 0, 0), head=(-4, 0, 0), ra=sat(-110, -12, 0), la=sat(-110, -12, 0))
    c.key(2.3, waist=(0, 0, 0), head=(-4, 0, 0), ra=sat(-50, -10, 0), la=sat(-50, -10, 0), lid=.4)


@clip("clap_in_the_seat", "Claps in the seat", trigger="happy", weight=4, require=SEATED, mirror="never", length=2.6,
      also={"clap_in_the_seat_delighted": "delighted"})
def _(c):
    c.key(0.25, ra=sat(-84, -10, 6), la=sat(-84, -10, 6), waist=(-4, 0, 0), head=(-8, 0, 0), lid=.5)
    c.cycle(0.35, 1.95, .28, dict(ra=sat(-88, -24, 0), la=sat(-88, -24, 0), head=(-10, 0, 0)),
            dict(ra=sat(-86, -4, 10), la=sat(-86, -4, 10), head=(-6, 0, 0)))
    c.key(2.2, ra=sat(-50, -8, 4), la=sat(-50, -8, 4), waist=(0, 0, 0), head=(-2, 0, 0), lid=.2)


@clip("bow_from_the_seat", "Bows from the seat with a hand on the heart", trigger="thanks", weight=4, require=SEATED,
      length=2.6)
def _(c):
    c.key(0.4, ra=sat(-58, -50, 0), head=(2, 0, 0))
    c.key(0.85, waist=(18, 0, 0), head=(14, 0, 0), lid=.55)
    c.key(1.35, waist=(19, 0, 0), head=(15, 0, 0))
    c.key(1.85, ra=sat(-50, -40, 0), waist=(0, 0, 0), head=(0, 0, 6), lid=.2)



@clip("giggle_in_the_seat", "Giggles behind a hand", trigger="laugh", weight=3, require=SEATED, length=2.6)
def _(c):
    c.key(0.3, ra=sat(-113, -40, 0), waist=(4, 0, 0), head=(8, 0, 10), lid=.6)
    c.wobble(0.35, 1.7, 6, "waist", 2, base=(4, 0, 0), axis=0)
    c.wobble(0.35, 1.7, 6, "ra_pos", .4, axis=1)
    c.key(1.8, ra=sat(-110, -40, 0), head=(6, 0, 8), lid=.5)
    c.key(2.2, ra=sat(-50, -10, 0), waist=(0, 0, 0), head=(2, 0, 2), lid=.2)
