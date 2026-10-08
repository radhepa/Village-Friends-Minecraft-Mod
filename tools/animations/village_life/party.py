"""Party: friends and family gather by the bell in the evening for a resident's birthday.

Guests and the guest of honor share the party clips (routine:party); children also hop about. The birthday resident
has three more of their own (birthday, all day long): making a wish over the candles, bowing thanks, and a quiet
beam that shows between their everyday moments. The compiler boosts every idle clip here during the party
(ROUTINE_BOOSTS in animations.py), so the gathering reads as a party rather than a crowd standing about.
"""
from kit import clip, HANDS_BEHIND, HAND_TO_CHEST

PARTY = ["routine:party"]
BIRTHDAY = ["birthday"]


@clip("party_clap_along", "Claps along to the music", weight=7, require=PARTY, mirror="never", length=4.0)
def _(c):
    c.key(0.3, ra=(-62, -10, 8), la=(-62, -10, 8), head=(-4, 0, 0), lid=.4)
    # A clap on every beat with a little bounce; the head tips to one side, then the other, on alternate beats.
    c.cycle(0.4, 3.4, .5, dict(ra=(-64, -36, 0), la=(-64, -36, 0), root_pos=(0, -.5, 0)),
            dict(ra=(-60, -10, 8), la=(-60, -10, 8), root_pos=(0, 0, 0)), end_on="b")
    c.cycle(0.4, 3.4, 1.0, dict(head=(-6, 0, 6), root=(0, 0, 2)), dict(head=(-6, 0, -6), root=(0, 0, -2)))
    c.hold(0.4, 3.4, lid=.45)
    c.key(3.7, ra=(-26, -6, 8), la=(-26, -6, 8), head=(-2, 0, 0), root=(0, 0, 0), lid=.2)


@clip("party_raise_cup", "Raises a cup in a toast", weight=6, require=PARTY, length=4.6)
def _(c):
    cup = (-54, -30, 0)
    c.key(0.4, ra=cup, head=(6, 0, 0), look=(0, .4))
    # The toast: the cup held up and out ahead, a little lift on "cheers!".
    c.key(0.9, ra=(-138, 4, 0), la=(-8, 0, 12), head=(-12, 0, 0), waist=(-4, 0, 0), look=(0, -.5), lid=.2)
    c.key(1.15, ra=(-146, 4, 0), root_pos=(0, -.5, 0))
    c.key(1.4, ra=(-136, 4, 0), root_pos=(0, 0, 0))
    c.key(1.7, ra=(-140, 4, 0), head=(-10, 0, 0), lid=.45)
    # Down to the lips for a sip, head tipped back, eyes closed with pleasure.
    c.key(2.2, ra=(-116, -40, 0), la=(-4, 0, 8), head=(-4, 0, 0), waist=(0, 0, 0), look=(0, .2), lid=.3)
    c.key(2.5, ra=(-124, -40, 0), head=(-12, 0, 0), lid=.7, look=(0, 0))
    c.key(3.0, ra=(-126, -40, 0), head=(-14, 0, 0), lid=.75)
    c.key(3.4, ra=cup, head=(4, 0, 6), lid=.3, look=(0, .2))
    c.key(3.8, head=(-2, 0, 2), lid=.2)
    c.key(4.2, ra=(-20, -10, 0), la=(0, 0, 0))


@clip("party_sway", "Sways to the music", weight=6, require=PARTY, mirror="free", length=5.0)
def _(c):
    a = dict(root=(0, 0, 4), waist=(0, 3, -3), head=(-4, 6, -9), ra=(-14, 0, 12), la=(4, 0, 6))
    b = dict(root=(0, 0, -4), waist=(0, -3, 3), head=(-4, -6, 9), ra=(4, 0, 6), la=(-14, 0, 12))
    c.cycle(0.5, 4.1, 1.6, a, b)
    c.hold(0.6, 4.1, lid=.4)
    c.key(4.5, root=(0, 0, 1), waist=(0, 0, 0), head=(-2, 0, -2), ra=(-4, 0, 4), la=(0, 0, 2), lid=.2)


@clip("party_jig", "Dances a happy jig", weight=6, require=PARTY, mirror="free", length=4.4)
def _(c):
    c.key(0.3, ra=(-30, 0, 20), la=(-30, 0, 20), head=(-4, 0, 0), lid=.4)
    # Step, step: a knee comes up while the opposite arm swings forward and the body turns toward it.
    c.cycle(0.45, 3.25, .7,
            dict(rl=(-36, 0, 6), ll=(4, 0, 0), ra=(-20, 0, 18), la=(-52, 0, 26), root=(0, 12, -3), head=(-4, -6, 6)),
            dict(rl=(4, 0, 0), ll=(-36, 0, 6), ra=(-52, 0, 26), la=(-20, 0, 18), root=(0, -12, 3), head=(-4, 6, -6)))
    c.cycle(0.45, 3.25, .35, dict(root_pos=(0, -1.2, 0)), dict(root_pos=(0, 0, 0)), end_on="b")
    c.hold(0.45, 3.25, lid=.5)
    # A little hop to finish, heels kicked out, arms flung wide.
    c.key(3.5, root_pos=(0, -2.4, 0), rl=(-8, 0, 12), ll=(-8, 0, 12), ra=(-40, 0, 44), la=(-40, 0, 44),
          root=(0, 0, 0), head=(-10, 0, 0), lid=.55)
    c.key(3.7, root_pos=(0, 0, 0), rl=(0, 0, 0), ll=(0, 0, 0))
    c.key(4.0, ra=(-20, 0, 16), la=(-20, 0, 16), head=(-4, 0, 0), lid=.2)


@clip("party_laugh", "Laughs with a hand on the belly", weight=5, require=PARTY, mirror="free", length=3.2)
def _(c):
    belly = (-36, -34, 0)
    c.key(0.3, ra=belly, la=(-16, 0, 18), waist=(-8, 0, 0), head=(-18, 0, 0), lid=.75)
    c.wobble(0.35, 1.5, 6, "root_pos", .45, axis=1, decay=.3)
    c.key(1.0, la=(-30, 0, 26), head=(-16, 0, 4))
    # Doubles forward, still laughing, then straightens up, still grinning.
    c.key(1.7, waist=(16, 0, 0), head=(12, 0, -4), ra=(-40, -36, 0), la=(-34, -10, 12), lid=.8)
    c.wobble(1.75, 2.4, 6, "root_pos", .35, axis=1)
    c.key(2.65, waist=(0, 0, 0), head=(-4, 0, 4), ra=(-30, -32, 0), la=(-10, 0, 8), lid=.4)


@clip("party_wave_cheer", "Waves both arms overhead", weight=5, require=PARTY, mirror="never", length=3.4)
def _(c):
    c.key(0.3, ra=(-10, 0, 60), la=(-10, 0, 60), root_pos=(0, .4, 0))
    c.key(0.6, ra=(-10, 0, 150), la=(-10, 0, 150), root_pos=(0, -1.6, 0), head=(-12, 0, 0), lid=.5)
    # Side raises (the overhead V), swung together from side to side with the whole body.
    c.cycle(0.85, 2.65, .8, dict(ra=(-10, 0, 166), la=(-10, 0, 134), root=(0, 0, 4), head=(-12, 0, 8)),
            dict(ra=(-10, 0, 134), la=(-10, 0, 166), root=(0, 0, -4), head=(-12, 0, -8)))
    c.cycle(0.85, 2.65, .4, dict(root_pos=(0, 0, 0)), dict(root_pos=(0, -.8, 0)))
    c.hold(0.6, 2.65, lid=.55)
    c.key(3.0, ra=(-10, 0, 50), la=(-10, 0, 50), root=(0, 0, 0), head=(-4, 0, 0), root_pos=(0, 0, 0), lid=.25)


@clip("party_hum_along", "Hums along with eyes half closed", weight=5, require=PARTY, mirror="free", length=4.8)
def _(c):
    c.key(0.4, **HANDS_BEHIND, head=(2, 0, 4), lid=.55)
    # Gentle nods on the beat, a slow drift of the head, and a foot that taps along.
    c.cycle(0.6, 4.0, .7, dict(head=(10, 4, 5), waist=(2, 0, 0)), dict(head=(0, -2, 3), waist=(0, 0, 0)), end_on="b")
    c.cycle(0.6, 4.0, 1.4, dict(rl=(-8, 0, 2)), dict(rl=(0, 0, 0)), end_on="b")
    c.hold(0.6, 4.0, lid=.55)
    c.key(4.3, head=(-2, 0, 0), waist=(0, 0, 0), lid=.2)


@clip("party_kid_hop", "Hops about at the party", weight=8, require=PARTY + ["child"], mirror="never", length=3.0)
def _(c):
    c.key(0.25, ra=(-6, 0, 30), la=(-6, 0, 30), root_pos=(0, .6, 0), head=(-4, 0, 0), lid=.3)
    # Up with the arms flapping high, down with them low; each hop turns a little to one side, then the other.
    for i, t in enumerate((0.5, 1.1, 1.7, 2.3)):
        side = 1 if i % 2 == 0 else -1
        c.key(t, root_pos=(0, -3, 0), ra=(-16, 0, 120), la=(-16, 0, 120), rl=(-12, 0, 4), ll=(-12, 0, 4),
              head=(-10, 0, 6 * side), root=(0, 8 * side, 0))
        c.key(t + .3, root_pos=(0, .4, 0), ra=(4, 0, 22), la=(4, 0, 22), rl=(0, 0, 0), ll=(0, 0, 0), head=(-2, 0, 0))
    c.hold(0.5, 2.4, lid=.5)
    c.key(2.75, root=(0, 0, 0), root_pos=(0, 0, 0), ra=(0, 0, 14), la=(0, 0, 14), lid=.2)


# -- the guest of honor (all day on their birthday) ---------------------------------------------


@clip("birthday_make_a_wish", "Makes a birthday wish and blows out the candles", weight=2, require=BIRTHDAY,
      mirror="never", length=5.0)
def _(c):
    clasped = dict(ra=(-100, -42, 0), la=(-100, -42, 0))
    c.key(0.5, **clasped, head=(8, 0, 0), waist=(4, 0, 0), lid=1)
    c.key(1.3, **clasped, head=(10, 0, 6), lid=1)
    c.key(1.9, ra=(-102, -42, 0), la=(-102, -42, 0), head=(8, 0, -4), root_pos=(0, -.4, 0), lid=1)
    # A big breath in, then a long puff over the cake, sweeping across the candles.
    c.key(2.4, ra=(-30, 0, 16), la=(-30, 0, 16), waist=(-6, 0, 0), head=(-8, 0, 0), root_pos=(0, 0, 0), lid=.1,
          look=(0, .3))
    c.key(2.8, **HANDS_BEHIND, waist=(24, 0, 0), head=(6, 16, 0), look=(.3, .6), lid=.2)
    c.key(3.35, waist=(25, 0, 0), head=(6, -16, 0), look=(-.3, .6))
    # Straightens up beaming and gives a happy little hop.
    c.key(3.8, ra=(-70, -30, 0), la=(-70, -30, 0), waist=(-4, 0, 0), head=(-12, 0, 0), root_pos=(0, -1.2, 0),
          look=(0, 0), lid=.55)
    c.key(4.05, root_pos=(0, 0, 0))
    c.key(4.4, ra=(-30, -14, 4), la=(-30, -14, 4), waist=(0, 0, 0), head=(-4, 0, 0), lid=.3)


@clip("birthday_bow_thanks", "Bows thanks to the well-wishers", weight=3, require=BIRTHDAY, length=4.2)
def _(c):
    c.key(0.4, **HAND_TO_CHEST, la=(-16, 14, 30))
    c.key(1.0, waist=(30, 0, 0), head=(14, 0, 0), la=(-22, 24, 46), lid=.5)
    c.key(1.6, waist=(31, 0, 0), head=(15, 0, 0), la=(-22, 24, 48))
    # Comes up beaming and looks around at everyone who came.
    c.key(2.2, waist=(-4, 0, 0), head=(-14, 0, 6), ra=(-56, -48, 0), la=(-14, 10, 22), look=(0, -.4), lid=.55)
    c.key(2.7, head=(-12, 18, 4), look=(.5, -.3))
    c.key(3.2, head=(-10, -14, -4), look=(-.5, -.3))
    c.key(3.7, head=(-4, 0, 0), waist=(0, 0, 0), ra=(-30, -30, 0), la=(-4, 4, 8), look=(0, 0), lid=.25)


@clip("birthday_beam", "Beams on their birthday", weight=4, require=BIRTHDAY, mirror="free", length=5.0)
def _(c):
    c.key(0.5, **HANDS_BEHIND, head=(-10, 0, 0), lid=.5, look=(0, -.2))
    # Rocks heel to toe with the chin up, smiling to themselves.
    for i, t in enumerate((0.9, 1.6, 2.3, 3.0, 3.7)):
        forward = i % 2 == 0
        c.key(t, root=(3, 0, 0) if forward else (-2.4, 0, 0), root_pos=(0, -.6, 0) if forward else (0, 0, 0),
              head=(-12, 0, 5) if forward else (-11, 0, -5))
    c.key(4.3, **HANDS_BEHIND, root=(0, 0, 0), root_pos=(0, 0, 0), head=(-6, 0, 0), lid=.4, look=(0, 0))
