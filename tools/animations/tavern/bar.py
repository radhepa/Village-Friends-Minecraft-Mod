"""Bar: standing patrons at the tavern bar, and the tavern staff at work.

Standing patrons hold their drink in the right hand the whole time (left-handed residents mirror these
clips). Clips that keep items leave that arm in vanilla's holding pose and move the free hand; clips that
drink (they require dining:drink) override items and lift the mug. A standing holding arm already pitches
-18 degrees, so the drinking arm is written with held() as the total angle it reaches. Every clip here
avoids "seated"; the bar counter is about a block high in front of the patron.
"""
from kit import clip, HAND_TO_MOUTH, HANDS_ON_HIPS

ITEM = -18  # vanilla's held-item pose for a standing arm


def held(pitch, yaw=0, roll=0):
    """The arm holding the drink, as the total angle it reaches, on top of the held-item pose."""
    return (pitch - ITEM, yaw, roll)


PATRON = ["adult", "tavern"]
STANDING = ["seated"]
COUNTER = (-82, -10, 0)            # the free forearm along the counter top
SIP = held(-104, -38, 0)
CUPPED = held(-78, -26, 0)


@clip("lean_on_the_counter", "Leans an elbow on the counter", weight=4, require=PATRON, avoid=STANDING,
      boost={"evening": 1.5, "night": 1.5}, length=6.0)
def _(c):
    c.key(0.6, la=COUNTER, waist=(10, -6, 0), root=(0, 0, -2), head=(0, 12, 0), rl=(-6, 0, 2), look=(.3, 0))
    c.key(1.8, head=(-2, 26, 2), look=(.6, 0))
    c.key(2.8, head=(4, 4, 0), lid=.3, look=(0, .2))
    c.key(3.8, head=(-2, -24, -2), look=(-.5, 0), lid=0)
    c.key(4.6, head=(0, -14, 0), look=(-.3, 0))
    c.key(5.3, la=COUNTER, waist=(9, -5, 0), root=(0, 0, -2), rl=(-6, 0, 2), head=(2, 0, 0), look=(0, 0))


@clip("wave_for_the_keeper", "Waves for the keeper", weight=3, require=PATRON, avoid=STANDING, length=3.6)
def _(c):
    c.key(0.4, la=(-24, 0, 120), head=(-6, 10, 0), look=(.3, -.2))
    c.key(0.7, la=(-24, 0, 142), head=(-10, 14, 0), root_pos=(0, -.6, 0), lid=0)
    c.cycle(0.8, 2.2, .4, dict(la=(-24, 0, 154)), dict(la=(-24, 0, 126)))
    c.key(2.4, la=(-24, 0, 70), root_pos=(0, 0, 0), head=(-6, 10, 0))
    c.key(2.8, la=COUNTER, waist=(6, 0, 0), head=(2, 4, 0), lid=.3, look=(.1, 0))
    c.key(3.2, head=(4, 0, 0))


@clip("sip_at_the_bar", "Sips at the bar", weight=6, require=PATRON + ["dining:drink"], avoid=STANDING,
      mirror="hand", items="override", length=4.6)
def _(c):
    c.key(0.5, ra=CUPPED, la=COUNTER, waist=(6, 0, 0), head=(4, 0, 0), look=(0, .3))
    c.key(1.0, ra=SIP, head=(-6, 0, 0), lid=.45, look=(0, .1))
    c.key(1.8, ra=held(-110, -38, 0), head=(-10, 0, 0), lid=.55)
    c.key(2.3, ra=CUPPED, head=(2, 0, 0), lid=.3, look=(0, .3))
    c.key(2.8, head=(-2, 8, 4), lid=.5, look=(.2, 0))
    c.key(3.5, ra=held(-60, -16, 0), la=COUNTER, waist=(5, 0, 0), head=(2, 4, 2), lid=.2)
    c.key(4.1, ra=held(-30, -6, 0), head=(0, 0, 0), lid=0, look=(0, 0))


@clip("toast_at_the_bar", "Raises a toast at the bar", weight=5, require=PATRON + ["dining:drink", "social"],
      avoid=STANDING, boost={"evening": 1.5, "night": 1.5, "personality:playful": 1.5}, mirror="hand", items="override",
      length=4.6)
def _(c):
    c.key(0.45, ra=CUPPED, head=(2, 0, 0))
    c.key(0.9, ra=held(-150, 4, 6), waist=(-4, 0, 0), head=(-10, 0, 0), root_pos=(0, -.4, 0), lid=.3, look=(0, -.4))
    c.key(1.5, ra=held(-154, 6, 8), head=(-12, 0, -4), lid=.4)
    c.key(1.7, ra=held(-146, 4, 6), root_pos=(0, 0, 0))
    c.key(2.2, ra=SIP, waist=(-2, 0, 0), head=(-6, 0, 0), lid=.5, look=(0, .1))
    c.key(2.7, ra=held(-114, -36, 0), head=(-14, 0, 0), waist=(-4, 0, 0), lid=.7)
    c.key(3.2, ra=CUPPED, head=(2, 0, 0), waist=(0, 0, 0), lid=.3, look=(0, 0))
    c.key(3.6, head=(-4, 0, 6), lid=.5)
    c.key(4.1, ra=held(-36, -8, 0), head=(0, 0, 2), lid=.1)


@clip("sway_at_the_bar", "Sways to the music at the bar", weight=5, require=["tavern", "music"], avoid=STANDING,
      boost={"evening": 1.5}, mirror="never", length=6.0)
def _(c):
    c.key(0.6, root=(0, 0, 3), waist=(0, 0, 3), head=(-4, 4, 6), la=(-10, 0, 8), lid=.4)
    c.cycle(0.8, 5.0, 1.4, dict(root=(0, 0, 3), waist=(0, 0, 3), head=(-4, 6, 8), la=(-14, 0, 10)),
            dict(root=(0, 0, -3), waist=(0, 0, -3), head=(-4, -6, -8), la=(-4, 0, 4)))
    c.key(5.5, root=(0, 0, 0), waist=(0, 0, 0), head=(0, 0, 0), la=(0, 0, 0), lid=.2)


@clip("clap_at_the_bar", "Claps along at the bar", weight=5, require=["tavern", "music"], avoid=STANDING + ["holding"],
      boost={"personality:playful": 1.5, "child": 1.5}, mirror="never", length=4.6)
def _(c):
    c.key(0.35, ra=(-64, -14, 4), la=(-64, -14, 4), head=(-4, 0, 0), lid=.3)
    c.cycle(0.5, 3.7, .5, dict(ra=(-70, -24, 0), la=(-70, -24, 0), head=(-2, 0, 3), root_pos=(0, .4, 0)),
            dict(ra=(-62, -4, 10), la=(-62, -4, 10), head=(-6, 0, -3), root_pos=(0, 0, 0)))
    c.key(4.0, ra=(-50, -10, 0), la=(-50, -10, 0), head=(-6, 0, 0), root_pos=(0, 0, 0), lid=.5)
    c.key(4.3, lid=.2)


# -- the tavern staff ------------------------------------------------------------------------------


@clip("wipe_down_a_table", "Wipes down a table", weight=5, require=["adult", "job:tavern_keeper", "routine:work"],
      avoid=STANDING + ["dining:carry"], boost={"evening": 1.5}, length=5.6)
def _(c):
    c.key(0.5, la=(-96, -12, 0), ra=(-100, -30, 0), waist=(24, 0, 0), head=(16, 0, 0), rl=(-10, 0, 0), look=(0, .6))
    loop = [(-100, -30, 0), (-96, -10, 8), (-102, 10, 12), (-108, -10, 4)]
    t, i = 0.7, 0
    while t < 3.5:
        c.key(t, ra=loop[i % 4], waist=(24, (-5, 0, 5, 0)[i % 4], 0), head=(16, (-4, 0, 4, 0)[i % 4], 0))
        t += .22
        i += 1
    c.key(3.8, ra=(-100, -20, 0), la=(-96, -12, 0), waist=(24, 0, 0), head=(18, 0, 0))
    c.key(4.3, ra=(-170, 10, 10), la=(-20, 0, 6), waist=(0, 0, 0), head=(-4, 8, 0), rl=(0, 0, 0), look=(.3, 0))
    c.key(4.7, ra=(-150, 14, 12), head=(-2, 8, 0), lid=.3)
    c.key(5.1, **HANDS_ON_HIPS, head=(-2, -6, 0), lid=0, look=(-.2, 0))


@clip("ring_last_orders", "Rings the bell for last orders", weight=5, require=["adult", "job:tavern_keeper", "night"],
      avoid=STANDING + ["dining:carry"], boost={"routine:work": 2}, length=4.8)
def _(c):
    c.key(0.45, ra=(-150, 0, -4), head=(-4, 0, 0))
    c.key(0.75, ra=(-168, 0, -12), la=(-60, -30, 0), head=(-8, 0, 0), look=(0, -.3))
    c.wobble(0.85, 2.15, 6, "ra", 9, base=(-168, 0, -12), axis=2)
    c.key(2.4, ra=(-166, 0, -12), **{"la": HAND_TO_MOUTH["ra"]}, head=(-10, 14, 0), lid=.2, look=(.4, -.2))
    c.key(3.0, head=(-10, -14, 0), look=(-.4, -.2))
    c.key(3.4, ra=(-166, 0, -12), la=(-60, -30, 0), head=(-6, 0, 0), look=(0, 0))
    c.wobble(3.5, 4.0, 6, "ra", 8, base=(-166, 0, -12), axis=2)
    c.key(4.4, ra=(-40, 0, 6), la=(0, 0, 0), head=(0, 0, 0), lid=0)


@clip("bow_to_the_room", "Bows to the room", weight=5, require=["adult", "job:bard", "routine:perform"],
      avoid=STANDING, boost={"evening": 1.5, "night": 1.5}, length=4.2)
def _(c):
    c.key(0.35, ra=(-40, 20, 62), la=(-40, 20, 62), waist=(-4, 0, 0), head=(-6, 0, 0), lid=.3)
    c.key(0.8, ra=(-60, 10, 70), la=(-60, 10, 70), head=(-8, 0, 0))
    c.key(1.2, ra=(-56, -48, 0), la=(16, 0, 40), rl=(-14, 0, 0), waist=(40, 0, 0), head=(16, 0, 0), lid=.5)
    c.key(2.0, ra=(-56, -48, 0), la=(16, 0, 42), rl=(-14, 0, 0), waist=(42, 0, 0), head=(18, 0, 0))
    c.key(2.6, ra=(-44, 22, 64), la=(-44, 22, 64), rl=(0, 0, 0), waist=(-6, 0, 0), head=(-10, 0, 0), lid=.6)
    c.key(3.2, ra=(-46, 24, 66), la=(-46, 24, 66), head=(-8, 10, 0), look=(.3, 0))
    c.key(3.7, ra=(-16, 6, 14), la=(-16, 6, 14), waist=(0, 0, 0), head=(0, 0, 0), lid=.1, look=(0, 0))
