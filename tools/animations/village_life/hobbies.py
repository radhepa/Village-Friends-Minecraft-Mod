"""Hobbies: one signature pastime for each of the twelve personalities in content.json."""
from kit import clip, BOOK, HANDS_BEHIND


@clip("knead_dough", "Kneads dough", weight=4, require=["personality:warmhearted|job:cook"], boost={"day": 1.5}, length=4.2)
def _(c):
    c.key(0.45, ra=(-44, -14, 0), la=(-44, -14, 0), waist=(14, 0, 0), head=(20, 0, 0), look=(0, .6))
    c.cycle(0.65, 3.25, .7,
            dict(ra=(-58, -16, 0), la=(-42, -14, 0), waist=(18, 0, 0), root_pos=(0, 0, -.4)),
            dict(ra=(-42, -14, 0), la=(-58, -16, 0), waist=(16, 0, 0), root_pos=(0, 0, 0)))
    c.key(3.6, ra=(-30, -30, 0), la=(-30, -30, 0), waist=(2, 0, 0), head=(4, 0, 0), look=(0, .2))


@clip("read_a_book", "Reads a book", weight=4, require=["personality:thoughtful|job:librarian|job:scholar"], avoid=["rain"],
      mirror="never", length=7.0)
def _(c):
    c.key(0.5, **BOOK, head=(24, 0, 0), waist=(4, 0, 0), look=(0, .7))
    for start in (1.0, 4.4):
        c.key(start, look=(-.45, .7)).key(start + .8, look=(.45, .7)).key(start + 1.0, look=(-.45, .78)).key(start + 1.8, look=(.45, .78))
    c.key(3.2, ra=(-48, -26, 0))
    c.key(3.45, ra=(-58, 8, 12), head=(24, 4, 0))
    c.key(3.75, ra=(-52, -32, -4), head=(24, -2, 0))
    c.key(4.0, **BOOK, head=(24, 0, 0))
    c.key(5.6, head=(28, 0, 2))
    c.key(6.3, **BOOK, head=(10, 0, 0), look=(0, .2))


@clip("conduct_a_tune", "Conducts a tune", weight=4, require=["personality:playful|job:bard"], length=4.8)
def _(c):
    c.key(0.4, ra=(-70, 20, 20), la=(-18, 0, 10), head=(-4, 0, 0), lid=.3)
    c.cycle(0.55, 4.0, .56,
            dict(ra=(-96, 10, 26), head=(-7, 0, 6), root=(0, 0, 2)),
            dict(ra=(-58, 32, 10), head=(2, 0, -6), root=(0, 0, -2)))
    c.hold(0.6, 4.0, lid=.35)
    c.key(4.3, ra=(-110, 10, 30), head=(-10, 0, 0), lid=0)


@clip("scout_the_horizon", "Scouts the horizon", weight=4, require=["personality:adventurous"], avoid=["night"], length=5.0)
def _(c):
    c.key(0.5, ra=(-146, -50, 0), head=(-6, -6, 0), waist=(-3, 0, 0), lid=.35)
    c.key(1.45, head=(-6, 24, 0), waist=(-3, 10, 0), look=(.5, 0))
    c.key(2.6, head=(-6, -24, 0), waist=(-3, -10, 0), look=(-.5, 0))
    c.key(3.3, ra=(-92, 24, 0), la=(-10, 0, 6), head=(-4, 22, 0), waist=(0, 8, 0), look=(.4, 0), lid=0)
    c.key(4.1, ra=(-90, 26, 0), head=(-4, 22, 0))


@clip("inspect_a_trinket", "Inspects a trinket", weight=4, require=["personality:meticulous"], length=4.8)
def _(c):
    c.key(0.5, ra=(-96, -30, 0), head=(16, -8, 0), waist=(4, 0, 0), look=(-.2, .4))
    c.key(1.2, ra=(-100, -36, 6), head=(14, -14, 7))
    c.key(1.9, ra=(-94, -26, -4), la=(-90, -36, 0), head=(18, -6, -6))
    c.cycle(2.5, 3.5, .34, dict(la=(-90, -36, 0)), dict(la=(-84, -26, 0)))
    c.key(4.0, ra=(-58, -50, 0), la=(-8, 0, 4), head=(4, 0, 0), lid=.35, look=(0, 0))


@clip("tend_the_soil", "Tends the soil", weight=4, require=["personality:steadfast|job:farmer"], avoid=["night"], length=5.6)
def _(c):
    c.key(0.7, waist=(46, 0, 0), head=(10, 0, 0), ra=(-62, -8, 0), la=(-62, -8, 0), look=(0, .6))
    c.cycle(1.0, 3.3, .5, dict(ra=(-72, -8, 0)), dict(ra=(-56, -8, 0)))
    c.key(1.0, la=(-64, -10, 0)).key(3.3, la=(-64, -10, 0))
    c.key(3.8, waist=(4, 0, 0), head=(0, 0, 0), ra=(-30, 0, 8), la=(-30, 0, 8), look=(0, .2))
    c.cycle(4.15, 4.95, .26, dict(ra=(-50, -36, 0), la=(-50, -36, 0)), dict(ra=(-44, -22, 0), la=(-44, -22, 0)))


@clip("cast_a_line", "Casts a fishing line", weight=4, require=["personality:reserved|job:fisherman"], length=5.2)
def _(c):
    c.key(0.4, ra=(-88, -10, 0), la=(-78, -20, 0))
    c.key(0.95, ra=(-168, -6, 0), la=(-148, -16, 0), waist=(-8, 4, 0), head=(-6, 0, 0))
    c.key(1.18, ra=(-70, -6, 0), la=(-62, -16, 0), waist=(10, -4, 0), head=(4, 0, 0))
    c.key(1.6, ra=(-80, -8, 0), la=(-72, -18, 0), waist=(3, 0, 0), head=(2, 0, 0), look=(0, .3))
    c.key(2.9, ra=(-80, -8, 0), la=(-72, -18, 0))
    c.key(3.1, ra=(-98, -8, 0), la=(-90, -18, 0), head=(-2, 0, 0))
    c.key(3.35, ra=(-82, -8, 0), la=(-74, -18, 0))
    c.key(4.1, ra=(-60, -8, 0), la=(-52, -16, 0), head=(4, 8, 6), look=(.2, .2))


@clip("frame_the_view", "Frames the view", weight=4, require=["personality:imaginative|job:painter"], length=5.4)
def _(c):
    c.key(0.5, ra=(-102, -22, 0), la=(-102, -22, 0), head=(-4, 0, -8), lid=.2)
    c.key(1.3, waist=(-6, 0, 0), root=(-2, 0, 0), head=(-4, 0, 8))
    c.key(2.0, ra=(-90, 0, 6), la=(-30, 0, 8), waist=(0, 0, 0), root=(0, 0, 0), head=(4, 8, 0), look=(.3, .1), lid=0)
    c.cycle(2.2, 4.2, .6, dict(ra=(-98, 6, 4)), dict(ra=(-70, 24, 18)))
    c.key(4.7, ra=(-22, 0, 6), la=(-10, 0, 4), head=(-2, 0, 4), look=(0, 0))


@clip("whittle", "Whittles wood", weight=4, require=["personality:pragmatic|job:carpenter|job:fletcher"], length=5.0)
def _(c):
    c.key(0.45, la=(-52, -24, 0), ra=(-50, -34, 0), head=(26, 0, 0), waist=(6, 0, 0), look=(0, .8))
    c.cycle(0.65, 3.65, .45, dict(ra=(-57, -42, 0)), dict(ra=(-40, -12, 0)))
    c.key(4.0, la=(-82, -30, 0), ra=(-30, -10, 0), head=(10, 0, 0), lid=.45, look=(0, .3))


@clip("stargaze", "Stargazes", weight=4, require=["personality:curious"], avoid=["rain"], boost={"night": 6, "evening": 3}, length=6.6)
def _(c):
    c.key(0.8, head=(-46, 0, 0), waist=(-10, 0, 0), look=(0, -.9), **HANDS_BEHIND)
    c.key(1.8, head=(-48, 6, 0), la=(24, 0, -9))
    c.key(2.1, ra=(-160, 14, 0), head=(-48, 10, 0), look=(.3, -.9))
    c.key(3.2, ra=(-150, 26, 0))
    c.key(3.8, ra=(-166, 4, 0), head=(-50, 2, 0))
    c.key(4.4, ra=(-152, -10, 0), head=(-46, -8, 0), look=(-.3, -.9))
    c.key(5.3, ra=(24, 0, -9), head=(-40, -6, 0))


@clip("sand_a_plank", "Sands a plank", weight=4, require=["personality:protective|job:carpenter"], length=4.4)
def _(c):
    c.key(0.4, ra=(-40, -10, 0), la=(-30, -6, 0), waist=(16, 0, 0), head=(18, 0, 0), look=(0, .6))
    c.cycle(0.6, 3.4, .5, dict(ra=(-54, -10, 0), waist=(18, 0, 0)), dict(ra=(-30, -10, 0), waist=(14, 0, 0)))
    c.key(3.8, waist=(12, 0, 0), head=(10, 0, 0), lid=.45, la=(-44, -12, 0))


@clip("smell_a_flower", "Smells a flower", weight=4, require=["personality:gentle|job:apothecary"], avoid=["night"], length=4.8)
def _(c):
    c.key(0.55, waist=(28, 0, 0), ra=(-52, -24, 0), la=(-52, -24, 0), head=(12, 0, 0), look=(0, .6))
    c.key(1.45, waist=(10, 0, 0), ra=(-106, -30, 0), la=(-106, -30, 0), head=(6, 0, 0), lid=.9, look=(0, .3))
    c.key(2.6, waist=(-6, 0, 0), head=(-10, 0, 0), root_pos=(0, -.4, 0), lid=.9)
    c.key(3.2, ra=(-60, -34, 0), la=(-60, -34, 0), root=(0, 0, 3), head=(-2, 0, -8), root_pos=(0, 0, 0), lid=.5)
    c.key(3.8, root=(0, 0, -2), head=(-2, 0, 6))
