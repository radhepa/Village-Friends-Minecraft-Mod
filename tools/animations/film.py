#!/usr/bin/env python3
"""Assemble the animation pack showcase film from frames captured in Minecraft.

    gradlew runClientGameTest -PanimationVideo        # writes build/run/clientGameTest/film/*.png
    python tools/animations/film.py [--out build/film/village-life.mp4]

Adds title, chapter and end cards, crossfades between sections and encodes H.264 (30 fps) with
ffmpeg. Frames are 1280x720 PNGs named <scene>_<number>.png.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "build/run/clientGameTest/film"
FPS, W, H = 30, 1280, 720
INK, PAPER, GOLD, MUTED = (70, 49, 36), (244, 232, 207), (176, 126, 72), (104, 86, 64)


def font(size, bold=False):
    names = ["georgiab.ttf", "timesbd.ttf"] if bold else ["georgia.ttf", "times.ttf"]
    for name in names:
        for folder in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")):
            if (folder / name).exists():
                return ImageFont.truetype(str(folder / name), size)
    return ImageFont.load_default()


def card(lines, backdrop: Image.Image | None = None):
    """A parchment card, optionally over a softened still from the film."""
    if backdrop is not None:
        img = backdrop.convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(10))
        img = Image.blend(img, Image.new("RGB", (W, H), PAPER), .74)
    else:
        img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=3)
    d.rectangle([52, 52, W - 52, H - 52], outline=(214, 190, 150), width=1)
    total = sum(size + gap for _, size, _, gap in lines)
    y = (H - total) // 2
    for text, size, color, gap in lines:
        f = font(size, bold=size >= 40)
        w = d.textlength(text, font=f)
        d.text(((W - w) / 2, y), text, font=f, fill=color)
        y += size + gap
    return img


def scene_frames(name):
    return sorted(FRAMES.glob(f"{name}_*.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "build/film/village-life-animation-pack.mp4"))
    ap.add_argument("--crf", default="21")
    ap.add_argument("--skip-village", type=int, default=54, help="frames to drop while the renderer settles")
    a = ap.parse_args()
    gallery, village = scene_frames("gallery"), scene_frames("village")[a.skip_village:]
    if not gallery and not village:
        sys.exit(f"No frames in {FRAMES}; run gradlew runClientGameTest -PanimationVideo first.")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    encoder = subprocess.Popen([ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-c:v", "libx264", "-preset", "slow", "-crf", a.crf, "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                                str(out)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    out_index = 0

    def emit(img):
        nonlocal out_index
        encoder.stdin.write(img.convert("RGB").resize((W, H)).tobytes())
        out_index += 1

    def hold(img, seconds):
        for _ in range(int(seconds * FPS)):
            emit(img)

    def fade(a_img, b_img, seconds=.6):
        n = int(seconds * FPS)
        for i in range(1, n + 1):
            emit(Image.blend(a_img.convert("RGB"), b_img.convert("RGB"), i / (n + 1)))

    def play(paths, fade_in_from=None):
        first = Image.open(paths[0])
        if fade_in_from is not None:
            fade(fade_in_from, first)
        for p in paths:
            emit(Image.open(p))
        return Image.open(paths[-1])

    title_bg = Image.open(village[len(village) // 5]) if village else None
    title = card([("VILLAGE FRIENDS", 26, GOLD, 18), ("Village Life", 64, INK, 14),
                  ("Animation Pack 1", 30, INK, 34),
                  ("90 motions  -  99 clips  -  every personality, every profession", 22, MUTED, 10),
                  ("Residents now idle, work, chat, greet you, react and play.", 22, MUTED, 0)], title_bg)
    hold(title, 3.6)
    last = title
    if gallery:
        last = play(gallery, fade_in_from=last)
    if village:
        chapter = card([("In the village", 54, INK, 18),
                        ("Nobody here is scripted: each resident chooses what to do from", 22, MUTED, 8),
                        ("their job, personality, the weather, a neighbor beside them - and you.", 22, MUTED, 0)],
                       Image.open(village[len(village) // 6]))
        fade(last, chapter)
        hold(chapter, 3.0)
        last = play(village, fade_in_from=chapter)
    end = card([("Village Life", 56, INK, 14), ("Animation Pack 1 for Village Friends", 26, INK, 30),
                ("Packs live in assets/<namespace>/resident_animations/ - resource packs can add more.", 20, MUTED, 0)],
               last)
    fade(last, end, .8)
    hold(end, 3.2)

    encoder.stdin.close()
    if encoder.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"{out}  ({out_index} frames, {out_index / FPS:.1f}s)")


if __name__ == "__main__":
    main()
