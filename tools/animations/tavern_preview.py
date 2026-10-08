#!/usr/bin/env python3
"""Check and preview the Tavern animation pack the way the game plays it: SEATED.

    python tools/animations/tavern_preview.py                         # check all modules, a sheet per module
    python tools/animations/tavern_preview.py --module dining --clips sip_the_drink,big_gulp --frames 8
    python tools/animations/tavern_preview.py --module dining --probe sip_the_drink   # hands and mouth over time

Seated clips (those that require "seated") are drawn on vanilla's riding pose: both arms pitched 36 degrees
forward, legs pitched 81 degrees forward and splayed 18 degrees, with the clip's leg and root tracks ignored
(the poser ignores them while seated). The figure sits on a stair chair with a fence-and-plate table in front,
at the heights the Seat entity gives a villager (feet 0.32 of their height below the seat surface). Every
frame shows a three-quarter view and the right side (the side view also shows the table).

Eating and drinking clips carry a stand-in dish in the right hand where vanilla draws a held flat item
(ItemInHandLayer plus item/generated's third-person transform). Standing patrons at the bar carry their drink
in the right hand all the time: vanilla's held-item pose (-18 degrees) is their right arm's base, and clips
that keep items leave that arm alone.

The checker adds the tavern rules to the compiler's: known tags, lengths 2.5-7 s, greetings require an age,
seated clips never key legs or root, eating and drinking clips hold the dish in the right hand
(mirror "hand", items "override"), bar clips avoid "seated". It also warns when an arm passes through the
torso, the head or the table top.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import numpy as np

TOOL = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL))
import kit  # noqa: E402
import animations  # noqa: E402

PACK = "tavern"
OUT = animations.ROOT / "build/previews"
TAG = re.compile(r"(adult|child|smith|guard|social|holding|rain|thunder|cold|morning|day|evening|night|seated|tavern|"
                 r"music|hearth|dining:(wait|eat|drink|done|carry)|food:(stew|pie|bread|platter|tart)|"
                 r"drink:(cider|coffee)|job:[a-z_]+|personality:[a-z]+|routine:[a-z_]+)")
RIDE_ARM = -36.0                      # vanilla riding pose: both arms pitch this far forward
RIDE_LEGS = {"right_leg": (-81.0, 18.0, 4.5), "left_leg": (-81.0, -18.0, -4.5)}
ITEM_ARM = -18.0                      # vanilla held-item pose for a standing arm (pitch * .5 - 18)
BLOCK = 16 / .9375                    # model pixels per block (residents render at 15/16 scale)

# Seated scene in model pixels (y down, z forward negative), from Seat.positionRider and the stair-chair taverns.
FLOOR_SEATED = 24 - (1.95 * .32 - .5) * BLOCK      # feet sit 0.32 * height below a half-block seat surface
TABLE_TOP = FLOOR_SEATED - 17 / 16 * BLOCK          # fence plus pressure plate
SEAT_TOP = FLOOR_SEATED - .5 * BLOCK
TABLE_NEAR = -(.5 + 1 / 16) * BLOCK                 # the plate starts a sixteenth into the next block
TABLE_FAR = -(1.5 - 1 / 16) * BLOCK
COUNTER_TOP = 24 - BLOCK                            # a bar counter (one block high) in front of a standing patron
COUNTER_NEAR = -.5 * BLOCK

MOUTH = np.array([0, -1.6, -4.2])                   # head space
HAND = {"right_arm": np.array([-1, 9.5, 0]), "left_arm": np.array([1, 9.5, 0])}
PROP_CENTER = np.array([-1, 9, -5.0])               # right-arm space: vanilla's held flat item
PROP_BOX = ((-3.75, 8.6, -7.75), (5.5, .8, 5.5))


def load(modules):
    entries = []
    for name in modules:
        kit.CLIPS.clear()
        spec = importlib.util.spec_from_file_location(f"{PACK}.{name}", TOOL / PACK / f"{name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        entries += [(name, c) for c in kit.CLIPS]
    kit.CLIPS.clear()
    return entries


def tags_of(c):
    return [t for group in c.require for t in group.split("|")]


def seated(c):
    return "seated" in c.require


def holds_dish(c):
    return any(t in ("dining:eat", "dining:drink") for t in tags_of(c))


def bar_patron(c):
    return not seated(c) and "tavern" in tags_of(c) and "holding" not in c.avoid


def check(entries):
    errors = animations.validate([c for _, c in entries])
    for module, c in entries:
        data = c.compile()
        tracks = data["tracks"]
        if not re.fullmatch(r"[a-z0-9_]+", c.id):
            errors.append(f"{c.id}: ids are lowercase letters, digits and underscores")
        if not 2.5 <= c.length <= 7:
            errors.append(f"{c.id}: tavern clips last 2.5 to 7 seconds ({c.length})")
        if "," in c.name:
            errors.append(f"{c.id}: clip names never contain commas")
        unknown = [t for t in tags_of(c) + list(c.avoid) + list(c.boost) if not TAG.fullmatch(t)]
        errors += [f"{c.id}: unknown tag {t!r}" for t in unknown]
        if c.trigger == "greet" and not any("adult" in g.split("|") or "child" in g.split("|") for g in c.require):
            errors.append(f"{c.id}: greetings require an age")
        if module != "bar" and not seated(c):
            errors.append(f"{c.id}: every clip in {module}.py requires \"seated\" as its own entry")
        if seated(c):
            keyed = sorted({k for k in tracks if k.split(".")[0] in ("right_leg", "left_leg", "root")})
            if keyed:
                errors.append(f"{c.id}: seated clips never key legs or root ({', '.join(keyed)})")
        if module == "bar" and "seated" not in c.avoid:
            errors.append(f"{c.id}: bar clips avoid \"seated\"")
        if holds_dish(c) and (seated(c) or bar_patron(c)):
            if c.mirror != "hand" or c.items != "override":
                errors.append(f"{c.id}: the dish is in the right hand: mirror \"hand\" and items \"override\"")
            if "right_arm.rot" not in tracks:
                errors.append(f"{c.id}: the right arm holds the dish and must move it")
        for k, keys in tracks.items():
            if keys[0][0] != 0 or any(v != 0 for v in keys[0][1:]) or any(v != 0 for v in keys[-1][1:]):
                errors.append(f"{c.id}: {k} must start and end at rest")
    return errors


# -- posing --------------------------------------------------------------------------------------
class Scene:
    def __init__(self):
        sys.modules.pop("kit", None)   # the wardrobe has its own kit module
        spec = importlib.util.spec_from_file_location("animation_preview", TOOL / "preview.py")
        self.V = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.V)
        self.P = self.V.P
        self.who = self.V.Resident(3)
        self.solid = {}

    def compiled(self, c):
        d = c.compile()
        d["_tracks"] = {k: self.V.Track(v) for k, v in d["tracks"].items()}
        d["_seated"], d["_dish"], d["_patron"] = seated(c), holds_dish(c), bar_patron(c)
        d["_items"] = c.items
        return d

    def pose(self, d, t):
        rot, pos, lid, look = self.V.sample(d, t)
        if d["_seated"]:
            for b in ("right_leg", "left_leg", "root"):
                rot[b][:] = 0
                pos[b][:] = 0
            for b, r in RIDE_LEGS.items():
                rot[b] += r
            rot["right_arm"][0] += RIDE_ARM
            rot["left_arm"][0] += RIDE_ARM
        elif d["_patron"]:
            if d["_items"] != "override":
                rot["right_arm"][:] = 0
                pos["right_arm"][:] = 0
            rot["right_arm"][0] += ITEM_ARM
        bones, rp, rr = self.V.pose(rot, pos)
        return bones, rp, rr

    @staticmethod
    def world(bones, rp, rr, bone, local):
        bp, br = bones[bone]
        return rp + rr @ (bp + br @ np.asarray(local, float))

    def has_prop(self, d):
        return d["_dish"] or d["_patron"]

    # -- drawing -------------------------------------------------------------------------------
    def texture(self, rgb):
        if rgb not in self.solid:
            tex = np.zeros((128, 128, 4), np.uint8)
            tex[..., :3] = rgb
            tex[..., 3] = 255
            self.solid[rgb] = tex
        return self.solid[rgb]

    def box(self, canvas, view, cx, cy, scale, origin, size, rgb, to_world=lambda v: v):
        tex = self.texture(rgb)
        for verts, uvs, normal in self.P.cube_quads(origin, size, (0, 0), 0):
            world = [to_world(np.asarray(v, float)) for v in verts]
            n = view @ (to_world(np.asarray(normal, float)) - to_world(np.zeros(3)))
            if n[2] >= -1e-6:
                continue
            light = 0.58 + 0.30 * max(0, -n[1]) + 0.12 * max(0, -n[2]) + 0.06 * max(0, -n[0])
            pts = [np.array([cx + (view @ w)[0] * scale, cy + (view @ w)[1] * scale, (view @ w)[2]]) for w in world]
            canvas.quad(pts, uvs, tex, min(1.0, light))

    def render(self, canvas, d, t, cx, cy, scale, yaw, pitch, props=True):
        bones, rp, rr = self.pose(d, t)
        view = self.P.rot(pitch, 0, 0) @ self.P.rot(0, yaw, 0)
        self.V.draw(canvas, self.who.skin, self.who.pieces, cx, cy, scale, yaw, pitch, bones, rp, rr)
        if d["_seated"]:
            wood, dark = (150, 104, 62), (112, 76, 44)
            self.box(canvas, view, cx, cy, scale, (-8.5, SEAT_TOP, -8.5), (17, FLOOR_SEATED - SEAT_TOP, 17), wood)
            if props:
                self.box(canvas, view, cx, cy, scale, (-8, TABLE_TOP, TABLE_FAR), (16, 1.07, TABLE_NEAR - TABLE_FAR), wood)
                mid = (TABLE_NEAR + TABLE_FAR) / 2
                self.box(canvas, view, cx, cy, scale, (-1.1, TABLE_TOP + 1.07, mid - 1.1),
                         (2.2, FLOOR_SEATED - TABLE_TOP - 1.07, 2.2), dark)
        elif props:
            stone = (128, 116, 104)
            self.box(canvas, view, cx, cy, scale, (-8.5, COUNTER_TOP, COUNTER_NEAR - BLOCK), (17, BLOCK, BLOCK), stone)
        if self.has_prop(d):
            rgb = (214, 150, 44) if d["_patron"] or "drink" in d["id"] or any(
                "dining:drink" in g for g in d.get("require", [])) else (176, 92, 52)
            self.box(canvas, view, cx, cy, scale, *PROP_BOX, rgb,
                     to_world=lambda v: self.world(bones, rp, rr, "right_arm", v))

    # -- measuring ------------------------------------------------------------------------------
    def measure(self, d, t):
        bones, rp, rr = self.pose(d, t)
        out = {"mouth": self.world(bones, rp, rr, "head", MOUTH)}
        for arm, local in HAND.items():
            out[arm] = self.world(bones, rp, rr, arm, local)
        out["prop"] = self.world(bones, rp, rr, "right_arm", PROP_CENTER)
        out["hits"] = []
        for arm, sx in (("right_arm", -1), ("left_arm", 1)):
            for y in np.linspace(3, 10, 8):
                p = self.world(bones, rp, rr, arm, (sx, y, 0))
                for part, lo, hi in (("body", (-4, 0, -2), (4, 12, 2)), ("head", (-4, -8, -4), (4, 0, 4))):
                    bp, br = bones[part]
                    q = br.T @ (rr.T @ (p - rp) - bp)
                    if all(lo[i] + .45 < q[i] < hi[i] - .45 for i in range(3)):
                        out["hits"].append(f"{arm} in {part}")
                if d["_seated"] and abs(p[0]) < 8 and TABLE_FAR < p[2] < TABLE_NEAR and TABLE_TOP + .2 < p[1] < TABLE_TOP + 1.6:
                    out["hits"].append(f"{arm} through the table")
        return out


def summarize(scene, d):
    steps = np.linspace(0, d["length"], int(d["length"] * 20) + 1)
    best = {"right_arm": (1e9, 0), "left_arm": (1e9, 0), "prop": (1e9, 0)}
    hits = {}
    for t in steps:
        m = scene.measure(d, t)
        for k in best:
            dist = float(np.linalg.norm(m[k] - m["mouth"]))
            if dist < best[k][0]:
                best[k] = (dist, t)
        for h in m["hits"]:
            hits.setdefault(h, []).append(t)
    parts = [f"R hand {best['right_arm'][0]:.1f}px@{best['right_arm'][1]:.2f}s",
             f"L hand {best['left_arm'][0]:.1f}px@{best['left_arm'][1]:.2f}s"]
    if scene.has_prop(d):
        parts.append(f"dish {best['prop'][0]:.1f}px@{best['prop'][1]:.2f}s")
    warn = []
    for h, ts in hits.items():   # contiguous runs of samples, so passing moments read differently from holds
        runs, start = [], ts[0]
        for a, b in zip(ts, ts[1:] + [None]):
            if b is None or b - a > .06:
                runs.append(f"{start:.2f}-{a:.2f}s" if a > start else f"{a:.2f}s")
                start = b
        warn.append(f"{h} {', '.join(runs)}")
    return "  ".join(parts), warn


def probe(scene, d, step=.2):
    print(f"{d['id']}: time  R hand (x y z)      L hand (x y z)      dish (x y z)        mouth (x y z)")
    for t in np.arange(0, d["length"] + 1e-6, step):
        m = scene.measure(d, t)
        f = lambda v: f"({v[0]:5.1f} {v[1]:5.1f} {v[2]:5.1f})"
        print(f"  {t:4.2f}  {f(m['right_arm'])}  {f(m['left_arm'])}  {f(m['prop'])}  {f(m['mouth'])}"
              f"  {'; '.join(sorted(set(m['hits'])))}")


def sheet(scene, chosen, out, frames, scale, times=None, yaw=-30):
    s = scale
    side_w, front_w, row_h = int(36 * s), int(24 * s), int(40 * s) + 30
    cw = side_w + front_w
    canvas = scene.P.Canvas(frames * cw + 200, len(chosen) * row_h)
    labels = []
    for row, d in enumerate(chosen):
        top = row * row_h
        floor = FLOOR_SEATED if d["_seated"] else 24
        cy = top + int((17 if d["_seated"] else 14) * s)
        ts = times or [d["length"] * (i + 1) / (frames + 1) for i in range(frames)]
        for col, t in enumerate(ts):
            x0 = 200 + col * cw
            scene.render(canvas, d, t, x0 + front_w // 2, cy, s, yaw=yaw, pitch=4, props=False)
            scene.render(canvas, d, t, x0 + front_w + int(10 * s), cy, s, yaw=-90, pitch=10)
            labels.append((x0 + cw // 2, top + row_h - 16, f"{t:.2f}s"))
        labels.append((100, top + 30, d["id"]))
        labels.append((100, top + 44, f"{d['trigger']}  w={d['weight']}  {d['length']}s"))
        req = " ".join(d.get("require", []))
        for i in range(0, min(len(req), 90), 30):
            labels.append((100, top + 58 + i // 30 * 14, req[i:i + 30]))
        if d.get("avoid"):
            labels.append((100, top + 102, "avoid " + " ".join(d["avoid"])[:26]))
        del floor
    out.parent.mkdir(parents=True, exist_ok=True)
    scene.P.save(canvas, labels, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", default="", help="one module (default: every module in the pack)")
    ap.add_argument("--clips", default="", help="comma-separated clip ids")
    ap.add_argument("--frames", type=int, default=6)
    ap.add_argument("--at", default="", help="comma-separated sample times instead of evenly spaced frames")
    ap.add_argument("--scale", type=float, default=3.4)
    ap.add_argument("--yaw", type=float, default=-30, help="three-quarter view angle (30 shows the left hand)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--probe", default="", help="print hand, dish and mouth positions over time for these clips")
    ap.add_argument("--no-sheet", action="store_true")
    a = ap.parse_args()
    modules = [a.module] if a.module else animations.PACKS[PACK]["modules"]
    entries = load(modules)
    errors = check(entries)
    wanted = [x for x in a.clips.split(",") if x]
    scene = Scene()
    by_module = {}
    for module, c in entries:
        if wanted and c.id not in wanted:
            continue
        d = scene.compiled(c)
        by_module.setdefault(module, []).append(d)
        summary, warn = summarize(scene, d)
        req = " ".join(c.require)
        print(f"  {module:7} {c.trigger:11} {c.id:28} {c.length:4.1f}s w={c.weight:<4} {req}")
        print(f"          {summary}" + (f"\n          WARN {'; '.join(warn)}" if warn else ""))
    for name in [x for x in a.probe.split(",") if x]:
        for ds in by_module.values():
            for d in ds:
                if d["id"] == name:
                    probe(scene, d)
    if errors:
        print("\nERRORS:\n" + "\n".join("  " + e for e in errors))
    else:
        print(f"OK: {len(entries)} clips valid")
    if not a.no_sheet:
        times = [float(x) for x in a.at.split(",") if x] or None
        for module, ds in by_module.items():
            out = Path(a.out) if a.out and len(by_module) == 1 else OUT / f"tavern_{module}.png"
            sheet(scene, ds, out, len(times) if times else a.frames, a.scale, times, a.yaw)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
