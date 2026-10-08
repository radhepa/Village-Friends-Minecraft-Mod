#!/usr/bin/env python3
"""Offline previews of pet tricks on the vanilla cat and wolf models, posed the way PetPoser.java poses
them (the root turns about the middle of the body). Textures are read straight from the Minecraft
client jar in the Gradle cache and never copied into the repository. For fast iteration only; the
game is the source of truth.

    python tools/pets/preview.py sheet [--species dog] [--tricks play_bow,beg] [--baby] [--frames 5]
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import math
import os
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

TOOL = Path(__file__).resolve().parent
ROOT = TOOL.parents[1]
sys.path.insert(0, str(TOOL.parent / "wardrobe"))
import importlib.util  # noqa: E402

# The wardrobe's tiny renderer (canvas and cube faces); this file shares its module name, so load it by path.
_spec = importlib.util.spec_from_file_location("wardrobe_preview", TOOL.parent / "wardrobe" / "preview.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

TRICKS = ROOT / "src/main/resources/assets/villagefriends/pet_tricks/pets.json"
SCRATCH = ROOT / "build/pet-preview"
PI = math.pi


# -- the vanilla models (net.minecraft.client.model.animal.*) ------------------------------------
# part: (parent, pivot, rotation in radians, [(uv, origin, size)])
def wolf_adult():
    leg = [((0, 18), (0, 0, -1), (2, 8, 2))]
    return {
        "head": (None, (-1, 13.5, -7), (0, 0, 0), []),
        "real_head": ("head", (0, 0, 0), (0, 0, 0), [((0, 0), (-2, -3, -2), (6, 6, 4)), ((16, 14), (-2, -5, 0), (2, 2, 1)),
                                                     ((16, 14), (2, -5, 0), (2, 2, 1)), ((0, 10), (-.5, -.001, -5), (3, 3, 4))]),
        "body": (None, (0, 14, 2), (PI / 2, 0, 0), [((18, 14), (-3, -2, -3), (6, 9, 6))]),
        "upper_body": (None, (-1, 14, -3), (PI / 2, 0, 0), [((21, 0), (-3, -3, -3), (8, 6, 7))]),
        "right_hind_leg": (None, (-2.5, 16, 7), (0, 0, 0), leg), "left_hind_leg": (None, (.5, 16, 7), (0, 0, 0), leg),
        "right_front_leg": (None, (-2.5, 16, -4), (0, 0, 0), leg), "left_front_leg": (None, (.5, 16, -4), (0, 0, 0), leg),
        "tail": (None, (-1, 12, 8), (PI / 5, 0, 0), []),
        "real_tail": ("tail", (0, 0, 0), (0, 0, 0), [((9, 18), (0, 0, -1), (2, 8, 2))]),
    }


def wolf_baby():
    return {
        "head": (None, (0, 18.25, -4), (0, 0, 0), [((0, 12), (-2.99, -3.25, -3), (6, 5, 5)), ((17, 12), (-1.5, -.24, -5), (3, 2, 2))]),
        "right_ear": ("head", (-2, -4.25, -.5), (0, 0, 0), [((0, 5), (-1, -1, -.5), (2, 2, 1))]),
        "left_ear": ("head", (2, -4.25, -.5), (0, 0, 0), [((20, 5), (-1, -1, -.5), (2, 2, 1))]),
        "body": (None, (0, 19, 0), (0, 0, 0), [((0, 0), (-3, -2, -4), (6, 4, 8))]),
        "right_hind_leg": (None, (-1.5, 21, 3), (0, 0, 0), [((0, 22), (-1, 0, -1), (2, 3, 2))]),
        "left_hind_leg": (None, (1.5, 21, 3), (0, 0, 0), [((8, 22), (-1, 0, -1), (2, 3, 2))]),
        "right_front_leg": (None, (-1.5, 21, -3), (0, 0, 0), [((0, 0), (-1, 0, -1), (2, 3, 2))]),
        "left_front_leg": (None, (1.5, 21, -3), (0, 0, 0), [((20, 0), (-1, 0, -1), (2, 3, 2))]),
        "tail": (None, (0, 19, 3), (-.5236, 0, 0), []),
        "tail_r1": ("tail", (0, -.6, .2), (-3.1, 0, 0), [((22, 16), (-1, -5.7, -1), (2, 6, 2))]),
    }


def cat_adult():
    hind = [((8, 13), (-1, 0, 1), (2, 6, 2))]
    front = [((40, 0), (-1, 0, 0), (2, 10, 2))]
    return {
        "head": (None, (0, 15, -9), (0, 0, 0), [((0, 0), (-2.5, -2, -3), (5, 4, 5)), ((0, 24), (-1.5, -.001, -4), (3, 2, 2)),
                                               ((0, 10), (-2, -3, 0), (1, 1, 2)), ((6, 10), (1, -3, 0), (1, 1, 2))]),
        "body": (None, (0, 12, -10), (PI / 2, 0, 0), [((20, 0), (-2, 3, -8), (4, 16, 6))]),
        "tail1": (None, (0, 15, 8), (.9, 0, 0), [((0, 15), (-.5, 0, 0), (1, 8, 1))]),
        "tail2": (None, (0, 20, 14), (0, 0, 0), [((4, 15), (-.5, 0, 0), (1, 8, 1))]),
        "left_hind_leg": (None, (1.1, 18, 5), (0, 0, 0), hind), "right_hind_leg": (None, (-1.1, 18, 5), (0, 0, 0), hind),
        "left_front_leg": (None, (1.2, 14.1, -5), (0, 0, 0), front), "right_front_leg": (None, (-1.2, 14.1, -5), (0, 0, 0), front),
    }


def cat_baby():
    return {
        "head": (None, (0, 20, -3.125), (0, 0, 0), [((0, 0), (-2.5, -3, -2.875), (5, 4, 4)), ((18, 0), (-2, -4, -.875), (1, 1, 2)),
                                                   ((24, 0), (1, -4, -.875), (1, 1, 2)), ((18, 3), (-1.5, -1, -3.875), (3, 2, 1))]),
        "left_front_leg": (None, (1, 22, -1.5), (0, 0, 0), [((18, 18), (-.5, 0, -1), (1, 2, 2))]),
        "right_front_leg": (None, (-1, 22, -1.5), (0, 0, 0), [((12, 18), (-.5, 0, -1), (1, 2, 2))]),
        "left_hind_leg": (None, (1, 22, 2.5), (0, 0, 0), [((18, 22), (-.5, 0, -1), (1, 2, 2))]),
        "body": (None, (0, 20.5, .5), (0, 0, 0), [((0, 8), (-2, -1.5, -3.5), (4, 3, 7))]),
        "right_hind_leg": (None, (-1, 22, 2.5), (0, 0, 0), [((12, 22), (-.5, 0, -1), (1, 2, 2))]),
        "tail1": (None, (0, 19.107, 3.9151), (-.567232, 0, 0), [((0, 18), (-.5, -.107, .0849), (1, 1, 5))]),
        "tail2": (None, (0, 0, 0), (0, 0, 0), []),
    }


# Bone name -> model part, per model.
BONE_PART = {"root": None, "head": "head", "body": "body", "upper_body": "upper_body", "tail": "tail",
             "right_front_leg": "right_front_leg", "left_front_leg": "left_front_leg",
             "right_hind_leg": "right_hind_leg", "left_hind_leg": "left_hind_leg"}
CAT_BONE_PART = {**BONE_PART, "tail": "tail1", "tail_tip": "tail2"}
# The middle of the body, which the root turns about (PetPoser.java keeps the same numbers).
PIVOT = {("dog", False): (0, 14, .5), ("dog", True): (0, 19, 0), ("cat", False): (0, 17, 1), ("cat", True): (0, 20.5, .5)}
BABY_OFFSETS = .5


def vanilla_pose(species, baby, sitting):
    """Mutable copies of each part's pose after the vanilla setupAnim for a standing (or sitting) tame pet."""
    model = (cat_baby if baby else cat_adult)() if species == "cat" else (wolf_baby if baby else wolf_adult)()
    pose = {name: [np.array(p[1], float), np.array(p[2], float)] for name, p in model.items()}
    if species == "dog":
        pose["tail"][1][0] = .55 * PI  # a tame, healthy wolf's tail angle
        if sitting:
            pose["body"][0] += (0, 4, -2)
            pose["body"][1][0] = PI / 4
            pose["tail"][0] += (0, 9, -2)
            for leg in ("right_hind_leg", "left_hind_leg"):
                pose[leg][0] += (0, 6.7, -5)
                pose[leg][1][0] = PI * 3 / 2
            for leg, dx in (("right_front_leg", .01), ("left_front_leg", -.01)):
                pose[leg][1][0] = 5.811947
                pose[leg][0] += (dx, 1, 0)
            if baby:
                pose["body"][1][0] -= PI / 2
            else:
                pose["upper_body"][0] += (0, 2, 0)
                pose["upper_body"][1][0] = PI * 2 / 5
    else:
        if not baby:
            pose["body"][1][0] = PI / 2
        pose["tail2"][1][0] = 1.7278761
        if sitting and not baby:
            pose["body"][1][0] = PI / 4
            pose["body"][0] += (0, -4, 5)
            pose["head"][0] += (0, -3.3, 1)
            pose["tail1"][0] += (0, 8, -2)
            pose["tail1"][1][0] = 1.7278761
            pose["tail2"][0] += (0, 2, -.8)
            pose["tail2"][1][0] = 2.670354
            for leg in ("left_front_leg", "right_front_leg"):
                pose[leg][1][0] = -PI / 20
                pose[leg][0] += (0, 2, -2)
            for leg in ("left_hind_leg", "right_hind_leg"):
                pose[leg][1][0] = -PI / 2
                pose[leg][0] += (0, 3, -4)
        elif sitting:
            pose["body"][1][0] += -0.43633232
            pose["body"][0] += (0, 1.25, 0)
            pose["head"][0] += (0, 0, .75)
    return model, pose


def rot(x, y, z):
    """ModelPart rotation: rotationZYX(z, y, x), i.e. Rz @ Ry @ Rx applied to a column vector."""
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    X = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Y = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Z = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Z @ Y @ X


class Track:
    """Monotone cubic sampler, identical to AnimationTrack.java."""

    def __init__(self, keys):
        self.t = np.array([k[0] for k in keys], float)
        self.v = np.array([k[1:] for k in keys], float)
        n = len(keys)
        m = np.zeros_like(self.v)
        for c in range(3):
            d = [(self.v[k + 1, c] - self.v[k, c]) / (self.t[k + 1] - self.t[k]) for k in range(n - 1)]
            for k in range(1, n - 1):
                m[k, c] = 0 if d[k - 1] * d[k] <= 0 else (d[k - 1] + d[k]) / 2
            for k in range(n - 1):
                if d[k] == 0:
                    m[k, c] = m[k + 1, c] = 0
                    continue
                a, b = m[k, c] / d[k], m[k + 1, c] / d[k]
                s = a * a + b * b
                if s > 9:
                    tau = 3 / math.sqrt(s)
                    m[k, c], m[k + 1, c] = tau * a * d[k], tau * b * d[k]
        self.m = m

    def __call__(self, x):
        t, v, m = self.t, self.v, self.m
        if len(t) == 1 or x <= t[0]:
            return v[0].copy()
        if x >= t[-1]:
            return v[-1].copy()
        k = int(np.searchsorted(t, x, side="right") - 1)
        h = t[k + 1] - t[k]
        s = (x - t[k]) / h
        h00, h10, h01, h11 = 2 * s**3 - 3 * s**2 + 1, s**3 - 2 * s**2 + s, -2 * s**3 + 3 * s**2, s**3 - s**2
        return h00 * v[k] + h10 * h * m[k] + h01 * v[k + 1] + h11 * h * m[k + 1]


def apply(trick, t, species, baby, pose):
    """PetPoser.apply: add the trick's rotations and offsets; returns the root (translation, rotation, scale)."""
    parts = CAT_BONE_PART if species == "cat" else BONE_PART
    scale = BABY_OFFSETS if baby else 1.0
    root_rot, root_pos = np.zeros(3), np.zeros(3)
    for channel, keys in trick["tracks"].items():
        bone, kind = channel.split(".")
        value = Track(keys)(t)
        if bone == "root":
            if kind == "rot":
                root_rot = value
            else:
                root_pos = value * scale
            continue
        part = parts.get(bone)
        if part is None or part not in pose:
            continue
        if kind == "rot":
            pose[part][1] = pose[part][1] + np.radians(value)
        else:
            pose[part][0] = pose[part][0] + value * scale
    t0, s = (np.array((0, 24.016 * .2, 0)), .8) if species == "cat" and not baby else (np.zeros(3), 1.0)
    R = rot(*np.radians(root_rot))
    c = np.array(PIVOT[(species, baby)], float)
    return t0 + s * (c - R @ c + root_pos), R, s


def texture(species, baby):
    jars = glob.glob(os.path.expanduser("~/.gradle/caches/fabric-loom/26.3/minecraft-client.jar")) + \
        glob.glob(str(ROOT.parents[2] / ".gradle/loom-cache/minecraftMaven/net/minecraft/minecraft-clientOnly-*/26.3/*.jar"))
    name = ("entity/cat/cat_tabby" if species == "cat" else "entity/wolf/wolf_tame") + ("_baby" if baby else "")
    for jar in jars:
        with zipfile.ZipFile(jar) as z:
            try:
                data = z.read(f"assets/minecraft/textures/{name}.png")
            except KeyError:
                continue
            return np.array(Image.open(io.BytesIO(data)).convert("RGBA"))
    raise SystemExit("Minecraft client jar not found in the Gradle cache; build the mod once first.")


def draw(canvas, species, baby, trick, t, cx, cy, scale, yaw, pitch, tex):
    sitting = trick.get("_sitting", False) if trick else False
    model, pose = vanilla_pose(species, baby, sitting)
    root_t, root_r, root_s = apply(trick, t, species, baby, pose) if trick else (
        (np.array((0, 24.016 * .2, 0)) if species == "cat" and not baby else np.zeros(3)), np.eye(3), .8 if species == "cat" and not baby else 1.0)
    view = rot(math.radians(pitch), 0, 0) @ rot(0, math.radians(yaw), 0)

    def transform(name):
        parent, *_ = model[name]
        pivot, angles = pose[name]
        R = rot(*angles)
        if parent is None:
            return lambda v: root_t + root_r @ (root_s * (pivot + R @ v)), root_r @ R
        pf, pr = transform(parent)
        return lambda v: pf(pivot + R @ v), pr @ R

    for name, (parent, _, _, cubes) in model.items():
        f, r = transform(name)
        for uv, origin, size in cubes:
            for verts, uvs, normal in P.cube_quads(origin, size, uv, 0):
                n = view @ (r @ np.array(normal, float))
                if n[2] >= -1e-6:
                    continue
                light = 0.58 + 0.30 * max(0, -n[1]) + 0.12 * max(0, -n[2]) + 0.06 * max(0, -n[0])
                pts = []
                for v in verts:
                    w = view @ (f(np.array(v, float)) - np.array((0, 24, 0)))
                    pts.append(np.array([cx + w[0] * scale, cy + w[1] * scale, w[2]]))
                canvas.quad(pts, uvs, tex, min(1.0, light))


SITTING = {("dog", "beg"), ("dog", "paw"), ("cat", "bat"), ("cat", "lean"), ("cat", "groom")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["sheet"])
    parser.add_argument("--species", default="")
    parser.add_argument("--tricks", default="")
    parser.add_argument("--baby", action="store_true")
    parser.add_argument("--frames", type=int, default=5)
    parser.add_argument("--yaw", type=float, default=-125)
    parser.add_argument("--scale", type=float, default=0)
    parser.add_argument("--out", default="")
    a = parser.parse_args()
    doc = json.loads(TRICKS.read_text(encoding="utf-8"))
    chosen = [t for t in doc["tricks"] if (not a.species or t["species"] == a.species)
              and (not a.tricks or t["id"] in a.tricks.split(","))]
    for t in chosen:
        t["_sitting"] = (t["species"], t["id"]) in SITTING
    scale = a.scale or (4.2 if not a.baby else 6)
    cw, ch = int(36 * scale), int(31 * scale)
    canvas = P.Canvas(a.frames * cw + 150, max(1, len(chosen)) * ch + ch // 3)
    labels = []
    textures = {}
    for row, t in enumerate(chosen):
        tex = textures.setdefault(t["species"], texture(t["species"], a.baby))
        labels.append((75, row * ch + ch // 2 - 6, f"{t['species']} {t['id']}"))
        for i in range(a.frames):
            time = t["length"] * i / max(1, a.frames - 1) if a.frames > 1 else 0
            draw(canvas, t["species"], a.baby, t, time, 150 + i * cw + cw // 2, row * ch + ch - 22, scale, a.yaw, -14, tex)
    out = Path(a.out or SCRATCH / f"tricks{'_' + a.species if a.species else ''}{'_baby' if a.baby else ''}.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    P.save(canvas, labels, out)
    print(out)


if __name__ == "__main__":
    main()
