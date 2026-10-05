# Wardrobe and outfit engine

Residents dress like characters from a Sims-style wardrobe. They pick from 10 hairstyles, 10 tops and 10 bottoms, colored by one of 10 master palettes and one of 10 natural hair colors. The previous voxel/role-mask wardrobe, its male, female and generic registries and their geometry were removed and replaced at the user's request. To add or change clothing, read [WARDROBE_EDITING.md](WARDROBE_EDITING.md).

## Pieces

Each hairstyle, top and bottom is one PNG and one JSON file under `assets/villagefriends/wardrobe/{hair,tops,bottoms}/`. Both are compiled from one Python module per piece in `tools/wardrobe/`.

- **Skin layer:** the top 64×64 of the PNG is painted in the standard player-skin layout. The base layer is the body; the hat, jacket, sleeve and pants overlays give clothing and hair half-pixel depth.
- **3D pieces:** the rows below the skin layer hold box-UV nets for the piece's cuboids, such as pauldrons, collars, coat skirts, hoods, cuffs, pouches and hair locks. Each cuboid is attached to a body bone with a pivot, a rotation in degrees and an optional inflation.
- **Motion:** the `flap_front` and `flap_back` motions follow the leading or trailing leg so coats and aprons never clip through a stride. `sway` swings ponytails, tassels and sash tails while the resident walks.

## Palette lock

The PNGs contain no clothing color. Every opaque pixel is a *key color*: a role (primary 60%, secondary 30%, accent 10%, leather, metal, ink, or natural hair) plus one of five shades (deep, shadow, base, light, highlight).

- **Palettes:** `palettes.json` stores the ten master palettes as five-shade ramps. Shadows shift cooler and highlights warmer, so pixel-art shading stays within the palette.
- **One palette per outfit:** each `Outfit` owns a single palette. Hair keys resolve through the natural `HairColor` ramp instead.
- **Shadow keys:** two translucent keys (`X1`/`X2`) darken whatever lies beneath them, such as hairline shadows or a tucked shirt's fold.

## Mix and match

The wardrobe is Sims-style: any top pairs with any bottom unless a tag rule forbids it.

- The Squire's Brigandine `requires` sturdy legwear.
- Plated Greaves require a martial or rugged top.
- Minstrel Hose `rejects` armor and work tops.

87 of the 100 top/bottom pairs are allowed. `Wardrobe.compatible` and `tools/wardrobe/wardrobe.py` apply the same rule.

Skin layers stack as: body, then the bottom, then the top, then hair. A `tucked` top (shirts) goes under the bottom instead, so waistbands and suspenders show over it. A top that `coversWaist` (its own belt, sash or long hem) hides the bottom's 3D pieces whose ids start with `waist`.

## Professions

`catalog.json` maps each profession to outfit templates (a top plus its matching bottom). `OutfitFactory.assembleOutfit` works in this order:

1. Hair and hair color come from the resident's seed alone, so a new job never changes them.
2. The profession's preferred template is chosen 70% of the time; otherwise one of its alternatives is used.
3. The template's bottom is kept 60% of the time; otherwise a random compatible bottom is used.

| Template | Top | Bottom | Professions (preferred) |
|---|---|---|---|
| Knight-Errant | Squire's Brigandine | Plated Greaves | Knight, Guard |
| Trailblazer | Trailblazer Vest | Trail Breeches | Adventurer, Cartographer |
| Arcanist | Arcanist Longcoat | Scholar's Slacks | Mage, Scholar, Librarian |
| Farmhand | Farmhand Flannel | Patched Workpants | Farmer, Shepherd, unemployed |
| Merchant | Merchant's Waistcoat | Pinstripe Trousers | Merchant, Tavern Keeper, Tailor |
| Mariner | Mariner's Knit | Rolled Canvas | Fisherman |
| Smith | Smith's Apron | Heavy Work Trousers | Smiths, Butcher, Cook, Mason, Carpenter, Leatherworker |
| Ranger | Ranger's Hood | Wrapped Leggings | Archer, Fletcher |
| Minstrel | Minstrel's Doublet | Minstrel Hose | Bard, Painter, Nitwit |
| Pilgrim | Pilgrim's Tabard | Wanderer's Pantaloons | Cleric, Apothecary |

Unknown or modded professions dress like the unemployed.

```java
Outfit outfit = OutfitFactory.assembleOutfit(Gender.MALE, Profession.MERCHANT, PaletteID.ROYAL_VELVET, 81L);
Outfit recolored = outfit.recolor(PaletteID.SAGE_AND_TERRACOTTA);
```

## Rendering

- **Model:** `ResidentModel` is the player mesh with its overlays, plus every garment's 3D pieces baked once. Only the worn outfit's pieces are visible.
- **Atlas:** `OutfitAtlas` lays out a 512×512 texture with the player skin at the origin, the face-detail swatches at (64..67, 0), and a 64-pixel-wide block per garment for its piece nets.
- **Baking:** `ResidentSkins` bakes one texture per complexion and outfit on a cache miss. It resolves key colors through the palette, applies the layering rules and copies the piece nets into their blocks. Animation allocates no textures.
- **Reload:** wardrobe PNGs reload with resource packs, so a pack can repaint any piece in key colors.
- **Armor:** a helmet hides the hair layer and hair pieces; chest and leg armor hide the matching garment pieces.
- **Eyes:** the Living Eyes UVs and face swatches are unchanged. Hair never paints the eye row, and the compiler rejects fringes that would hang over the eyes, nose or mouth.

## Recipes and genders

Recipes keep the `outfitN:complexion:GENDER:PALETTE_ID:seed` format. Saved residents keep their complexion, palette, seed, identity and history, and are redressed from the new wardrobe.

The wardrobe is currently shared by all genders. A dedicated female set is future work: add garments tagged for it and filter by gender in the factory. The old draft female data was removed with the old engine.

## Verification

```text
python tools/wardrobe/wardrobe.py --check
gradlew.bat test
gradlew.bat runClientGameTest -PoutfitsOnly
gradlew.bat runClientGameTest -PhairFacesOnly
```

The focused Minecraft run checks palette lock on every baked texel, profession dressing, armor hiding and reload. It also captures these screenshots in `build/run/clientGameTest/screenshots/`:

- the ten outfits from the front, from the back and mid-stride
- the ten hairstyles from the front and back
- a mix-and-match gallery
- one outfit across all ten palettes
- an in-world scene
