"""Pets: residents playing with their cats and dogs, and befriending strays.

Every clip here has the "pet" trigger and plays one part of a game the server is running
(PetPlays.java): the resident's part is tagged play:<phase>, and the pet's part is a trick in
tools/pets/tricks.py. Clip lengths match the script's steps; looping parts (watching a dog run,
rubbing a belly) repeat while the step lasts. Clips that use something in the hand (a stick, a
treat, a bit of string) never mirror, because residents always hold things in the right hand.
"""
from kit import clip

AGE = "adult|child"
SQUAT = dict(rl=(-62, 0, 10), ll=(-62, 0, 10), root_pos=(0, 6, 0), waist=(30, 0, 0))
KNEEL = dict(rl=(-58, 0, 0), ll=(58, 0, 0), root_pos=(0, 5.6, 0))
HANDS_ON_KNEES = dict(ra=(-30, -8, 4), la=(-30, -8, 4), waist=(24, 0, 0), rl=(-16, 0, 2), ll=(-16, 0, 2), root_pos=(0, 1.2, 0))


def pet(phase, name, length, species=None, **options):
    require = [AGE, f"play:{phase}"] + ([f"pet:{species}"] if species else [])
    return clip(f"pet_{phase}", name, trigger="pet", length=length, require=require, items="override", **options)


# -- befriending a stray -----------------------------------------------------------------------

@pet("coax", "Coaxes a stray with a treat", 3.5, mirror="never", blend=(.4, .35))
def _(c):
    c.key(0.6, **SQUAT, ra=(-40, -4, 0), la=(-18, 0, 10), head=(22, 0, 0), look=(0, .8))
    c.key(1.1, ra=(-50, -4, 0), head=(24, 0, 4))
    c.wobble(1.2, 2.2, 3, "ra", 3, base=(-50, -4, 0), axis=1)
    c.key(2.6, **{**SQUAT, "waist": (36, 0, 0)}, ra=(-54, -4, 0), head=(26, 0, -4), lid=.15)
    c.key(3.2, ra=(-52, -4, 0), head=(24, 0, 0), lid=0)


@pet("tamed", "Takes the stray home", 2.2, mirror="never", blend=(.2, .35))
def _(c):
    c.key(0.25, **SQUAT, ra=(-30, 0, 10), la=(-30, 0, 10), head=(20, 0, 0))
    c.key(0.75, rl=(0, 0, 0), ll=(0, 0, 0), root_pos=(0, -1.6, 0), waist=(-4, 0, 0), ra=(-20, 0, 150), la=(-20, 0, 150), head=(-12, 0, 0), lid=.5)
    c.key(1.0, root_pos=(0, 0, 0))
    c.key(1.25, root_pos=(0, -1.4, 0), ra=(-20, 0, 158), la=(-20, 0, 142))
    c.key(1.5, root_pos=(0, 0, 0), ra=(-52, -46, 0), la=(-52, -46, 0), head=(10, 0, 10), lid=.8)
    c.key(1.9, ra=(-50, -44, 0), la=(-50, -44, 0), head=(10, 0, -8), lid=.7)


@pet("coax_fail", "Sighs as the stray backs away", 1.7, blend=(.2, .35))
def _(c):
    c.key(0.35, ra=(-20, 18, 28), la=(-20, 18, 28), head=(6, 0, 0), waist=(4, 0, 0))
    c.key(0.75, ra=(-24, 22, 34), la=(-24, 22, 34), head=(10, 12, 0), lid=.4)
    c.key(1.1, head=(14, -10, 0), lid=.5)
    c.key(1.4, ra=(-6, 0, 8), la=(-6, 0, 8), head=(12, 0, 0), lid=.2)


# -- shared moments ----------------------------------------------------------------------------

@pet("call", "Pats their knees: come here!", 1.2, blend=(.15, .25))
def _(c):
    c.key(0.2, waist=(16, 0, 0), head=(14, 0, 0), ra=(-20, -6, 6), la=(-20, -6, 6), rl=(-10, 0, 0), ll=(-10, 0, 0), root_pos=(0, .8, 0))
    c.cycle(0.3, 1.0, .3, dict(ra=(-32, -6, 6), la=(-32, -6, 6)), dict(ra=(-14, -6, 6), la=(-14, -6, 6)))


@pet("clap", "Claps for the pet", 1.5, blend=(.15, .3))
def _(c):
    c.key(0.15, ra=(-62, -34, 0), la=(-62, -34, 0), head=(12, 0, 0), lid=.3)
    c.cycle(0.25, 1.2, .24, dict(ra=(-64, -48, 0), la=(-64, -48, 0)), dict(ra=(-62, -26, 0), la=(-62, -26, 0)))


@pet("giggle", "Laughs, hands on knees", 2.0, blend=(.2, .35))
def _(c):
    c.key(0.3, **HANDS_ON_KNEES, head=(-6, 0, 0), lid=.6)
    c.wobble(0.35, 1.6, 7, "root_pos", .4, base=(0, 1.2, 0), axis=1, decay=.4)
    c.key(1.7, **HANDS_ON_KNEES, head=(4, 0, 0), lid=.3)


@pet("watch_fond", "Watches the cat fondly", 3.0, blend=(.35, .35))
def _(c):
    clasp = dict(ra=(-38, -32, 0), la=(-38, -32, 0), waist=(8, 0, 0))
    c.key(0.5, **clasp, head=(28, 0, 8), look=(0, .8), lid=.2)
    c.key(1.5, **clasp, head=(30, 10, -6), look=(.3, .8), lid=.25)
    c.key(2.5, **clasp, head=(28, -8, 8), look=(-.3, .8), lid=.2)


# -- dogs --------------------------------------------------------------------------------------

@pet("fetch_ready", "Teases with a stick", 1.2, species="dog", mirror="never", blend=(.2, .2))
def _(c):
    c.key(0.3, ra=(-150, 6, 10), la=(-10, 0, 10), head=(16, 0, 0), look=(0, .6), waist=(-4, 0, 0))
    c.wobble(0.35, 1.0, 5, "ra", 10, base=(-150, 6, 10), axis=2)


@pet("throw", "Throws the stick", .7, species="dog", mirror="never", blend=(.08, .15))
def _(c):
    c.key(0.25, ra=(-196, 10, 14), la=(-30, 0, 18), waist=(-8, -18, 0), head=(-6, -6, 0))
    c.key(0.5, ra=(-110, 4, 8), la=(-10, 0, 20), waist=(12, 16, 0), head=(-4, 8, 0), root_pos=(0, .4, -.6))
    c.key(0.62, ra=(-80, 0, 6), waist=(14, 18, 0))


@pet("watch", "Watches the dog run", 2.4, species="dog", blend=(.3, .3))
def _(c):
    c.key(0.4, **HANDS_ON_KNEES, head=(-12, 0, 0), look=(0, -.2))
    c.key(1.0, **{**HANDS_ON_KNEES, "root_pos": (0, .8, 0)}, head=(-14, 6, 0))
    c.key(1.3, root_pos=(0, 1.6, 0))
    c.key(1.6, root_pos=(0, .8, 0))
    c.key(2.1, **HANDS_ON_KNEES, head=(-12, -4, 0))


@pet("receive", "Takes the stick back", 1.8, species="dog", mirror="never", blend=(.25, .35))
def _(c):
    c.key(0.45, **SQUAT, ra=(-30, -4, 4), la=(-20, 0, 10), head=(24, 0, 0), look=(0, .8))
    c.key(0.75, ra=(-52, -10, 0), head=(26, 0, 0))
    c.key(1.05, ra=(-74, -6, 4), head=(18, 0, 0))
    c.key(1.35, la=(-50, -14, 0), ra=(-64, -6, 4), head=(22, 0, 6), lid=.3)
    c.key(1.55, la=(-36, -14, 0))


@pet("pat_dog", "Pats the dog's head", 2.0, species="dog", blend=(.25, .35))
def _(c):
    c.key(0.45, **SQUAT, ra=(-40, -8, 0), la=(-18, 0, 10), head=(24, 0, 0), look=(0, .8))
    for t in (0.6, 0.95, 1.3):
        c.key(t, ra=(-56, -8, 0)).key(t + .18, ra=(-38, -8, 0), head=(24, 0, 6), lid=.3)
    c.key(1.75, **SQUAT, ra=(-30, -6, 4), head=(20, 0, 8), lid=.2)


@pet("belly_rub", "Rubs the dog's belly", 3.0, species="dog", blend=(.4, .4))
def _(c):
    low = dict(**KNEEL, waist=(36, 0, 0), head=(26, 0, 0), look=(0, .8), lid=.15)
    c.key(0.4, **low, ra=(-50, -14, 0), la=(-44, -14, 0))
    c.key(0.75, **low, ra=(-42, -2, 0), la=(-52, -24, 0))
    c.key(1.1, **low, ra=(-58, -24, 0), la=(-42, -2, 0))
    c.key(1.45, **{**low, "head": (28, 8, 6)}, ra=(-50, -14, 0), la=(-44, -14, 0))
    c.key(1.8, **low, ra=(-42, -2, 0), la=(-52, -24, 0))
    c.key(2.15, **low, ra=(-58, -24, 0), la=(-42, -2, 0))
    c.key(2.6, **low, ra=(-50, -14, 0), la=(-44, -14, 0))


@pet("treat_show", "Holds up a treat: sit!", 2.8, species="dog", mirror="never", blend=(.3, .3))
def _(c):
    c.key(0.4, ra=(-160, 4, 8), la=(-12, 0, 8), head=(16, 0, 0), look=(0, .7))
    c.key(0.8, la=(-74, -22, 0))
    c.wobble(0.9, 2.2, 3, "la", 12, base=(-74, -22, 0), axis=1)
    c.key(2.5, ra=(-162, 4, 8), la=(-24, -6, 6), head=(16, 0, 6))


@pet("treat_toss", "Tosses the treat", .6, species="dog", mirror="never", blend=(.05, .2))
def _(c):
    c.key(0.1, ra=(-160, 4, 8), head=(16, 0, 0))
    c.key(0.26, ra=(-104, 0, 6), head=(10, 0, 0))
    c.key(0.42, ra=(-150, 0, 6), head=(-8, 0, 0), look=(0, -.4))


@pet("shake_paw", "Shakes the dog's paw", 3.0, species="dog", blend=(.35, .35))
def _(c):
    c.key(0.5, **SQUAT, ra=(-58, -10, 0), la=(-18, 0, 10), head=(22, 0, 0), look=(0, .7))
    c.key(1.0, ra=(-62, -12, 0), head=(22, 0, 8), lid=.2)
    c.cycle(1.1, 2.3, .3, dict(ra=(-68, -12, 0)), dict(ra=(-54, -12, 0)))
    c.key(2.6, **SQUAT, ra=(-40, -6, 0), head=(18, 0, -6), lid=.3)


@pet("spin_cue", "Twirls a finger: spin!", 3.0, species="dog", blend=(.3, .35))
def _(c):
    c.key(0.35, ra=(-100, -6, 10), la=(14, 0, 26), head=(14, 0, 0), look=(0, .6))
    for i, t in enumerate((0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25)):
        c.key(t, ra=(-100 + (8 if i % 2 else -8), -6 + (12 if i % 4 < 2 else -12), 10))
    c.key(2.6, ra=(-96, -6, 10), la=(14, 0, 26), head=(10, 0, 0))


@pet("tag", "Tags the dog: you're it!", 1.0, species="dog", blend=(.1, .2))
def _(c):
    c.key(0.3, waist=(24, 0, 0), ra=(-52, -6, 0), head=(18, 0, 0))
    c.key(0.5, ra=(-34, -6, 0))
    c.key(0.8, waist=(0, 0, 0), root=(0, -26, 0), ra=(10, 0, 14), la=(-30, 0, 14), head=(-4, 22, 0), lid=.4)


# -- cats --------------------------------------------------------------------------------------

@pet("dangle", "Dangles a bit of string", 3.0, species="cat", mirror="never", blend=(.35, .35))
def _(c):
    bend = dict(waist=(26, 0, 0), head=(30, 0, 0), look=(0, .9), la=(14, 0, 18))
    c.key(0.35, **bend, ra=(-62, -6, 0))
    for i, t in enumerate((0.55, 0.75, 0.95, 1.15, 1.35, 1.55, 1.75, 1.95, 2.15, 2.35, 2.55)):
        c.key(t, **bend, ra=(-62 + (6 if i % 2 else -4), -6 + (8 if i % 3 == 0 else -6 if i % 3 == 1 else 0), 0))
    c.key(2.7, **bend, ra=(-62, -6, 0))


@pet("stroke", "Strokes the cat", 3.5, species="cat", blend=(.45, .4))
def _(c):
    low = dict(**KNEEL, waist=(34, 0, 0), la=(-14, 0, 12), look=(0, .8))
    c.key(0.45, **low, ra=(-62, -6, 0), head=(26, 0, 0), lid=.3)
    c.key(1.4, **low, ra=(-30, -4, 0), head=(26, 0, 6), lid=.45)
    c.key(1.85, **low, ra=(-62, -6, 0), head=(26, 0, 0), lid=.3)
    c.key(2.8, **low, ra=(-30, -4, 0), head=(26, 0, -6), lid=.45)
    c.key(3.15, **low, ra=(-50, -6, 0), head=(26, 0, 0), lid=.3)


@pet("chin_scratch", "Scratches the cat's chin", 2.5, species="cat", blend=(.35, .35))
def _(c):
    low = dict(**SQUAT, la=(-16, 0, 10), look=(0, .8))
    c.key(0.4, **low, ra=(-46, -10, 0), head=(24, 0, 8), lid=.3)
    c.wobble(0.45, 2.1, 8, "ra", 3, base=(-46, -10, 0), axis=0)
    c.key(2.2, **low, ra=(-46, -10, 0), head=(24, 0, 8), lid=.3)


@pet("wave_toy", "Swishes a feather for the cat", 2.8, species="cat", mirror="never", blend=(.3, .35))
def _(c):
    bend = dict(waist=(24, 0, 0), la=(14, 0, 18), look=(0, .8))
    c.key(0.35, **bend, ra=(-58, 26, 0), head=(26, 14, 0))
    c.key(0.95, **bend, ra=(-50, -30, 0), head=(26, -14, 0))
    c.key(1.55, **bend, ra=(-58, 26, 0), head=(26, 14, 0))
    c.key(2.15, **bend, ra=(-50, -30, 0), head=(26, -14, 0))
    c.key(2.5, **bend, ra=(-54, 0, 0), head=(26, 0, 0))


@pet("treat_offer", "Offers the cat a fish", 2.4, species="cat", mirror="never", blend=(.3, .35))
def _(c):
    c.key(0.5, **SQUAT, ra=(-44, -6, 0), la=(-16, 0, 10), head=(24, 0, 0), look=(0, .8))
    c.wobble(0.7, 2.0, 2, "ra", 2, base=(-44, -6, 0), axis=0)
    c.key(2.2, **SQUAT, ra=(-42, -6, 0), head=(24, 0, 6), lid=.2)


@pet("pat_cat", "Pats the cat gently", 1.8, species="cat", blend=(.25, .35))
def _(c):
    c.key(0.4, **SQUAT, ra=(-38, -8, 0), la=(-16, 0, 10), head=(24, 0, 0), look=(0, .8))
    for t in (0.55, 0.95):
        c.key(t, ra=(-46, -8, 0)).key(t + .22, ra=(-34, -8, 0), head=(24, 0, 8), lid=.4)
    c.key(1.55, **SQUAT, ra=(-30, -6, 4), head=(22, 0, 6), lid=.3)
