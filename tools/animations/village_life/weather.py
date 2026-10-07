"""Weather: rain and cold change how residents stand around."""
from kit import clip

HUDDLE = dict(ra=(-70, -50, -8), la=(-62, -46, -8), ra_pos=(0, -1, 0), la_pos=(0, -1, 0))


@clip("hunch_in_the_rain", "Hunches in the rain", weight=6, require=["rain"], mirror="never", length=4.2)
def _(c):
    c.key(0.5, **HUDDLE, head=(18, 0, 0), waist=(6, 0, 0), lid=.4)
    c.wobble(1.0, 2.2, 8, "root", 1.2, axis=2)
    c.key(2.8, head=(16, 0, 0))
    c.key(3.4, **HUDDLE, head=(18, 0, 0), waist=(6, 0, 0), lid=.4)


@clip("catch_raindrops", "Catches raindrops", weight=3, require=["rain"],
      boost={"personality:playful": 3, "personality:gentle": 3, "personality:curious": 3, "child": 3}, length=4.2)
def _(c):
    c.key(0.5, ra=(-80, 20, 24), head=(-26, 10, 0), look=(.2, -.8), lid=.3)
    c.key(1.8, ra=(-82, 20, 24), head=(-28, 12, 0))
    c.key(2.2, head=(16, 14, 0), look=(.3, .6), lid=0)
    c.wobble(2.9, 3.6, 7, "ra", 10, base=(-70, 20, 20), axis=1)


@clip("shake_off_rain", "Shakes off the rain", weight=2, require=["rain"], mirror="free", length=2.4)
def _(c):
    c.wobble(0.2, 1.4, 7, "waist", 10, axis=1, decay=.5)
    c.wobble(0.2, 1.4, 7, "head", 14, axis=1, decay=.4)
    c.wobble(0.2, 1.4, 7, "ra", 12, base=(0, 0, 14), axis=2, decay=.5)
    c.wobble(0.2, 1.4, 7, "la", 12, base=(0, 0, 14), axis=2, decay=.5)
    c.key(1.7, lid=.4).key(2.0, lid=0)


@clip("shiver", "Shivers", weight=5, require=["cold"], mirror="never", length=3.2)
def _(c):
    c.key(0.4, **HUDDLE, head=(10, 0, 0), lid=.3)
    c.wobble(0.5, 2.5, 9, "root", 1.5, axis=2)
    c.wobble(0.5, 2.5, 9, "head", 3, base=(10, 0, 0), axis=1)
    c.key(2.7, **HUDDLE, head=(10, 0, 0), lid=.3)
