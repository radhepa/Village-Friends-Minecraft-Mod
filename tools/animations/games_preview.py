#!/usr/bin/env python3
"""Animated previews of the children's game clips (trigger ``play``, tools/animations/village_life/games.py),
one looping animated WebP per clip, using the offline renderer in preview.py.

Clips that play while a child runs about keep only their upper body in game: root, waist and legs come from
the walk instead. Those are shown over a simple running gait, the way they look in a game.

    python tools/animations/games_preview.py [--clips tag_flee,ring_fall] [--out build/previews/games]

Writes <out>/<clip>.webp and <out>/clips.json (id, name, tags, length, walking). The in-game test
(gradlew runClientGameTest -Ptests=PlaygroundGameTest) is the source of truth; children are smaller in game.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

import importlib.util

# Load the animation preview under its own name: it imports the wardrobe's `preview` module itself.
_spec = importlib.util.spec_from_file_location("animation_preview", Path(__file__).resolve().parent / "preview.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)

FPS = 15
W, H, SCALE = 200, 330, 7.2
# Shown walking or running even though they don't require it: they're mostly seen on the move.
ON_THE_MOVE = {"ring_walk", "leader_march"}
LOWER = ("root", "waist", "right_leg", "left_leg")


def walking(clip):
    return clip["id"] in ON_THE_MOVE or any("moving" in group for group in clip.get("require", []))


def gait(rot, pos, t, run):
    """Replace the lower body with a walk (or run) cycle, and add the arms' natural swing."""
    for b in LOWER:
        rot[b] = np.zeros(3)
        pos[b] = np.zeros(3)
    rate, swing = (2.4, 42) if run else (1.7, 30)
    s = math.sin(t * rate * math.tau)
    rot["right_leg"][0] = swing * s
    rot["left_leg"][0] = -swing * s
    rot["right_arm"][0] += -swing * .45 * s
    rot["left_arm"][0] += swing * .45 * s
    pos["root"][1] = -abs(s) * (1.1 if run else .5)


def frame(who, clip, t, walk, run):
    canvas = A.P.Canvas(W, H)
    rot, pos, _, _ = A.sample(clip, min(t, clip["length"]))
    if walk:
        gait(rot, pos, t, run)
    bones, rp, rr = A.pose(rot, pos)
    # A soft shadow under the feet.
    cx, cy = W // 2, 112
    ground = int(cy + 24 * SCALE * .99)
    yy, xx = np.ogrid[:H, :W]
    shadow = ((xx - cx) / (W * .2)) ** 2 + ((yy - ground) / 7) ** 2 < 1
    canvas.img[shadow] *= .86
    A.draw(canvas, who.skin, who.pieces, cx, cy, SCALE, -28, -8, bones, rp, rr)
    return Image.fromarray(canvas.img.clip(0, 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", default="")
    ap.add_argument("--out", default=str(A.W.ROOT / "build/previews/games"))
    a = ap.parse_args()
    clips = [c for c in A.load_pack().values() if c["trigger"] == "play"]
    if a.clips:
        wanted = set(a.clips.split(","))
        clips = [c for c in clips if c["id"].split(":")[-1] in wanted]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    who = A.Resident(5)
    meta = []
    for c in clips:
        cid = c["id"].split(":")[-1]
        walk = walking(c)
        run = cid.startswith("tag_") or cid == "curious_skip"
        # Walking clips loop seamlessly over whole gait cycles; others hold still a moment between plays.
        length = c["length"] if walk else c["length"] + .5
        frames = [frame(who, c, f / FPS, walk, run) for f in range(max(2, round(length * FPS)))]
        frames[0].save(out / f"{cid}.webp", save_all=True, append_images=frames[1:], duration=round(1000 / FPS), loop=0,
                       lossless=False, quality=82, method=4)
        meta.append({"id": cid, "name": c["name"], "length": c["length"], "walking": walk,
                     "require": c.get("require", []), "avoid": c.get("avoid", [])})
        print(f"{cid}: {len(frames)} frames", flush=True)
    (out / "clips.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
