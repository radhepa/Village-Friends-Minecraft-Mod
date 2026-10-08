"""Skies: rain, thunder, cold, dawn and dusk change what residents do."""
from kit import clip

HANDS_ON_HEAD = dict(ra=(-164, 0, 14), la=(-164, 0, 14))
HANDS_ON_EARS = dict(ra=(-160, -10, 20), la=(-160, -10, 20))
SELF_HUG = dict(ra=(-78, -64, 0), la=(-72, -60, 0))


@clip("shelter_head_from_rain", "Shelters head from the rain", weight=3, require=["rain"], mirror="never", length=3.8)
def _(c):
    c.key(0.35, ra=(-120, 0, 30), la=(-120, 0, 30), head=(6, 0, 0))
    c.key(0.65, **HANDS_ON_HEAD, head=(16, 0, 0), waist=(10, 0, 0), lid=.5, look=(0, -.4))
    c.cycle(0.8, 2.4, .36, dict(rl=(-10, 0, 2), root_pos=(0, .4, 0)), dict(rl=(0, 0, 2), ll=(-10, 0, 2), root_pos=(0, 0, 0)))
    c.key(2.5, head=(-6, 10, 0), look=(.3, -.8), lid=.3, rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(2.9, head=(14, 0, 0), look=(0, 0), lid=.5)
    c.key(3.2, **HANDS_ON_HEAD, waist=(8, 0, 0))


@clip("wring_out_sleeve", "Wrings out a sleeve", weight=2, require=["rain"], length=4.4)
def _(c):
    c.key(0.5, la=(-84, 6, 0), ra=(-66, -52, 0), head=(20, -12, 0), look=(-.3, .6))
    for t in (0.9, 2.0):
        c.key(t, ra=(-66, -54, 0), lid=.2)
        c.wobble(t, t + .45, 8, "ra", 6, base=(-72, -46, 0), axis=1)
        c.key(t + .8, ra=(-88, -26, 0), la=(-84, 6, 0), head=(20, -16, 0), lid=.45)
    c.key(3.0, ra=(-24, 0, 6))
    c.wobble(3.1, 3.7, 8, "la", 12, base=(-40, 0, 8), axis=0, decay=.4)
    c.key(3.9, head=(4, 0, 0), look=(0, 0), lid=0)


@clip("splash_a_puddle", "Splashes in a puddle", weight=2, require=["rain"], mirror="free",
      boost={"personality:playful": 3, "child": 4}, length=3.6)
def _(c):
    c.key(0.4, rl=(-46, 0, 0), ra=(-24, 0, 30), la=(-20, 0, 34), head=(22, 0, 0), look=(0, .8), waist=(6, 0, 0))
    c.key(0.6, rl=(4, 0, 0), root_pos=(0, .8, 0))
    c.key(0.8, ll=(-46, 0, 0), rl=(0, 0, 0), root_pos=(0, 0, 0))
    c.key(1.0, ll=(4, 0, 0), root_pos=(0, .8, 0))
    c.key(1.35, ll=(0, 0, 0), root_pos=(0, 1.8, 0), ra=(-10, 0, 12), la=(-10, 0, 12), head=(14, 0, 0))
    c.key(1.6, root_pos=(0, -4.5, 0), rl=(-18, 0, 4), ll=(-18, 0, 4), ra=(-40, 0, 70), la=(-40, 0, 70), head=(-10, 0, 0))
    c.key(1.85, root_pos=(0, 1.2, 0), rl=(0, 0, 4), ll=(0, 0, 4), ra=(-20, 0, 40), la=(-20, 0, 40))
    c.key(2.1, root_pos=(0, 0, 0), head=(6, 0, 0), lid=.6, look=(0, 0))
    c.wobble(2.2, 3.0, 6, "head", 6, base=(6, 0, 0), axis=2)
    c.key(3.1, lid=0, waist=(0, 0, 0))


@clip("glum_at_the_clouds", "Looks glumly up at the clouds", weight=2, require=["rain"], mirror="free", length=5.0)
def _(c):
    c.key(0.8, head=(-34, 6, 0), waist=(-4, 0, 0), look=(.1, -.9), lid=.35)
    c.key(2.0, head=(-32, -6, 4), look=(-.2, -.9))
    c.key(2.5, head=(-34, -4, 4), ra=(-18, 0, 22), la=(-18, 0, 22), root_pos=(0, -.4, 0))
    c.key(3.0, head=(14, 0, 6), waist=(6, 0, 0), ra=(4, 0, 2), la=(4, 0, 2), root_pos=(0, .6, 0), lid=.6, look=(0, .4))
    c.wobble(3.1, 4.0, 2, "head", 8, base=(14, 0, 6), axis=1)
    c.key(4.4, lid=.3, look=(0, 0))


@clip("thunderclap_jump", "Jumps at a thunderclap", weight=3, require=["thunder"], mirror="never", length=3.2, blend=(.08, .35))
def _(c):
    c.key(0.1, **HANDS_ON_HEAD, root_pos=(0, -3.5, 0), head=(-8, 0, 0), waist=(-4, 0, 0), look=(0, -.6))
    c.key(0.3, root_pos=(0, 2.5, 0), rl=(-20, 0, 4), ll=(-20, 0, 4), head=(18, 0, 0), waist=(14, 0, 0), lid=.9)
    c.wobble(0.4, 1.4, 8, "root", 2, base=(0, 0, 0), axis=2, decay=.6)
    c.key(1.4, **HANDS_ON_HEAD, root_pos=(0, 2.5, 0), head=(18, 0, 0), waist=(14, 0, 0), lid=.9)
    c.key(1.9, head=(-10, 14, 0), look=(.5, -.7), lid=0)
    c.key(2.3, head=(-8, -14, 0), look=(-.5, -.6), waist=(6, 0, 0), root_pos=(0, 1, 0))
    c.key(2.7, **HANDS_ON_HEAD, rl=(0, 0, 0), ll=(0, 0, 0))


@clip("cover_ears_from_thunder", "Covers ears in the thunder", weight=2, require=["thunder"], mirror="never", length=4.4)
def _(c):
    c.key(0.35, **HANDS_ON_EARS, head=(14, 0, 0), waist=(8, 0, 0), lid=1, root_pos=(0, .6, 0))
    c.wobble(0.5, 1.6, 9, "head", 4, base=(14, 0, 0), axis=1, decay=.5)
    c.key(2.0, **HANDS_ON_EARS, head=(10, 0, 0), lid=.7)
    c.key(2.5, ra=(-148, -6, 30), la=(-148, -6, 30), head=(-14, 8, 0), lid=.25, look=(.3, -.8))
    c.key(2.9, **HANDS_ON_EARS, head=(14, 0, 0), waist=(10, 0, 0), lid=1)
    c.wobble(3.0, 3.6, 9, "head", 3, base=(14, 0, 0), axis=1)
    c.key(3.8, lid=.5, root_pos=(0, .6, 0))


@clip("stamp_feet_warm", "Stamps feet to keep warm", weight=3, require=["cold"], mirror="never", length=3.8)
def _(c):
    c.key(0.4, **SELF_HUG, head=(10, 0, 0), lid=.3)
    c.cycle(0.55, 3.0, .5, dict(rl=(-26, 0, 2), ll=(0, 0, 2), root=(0, 0, -3), root_pos=(0, .5, 0)),
            dict(rl=(0, 0, 2), ll=(-26, 0, 2), root=(0, 0, 3), root_pos=(0, .5, 0)))
    c.wobble(0.6, 3.0, 6, "head", 3, base=(10, 0, 0), axis=1)
    c.key(3.3, **SELF_HUG, lid=.3)


@clip("hug_self_cold", "Hugs self against the cold", weight=3, require=["cold"], mirror="never", length=4.6)
def _(c):
    c.key(0.5, **SELF_HUG, head=(16, 0, 0), waist=(6, 0, 0), root_pos=(0, .6, 0), lid=.5)
    c.cycle(0.7, 2.9, .5, dict(ra=(-70, -64, 0), la=(-80, -60, 0)), dict(ra=(-84, -64, 0), la=(-66, -60, 0)))
    c.cycle(0.7, 3.5, 1.4, dict(root=(0, 0, 4)), dict(root=(0, 0, -4)))
    c.key(3.6, **SELF_HUG, head=(12, 0, 0), lid=.35)
    c.key(4.0, head=(8, 0, 0), lid=0, root_pos=(0, 0, 0), waist=(0, 0, 0))


@clip("blow_into_cupped_hands", "Blows into cupped hands", weight=2.5, require=["cold"], mirror="never", length=5.0)
def _(c):
    cupped = dict(ra=(-108, -40, 0), la=(-108, -40, 0))
    c.key(0.4, **cupped, head=(4, 0, 0), waist=(4, 0, 0), look=(0, .5))
    for t in (0.8, 1.4, 2.0):
        c.key(t, head=(-4, 0, 0), lid=.8, root_pos=(0, -.3, 0))
        c.key(t + .3, head=(6, 0, 0), lid=.2, root_pos=(0, 0, 0))
    c.key(2.4, **cupped)
    c.key(2.8, ra=(-62, -52, 0), la=(-56, -48, 0), head=(12, 0, 0), lid=.4, look=(0, .3))
    c.wobble(3.0, 4.2, 9, "root", 1.4, axis=2)
    c.key(4.4, ra=(-62, -52, 0), la=(-56, -48, 0), head=(10, 0, 0), waist=(4, 0, 0), lid=.4)


@clip("rub_sleepy_eyes", "Rubs sleepy eyes", weight=1.2, require=["morning"], mirror="never", length=4.4)
def _(c):
    c.key(0.5, ra=(-124, -26, 0), la=(-124, -26, 0), head=(8, 0, 0), lid=1)
    c.cycle(0.6, 1.9, .34, dict(ra=(-130, -22, 0), la=(-120, -30, 0)), dict(ra=(-120, -30, 0), la=(-130, -22, 0)))
    c.key(2.2, ra=(-18, 0, 6), la=(-14, 0, 6), head=(-4, 0, 0), lid=.7)
    c.key(2.4, lid=.05).key(2.6, lid=.8).key(2.8, lid=0).key(3.0, lid=.5)
    c.wobble(3.0, 3.6, 6, "head", 10, base=(-2, 0, 0), axis=1, decay=.5)
    c.key(3.8, ra=(0, 0, 0), la=(0, 0, 0), lid=.15)


@clip("greet_the_sun", "Greets the morning sun", weight=1.3, require=["morning"], avoid=["rain"], mirror="never", length=5.0)
def _(c):
    c.key(0.6, ra=(12, 0, 18), la=(12, 0, 18), head=(6, 0, 0), waist=(2, 0, 0), lid=.2)
    c.key(1.5, ra=(-112, 36, 36), la=(-112, 36, 36), head=(-34, 0, 0), waist=(-8, 0, 0), root_pos=(0, -.8, 0),
          look=(0, -.8), lid=.85)
    c.key(2.4, ra=(-116, 38, 40), la=(-116, 38, 40), head=(-36, 0, 3))
    c.key(3.2, ra=(-112, 36, 36), la=(-112, 36, 36), head=(-34, 0, -3), root_pos=(0, -.8, 0), lid=.85)
    c.key(3.9, ra=(-30, 10, 20), la=(-30, 10, 20), head=(-6, 0, 0), waist=(0, 0, 0), root_pos=(0, 0, 0), look=(0, 0), lid=.3)
    c.key(4.4, ra=(0, 0, 4), la=(0, 0, 4), head=(2, 0, 0), lid=0)


@clip("nod_off_standing", "Nods off standing up", weight=1.2, require=["night"], mirror="never", length=6.4)
def _(c):
    c.key(0.4, lid=.4)
    c.key(1.9, head=(34, 0, 4), waist=(6, 0, 0), root=(3, 0, 0), ra=(-6, 0, 2), la=(-6, 0, 2), lid=1)
    c.key(2.1, head=(36, 0, 6), root=(4, 0, 0))
    c.key(2.3, head=(-12, 0, 0), waist=(-4, 0, 0), root=(-2, 0, 0), ra=(-24, 0, 26), la=(-24, 0, 26),
          root_pos=(0, -1.4, 0), lid=0)
    c.key(2.55, root_pos=(0, 0, 0), ra=(-4, 0, 6), la=(-4, 0, 6), root=(0, 0, 0), waist=(0, 0, 0))
    c.key(2.9, head=(-4, 18, 0), look=(.6, 0))
    c.key(3.4, head=(-4, -16, 0), look=(-.6, 0), lid=.2)
    c.key(3.8, head=(4, 0, 0), look=(0, 0), lid=.5, ra=(0, 0, 0), la=(0, 0, 0))
    c.key(5.2, head=(26, 0, -4), waist=(4, 0, 0), lid=.95)
    c.key(5.5, head=(-4, 0, 0), waist=(0, 0, 0), lid=.1)
    c.key(5.9, head=(0, 0, 0), lid=.3)


@clip("wish_on_a_star", "Wishes on a star", weight=1.3, require=["evening|night"], avoid=["rain"], mirror="never", length=5.6)
def _(c):
    c.key(0.6, head=(-34, 10, 0), waist=(-4, 0, 0), look=(.2, -.9))
    c.key(1.0, ra=(-152, 12, 0), head=(-36, 12, 0))
    c.key(1.5, ra=(-150, 14, 0))
    c.key(2.0, ra=(-96, -42, 0), la=(-96, -42, 0), head=(8, 0, 0), waist=(2, 0, 0), look=(0, .3), lid=1)
    c.key(3.0, root_pos=(0, -.6, 0), head=(10, 0, 0))
    c.key(3.6, ra=(-98, -42, 0), la=(-98, -42, 0), root_pos=(0, 0, 0), head=(8, 0, 0), lid=1)
    c.key(4.1, head=(-28, 6, 0), look=(.1, -.8), lid=.15)
    c.key(4.6, ra=(-60, -48, 0), la=(-60, -48, 0), head=(-20, 4, 0))
    c.key(5.1, head=(-4, 0, 0), waist=(0, 0, 0), look=(0, 0), lid=0)


@clip("watch_fireflies", "Watches the fireflies", weight=1.4, require=["evening|night"], avoid=["rain", "cold"], mirror="free",
      length=6.6)
def _(c):
    c.key(0.6, head=(-8, 22, 0), look=(.6, -.2))
    c.key(1.4, head=(-16, 6, 0), look=(.2, -.5))
    c.key(2.1, head=(2, -14, 0), look=(-.5, .2))
    c.key(2.8, head=(-4, -6, 0), look=(-.2, -.1), ra=(-58, -8, 0))
    c.key(3.4, ra=(-76, -20, 0), la=(-56, -30, 0), head=(6, -4, 0), look=(-.1, .3))
    c.key(3.9, ra=(-64, -38, 0), la=(-64, -38, 0), head=(20, 0, 0), look=(0, .7), lid=.15)
    c.key(4.5, ra=(-66, -38, 0), la=(-66, -38, 0), head=(22, 0, 0))
    c.key(4.9, ra=(-92, 10, 20), la=(-92, 10, 20), head=(-24, 0, 0), look=(0, -.8), lid=.35)
    c.key(5.6, ra=(-30, 4, 8), la=(-30, 4, 8), head=(-30, 8, 0), look=(.2, -.9))
    c.key(6.1, look=(0, 0), lid=0)
