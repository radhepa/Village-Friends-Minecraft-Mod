# Palette-locked outfit engine

The engine lives in `src/main/java/dev/villagefriends/outfit/`. `MasterPalettes.ALL` contains the ten master palettes. One immutable `Outfit` owns the active `ColorPalette`; every equipped layer resolves its materials through that same palette instance. Hair pigment is independent; hair ornaments, where present, use palette roles.

```java
Outfit outfit = OutfitFactory.assembleOutfit(Gender.MALE, Profession.MERCHANT, PaletteID.ROYAL_VELVET, 81L);
Outfit recolored = outfit.recolor(PaletteID.SAGE_AND_TERRACOTTA);
```

The current male starter set has five hairs, five tops and five bottoms. Read [MALE_ASSETS.md](MALE_ASSETS.md) for the canonical JSON, structural trim rules and shading pipeline. Female expansion is on hold. Other genders currently use the original starter silhouettes.

`RoleMask` packs primary/secondary/accent/hardware weights as `0xPPSSAAHH`; covered texels sum to 255. Opacity and neutral shade are separate. `MaterialMask` validates exact disjoint pixel bounds and 60/30/10 textile coverage; hardware is additional. Those allocations are authoring targets, not projected screen-area guarantees after geometry, occlusion and pose. Records and mask arrays are immutable.

`HairModel` requires positive-volume head-mounted cuboids with outer layers beyond the 8×8×8 head. `TopGarment` defines underlayer/outerwear/trim/hardware; `BottomGarment` declares compatible styles. The factory selects the profession's workwear, relaxed, tailored, robes or traveler top and a compatible bottom. Selecting hair before garments keeps it stable when a resident changes profession.

Minecraft's `OutfitAtlas` provides padded, multi-texel unfolded UVs in a 512×512 atlas. `ResidentModel` scales integer UV geometry to the authored cuboid dimensions. `ResidentSkins` resolves roles and bakes deterministic HSV microtexture, directional face shading, 15–20% overlap occlusion and fringe shadows. Surface hue remains palette-bound. Baking occurs on outfit selection/cache miss; animation allocates no per-frame textures. Six complexion/face bases remain in `textures/body/`.

New recipes use `outfit4:complexion:GENDER:PALETTE_ID:seed`. Recipes 1–3 remain readable. Male appearances intentionally regenerate through the new five-piece set while preserving complexion, palette, stable seed and resident history. Existing children, armor and portrait rendering use the same engine.

The build uses Minecraft's bundled Gson to load compact registries; rebuild after JSON edits. Resource reload clears generated textures and reloads body bases. `build.ps1` runs unit tests and produces the release JAR. `gradlew.bat runClientGameTest -PoutfitsOnly` validates the actual Minecraft renderer and captures the five-outfit gallery.
