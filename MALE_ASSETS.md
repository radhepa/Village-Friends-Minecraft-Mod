# Male starter assets — textured rebuild

The active male wardrobe contains **five hairstyles, five tops and five bottoms**. The previous 150-item male registry and its geometry were replaced at the user's request. Canonical arrays: `src/main/resources/assets/villagefriends/outfits/male-registry.json`.

| Hair | Top | Bottom |
|---|---|---|
| Messy layered part | Hearth linen tunic | Straight linen trousers |
| Stepped spiky crown | Canvas artisan vest | Heavy woven trousers |
| Full curly clumps | Tailored merchant coat | Clean cuffed denim |
| Sweeping undercut fringe | Layered scholar robe | Fitted trail breeches |
| Layered low ponytail | Split trail coat | Pleated tailored trousers |

These columns are independent registries. The factory selects the profession's top style, random hair and a compatible bottom. All five bottoms accept all five styles. Every equipped layer uses one `ColorPalette`; natural hair pigment remains independent.

Material bounds are `[x0,y0,x1,y1]` with exclusive end coordinates in a 20×16 role atlas. Every layout has 180 primary, 90 secondary, 30 accent and 20 hardware pixels: 60/30/10 textile allocation plus separate hardware. These islands identify materials; the renderer separately unwraps all six cuboid faces at approximately one texel per model pixel. Garment definitions contain no RGB overrides.

`SurfaceTexture` bakes deterministic woven cloth, leather grain, hair strands and metal variation. HSV value/saturation noise stays within ±5%; hue stays tied to the selected palette role. Directional face shading and geometry-derived ambient occlusion add depth. Nearby protruding collars, hems, belts and fringes darken texels by 15–20%; foreheads receive the actual hairstyle's baked fringe shadow. Leather boots receive a darker value treatment of the primary role, preserving its hue. Textures are baked on outfit creation, not every frame.

There are no knee/shin patches, cargo rectangles or top belts. Each bottom owns one connected waist belt and one buckle. Other accents are continuous collar/lapel edges, sleeve cuffs and long-coat hems. Connected boots use primary-role leather; folded trouser cuffs use primary cloth. The trouser center seam is pixel shading, not extra geometry.

Hair uses recessed scalp pieces covered by an irregular stepped crown, 1–2 pixel fringe/side overhangs and solid strand clumps. No broad exposed cap slab is used. Volume tiers 1–3 affect fullness; `strandLayerDepth` matches the maximum actual natural-hair layer.

`OutfitAtlas` packs padded per-cuboid UV islands into a 512×512 texture. Its mesh uses multi-texel face dimensions rather than stretching a single texel. The texture cache includes the actual hair/top/bottom IDs so overlap shadows cannot leak between outfits; it trims inactive textures toward 64 entries. Armor hiding, body proportions and existing animation remain supported.

New recipes use `outfit4`. Accepted older male recipes now resolve through the rebuilt five-piece catalog, keeping their complexion, palette, identity and seed. Female expansion is on hold: its draft data/code remain in the workspace but are excluded from the active factory and renderer catalog.

Build: `build.ps1`. Minecraft verification: `gradlew.bat runClientGameTest -PoutfitsOnly` with the installed JDK. The focused test captures all five male constructions using the actual game renderer: `build/run/clientGameTest/screenshots/0000_village-friends-five-male-textured-outfits.png`.
