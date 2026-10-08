#!/usr/bin/env python3
"""Offline animation previews using the wardrobe's tiny renderer and the same posing rules as
ResidentPoser (waist bends at the hips, root pivots at the feet). For fast iteration only; the
in-game gallery (gradlew runClientGameTest -PanimationPack) is the source of truth.

    python tools/animations/preview.py sheet [--only everyday] [--clips wave_hello,cheer]
    python tools/animations/preview.py gif --clips wave_hello,cheer [--child]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

TOOL = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL.parent / "wardrobe"))
import preview as P  # noqa: E402  (the wardrobe preview)
import wardrobe as W  # noqa: E402

PACK = W.ROOT / "src/main/resources/assets/villagefriends/resident_animations/village_life.json"
SCRATCH = W.ROOT / "build/animation-preview"
BONES = ("root", "waist", "body", "head", "right_arm", "left_arm", "right_leg", "left_leg")
MODEL_BONE = {"HEAD": "head", "TORSO": "body", "RIGHT_ARM": "right_arm", "LEFT_ARM": "left_arm",
              "RIGHT_LEG": "right_leg", "LEFT_LEG": "left_leg"}


class Track:
    """Monotone cubic sampler, identical to AnimationTrack.java."""

    def __init__(self, keys):
        self.t = np.array([k[0] for k in keys], float)
        v = np.zeros((len(keys), 3))
        for i, k in enumerate(keys):
            v[i, :len(k) - 1] = k[1:]
        self.v = v
        n = len(keys)
        m = np.zeros_like(v)
        for c in range(3):
            d = [(v[k + 1, c] - v[k, c]) / (self.t[k + 1] - self.t[k]) for k in range(n - 1)]
            for k in range(1, n - 1):
                m[k, c] = 0 if d[k - 1] * d[k] <= 0 else (d[k - 1] + d[k]) / 2
            for k in range(n - 1):
                if d[k] == 0:
                    m[k, c] = m[k + 1, c] = 0
                    continue
                a, b = m[k, c] / d[k], m[k + 1, c] / d[k]
                s = a * a + b * b
                if s > 9:
                    tau = 3 / np.sqrt(s)
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


def load_pack(path=PACK):
    doc = json.loads(path.read_text(encoding="utf-8"))
    clips = {}
    for c in doc["clips"]:
        c["_tracks"] = {k: Track(v) for k, v in c["tracks"].items()}
        clips[c["id"]] = c
    return clips


def sample(clip, t, mirror=False):
    rot = {b: np.zeros(3) for b in BONES}
    pos = {b: np.zeros(3) for b in BONES}
    lid, look = 0.0, np.zeros(2)
    for key, track in clip["_tracks"].items():
        bone, channel = key.split(".")
        value = track(t)
        if bone == "eyes":
            if channel == "lid":
                lid = value[0]
            else:
                look = value[:2] * (-1 if mirror else 1, 1)
            continue
        if mirror:
            bone = {"right_arm": "left_arm", "left_arm": "right_arm", "right_leg": "left_leg", "left_leg": "right_leg"}.get(bone, bone)
            value = value * ((1, -1, -1) if channel == "rot" else (-1, 1, 1))
        (rot if channel == "rot" else pos)[bone] += value
    return rot, pos, lid, look


def pose(rot, pos, scale=1.0, leg_y=12.0):
    """Bone pivot positions and rotation matrices after ResidentPoser's rules."""
    pivots = {"head": (0, 0, 0), "body": (0, 0, 0), "right_arm": (-5, 2, 0), "left_arm": (5, 2, 0),
              "right_leg": (-1.9, 12, 0), "left_leg": (1.9, 12, 0)}
    bones = {}
    for b, p in pivots.items():
        bones[b] = [np.array(p, float) + pos[b] * scale, P.rot(*rot[b])]
    hip = np.array([0, leg_y, 0.0])
    waist = P.rot(*rot["waist"])
    for b in ("body", "head", "right_arm", "left_arm"):
        bones[b][0] = hip + waist @ (bones[b][0] - hip)
        bones[b][1] = waist @ bones[b][1]
    feet = np.array([0, 24, 0.0])
    root_r = P.rot(*rot["root"])
    root_p = feet + root_r @ (np.zeros(3) - feet) + pos["root"] * scale
    return bones, root_p, root_r


def draw(canvas, skin, pieces, cx, cy, scale, yaw, pitch, bones, root_p, root_r):
    view = P.rot(pitch, 0, 0) @ P.rot(0, yaw, 0)
    items = [(MODEL_BONE[bone], np.zeros(3), np.eye(3), o, s, uv, g, None, skin) for _, bone, o, s, uv, g in P.PARTS]
    for p, tex in pieces:
        rx, ry, rz = p.rotation
        items.append((MODEL_BONE[p.bone], np.array(p.pivot, float), P.rot(rx, ry, rz), p.origin, p.size, p.box.u_v, p.inflate, p.scale, tex))
    for bone, ppivot, prot, origin, size, uv, inflate, pscale, tex in items:
        bp, br = bones[bone]
        for verts, uvs, normal in P.cube_quads(origin, size, uv, inflate, pscale or (1, 1, 1)):
            world = [root_p + root_r @ (bp + br @ (ppivot + prot @ v)) for v in verts]
            n = view @ (root_r @ (br @ (prot @ np.array(normal, float))))
            if n[2] >= -1e-6:
                continue
            light = 0.58 + 0.30 * max(0, -n[1]) + 0.12 * max(0, -n[2]) + 0.06 * max(0, -n[0])
            pts = [np.array([cx + (view @ w)[0] * scale, cy + (view @ w)[1] * scale, (view @ w)[2]]) for w in world]
            canvas.quad(pts, uvs, tex, min(1.0, light))


class Resident:
    def __init__(self, index=0):
        garments = W.build_all()
        palettes, hairs = W.load_palettes(), W.load_hair_colors()
        catalog = W.load_templates()
        outfit = catalog["outfits"][index % len(catalog["outfits"])]
        hair = [g for g in garments.values() if g.kind == "hair"][index * 7 % 30]
        top, bottom = garments[outfit["top"]], garments[outfit["bottom"]]
        pal = palettes[list(palettes)[index % len(palettes)]]
        ramp = hairs[list(hairs)[index % len(hairs)]]["ramp"]
        self.skin = P.skin_texture(index % 6, P.layering(top, bottom, hair), pal, ramp)
        self.pieces = [(p, P.resolve(g.extras, pal, ramp)) for g in (top, bottom, hair) for p in g.pieces]


def render_frame(canvas, who, clip, t, cx, cy, scale, yaw=-30, pitch=-8, mirror=False):
    rot, pos, lid, look = sample(clip, t, mirror) if clip else ({b: np.zeros(3) for b in BONES}, {b: np.zeros(3) for b in BONES}, 0, 0)
    bones, rp, rr = pose(rot, pos)
    draw(canvas, who.skin, who.pieces, cx, cy, scale, yaw, pitch, bones, rp, rr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sheet", "gif"])
    ap.add_argument("--clips", default="")
    ap.add_argument("--only", default="", help="clip id prefix filter or trigger name")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--yaw", type=float, default=-30)
    ap.add_argument("--out", default=None)
    ap.add_argument("--scale", type=float, default=5.2)
    a = ap.parse_args()
    clips = load_pack()
    chosen = [clips[c] for c in a.clips.split(",") if c] if a.clips else list(clips.values())
    if a.only:
        chosen = [c for c in chosen if c["trigger"] == a.only or c["id"].startswith(a.only)]
    who = Resident(3)
    if a.mode == "sheet":
        sc = a.scale
        cw, ch = int(150 * sc / 5.2), int(230 * sc / 5.2)
        cols = a.frames
        canvas = P.Canvas(cols * cw + 170, len(chosen) * ch)
        labels = []
        for row, c in enumerate(chosen):
            for col in range(cols):
                t = c["length"] * (col + 1) / (cols + 1)
                render_frame(canvas, who, c, t, 170 + col * cw + cw // 2, row * ch + int(70 * sc / 5.2), sc, yaw=a.yaw)
                labels.append((170 + col * cw + cw // 2, row * ch + ch - 18, f"{t:.2f}s"))
            labels.append((85, row * ch + 100, c["id"]))
            labels.append((85, row * ch + 114, c["trigger"]))
        P.save(canvas, labels, Path(a.out or SCRATCH / f"sheet{'_' + a.only if a.only else ''}.png"))
    else:
        cols = min(4, len(chosen))
        rows = (len(chosen) + cols - 1) // cols
        cw, ch, sc = 240, 330, 8
        length = max(c["length"] for c in chosen) + .4
        frames = []
        for f in range(int(length * 15)):
            t = f / 15
            canvas = P.Canvas(cols * cw, rows * ch)
            for i, c in enumerate(chosen):
                render_frame(canvas, who, c, min(t, c["length"]), (i % cols) * cw + cw // 2, (i // cols) * ch + 110, sc, yaw=a.yaw)
            img = Image.fromarray(canvas.img.clip(0, 255).astype(np.uint8))
            for i, c in enumerate(chosen):
                P.label(img, (i % cols) * cw + cw // 2, (i // cols) * ch + 310, c["name"])
            frames.append(img)
        out = Path(a.out or SCRATCH / "clips.gif")
        out.parent.mkdir(parents=True, exist_ok=True)
        frames[0].save(out, save_all=True, append_images=frames[1:], duration=66, loop=0)
        print(out)


if __name__ == "__main__":
    main()
