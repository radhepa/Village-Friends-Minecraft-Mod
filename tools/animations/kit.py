"""Authoring kit for resident animation packs.

A clip is a list of keyed poses. Angles are degrees added to the resident's live pose, so a
pose of zero is "whatever they were already doing" (standing, breathing, looking at you).
Each channel interpolates only between its own keys; every channel starts and ends at rest
unless the clip keys it otherwise.

Conventions (chosen so poses read the same on both sides of the body):

    head, body, waist, root   (pitch, yaw, roll)
                              pitch + bows/looks down, yaw + turns to the resident's right,
                              roll + tilts toward their left shoulder.
                              waist bends at the hips; root pivots the whole body at the feet.
    ra, la / rl, ll           right/left arm and leg (pitch, yaw_out, roll_out)
                              pitch - raises the limb forward (-90 points ahead, -180 is
                              straight up), + swings it back. yaw_out + swings a raised arm
                              outward, - across the chest. roll_out + lifts it out to the side.
    root_pos, head_pos, body_pos   model pixels (x, y, z): y - is up, z - is forward.
    ra_pos, la_pos, rl_pos, ll_pos (out, y, z): out + moves away from the body.
    lid                       0 open .. 1 closed (combined with natural blinking)
    look                      (x, y) iris offset: x + toward the resident's right, y + down;
                              kept inside the eye whites by the renderer.
"""
from __future__ import annotations

import math

LIMBS = {"ra": "right_arm", "la": "left_arm", "rl": "right_leg", "ll": "left_leg"}
TRUNK = {"head": "head", "body": "body", "waist": "waist", "root": "root"}
POSITIONS = {"root_pos": "root", "head_pos": "head", "body_pos": "body",
             "ra_pos": "right_arm", "la_pos": "left_arm", "rl_pos": "right_leg", "ll_pos": "left_leg"}
TRIGGERS = {"idle", "greet", "talk", "chat_speak", "chat_listen", "laugh", "delighted", "thanks",
            "decline", "happy", "love", "angry", "nervous", "hurt", "play"}


def _channel_value(name, value):
    """Map an authoring keyword and value to (track key, model-space components)."""
    if name in TRUNK:
        x, y, z = value
        return f"{TRUNK[name]}.rot", (x, y, z)
    if name in LIMBS:
        x, y, z = value
        left = name[0] == "l"
        return f"{LIMBS[name]}.rot", (x, -y if left else y, -z if left else z)
    if name in POSITIONS:
        x, y, z = value
        bone = POSITIONS[name]
        if bone.startswith("right"):
            x = -x
        return f"{bone}.pos", (x, y, z)
    if name == "lid":
        return "eyes.lid", (float(value),)
    if name == "look":
        x, y = value
        return "eyes.look", (-x, y)
    raise KeyError(f"Unknown pose channel {name!r}")


class Clip:
    def __init__(self, id, name, trigger="idle", length=3.0, weight=1.0, require=(), avoid=(),
                 boost=None, blend=(.25, .35), mirror="hand", items="keep"):
        if trigger not in TRIGGERS:
            raise ValueError(f"{id}: unknown trigger {trigger}")
        self.id, self.name, self.trigger, self.length, self.weight = id, name, trigger, length, weight
        self.require, self.avoid, self.boost = list(require), list(avoid), dict(boost or {})
        self.blend, self.mirror, self.items = blend, mirror, items
        self.channels: dict[str, dict[float, tuple]] = {}

    # -- keys --------------------------------------------------------------------------------
    def key(self, t, **pose):
        """Key every given channel at time t. With no channels, returns all used channels to rest."""
        t = round(float(t), 4)
        if t < 0 or t > self.length + 1e-6:
            raise ValueError(f"{self.id}: key {t} outside 0..{self.length}")
        if not pose:
            for channel, keys in self.channels.items():
                keys[t] = tuple(0.0 for _ in next(iter(keys.values())))
            return self
        for name, value in pose.items():
            channel, values = _channel_value(name, value)
            self.channels.setdefault(channel, {})[t] = tuple(float(v) for v in values)
        return self

    def hold(self, start, end, **pose):
        return self.key(start, **pose).key(end, **pose)

    def rest(self, t, *names):
        """Return just these authoring channels (e.g. "ra", "head") to rest at t."""
        for name in names:
            channel, values = _channel_value(name, {"lid": 0, "look": (0, 0)}.get(name, (0, 0, 0)))
            self.channels.setdefault(channel, {})[round(float(t), 4)] = tuple(0.0 for _ in values)
        return self

    def cycle(self, start, end, period, a, b, end_on="a"):
        """Alternate between pose dicts a and b every half period from start to end."""
        t, flip = start, False
        while t < end - 1e-6:
            self.key(t, **(b if flip else a))
            t += period / 2
            flip = not flip
        self.key(end, **(a if end_on == "a" else b))
        return self

    def wobble(self, start, end, rate, channel, amplitude, base=(0, 0, 0), axis=0, decay=0.0):
        """Small oscillation on one component (shivers, giggles, scratching)."""
        steps = max(2, int((end - start) * rate * 2))
        for i in range(steps + 1):
            t = start + (end - start) * i / steps
            sign = 0 if i in (0, steps) else (1 if i % 2 else -1)
            fade = (1 - decay * i / steps)
            v = list(base)
            v[axis] += sign * amplitude * fade
            self.key(t, **{channel: tuple(v)})
        return self

    # -- output ------------------------------------------------------------------------------
    def compile(self):
        tracks = {}
        for channel, keys in sorted(self.channels.items()):
            width = len(next(iter(keys.values())))
            times = sorted(keys)
            if times[0] > 0:
                keys[0.0] = (0.0,) * width
            if times[-1] < self.length - 1e-6:
                keys[round(self.length, 4)] = (0.0,) * width
            tracks[channel] = [[t, *[round(v, 3) for v in keys[t]]] for t in sorted(keys)]
        out = {"id": self.id, "name": self.name, "trigger": self.trigger, "length": round(self.length, 3),
               "weight": self.weight}
        if self.require:
            out["require"] = self.require
        if self.avoid:
            out["avoid"] = self.avoid
        if self.boost:
            out["boost"] = self.boost
        if tuple(self.blend) != (.25, .35):
            out["blend"] = list(self.blend)
        if self.mirror != "hand":
            out["mirror"] = self.mirror
        if self.items != "keep":
            out["items"] = self.items
        out["tracks"] = tracks
        return out


CLIPS: list[Clip] = []


def clip(id, name, also=None, **options):
    """Decorator: the function receives a fresh Clip to key, and the clip joins the pack.

    ``also`` maps extra clip ids to other triggers, e.g. ``also={"chat_open_palm": "chat_speak"}``,
    so one motion can serve several situations without copying its keys.
    """
    def register(fn):
        c = Clip(id, name, **options)
        fn(c)
        CLIPS.append(c)
        for other_id, trigger in (also or {}).items():
            twin = Clip(other_id, name, **{**options, "trigger": trigger})
            twin.channels = c.channels
            CLIPS.append(twin)
        return c
    return register


# -- shared poses (authoring convention) -------------------------------------------------------
ARMS_CROSSED = dict(ra=(-64, -46, -6), la=(-56, -40, -6))
HANDS_BEHIND = dict(ra=(24, 0, -9), la=(24, 0, -9))
HANDS_ON_HIPS = dict(ra=(14, 0, 26), la=(14, 0, 26))
PRAYER = dict(ra=(-62, -38, 0), la=(-62, -38, 0))
BOOK = dict(ra=(-48, -26, 0), la=(-48, -26, 0))
HAND_TO_CHIN = dict(ra=(-104, -42, 0))
HAND_TO_CHEST = dict(ra=(-58, -50, 0))
HAND_TO_MOUTH = dict(ra=(-113, -40, 0))
SHIELD_EYES = dict(ra=(-146, -50, 0))
PALMS_OUT = dict(ra=(-34, 22, 18), la=(-34, 22, 18))


def sine(t, period, phase=0.0):
    return math.sin((t / period + phase) * math.tau)
