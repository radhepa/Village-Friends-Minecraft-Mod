"""Render a small README wardrobe gallery from the current garment sources.

Run from the repository root with Python, Pillow and NumPy installed.
Uses the existing offline renderer; this is an asset preview, not a game capture.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "wardrobe"))

import preview as P
import wardrobe as W
from PIL import Image, ImageDraw, ImageFont


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts") / ("georgiab.ttf" if bold else "segoeui.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def main():
    selections = [
        ("arcanist", "h09_curtain_part", "SCHOLARLY_PLUM", "ESPRESSO", 2),
        ("f_court_lady", "hf02_long_waves", "ROYAL_VELVET", "AUBURN", 0),
        ("m_pikeman", "h07_swept_undercut", "TANNER_AMBER", "RAVEN", 4),
        ("f_flask_physician", "hf01_very_long_straight", "SAGE_AND_TERRACOTTA", "ESPRESSO", 3),
        ("m_plain_tee_jeans", "h04_tousled_crop", "WASHED_INDIGO_AND_CREAM", "CHESTNUT", 1),
        ("f_huntress", "hf02_long_waves", "FOREST_AND_HEARTH", "HONEY", 5),
    ]
    outfits = {o["id"]: o for o in W.load_templates()["outfits"]}
    wanted = {part for oid, hair, *_ in selections for part in (outfits[oid]["top"], outfits[oid]["bottom"], hair)}
    garments = W.build_all(wanted)
    palettes, colors = W.load_palettes(), W.load_hair_colors()
    canvas = P.Canvas(1560, 650, bg=(245, 239, 222))
    for i, (oid, hair, palette, color, skin) in enumerate(selections):
        outfit = outfits[oid]
        P.figure(canvas, 130 + i * 260, 267, 11.5,
                 garments[outfit["top"]], garments[outfit["bottom"]], garments[hair],
                 palettes[palette], colors[color]["ramp"], complexion=skin, yaw=-22, pitch=-8)
    result = Image.fromarray(canvas.img.clip(0, 255).astype("uint8"))
    draw = ImageDraw.Draw(result)
    draw.text((42, 29), "A wardrobe full of character.", font=font(30, True), fill="#29483d")
    draw.text((44, 80), "A few looks from the current Village Friends collection", font=font(19), fill="#6b705a")
    draw.line((44, 122, 1516, 122), fill="#d3c9ad", width=2)
    for i, (oid, _, palette, *_) in enumerate(selections):
        x = 130 + i * 260
        draw.text((x, 570), outfits[oid]["name"], font=font(19, True), fill="#29483d", anchor="mt")
        draw.text((x, 602), palettes[palette]["name"], font=font(15), fill="#6b705a", anchor="mt")
    output = ROOT / "docs/assets/wardrobe-gallery.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, optimize=True)
    print(output)


if __name__ == "__main__":
    main()
