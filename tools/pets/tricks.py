#!/usr/bin/env python3
"""Pet tricks: the poses residents' cats and dogs strike while they play (see kit.py for conventions).

Compiles to src/main/resources/assets/villagefriends/pet_tricks/pets.json, which the game loads (a
resource pack can replace it). Never hand-edit the JSON. The play scripts in PetPlays.java name
these tricks; ResidentPetsTest checks every one they use exists.

    python tools/pets/tricks.py            # compile
    python tools/pets/tricks.py --check    # validate and confirm the JSON is current
    python tools/pets/preview.py sheet     # offline contact sheet of every trick
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parent
ROOT = TOOL.parents[1]
OUT = ROOT / "src/main/resources/assets/villagefriends/pet_tricks/pets.json"
sys.path.insert(0, str(TOOL))
from kit import TRICKS, trick  # noqa: E402


# -- dogs --------------------------------------------------------------------------------------

@trick("play_bow", "dog", 1.08, loop=True, blend=(.25, .3), name="Play bow")
def _(t):
    bow = dict(root=(14, 0, 0), root_pos=(0, 1.6, 0), fronts=(-62, 0, 0), hinds=(-14, 0, 0), head=(-22, 0, 0), upper=(0, 0, 0))
    for i, s in enumerate((0, .27, .54, .81)):
        t.key(s, **bow, tail=(34, 34 if i % 2 else -34, 0), head_pos=(0, .4 if i % 2 else 0, 0))
    t.key(1.08, **bow, tail=(34, -34, 0), head_pos=(0, 0, 0))


@trick("wag", "dog", .72, loop=True, name="Wags happily")
def _(t):
    for i, s in enumerate((0, .18, .36, .54)):
        t.key(s, tail=(26, 34 if i % 2 else -34, 0), head=(-6, 0, 5 if i % 2 else -5), root_pos=(0, 0, 0))
    t.key(.72, tail=(26, -34, 0), head=(-6, 0, -5), root_pos=(0, 0, 0))


@trick("happy", "dog", .8, loop=True, blend=(.15, .3), name="Bounces happily")
def _(t):
    t.key(0, root_pos=(0, 0, 0), fronts=(0, 0, 0), tail=(32, -34, 0), head=(-12, 0, 0))
    t.key(.2, root_pos=(0, -1.8, 0), rf=(-28, 0, 0), lf=(-6, 0, 0), tail=(32, 34, 0), head=(-18, 0, 6))
    t.key(.4, root_pos=(0, 0, 0), fronts=(0, 0, 0), tail=(32, -34, 0), head=(-12, 0, 0))
    t.key(.6, root_pos=(0, -1.8, 0), lf=(-28, 0, 0), rf=(-6, 0, 0), tail=(32, 34, 0), head=(-18, 0, -6))
    t.key(.8, root_pos=(0, 0, 0), fronts=(0, 0, 0), tail=(32, -34, 0), head=(-12, 0, 0))


@trick("beg", "dog", 1.2, loop=True, blend=(.3, .3), name="Sits up and begs")
def _(t):
    # Sitting already: rock back onto the haunches, chest up, front paws tucked and pawing the air.
    up = dict(root=(-24, 0, 0), root_pos=(0, -1.2, 1.2), head=(-4, 0, 0))
    t.key(0, **up, rf=(-58, 0, 0), lf=(-44, 0, 0), tail=(0, -20, 0))
    t.key(.3, **up, rf=(-44, 0, 0), lf=(-62, 0, 0), tail=(0, 20, 0))
    t.key(.6, **up, rf=(-58, 0, 0), lf=(-44, 0, 0), tail=(0, -20, 0))
    t.key(.9, **up, rf=(-44, 0, 0), lf=(-62, 0, 0), tail=(0, 20, 0))
    t.key(1.2, **up, rf=(-58, 0, 0), lf=(-44, 0, 0), tail=(0, -20, 0))


@trick("paw", "dog", 1.6, loop=True, blend=(.25, .3), name="Offers a paw")
def _(t):
    for i, s in enumerate((0, .4, .8, 1.2)):
        t.key(s, rf=(-96 if i % 2 else -84, 0, -8), head=(-10, 0, 12 if i % 2 else 10), tail=(0, 18 if i % 2 else -18, 0))
    t.key(1.6, rf=(-84, 0, -8), head=(-10, 0, 10), tail=(0, -18, 0))


@trick("spin", "dog", 1.5, blend=(.08, .12), name="Spins in a circle")
def _(t):
    t.key(0, root=(0, 0, 0), root_pos=(0, 0, 0), tail=(30, 0, 0))
    t.key(.35, root=(0, 120, 0), root_pos=(0, -1.5, 0), tail=(30, 30, 0), head=(-10, 0, 0))
    t.key(.7, root=(0, 240, 0), root_pos=(0, -2.2, 0), tail=(30, -30, 0), head=(-10, 0, 0))
    t.key(1.05, root=(0, 360, 0), root_pos=(0, 0, 0), tail=(30, 30, 0), head=(-14, 0, 0))
    t.key(1.5, root=(0, 360, 0), root_pos=(0, 0, 0), tail=(30, -30, 0), head=(-14, 0, 0))


@trick("belly_up", "dog", 1.6, loop=True, blend=(.5, .45), name="Rolls over for a belly rub")
def _(t):
    over = dict(root=(0, 0, 172), root_pos=(0, 7, 0), head=(-10, 0, -14), tail=(-40, 0, 0))
    t.key(0, **over, rf=(-56, 0, 10), lf=(-30, 0, -10), rh=(-34, 0, 12), lh=(-50, 0, -12))
    t.key(.4, **over, rf=(-36, 0, 10), lf=(-54, 0, -10), rh=(-50, 0, 12), lh=(-32, 0, -12))
    t.key(.8, **over, rf=(-56, 0, 10), lf=(-30, 0, -10), rh=(-34, 0, 12), lh=(-50, 0, -12))
    t.key(1.2, **over, rf=(-36, 0, 10), lf=(-54, 0, -10), rh=(-50, 0, 12), lh=(-32, 0, -12))
    t.key(1.6, **over, rf=(-56, 0, 10), lf=(-30, 0, -10), rh=(-34, 0, 12), lh=(-50, 0, -12))


@trick("shake_off", "dog", 1.2, blend=(.05, .2), name="Shakes off")
def _(t):
    for i in range(9):
        s = i * .12
        amp = (1 - i / 9) * 16
        t.key(s, root=(0, 0, amp if i % 2 else -amp), head=(0, 0, -amp * 1.2 if i % 2 else amp * 1.2), tail=(20, -amp * 2 if i % 2 else amp * 2, 0))
    t.key(1.2, root=(0, 0, 0), head=(0, 0, 0), tail=(0, 0, 0))


@trick("carry", "dog", .8, loop=True, name="Trots back proudly")
def _(t):
    t.key(0, head=(-16, 0, 0), tail=(30, -26, 0))
    t.key(.2, head=(-18, 0, 3), tail=(30, 26, 0))
    t.key(.4, head=(-16, 0, 0), tail=(30, -26, 0))
    t.key(.6, head=(-18, 0, -3), tail=(30, 26, 0))
    t.key(.8, head=(-16, 0, 0), tail=(30, -26, 0))


@trick("catch", "dog", .8, blend=(.04, .25), name="Snaps up a treat")
def _(t):
    t.key(.1, head=(-38, 0, 0), root=(-8, 0, 0), tail=(30, 20, 0))
    t.key(.25, head=(-30, 0, 0), root=(-4, 0, 0), tail=(30, -20, 0))
    t.key(.45, head=(10, 0, 0), root=(0, 0, 0), tail=(30, 20, 0))
    t.key(.6, head=(4, 0, 0), tail=(30, -20, 0))


@trick("sniff", "dog", 1.2, loop=True, name="Sniffs curiously")
def _(t):
    for i, s in enumerate((0, .2, .4, .6, .8, 1.0)):
        t.key(s, head=(34 + (4 if i % 2 else -2), 4 if i % 3 == 1 else -4 if i % 3 == 2 else 0, 0), root=(5, 0, 0), tail=(10, -10 if i % 2 else 10, 0))
    t.key(1.2, head=(32, 0, 0), root=(5, 0, 0), tail=(10, 10, 0))


# -- cats --------------------------------------------------------------------------------------

@trick("bat", "cat", .9, loop=True, blend=(.15, .25), name="Bats at the string")
def _(t):
    look = dict(head=(-26, 0, 0))
    t.key(0, **look, rf=(-40, 0, 0), tip=(0, 0, 0))
    t.key(.15, **look, rf=(-118, 0, 14), tip=(0, 0, 0))
    t.key(.28, **look, rf=(-70, 0, -8), tip=(0, 0, 0))
    t.key(.45, **look, rf=(-40, 0, 0), lf=(-40, 0, 0), tip=(0, 0, 0))
    t.key(.6, **look, lf=(-118, 0, -14), rf=(-40, 0, 0), tip=(0, 0, 0))
    t.key(.73, **look, lf=(-70, 0, 8), tip=(0, 0, 0))
    t.key(.9, **look, rf=(-40, 0, 0), lf=(0, 0, 0), tip=(0, 0, 0))


@trick("crouch_wiggle", "cat", .5, loop=True, blend=(.2, .15), name="Wiggles, ready to pounce")
def _(t):
    # Low to the ground, tail stretched straight back with the tip twitching, rear end waggling.
    low = dict(root_pos=(0, 2.2, 0), fronts=(-34, 0, 0), hinds=(40, 0, 0), head=(-12, 0, 0), head_pos=(0, 1.0, 0),
               tail=(38, 0, 0), tip_pos=(0, -5, 2))
    t.key(0, **low, root=(0, -7, 0), tip=(-9, -14, 0))
    t.key(.125, **low, root=(0, 0, 0), tip=(-9, 0, 0))
    t.key(.25, **low, root=(0, 7, 0), tip=(-9, 14, 0))
    t.key(.375, **low, root=(0, 0, 0), tip=(-9, 0, 0))
    t.key(.5, **low, root=(0, -7, 0), tip=(-9, -14, 0))


@trick("pounce", "cat", .6, blend=(.03, .2), name="Pounces")
def _(t):
    t.key(.12, root=(-14, 0, 0), fronts=(-86, 0, 0), hinds=(48, 0, 0), head=(-16, 0, 0), tail=(-20, 0, 0))
    t.key(.32, root=(-4, 0, 0), fronts=(-60, 0, 0), hinds=(30, 0, 0), head=(-8, 0, 0), tail=(-10, 0, 0))
    t.key(.5, root=(4, 0, 0), fronts=(-10, 0, 0), hinds=(0, 0, 0), head=(6, 0, 0))


@trick("lean", "cat", 1.6, loop=True, blend=(.3, .3), name="Leans into a scratch")
def _(t):
    t.key(0, head=(-30, 0, 16), root=(0, 0, 4))
    t.key(.8, head=(-34, 6, 22), root=(0, 0, 6))
    t.key(1.6, head=(-30, 0, 16), root=(0, 0, 4))


# The tail's tip isn't attached to the rest of the tail, so raising the tail also moves the tip up.
TAIL_UP = dict(tail=(110, 0, 0), tip_pos=(0, -12.3, -3.3), tip=(76, 0, 0))


@trick("tail_up", "cat", 1.4, loop=True, name="Trots with tail up")
def _(t):
    t.key(0, **TAIL_UP, head=(-6, 0, 0))
    t.key(.7, tail=(104, 8, 0), tip_pos=(1.1, -12.0, -3.0), tip=(80, 12, 0), head=(-8, 0, 0))
    t.key(1.4, **TAIL_UP, head=(-6, 0, 0))


@trick("sniff", "cat", 1.0, loop=True, name="Sniffs the treat")
def _(t):
    for i, s in enumerate((0, .2, .4, .6, .8)):
        t.key(s, head=(28 + (4 if i % 2 else 0), 0, 0), head_pos=(0, 0, -.8 if i % 2 else 0), root=(6, 0, 0))
    t.key(1.0, head=(28, 0, 0), head_pos=(0, 0, 0), root=(6, 0, 0))


@trick("groom", "cat", 1.4, loop=True, blend=(.3, .3), name="Grooms a paw")
def _(t):
    # Sitting: one forepaw lifted, head bowed to lick it.
    paw = dict(rf=(-62, 0, -10), head_pos=(0, 3, -1.5))
    for i, s in enumerate((0, .2, .4, .6, .8, 1.0, 1.2)):
        t.key(s, **paw, head=(46 + (8 if i % 2 else 0), -8, 0))
    t.key(1.4, **paw, head=(46, -8, 0))


@trick("stretch", "cat", 1.4, blend=(.25, .3), name="Has a big stretch")
def _(t):
    t.key(.45, root=(16, 0, 0), root_pos=(0, 1.2, 0), fronts=(-62, 0, 0), hinds=(-12, 0, 0), head=(-26, 0, 0), **TAIL_UP)
    t.key(.95, root=(16, 0, 0), root_pos=(0, 1.2, 0), fronts=(-66, 0, 0), hinds=(-14, 0, 0), head=(-30, 0, 0), **TAIL_UP)


@trick("belly_up", "cat", 1.2, loop=True, blend=(.45, .4), name="Rolls over, paws in the air")
def _(t):
    over = dict(root=(0, 0, 168), root_pos=(0, 4.4, 0), head=(-12, 0, -16))
    t.key(0, **over, rf=(-80, 0, 12), lf=(-40, 0, -8), hinds=(-30, 0, 0))
    t.key(.3, **over, rf=(-40, 0, 12), lf=(-84, 0, -8), hinds=(-36, 0, 0))
    t.key(.6, **over, rf=(-80, 0, 12), lf=(-40, 0, -8), hinds=(-30, 0, 0))
    t.key(.9, **over, rf=(-40, 0, 12), lf=(-84, 0, -8), hinds=(-36, 0, 0))
    t.key(1.2, **over, rf=(-80, 0, 12), lf=(-40, 0, -8), hinds=(-30, 0, 0))


# ----------------------------------------------------------------------------------------------

def document():
    return {"format": 1, "name": "Village pets",
            "description": "Poses residents' cats and dogs strike while they play. Authored in tools/pets/tricks.py.",
            "tricks": [t.compile() for t in TRICKS]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    seen = set()
    for t in TRICKS:
        key = f"{t.species}:{t.id}"
        if key in seen:
            raise SystemExit(f"Duplicate trick {key}")
        seen.add(key)
    text = json.dumps(document(), indent=1) + "\n"
    if args.list:
        for t in TRICKS:
            print(f"{t.species:4} {t.id:16} {t.length:4.2f}s {'loop' if t.loop else '    '} {t.name}")
        return
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is out of date: run python tools/pets/tricks.py")
        print(f"{len(TRICKS)} pet tricks OK")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {len(TRICKS)} pet tricks to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
