"""Reactions: jokes, gifts, trades, hearts, anger, fear and getting hurt."""
from kit import clip, ARMS_CROSSED, HANDS_BEHIND, HAND_TO_CHEST, HAND_TO_MOUTH, PALMS_OUT


@clip("belly_laugh", "Belly laugh", trigger="laugh", weight=3, mirror="free", length=2.9)
def _(c):
    c.key(0.25, waist=(-10, 0, 0), head=(-16, 0, 0), la=(-36, -30, 0), ra=(-20, 0, 16), lid=.7)
    c.wobble(0.3, 1.9, 7, "root_pos", .4, axis=1, decay=.5)
    c.key(1.15, waist=(14, 0, 0), head=(10, 0, 0), ra=(-34, -12, 4))
    c.key(1.35, ra=(-20, -8, 4))
    c.key(2.0, waist=(-2, 0, 0), head=(-2, 0, 0), ra=(-10, 0, 6), la=(-20, -20, 0), lid=.4)


@clip("giggle", "Giggles", trigger="laugh", weight=2, length=2.1)
def _(c):
    c.key(0.3, **HAND_TO_MOUTH, head=(6, 0, 10), lid=.6)
    c.wobble(0.35, 1.5, 6, "ra_pos", .4, axis=1)
    c.wobble(0.35, 1.5, 6, "la_pos", .4, axis=1)
    c.key(1.55, ra=(-110, -40, 0), head=(4, 0, 8))


@clip("cheer", "Cheers", trigger="delighted", weight=3, mirror="never", length=2.5, also={"cheer_happy": "happy"})
def _(c):
    c.key(0.25, ra=(-10, 0, 40), la=(-10, 0, 40), root_pos=(0, .5, 0), waist=(6, 0, 0))
    c.key(0.5, ra=(-20, 0, 160), la=(-20, 0, 160), root_pos=(0, -2.4, 0), waist=(-4, 0, 0), head=(-14, 0, 0), lid=.55)
    c.key(0.75, root_pos=(0, 0, 0))
    c.key(0.97, ra=(-20, 0, 150), la=(-20, 0, 166), root_pos=(0, -1.8, 0))
    c.key(1.22, root_pos=(0, 0, 0))
    c.key(1.6, ra=(-20, 0, 140), la=(-20, 0, 140), head=(-8, 0, 0))


@clip("hug_the_gift", "Hugs the gift", trigger="delighted", weight=2, mirror="free", length=2.7)
def _(c):
    c.key(0.4, ra=(-52, -46, 0), la=(-52, -46, 0), head=(8, 0, 10), lid=.8)
    c.key(1.0, root=(0, 0, 4))
    c.key(1.6, root=(0, 0, -4), head=(8, 0, -8))
    c.key(2.1, root=(0, 0, 2), ra=(-50, -44, 0), la=(-50, -44, 0), lid=.5)


@clip("bashful_thanks", "Bashful thanks", trigger="thanks", weight=3, mirror="free", length=3.1, also={"lovestruck_sway": "love"})
def _(c):
    c.key(0.4, **HANDS_BEHIND, head=(16, 0, -10), waist=(0, 0, 4), look=(-.5, .5), lid=.3)
    c.cycle(0.6, 2.4, .9, dict(root=(0, 0, 3), rl=(0, 14, 0)), dict(root=(0, 0, -3), rl=(0, -4, 0)))
    c.key(2.5, **HANDS_BEHIND, head=(10, 0, -6), look=(0, .2))


@clip("grateful_nod", "Grateful nod", trigger="thanks", weight=3, length=2.3)
def _(c):
    c.key(0.4, **HAND_TO_CHEST)
    c.key(0.7, head=(18, 0, 0), waist=(10, 0, 0), lid=.5)
    c.key(1.5, head=(0, 0, 0), waist=(0, 0, 0), lid=.2)


@clip("shake_head", "Shakes head", trigger="decline", weight=3, mirror="free", length=1.9)
def _(c):
    c.key(0.35, **PALMS_OUT, lid=.3)
    c.cycle(0.35, 1.4, .3, dict(head=(4, 24, 0)), dict(head=(4, -24, 0)))
    c.key(1.45, head=(2, 0, 0), lid=0)


@clip("wag_a_finger", "Wags a finger", trigger="decline", weight=1.5, length=2.0)
def _(c):
    c.key(0.4, ra=(-100, 0, 0), head=(4, 0, 0), lid=.3)
    c.wobble(0.5, 1.5, 4, "ra", 12, base=(-100, 0, 0), axis=1)
    c.wobble(0.5, 1.5, 2, "head", 6, base=(4, 0, 0), axis=1)


@clip("clap", "Claps", trigger="happy", weight=3, mirror="never", length=2.3)
def _(c):
    c.key(0.25, ra=(-62, -10, 8), la=(-62, -10, 8), head=(-6, 0, 0), lid=.5)
    c.cycle(0.3, 1.8, .3, dict(ra=(-64, -36, 0), la=(-64, -36, 0), root_pos=(0, -.3, 0)),
            dict(ra=(-60, -10, 8), la=(-60, -10, 8), root_pos=(0, 0, 0)))


@clip("fist_pump", "Fist pump", trigger="happy", weight=2, length=1.9)
def _(c):
    c.key(0.3, ra=(-60, 0, 20), root_pos=(0, .3, 0))
    c.key(0.55, ra=(-170, 0, 10), root_pos=(0, -1.6, 0), head=(-10, 0, 0), lid=.5)
    c.key(0.75, ra=(-128, 0, 10), root_pos=(0, 0, 0))
    c.key(0.95, ra=(-170, 0, 10))
    c.key(1.25, ra=(-60, 0, 14), head=(-2, 0, 0), lid=.2)


@clip("lovestruck", "Lovestruck", trigger="love", weight=3, mirror="free", length=3.1)
def _(c):
    c.key(0.4, ra=(-56, -42, 0), la=(-56, -42, 0), head=(-6, 0, 12), lid=.6)
    c.key(1.0, root=(0, 0, 4), root_pos=(0, -.6, 0))
    c.key(1.7, root=(0, 0, -4), root_pos=(0, 0, 0), head=(-6, 0, -10))
    c.key(2.3, root=(0, 0, 2), head=(-4, 0, 8))


@clip("huff", "Huffs", trigger="angry", weight=3, length=2.7, blend=(.12, .4))
def _(c):
    c.key(0.25, **ARMS_CROSSED)
    c.key(0.4, head=(-8, -40, 0), lid=.45, look=(-.4, 0))
    c.key(0.85, rl=(-24, 0, 0))
    c.key(1.0, rl=(4, 0, 0), root_pos=(0, .3, 0))
    c.key(1.15, rl=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(2.0, **ARMS_CROSSED, head=(-6, -36, 0))


@clip("shake_a_fist", "Shakes a fist", trigger="angry", weight=2, length=2.2, blend=(.12, .4))
def _(c):
    c.key(0.3, ra=(-130, 0, 10), waist=(-4, 0, 0), head=(-6, 0, 0), lid=.4)
    c.wobble(0.35, 1.5, 6, "ra", 12, base=(-130, 0, 10), axis=0)


@clip("nervous_glances", "Nervous glances", trigger="nervous", weight=3, length=3.1)
def _(c):
    c.key(0.3, ra=(-34, -38, 0), la=(-34, -38, 0), ra_pos=(0, -.8, 0), la_pos=(0, -.8, 0))
    for t, yaw in ((0.4, 34), (0.9, -34), (1.35, 20), (1.95, -30), (2.4, 0)):
        c.key(t, head=(2, yaw, 0), look=(yaw / 45, 0))
    c.wobble(0.4, 2.4, 9, "root", 1, axis=2)


@clip("flinch", "Flinches", trigger="hurt", weight=3, mirror="free", length=1.0, blend=(.04, .3))
def _(c):
    c.key(0.09, waist=(-12, 0, 0), ra=(-100, -34, 0), la=(-90, -30, 0), head=(10, 0, 0), root_pos=(0, 0, .8), lid=1)
    c.key(0.45, waist=(-10, 0, 0), ra=(-96, -34, 0), la=(-88, -30, 0), lid=.8)


@clip("stagger", "Staggers", trigger="hurt", weight=2, mirror="free", length=1.2, blend=(.04, .35))
def _(c):
    c.key(0.1, root=(-6, 0, 4), waist=(-8, 0, 6), ra=(-40, 0, 40), la=(-30, 0, 50), lid=.8)
    c.key(0.5, root=(2, 0, -2), waist=(2, 0, -2), ra=(-20, 0, 20), la=(-16, 0, 24), lid=.3)
