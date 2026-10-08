"""Authoring kit for pet tricks: the poses residents' cats and dogs strike while they play.

A trick keys a few bones over time. Angles are degrees and offsets are model pixels, both added to
the pet's own pose (standing, sitting or lying, as the game has it), in Minecraft's model space:

    pitch + tips a bone down and back: a leg's paw swings backward, the head looks down, the root
               (the whole pet) dips its nose. pitch - raises a paw forward or lifts the chin.
    yaw   + turns a bone to the pet's left; the root spins the pet about the middle of its body.
    roll  + tips a bone's top toward the pet's left; the root rolls the pet onto its side and back.
    y pos + moves down (toward the ground), z pos - moves forward.

The root turns about the middle of the body, so rolling over or spinning happens on the spot; root
offsets are written for a grown pet and halved for kittens and puppies.

Keyword channels: root, head, body, upper (a grown dog's shoulders), tail, tip (a cat's tail tip,
which isn't attached to the rest of the tail, so it needs moving as well as turning), rf, lf, rh, lh
(right/left front/hind leg), fronts and hinds (both legs of a pair). Add _pos for an offset.
"""
from __future__ import annotations

import math

BONES = ("root", "head", "body", "upper_body", "tail", "tail_tip",
         "right_front_leg", "left_front_leg", "right_hind_leg", "left_hind_leg")
NAMES = {"root": ("root",), "head": ("head",), "body": ("body",), "upper": ("upper_body",), "tail": ("tail",),
         "tip": ("tail_tip",), "rf": ("right_front_leg",), "lf": ("left_front_leg",), "rh": ("right_hind_leg",),
         "lh": ("left_hind_leg",), "fronts": ("right_front_leg", "left_front_leg"), "hinds": ("right_hind_leg", "left_hind_leg")}
SPECIES = ("cat", "dog")


def channels(name, value):
    """An authoring keyword to (track keys, xyz)."""
    position = name.endswith("_pos")
    bones = NAMES[name[:-4] if position else name]
    return [f"{b}.{'pos' if position else 'rot'}" for b in bones], tuple(float(v) for v in value)


class Trick:
    def __init__(self, id, species, length, loop=False, blend=(.2, .3), name=""):
        if species not in SPECIES:
            raise ValueError(f"{id}: species must be cat or dog")
        self.id, self.species, self.length, self.loop, self.blend, self.name = id, species, length, loop, blend, name or id
        self.channels: dict[str, dict[float, tuple]] = {}

    def key(self, t, **pose):
        t = round(float(t), 4)
        if t < 0 or t > self.length + 1e-6:
            raise ValueError(f"{self.species}:{self.id}: key {t} outside 0..{self.length}")
        for name, value in pose.items():
            keys, xyz = channels(name, value)
            for k in keys:
                self.channels.setdefault(k, {})[t] = xyz
        return self

    def hold(self, start, end, **pose):
        return self.key(start, **pose).key(end, **pose)

    def cycle(self, start, end, period, a, b):
        """Alternate pose dicts a and b every half period, from start to end (ending on a)."""
        t, flip = start, False
        while t < end - 1e-6:
            self.key(t, **(b if flip else a))
            t += period / 2
            flip = not flip
        return self.key(end, **a)

    def compile(self):
        tracks = {}
        for channel, keys in sorted(self.channels.items()):
            keys = dict(keys)
            times = sorted(keys)
            if self.loop:
                # A loop repeats seamlessly: it ends where it began.
                if times[0] > 0:
                    keys[0.0] = keys[times[0]]
                keys[round(self.length, 4)] = keys[min(keys)]
            else:
                if times[0] > 0:
                    keys[0.0] = (0.0, 0.0, 0.0)
                if times[-1] < self.length - 1e-6:
                    keys[round(self.length, 4)] = (0.0, 0.0, 0.0)
            tracks[channel] = [[t, *[round(v, 3) for v in keys[t]]] for t in sorted(keys)]
        out = {"id": self.id, "species": self.species, "name": self.name, "length": round(self.length, 3)}
        if self.loop:
            out["loop"] = True
        if tuple(self.blend) != (.2, .3):
            out["blend"] = list(self.blend)
        out["tracks"] = tracks
        return out


TRICKS: list[Trick] = []


def trick(id, species, length, **options):
    """Decorator: the function keys a fresh Trick, which joins the file."""
    def register(fn):
        t = Trick(id, species, length, **options)
        fn(t)
        TRICKS.append(t)
        return t
    return register


def wave(t, period, phase=0.0):
    return math.sin((t / period + phase) * math.tau)
