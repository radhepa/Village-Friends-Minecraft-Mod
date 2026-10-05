# Editing the wardrobe

Every hairstyle, top and bottom is one Python module that paints pixel art and declares 3D pieces. Keep each piece self-contained so it can be replaced on its own. Read [OUTFIT_ENGINE.md](OUTFIT_ENGINE.md) for how the game uses the output.

| What | Where |
|---|---|
| Hairstyles | `tools/wardrobe/hair/hNN_name.py` |
| Tops | `tools/wardrobe/tops/tNN_name.py` |
| Bottoms | `tools/wardrobe/bottoms/bNN_name.py` |
| Outfit templates and profession mapping | `tools/wardrobe/outfits.json` |
| Master palettes (base colors or explicit ramps) | `tools/wardrobe/palettes.json` |
| Natural hair colors (five-shade ramps) | `tools/wardrobe/hair_colors.json` |
| Shared brushes (cloth, hems, hair strands, curls, scalp) | `tools/wardrobe/paint.py` |
| Garment building blocks (bodies, necklines, sleeves, belts, skirt flaps, legs, footwear) | `tools/wardrobe/kit.py` |
| Anime hair building blocks (cel shading, sheen ring, pointed locks, bangs, sidelocks) | `tools/wardrobe/anime.py` |
| Compiler, key colors, validation | `tools/wardrobe/wardrobe.py` |
| Offline 3D previews | `tools/wardrobe/preview.py` |
| Compiled runtime assets (do not hand-edit) | `src/main/resources/assets/villagefriends/wardrobe/` |

## Workflow

```text
python tools/wardrobe/wardrobe.py --only t03_arcanist_longcoat   # rebuild one piece
python tools/wardrobe/wardrobe.py                                # rebuild everything and the catalog
python tools/wardrobe/wardrobe.py --check                        # validate; fail if outputs are stale
python tools/wardrobe/preview.py one --top t03_arcanist_longcoat --bottom b03_scholars_slacks --hair h03_voluminous_curls
python tools/wardrobe/preview.py outfits | hair | tops | bottoms [--back] [--ids t2 b15] | mix [--walk]
```

The tools need Python 3 with Pillow and NumPy. Previews go to `build/wardrobe-preview/` unless you pass `--out`. They are for fast iteration only; confirm in Minecraft with `gradlew.bat runClientGameTest -PoutfitsOnly`, which saves screenshots to `build/run/clientGameTest/screenshots/`.

## Writing a piece

A module defines `META` (`name`, `description`, `tags`, optional `requires`/`rejects`, and for tops `tucked`/`covers_waist`) and a `build(g)` function:

- `g.part("body")` returns the skin-layout box of a body part. Tops paint `body`, `jacket` and the arms or sleeves. Bottoms paint `body`, `jacket` and the legs or pants. Hair paints `head` and `hat`.
- `box.front`, `.back`, `.left`, `.right`, `.top` and `.bottom` are faces. `box.strip` is the four sides as one wrap-around strip. On every face, x runs left to right as you look at it from outside.
- `g.piece(id, bone, origin, size, pivot=..., rotation=..., inflate=..., motion=...)` adds a cuboid and returns its box to paint. Coordinates are bone-local model pixels (y down, +x is the wearer's left). Sizes are whole texels, and every texel of a piece must be painted.
- Paint only key colors: `P/S/A/L/M/K` (primary, secondary, accent, leather, metal, ink) or `H` (hair, hairstyles only), with shade `0`–`4`, for example `"P2"`. Use `X1`/`X2` for translucent shadows.

Prefer calm, structured cloth (weave, twill, knit, quilt) and deliberate details (hems, seams, buttons, folds) over random noise. Break large hair masses into several smaller locks with varied angles and lengths; one big slab reads as a helmet.

`kit.py` and `anime.py` hold the shared shapes so that a module only describes what makes its piece distinctive. They paint key colors only and return the boxes they create, so a module can add its own details on top. Keep a piece's identity (its lacing, trim or silhouette) in its own module.

The wardrobe's style targets:

- **Tops and bottoms:** casual medieval village wear such as tunics, smocks, jerkins, hoods, cloaks, braies, hose, trews and boots. Avoid modern cuts like t-shirts, hoodies and jeans.
- **Hair:** anime-inspired, with clean cel-shaded clumps, a sheen ring and pointed tapered locks, but grounded. Avoid gravity-defying spikes.

## Rules the compiler enforces

- Pixels stay inside the parts the kind may paint. Garments never use hair keys.
- Hair never paints the Living Eyes row or the hat layer over the eyes, nose and mouth. No hair piece may hang in front of them. A fringe may reach the brows: in front of the face, any part of a lock within |x| < 3 must end above y = -5. Long sidelocks and outer bangs therefore sit at |x| ≥ 4.1.
- Inflation is never negative, and the piece nets fit the kind's atlas slot (504 rows for hair, 512 for tops and bottoms).
- Pieces attach to the bones their kind may dress, and their nets fit the extras area.
- Every outfit template is compatible and worn by at least one profession, every top and bottom pairs with something, and all ten palette ids exist.

To add a variant, add a module with the next number, give it tags, and optionally add it to a template in `outfits.json`. Then run the full compiler. The catalog and tests derive their lists from the compiled output, so no Java changes are needed.
