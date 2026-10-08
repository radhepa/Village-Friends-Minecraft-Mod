"""Seated: idles for residents sitting at a tavern table, waiting for their food and listening to the bard.

Seated residents ride an invisible seat, so vanilla's riding pose is their base: both arms already pitch 36
degrees forward (hands on the thighs) and the legs stick out under the table. The poser ignores the legs and
root while seated, so these clips never key them; the waist bends at the hips to lean over the table or back
in the chair. Arm poses are written with sat(): the total angle the arm reaches (the numbers a standing clip
would use), minus what the riding pose already adds. Tables in the village taverns are fence posts with a
pressure plate, which puts the table top just under the shoulders: forearms rest on it with the arms nearly
level (about -85).
"""
from kit import clip

RIDE = -36  # vanilla's riding pose pitches both arms this far forward


def sat(pitch, yaw=0, roll=0):
    """An arm pose as the total angle it reaches, written relative to the riding pose."""
    return (pitch - RIDE, yaw, roll)


LAP = dict(ra=sat(-36), la=sat(-36))
ON_TABLE = dict(ra=sat(-90, -16, 0), la=sat(-90, -16, 0))
FOLDED = dict(ra=sat(-64, -46, -6), la=sat(-56, -40, -6))
NO_MEAL = ["dining:eat"]
LATE = {"evening": 1.5, "night": 2}


@clip("settle_into_the_seat", "Settles into the seat", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"dining:wait": 2}, length=4.2)
def _(c):
    c.key(0.45, ra=sat(-92, -10, 0), la=sat(-92, -10, 0), waist=(6, 0, 0), head=(8, 0, 0), look=(0, .4))
    c.key(0.9, ra=sat(-100, -12, 0), la=sat(-100, -12, 0), waist=(12, 0, 0), head=(4, 0, 0))
    c.key(1.25, ra=sat(-50, -8, 6), la=sat(-50, -8, 6), waist=(2, 0, 5), head=(2, 0, -4), look=(0, 0))
    c.key(1.6, waist=(2, 0, -5), head=(2, 0, 5))
    c.key(1.95, ra=sat(-40, -6, 4), la=sat(-40, -6, 4), waist=(0, 0, 0), head=(0, 0, 0))
    c.key(2.4, ra_pos=(0, -.7, 0), la_pos=(0, -.7, 0), waist=(-6, 0, 0), head=(-12, 0, 0), lid=.6, look=(0, -.3))
    c.key(3.0, ra_pos=(0, 0, 0), la_pos=(0, 0, 0), waist=(-3, 0, 0), head=(4, 0, 0), lid=.3, look=(0, 0))
    c.key(3.6, ra=sat(-38, -4, 2), la=sat(-38, -4, 2), head=(6, 6, 0), lid=.1)


@clip("look_around_the_room", "Looks around the room", weight=4, require=["seated"], avoid=NO_MEAL, mirror="free",
      length=5.2)
def _(c):
    c.key(0.6, head=(-2, 38, 3), waist=(0, 8, 0), look=(.6, 0))
    c.key(1.5, head=(-6, 44, 4), waist=(0, 9, 0), look=(.75, -.2))
    c.key(2.1, head=(2, 0, 0), waist=(0, 0, 0), look=(0, 0))
    c.key(2.4, head=(4, -4, 0))
    c.key(3.1, head=(-2, -40, -3), waist=(0, -8, 0), look=(-.7, 0), ra=sat(-40, -6, 0))
    c.key(4.0, head=(0, -36, -2), waist=(0, -7, 0), look=(-.6, .15))
    c.key(4.5, ra=sat(-36))


@clip("admire_the_beams", "Admires the beams overhead", weight=3, require=["seated"], avoid=NO_MEAL, length=5.0)
def _(c):
    c.key(0.6, head=(-28, -8, 0), waist=(-6, 0, 0), look=(0, -.7))
    c.key(1.5, head=(-32, 16, 3), waist=(-7, 3, 0), look=(.4, -.7))
    c.key(2.0, ra=sat(-150, 6, 8), head=(-34, 18, 3))
    c.key(2.9, ra=sat(-152, 24, 8), head=(-34, 26, 2), look=(.6, -.7))
    c.key(3.4, ra=sat(-50, -6, 0), head=(-20, 8, 0), waist=(-4, 0, 0), lid=.2, look=(.2, -.4))
    c.key(4.0, head=(4, 0, 6), lid=.4, look=(0, 0))
    c.key(4.5, ra=sat(-36), head=(4, 0, 4))


@clip("lean_back_and_stretch", "Leans back and stretches", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"morning": 1.5, "evening": 1.5}, mirror="never", length=4.6)
def _(c):
    c.key(0.5, ra=sat(-40, 0, 60), la=sat(-40, 0, 60), waist=(-4, 0, 0), head=(-6, 0, 0))
    c.key(1.2, ra=sat(-14, 0, 150), la=sat(-14, 0, 150), waist=(-14, 0, 0), head=(-20, 0, 0), lid=.7)
    c.key(2.0, ra=sat(-10, 0, 160), la=sat(-10, 0, 160), waist=(-16, 0, 0), head=(-24, 0, 0), lid=.9)
    c.key(2.35, waist=(-15, 0, 5))
    c.key(2.7, waist=(-14, 0, -5))
    c.key(3.3, ra=sat(-30, 0, 40), la=sat(-30, 0, 40), waist=(-2, 0, 0), head=(4, 0, 0), lid=.2)
    c.key(3.9, ra=sat(-36), la=sat(-36), head=(2, 0, 0), lid=0)


@clip("hands_behind_the_head", "Leans back with hands behind the head", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"personality:playful": 1.5, "personality:adventurous": 1.5, "evening": 1.5}, mirror="never", length=6.0)
def _(c):
    behind = dict(ra=sat(-210, 0, 15), la=sat(-210, 0, 15))
    c.key(0.5, ra=sat(-150, 0, 30), la=sat(-150, 0, 30), waist=(-4, 0, 0), head=(-4, 0, 0))
    c.key(1.0, **behind, waist=(-12, 0, 0), head=(-8, 0, 0), lid=.3)
    c.key(2.2, waist=(-13, 0, 2), head=(-10, 6, 3), lid=.5, look=(.3, -.2))
    c.key(3.4, waist=(-12, 0, -2), head=(-10, -6, -3), lid=.5, look=(-.3, -.2))
    c.key(4.4, **behind, waist=(-12, 0, 0), head=(-8, 0, 0), lid=.7)
    c.key(5.0, ra=sat(-120, 0, 30), la=sat(-120, 0, 30), waist=(-4, 0, 0), head=(-2, 0, 0), lid=.2)
    c.key(5.5, ra=sat(-38), la=sat(-38), head=(2, 0, 0), lid=0)


@clip("chin_in_hand", "Rests chin in hand", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"personality:thoughtful": 2, "personality:reserved": 1.5, "evening": 1.3}, length=5.8)
def _(c):
    chin = dict(ra=sat(-104, -42, 0), la=sat(-92, -26, 0), waist=(12, 0, 0))
    c.key(0.6, **chin, head=(6, 0, -10), look=(0, .2))
    c.key(1.6, head=(8, 0, -12), lid=.3, look=(.3, .2))
    c.key(2.6, head=(6, 0, -11), lid=.4, look=(-.3, .3))
    c.key(3.1, lid=.75)
    c.key(3.3, lid=.3)
    c.key(4.2, **chin, head=(8, 0, -12), look=(0, .3))
    c.key(4.9, ra=sat(-60, -20, 0), la=sat(-60, -14, 0), waist=(4, 0, 0), head=(4, 0, -4), lid=0, look=(0, 0))


@clip("drum_fingers_on_the_table", "Drums fingers on the table", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"personality:pragmatic": 1.5, "personality:meticulous": 1.5, "dining:wait": 1.5}, length=4.8)
def _(c):
    c.key(0.5, ra=sat(-86, -14, 0), la=sat(-40, -6, 0), waist=(6, 0, 0), head=(4, 12, -4), lid=.35, look=(.3, .2))
    t = 0.7
    while t < 3.4:
        c.key(t, ra=sat(-84, -14, 0), ra_pos=(0, 0, 0))
        c.key(t + .08, ra=sat(-89, -14, 0), ra_pos=(0, -.4, 0))
        t += .2
    c.key(2.0, head=(4, -14, 4), look=(-.4, .2))
    c.key(3.2, head=(6, 0, 0), lid=.5, look=(0, .4))
    c.key(3.6, ra=sat(-86, -14, 0), ra_pos=(0, 0, 0), head=(-8, 0, 0), lid=.6, look=(0, -.3))
    c.key(4.2, ra=sat(-40, -6, 0), waist=(2, 0, 0), head=(0, 0, 0), lid=.2, look=(0, 0))


@clip("arms_folded_content", "Folds arms contentedly", weight=3, require=["seated"], avoid=NO_MEAL,
      boost={"personality:steadfast": 1.5, "personality:reserved": 1.5, "personality:pragmatic": 1.5}, length=5.6)
def _(c):
    c.key(0.6, **FOLDED, waist=(-6, 0, 0), head=(-4, 0, 0))
    c.key(1.6, head=(-4, 8, 4), lid=.35, look=(.2, 0))
    c.key(2.3, head=(4, 8, 4))
    c.key(2.7, head=(-3, 8, 4))
    c.key(3.6, head=(-2, -12, -2), look=(-.4, 0), lid=.2)
    c.key(4.7, **FOLDED, waist=(-5, 0, 0), head=(-2, -8, 0), look=(-.2, 0))


@clip("yawn_in_the_seat", "Yawns in the seat", weight=2, require=["seated"], avoid=NO_MEAL,
      boost={"morning": 2, "evening": 2.5, "night": 3}, length=3.6)
def _(c):
    c.key(0.5, head=(-12, 0, 4), ra=sat(-88, -30, 0), waist=(-4, 0, 0), lid=.5)
    c.key(1.0, head=(-24, 0, 6), ra=sat(-113, -40, 0), la=sat(-24, 0, 16), waist=(-8, 0, 0), lid=1)
    c.key(1.9, head=(-26, 0, 6), ra=sat(-115, -42, 0), lid=1)
    c.key(2.5, head=(6, 0, 0), ra=sat(-42, -6, 0), la=sat(-36), waist=(2, 0, 0), lid=.4)
    c.key(3.0, head=(2, 0, 0), lid=.1)


@clip("doze_off", "Dozes off", weight=2, require=["seated"], avoid=NO_MEAL, boost={"evening": 2, "night": 3},
      mirror="free", length=7.0)
def _(c):
    c.key(0.6, head=(6, 0, 0), lid=.5)
    c.key(1.4, head=(14, 0, 4), waist=(3, 0, 0), ra=sat(-30, 0, 2), la=sat(-30, 0, 2), lid=.8)
    c.key(2.4, head=(26, 0, 8), waist=(6, 0, 2), lid=1)
    c.key(3.4, head=(30, 0, 10), waist=(8, 0, 3))
    c.key(3.9, head=(34, 0, 12), waist=(9, 0, 3), lid=1, look=(0, 0))
    c.key(4.05, head=(-8, 0, 0), waist=(-4, 0, 0), ra=sat(-44, -4, 0), la=sat(-44, -4, 0), lid=0, look=(0, -.3))
    c.key(4.45, head=(-4, 24, 0), look=(.6, 0))
    c.key(4.95, head=(-4, -20, 0), look=(-.6, 0))
    c.key(5.45, head=(4, 0, 0), waist=(0, 0, 0), ra=sat(-36), la=sat(-36), look=(0, 0), lid=.3)
    c.key(6.3, head=(8, 0, 4), lid=.6)


@clip("warm_hands_at_the_fire", "Warms hands toward the fire", weight=4, require=["seated", "hearth"], avoid=NO_MEAL,
      boost={"evening": 1.5, "night": 1.5, "cold": 2, "personality:gentle": 1.5}, mirror="never", length=5.4)
def _(c):
    toward = dict(ra=sat(-98, -4, 4), la=sat(-98, -4, 4))
    c.key(0.6, **toward, waist=(8, 0, 0), head=(4, 0, 0), lid=.3)
    c.cycle(0.9, 2.3, .34, dict(ra=sat(-100, -22, 0), la=sat(-94, -22, 0)), dict(ra=sat(-94, -22, 0), la=sat(-100, -22, 0)))
    c.key(2.6, **toward, waist=(10, 0, 0), head=(6, 0, 4), lid=.6)
    c.key(3.8, **toward, waist=(10, 0, 0), head=(6, 0, -4), lid=.65)
    c.key(4.5, ra=sat(-50, -10, 0), la=sat(-50, -10, 0), waist=(2, 0, 0), head=(0, 0, 0), lid=.2)


@clip("rub_hands_waiting", "Rubs hands together hungrily", weight=6, require=["seated", "dining:wait"],
      mirror="never", length=3.8)
def _(c):
    c.key(0.4, ra=sat(-70, -22, 0), la=sat(-70, -22, 0), waist=(4, 0, 0), head=(-4, 0, 0), lid=.2)
    c.cycle(0.6, 2.6, .3, dict(ra=sat(-76, -22, 0), la=sat(-64, -22, 0)), dict(ra=sat(-64, -22, 0), la=sat(-76, -22, 0)))
    c.key(2.9, **ON_TABLE, waist=(6, 0, 0), head=(-6, 0, 0), lid=.35, look=(0, -.2))
    c.key(3.4, head=(2, 0, 0), look=(0, 0))


@clip("crane_for_the_keeper", "Cranes over the shoulder for the keeper", weight=6, require=["seated", "dining:wait"],
      mirror="free", length=4.6)
def _(c):
    c.key(0.5, waist=(0, 10, 0), head=(-4, 40, 0), look=(.5, 0))
    c.key(1.0, waist=(-4, 22, -4), head=(-8, 62, 4), ra=sat(-30, 0, 12), look=(.8, -.1))
    c.key(1.9, waist=(-4, 22, -4), head=(-6, 64, 4))
    c.key(2.3, head=(-6, 52, 2), look=(.6, 0))
    c.key(2.8, waist=(0, 0, 0), head=(2, 0, 0), ra=sat(-36), look=(0, 0), lid=.4)
    c.key(3.2, head=(8, -6, 0), ra_pos=(0, .5, 0), la_pos=(0, .5, 0), lid=.5)
    c.key(3.9, head=(4, 0, 0), ra_pos=(0, 0, 0), la_pos=(0, 0, 0), lid=.2)


@clip("tap_a_spoon", "Taps a spoon on the table", weight=6, require=["seated", "dining:wait"], length=4.2)
def _(c):
    c.key(0.4, ra=sat(-92, -14, 0), waist=(4, 0, 0), head=(10, 0, 0), look=(0, .5))
    t = 0.7
    while t < 2.6:
        c.key(t, ra=sat(-86, -14, 0))
        c.key(t + .12, ra=sat(-94, -14, 0))
        t += .3
    c.key(1.6, head=(8, 14, 0), look=(.4, .2))
    c.key(2.3, head=(10, 0, 0), look=(0, .5))
    c.key(2.5, la=sat(-36))
    c.key(2.9, ra=sat(-94, -14, 0), la=sat(-92, -14, 0), head=(-6, 0, 0), lid=.45, look=(0, -.2))
    c.key(3.5, ra=sat(-50, -8, 0), la=sat(-46, -8, 0), waist=(0, 0, 0), head=(4, 0, 0), lid=.2, look=(0, 0))


@clip("sway_to_the_music", "Sways to the music", weight=5, require=["seated", "music"], avoid=NO_MEAL, boost={"evening": 1.5},
      mirror="never", length=6.4)
def _(c):
    c.key(0.6, waist=(0, 0, 4), head=(-4, 4, 6), lid=.4)
    c.cycle(0.8, 5.2, 1.6, dict(waist=(0, 0, 5), head=(-4, 6, 8), ra=sat(-40, 0, 2)),
            dict(waist=(0, 0, -5), head=(-4, -6, -8), ra=sat(-34, 0, 2)))
    c.key(5.8, waist=(0, 0, 0), head=(0, 0, 0), ra=sat(-36), lid=.2)


@clip("clap_along", "Claps along with the music", weight=5, require=["seated", "music"], avoid=NO_MEAL,
      boost={"personality:playful": 1.5},
      mirror="never", length=5.0)
def _(c):
    c.key(0.4, ra=sat(-72, -14, 4), la=sat(-72, -14, 4), head=(-4, 0, 0), lid=.3)
    c.cycle(0.6, 3.8, .5, dict(ra=sat(-74, -24, 0), la=sat(-74, -24, 0), head=(-2, 0, 3)),
            dict(ra=sat(-70, -4, 10), la=sat(-70, -4, 10), head=(-6, 0, -3)))
    c.key(4.1, ra=sat(-60, -10, 0), la=sat(-60, -10, 0), head=(-6, 0, 0), lid=.5)
    c.key(4.6, ra=sat(-38), la=sat(-38), head=(-2, 0, 0), lid=.2)


@clip("tap_the_table_in_rhythm", "Taps the table in rhythm", weight=5, require=["seated", "music"], avoid=NO_MEAL,
      length=5.6)
def _(c):
    c.key(0.5, ra=sat(-94, -14, 0), head=(2, 0, 0), lid=.3)
    i, t = 0, 0.8
    while t < 4.3:
        c.key(t, ra=sat(-86, -14, 0), la=sat(-30 if i % 2 else -40), head=(6, 0, 2 if i % 2 else -2))
        c.key(t + .2, ra=sat(-96, -14, 0), la=sat(-38), head=(0, 0, 0))
        t += .45
        i += 1
    c.key(4.7, ra=sat(-50, -8, 0), la=sat(-36), head=(-4, 0, 4), lid=.4)
    c.key(5.2, head=(-2, 0, 2), lid=.2)
