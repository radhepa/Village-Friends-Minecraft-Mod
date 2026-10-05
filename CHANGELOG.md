# Village Friends 2.7.0 — Sims-style wardrobe

- Replace the outfit engine and every old garment and hair model with a palette-locked pixel-art wardrobe of ten hairstyles, ten tops and ten bottoms.
- Paint garments as key colors (role + shade) resolved through five-shade, hue-shifted ramps of the ten master palettes; one palette per outfit, natural hair colors separate.
- Use the player overlay layers for depth, plus textured 3D pieces: pauldrons, collars, mantles, coat skirts, hoods, quivers, pouches, cuffs, buns, ponytails and layered hair locks.
- Let coat skirts, aprons and tabards follow the leading leg; let ponytails, tassels and sash tails sway.
- Mix any top with any compatible bottom; tag rules keep armor with sturdy legwear and hose away from armor and aprons.
- Map professions to ten outfit templates; keep hair and hair color when a resident changes jobs.
- Add `tools/wardrobe/` (one module per piece, compiler, offline previews) and gametest galleries of all outfits, hairstyles, mixes, palettes and an in-world scene.

# Male starter set and texture overhaul

- Replace the 150 male entries with five hairs, five tops and five bottoms.
- Replace stretched solid texels with multi-texel cuboid face UVs, deterministic HSV woven/leather/hair grain and geometry-derived overlap shadows.
- Remove floating knee/shin patches and duplicate belts; keep connected collars, cuffs, coat hems and one waist belt.
- Add stepped crowns, fringe/side overhangs, forehead shadows, trouser seam shading and connected leather boots.
- Bake outfit-specific 512×512 atlases; use version 4 recipes and regenerate older male appearances through the starter set.
- Hold female expansion outside the active catalog; capture five revised male outfits inside Minecraft.
# Male asset registry — Phase 2

- Add all 150 explicit male IDs: 50 hair models, 50 tops and 50 bottoms, grouped in compact JSON arrays.
- Compile exact disjoint four-role material bounds with 60/30/10 textile pixel coverage and separate hardware coverage.
- Build distinct solid geometry, use the registries in male outfit assembly, and share identical material swatches.
- Introduce version 2 recipes while preserving Phase 1 selections; add registry and native renderer checks.
# Outfit engine rebuild

- Remove the previous wardrobe code, preset resources, generators and obsolete wardrobe tests.
- Add ten master palettes, four-channel role masks, validated hair/top/bottom models and a palette-locked outfit factory.
- Render the new solid voxel silhouettes on animated resident bones; reset retired appearance recipes while preserving resident history.
- Add core invariants and focused Minecraft renderer verification. Earlier entries below describe retired releases.
# 2.6.0

- Give residents six stable, understated gaits with individual cadence, stride, shoulder swing, balance and step height. Children take lighter, quicker steps.
- Add quiet breathing, small head tilts, softly moving braids, satchels and scarf tails.
- Add articulated eyes using the original complexion and eye colors, with varied blink timing, occasional double blinks, subtle idle glances and nearby eye contact. Hair and glasses stay in front of the eyes.
- Animate armor with the same poses. Preserve sleeping, seated, airborne, swimming, crouching, item-use and attack behavior; sleeping eyes close.
- Preserve saved recipes, identities, names, relationships and every skin asset. No per-frame textures or new saved animation records.
- Add native Minecraft art previews and animation/compatibility/navigation/reload checks.

# 2.5.0

- Complete Codex Phase 3 with 494 separately editable JSON definitions and 366 native 64×64 material masks for the local compositor.
- Independently combine 96 tops, 64 bottoms, 72 hairstyle variants, 96 clothing palettes, 32 hair colors and 32 clothing details using stable saved `m3` recipes.
- Add straight, slim, relaxed, bootcut and ripped jeans, each in eight casual washes, plus six other trouser families.
- Add partial work layers for all 23 professions, preserving personal trousers, uncovered shirts, faces and hair.
- Import and deduplicate the supplied name list, retaining existing names: 1,097 first names and 250 surnames. Restrict the supplied Indian pool and overlapping surname to brown/dark complexion indices 2–5.
- Generate names after assigning the actual saved complexion. Preserve existing/custom names, earlier recipes, child identity, growth and save/reload.
- Document individual layer edits, semantic masks, palettes, data/resource packs and the Claude handoff. Add focused and full Minecraft verification.

# 2.4.0

- Implement Phase 2 with fifteen native structure templates, thirteen jigsaw pools and a complete connected village layout: plaza, tavern, garrison, cemetery, enclosed homes, apothecary, workshop and library.
- Add natural plains/meadow generation alongside vanilla villages, with separate placement and vanilla-village exclusion. Integrate the new structure with existing hometown discovery.
- Place fourteen starter residents, all ten new profession anchors, benches, treatment cots, administrative blocks, beds and practical building interiors.
- Provide three cottage variants, separately enclosed bedrooms and clear doors for future spatial bed scans. The scanner and specialized AI remain later work.
- Add deterministic template tooling and Minecraft tests for loading, rotation, room boundaries, assembly, natural generation and persistence.
- Keep every building in a separate editable layered JSON blueprint, with independent role pools, single-building regeneration and a documented Claude handoff/entrance contract.

# 2.3.0

- Implement the master specification's Phase 1 foundation: ten professions and their distinct workstation POIs, preserving vanilla job anchors.
- Add 17 directional blocks, four registered block entity types with public integration hooks, and self-drop loot tables.
- Add 24 items: medical supplies, meals/coffee, weather wearables, ten uniforms and five tools. Meals heal; coffee grants Speed I; wearable equipment renders on players and companions.
- Package original pixel art, block/item/equipment models, localization, 41 crafting recipes/unlocks, and 50 trade sets with 100 offers. Revival Tonic requires an Awkward Potion.
- Add reproducible asset tooling and actual Minecraft verification of natural profession acquisition, crafting, trading, placement, loot, consumption, rendering and save/reload.
- Document the hooks and remaining behavior in PHASE1.md. Specialized AI, real-time revival, seating, housing scans, worldgen and advanced animations remain later work.

# 2.2.0

- Align all glasses around the actual iris pixels; remove duplicated, misaligned painted frames from older hairstyles and the Ink resident at composition time.
- Add five frame styles alongside round glasses: rectangular, octagonal brass, browline, half-rim and aviator, each with its own geometry/material.
- Add specific clothing for all 13 working professions, with consistent occupational colors and eight personal trim variations per job.
- Give garments physical depth with raised panels, collars, articulated sleeves/cuffs, hanging aprons, coat tails, book pockets, a map roll, quiver, smith shoulder plates and belt pouches.
- Update clothes immediately from the synced vanilla profession while retaining saved appearance recipes, faces, names, friendship and trade behavior.
- Keep child play-clothes and hide conflicting garment/eyewear geometry under armor.
- Add geometry/asset checks and an actual Minecraft wardrobe test covering all professions, six frames, old appearances, job changes, portraits, trading and reload.

# 2.1.0

- Give children proportionally larger heads, shorter bodies, child faces and six play-clothes designs in the world and live portrait. Preserve identity when they grow up.
- Discover and save natural village names; add "First Last of Village" hover names, village welcome messages, hometown dialogue and journal entries.
- Add a craftable carved Village Marker for player-built settlements, anvil naming/renaming, right-click information and persistent origins after removal.
- Preserve hometowns through travel, conversion, curing and reload; preserve old names as the personal part and keep existing friendship, trades and adult appearance recipes.
- Add 2,400 personality-directed appearances, six additional hairstyles, eight additional outfits, eight facial details and ten articulated accessories. Retain all 2,000 original recipes.
- Add actual outer garment/hair layers and small 3D hats, glasses, bags, jewelry, scarves and hair shapes; hide accessories that conflict with armor.
- Wrap long hometown names in the conversation card and expose full names and metadata on hover.

# 2.0.0

- Preserve 1.1.0 names, skins, points, daily limits, trades, and unlocked tiers; migrate to stable resident IDs and modular recipes.
- Add persistent personalities, hobbies, values, preferences, private trust, permanent story flags, recent memories, and resident friendships.
- Add eight authored four-chapter stories, 24 requests, twelve dialogue profiles, branching endings, and reciprocal gifts.
- Add Story, Journal, Time, and Travel controls with a live equipment-aware portrait.
- Add walks, picnics, exploration, gatherings, and personal invitations.
- Add one Overworld melee companion per player, equipment exchange, follow/wait/home, downed rescue, home recovery, and owner-state cleanup.
- Preserve identity through conversion and curing; keep shared request credit separate from private relationships.
- Add 2,000 original modular appearances with local composition, texture caching, fallback handling, and reproducible art tooling.
- Gate upper friendship tiers on experiences and stories; retain existing tiers during migration and avoid absence penalties.

Romance/family, dimension travel, ranged roles, and larger parties remain future work.


