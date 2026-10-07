# Village Life animation pack verification (2.12.0)

Verified October 6, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25, first on the 2.10.1 base and again after merging the 2.11.0 wardrobes.

- `python tools/animations/animations.py --check` validated all 99 clips (90 distinct motions) and confirmed the compiled pack is current.
- Release build passed with 63 unit tests, including eight new pack tests: coverage of every trigger, personality and vanilla/Village Friends profession; children's play and weather clips; every clip starting and ending at rest within bounds; monotone curves without overshoot or pops; weighted picking with repeat avoidance; and rejection of broken packs. The JAR contains the engine, the pack and the client mixin, and no test code.
- `runClientGameTest -PanimationPack` passed. For every clip at three moments, armor matched the resident model and the feet stayed under the resident. Bows leave the legs planted; right- and left-handed waves raise the correct arm; carried items keep their pose except in work clips; reactions leave a stride alone; prayer closes the eyes and reading keeps irises in the eye whites; children hop at their own scale; twirls end facing forward; posing bakes no textures.
- The same run drove real residents: idles (four different clips from one resident), a face-to-face neighbor chat, a greeting when the player walked up, the conversation window (greeting, talking gestures, laughing at a joke, delight at a loved gift, refusing a disliked one), happy/heart/angry/raid-sweat events, harm, a refused trade, and `/tick freeze` holding residents mid-motion while `/tick step` advances them one tick at a time. The resident's personality reached the client.
- `-PanimationsOnly`, `-PcompanionsOnly` (friendship and roadmap), and `-PoutfitsOnly` passed on both bases; on 2.11.0 the wardrobe check covered 180 outfits, 130 hairstyles, 180 tops and 180 bottoms.
- After merging the wordless voices and typed dialogue, `-PanimationPack`, `-PcompanionsOnly` and `-PanimationsOnly` passed again, including residents listening once their line has typed out and gesturing while a new reply types.
- `-PanimationVideo` captured 1,275 gallery and 1,456 village frames at 30 fps; `tools/animations/film.py` assembled a 1:42 showcase. The first 54 village frames rendered dark while the renderer settled after the freeze and are trimmed.
- Evidence: `build/run/clientGameTest/screenshots/*animation-pack-*.png` (a still of every clip), `*animation-portrait-*.png`, and `build/film/village-life-animation-pack.mp4`.

# Men's and women's wardrobe verification (2.11.0)

Verified October 6, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- `python tools/wardrobe/wardrobe.py` compiled all 490 pieces with no errors:
  - men: 80 hairstyles, 120 tops and 120 bottoms;
  - women: 50 hairstyles, 60 tops and 60 bottoms.
- The compiler also checks the new rules:
  - gender declared on every piece;
  - locked sets that name each other;
  - every top in a template, and no template worn only by unregistered archetypes;
  - every profession dressed for both sets;
  - at least seven partners per free top.
- Release build passed with 55 unit tests, no failures or errors, and no gameplay fixtures in the release JAR. `WardrobeTest` checks:
  - per-set counts and set-only hair, tops and bottoms;
  - locked sets pairing only with their partner;
  - mixing coverage: 9,849 of 10,201 men's and 2,665 of 2,704 women's free pairs;
  - every top reachable through a profession, every hairstyle worn, and hair kept across job changes;
  - palette lock under all ten palettes, including the new denim role.
- The full `runClientGameTest` gameplay suite passed: guard spawn eggs, guards, guard progression, animation, structures, Phase 2 villages, foundation, gameplay, roadmap (2,000 textures), community (2,400 textures), wardrobe and hair/eyes.
- `-PoutfitsOnly` passed inside Minecraft:
  - all 180 outfit templates are dressed by real professions in their own set;
  - palette lock holds on every baked atlas texel;
  - full armor hides every wardrobe piece, and the pieces return without it;
  - cache release and resource reload work.
- A first run found two women's outfits listed only under the unregistered Merchant/Mage archetypes. They now have real jobs, and the compiler rejects such outfits.
- Rendering performance:
  - **Before:** baking every garment's pieces into the resident model gave 4,391 parts, and posing them took 67 µs per resident, twice per frame.
  - **After:** the model is now 33 body parts. `WardrobeLayer` draws only the about 35 worn pieces, which took 8.1 µs per resident in the focused run and 40 µs in the busier full-suite run.
  - Gallery, in-world and mid-stride screenshots show the pieces in place.
- `-PhairFacesOnly` passed for all 130 hairstyles on six complexions. `-PanimationsOnly` passed.
- `-PresidentSample` dressed five random men and five random women with real professions, each wearing only their own set; evidence is in `build/resident-sample/`.
- Evidence logs: `build/outfits-2.11*.log`, `build/hairfaces-2.11.log`, `build/animations-2.11.log` and `build/full-suite-2.11.log`. Screenshots: `build/run/clientGameTest/screenshots/` and `build/wardrobe-preview/`.

# Guard spawn egg verification (2.10.1)

Verified October 5, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- Release build passed with the existing 54 unit tests, no failures/errors, and no gameplay fixtures in the release JAR.
- `runClientGameTest -PguardsOnly` passed the spawn-egg, defense and progression suites. Real egg use creates adult `minecraft:villager` residents with the exact requested profession, generated levels 15–30, full leveled health, native weapons and two iron/two chainmail armor pieces. Combat XP begins at zero with no combat lock.
- Survival egg use consumes one item; Creative preserves the stack. Powered dispensers spawn both professions and consume one egg. Guards retain their jobs after 200 AI ticks without workstations; jobs, equipment and levels survive save/reload without rerolling.
- `-PfoundationOnly` passed all ten natural profession acquisitions, 100 trades, 26 items and existing recipes. Both egg names and distinct tinted icons render in the native item gallery; its rows now fit all 43 blocks/items.
- Evidence: `build/spawn-eggs-2.10.1-*.log` and `build/run/clientGameTest/screenshots/0000_village-friends-phase1-content.png`.

# Guard progression verification (2.10.0)

Verified October 5, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- Final release build passed with 54 unit tests and no failures/errors. New policy cases cover weighted/stable starting levels, trained level zero, one-time initialization, thresholds/caps, fractional credit and floating-point threshold precision, codecs, full-key locking, damage shares, mitigation/overkill, blocked hits, expiry and unloading.
- `runClientGameTest -PguardsOnly` passed both native defense and progression suites. Actual melee, upgraded swords/Sharpness, ordinary arrows/Power and firing-time level capture produce the expected capped damage increase. Existing armor protection, bow poses and protected projectile impacts remain verified.
- Native death fixtures passed guard/guard/player damage splitting, player killing blows, first-kill locking, duplicate notifications, blocked/excluded mobs, actual non-predator villager attackers and 30-second credit expiry. Downed guards gain capacity without healing or being revived.
- Generated and migrated guards start in range, migration preserves injury percentage, later profession acquisition starts at zero, temporary job changes preserve progress and repeated refresh never stacks health. Conversion/cure and NBT reload retain fractional XP, locks, wounded health and empty/broken equipment. Restart clears pending damage contributions.
- `-PcompanionsOnly`, `-PfoundationOnly` and `-PoutfitsOnly` passed existing follow/wait/rescue, professions/trades, all thirty wardrobe sets, armor hiding and resource reload regressions.
- Evidence logs are `build/leveling-2.10-*.log`; gameplay fixtures and previews are excluded from the release JAR. The 2.9.0 release was installed and pushed separately before progression work.

# Guard defense verification (2.9.0)

Verified October 5, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25, integrated with the 2.8 wardrobe and procedural villages.

- Release build and 41 unit tests passed, including threat filtering, effective friendship, anger expiry and deterministic equipment policy.
- `runClientGameTest -PguardsOnly` passed: natural job acquisition, physical equipment exchanges, native melee/bow damage, durability, armor protection, targeting/retaliation, safe projectile impacts, bounded pursuit, companion Wait/rescue, conversion and reload.
- `-PcompanionsOnly` passed existing friendship and roadmap fixtures: owner follow/defense/wait, equipment, downing/rescue/home/logout, co-op relationships, conversion/cure, texture cache and save/reload.
- `-PfoundationOnly` passed all ten natural professions, 100 trades, blocks/items/recipes and profession persistence.
- `-PoutfitsOnly` passed all thirty outfits, hairstyles, tops and bottoms, palette lock, armor hiding and reload. Its armor comparison now explicitly starts unarmored because guard professions spawn with real equipment.
- Native profession acquisition initializes equipment immediately; reloads and breakage never replenish it. Development logs are `build/defense-2.9-*.log` and test classes remain outside the release JAR.

# Wardrobe expansion verification (2.8.0)

Verified October 5, 2026 with Minecraft 26.3/Fabric/Java 25 (Linux, Xvfb, Mesa lavapipe Vulkan backend).

- `python tools/wardrobe/wardrobe.py --check` passed. All 90 pieces compile with key colors only, painted piece nets, eye/nose/mouth clearance for every hairstyle, compatible templates worn by at least one profession, and complete palettes.
- Release build passed and all unit tests passed. `WardrobeTest` checks the 30/30/30 counts, distinct template tops and bottoms, key-color textures, Living Eyes protection, the mix-and-match rules (861 of 900 pairs allowed), palette lock for every texel under all ten palettes and hair colors, profession templates reaching all 90 pieces, and hair kept across job changes.
- `runClientGameTest -PoutfitsOnly` passed inside Minecraft: 30 outfits, 30 hairstyles, 30 tops and 30 bottoms, palette lock on every baked 256×512 atlas texel, armor hiding, cache release and resource reload.
- The full `runClientGameTest` gameplay suite passed: animation, structures, Phase 2 villages, foundation, gameplay, roadmap (2,000 textures), community (2,400 textures), wardrobe and hair/eyes.
- `-PhairFacesOnly` passed for all 30 hairstyles on six complexions: protected eye UVs, brows and lashes, blink, gaze, sleep, helmet and baby. `-PanimationsOnly` passed.
- Game-rendered screenshots in `build/run/clientGameTest/screenshots/`: `village-friends-wardrobe-in-world-1..3`, `-outfits-1..3` (each with `-back` and `-walking`), `-hairstyles-1..3` (each with `-back`), `-mix-and-match-1..2` and `-ten-palettes`.

Earlier verification below records superseded wardrobe versions.
# Sims-style wardrobe verification (2.7.0)

Verified October 5, 2026 with Minecraft 26.3/Fabric/Java 25 (Linux, Xvfb, Mesa lavapipe Vulkan backend).

- `python tools/wardrobe/wardrobe.py --check` passed. All 30 pieces compile with key colors only, painted piece nets, eye/nose/mouth clearance for every hairstyle, compatible templates and complete palettes.
- Release build passed; 37 unit tests passed. `WardrobeTest` checks the 10/10/10 counts, key-color textures, Living Eyes protection, the mix-and-match rules (87 of 100 top/bottom pairs allowed), palette lock for every texel under all ten palettes and hair colors, profession templates, and hair kept across job changes.
- `runClientGameTest -PoutfitsOnly` passed inside Minecraft: profession dressing, palette lock on every baked atlas texel, armor hiding the hair layer and pieces, cache release and resource reload.
- The full `runClientGameTest` gameplay suite passed: animation, structures, Phase 2 villages, foundation, friendship, roadmap, community, wardrobe and hair/eyes.
- `-PhairFacesOnly` passed for all ten hairstyles on six complexions: protected eye UVs, brows and lashes, blink, gaze, sleep, helmet and baby. `-PanimationsOnly` passed unchanged.
- Game-rendered screenshots in `build/run/clientGameTest/screenshots/`: `village-friends-ten-outfits`, `-ten-outfits-back`, `-ten-outfits-walking`, `-ten-hairstyles`, `-ten-hairstyles-back`, `-mix-and-match`, `-ten-palettes` and `-wardrobe-in-world`.
- One run hung in Fabric's client game-test shutdown (render thread halting the integrated server while the test thread waited on the tick phaser), after all assertions and screenshots had completed. The test now settles for 40 ticks before closing the world; the rerun passed.

Earlier verification below records superseded wardrobe versions.

# Procedural plains village verification

Verified October 5, 2026 with Minecraft 26.3/Fabric/Java 25 (headless client on Mesa lavapipe).

- `python tools/design_village.py`, then `python tools/create_village_structures.py` rebuilt 60 independent templates and 13 pools. The design kit checked door clearances and the size, separation and enclosure of every bedroom; the compiler checked lot entrances, civic slot widths, start jigsaws and pool references.
- `python tools/village_design/simulate.py --seeds 300`: 56–139 pieces (median 85), 22–70 residents (median 38), and every civic building present in every seed.
- `gradlew runClientGameTest -PstructuresOnly` passed. All 60 templates loaded with their connectors; bedrooms stayed sealed and doors stayed walkable in four rotations; block entities were created; 12 procedural assemblies passed without overlapping lots. A natural seed-1 world generated "Willowbridge": 113 pieces, 34 residents, all ten professions with trades, hometown names and save/reload.
- `gradlew build` passed with 46 unit tests.
- `gradlew runClientGameTest -PvillageGallery` captured art-direction screenshots of templates and whole villages.
- The full `gradlew runClientGameTest` suite passed (animation, structures, foundation, friendship, roadmap, community, outfits, hair/faces). The first full run failed the roadmap test's one-minute companion recovery: the client waits a fixed 1,220 ticks, and the software-rendered server fell about 160 ticks behind. That test world is superflat with structures disabled. The same suite passed on `main` and on a rerun of this branch.

Earlier verification below records previous releases.
# Male starter texture rebuild verification

Verified October 3, 2026 with Minecraft 26.3/Fabric/Java 25.

- Release build passed; 41 unit tests passed with zero failures/errors.
- The male registry and bundled release contain exactly five hairs, five tops and five bottoms. Retired male recipes resolve through this rebuilt catalog.
- Shader tests validate repeatable HSV noise within ±5%, hue preservation, 15–20% geometric occlusion, cross-bone belt shadows, fringe shadows, structural-only accent components and one waist buckle.
- The focused Minecraft run passed with all five male hair/top/bottom constructions, a 512×512 textured atlas, more than 45 distinct rendered texture colors per outfit, palette identity, armor handling, cache clearing and resource reload.
- Actual game-rendered gallery: `build/run/clientGameTest/screenshots/0000_village-friends-five-male-textured-outfits.png`.
- Build/native log: `build/male-starter-textured-gameplay.log`. Release: `build/libs/village-friends-2.6.0.jar`.
- Female expansion is on hold; draft female data/code remain outside the active renderer/factory catalog. The installed launcher profile was not changed by this build.

Earlier verification below records superseded wardrobe versions.
# Male asset registry Phase 2 verification

Verified October 3, 2026 with the existing Minecraft 26.3/Fabric/Java 25 toolchain.

- Release build passed; all 33 unit tests passed.
- Six registry checks validate exactly 50 consecutive IDs in each category, 60/30/10 textile pixels plus separate hardware, actual strand depth, positive voxel volume, distinct constructions, all-item factory reachability, cowl/hood compatibility, palette identity and version 1/2 recipes.
- The focused Minecraft run passed using male registry models across all ten palettes. It checks actual secondary and hardware pixels, compiled hair geometry, armor state handling, texture cache cleanup and resource reload.
- Evidence: `build/male-registry-gameplay.log` and `build/run/clientGameTest/screenshots/0000_village-friends-phase2-male-assets.png`.
- The complete registry is bundled as `assets/villagefriends/outfits/male-registry.json` in `build/libs/village-friends-2.6.0.jar`.
# Outfit engine Phase 1 verification

Verified October 3, 2026 with the existing Minecraft 26.3, Fabric and Java 25 toolchain.

- Clean release build passed; 27 JUnit tests passed.
- Six new engine tests cover every gender/profession/palette combination, compatible garments, shared palette identity, four role channels, separate hardware opacity, immutable masks, recoloring, volumetric hair, deterministic seeds, invalid inputs, recipe round trips and name eligibility.
- `gradlew.bat runClientGameTest -PoutfitsOnly` passed inside Minecraft. It validates ten palette atlases, actual secondary-role pixels, bound layer palettes, baked solid hair, armor state handling, cache release and resource reload. Evidence: `build/outfit-gameplay.log` and `build/run/clientGameTest/screenshots/0000_village-friends-new-outfit-engine.png`.
- All remaining gameplay fixtures compile against the replacement. The full gameplay suite was not rerun for this step.

Release: `build/libs/village-friends-2.6.0.jar`. The existing installed launcher profile is separate from this workspace build.

The previous wardrobe source, preset catalogs, semantic-mask assets, generators and obsolete wardrobe tests have been deleted. Six body/face bases remain as identity assets. `OUTFIT_ENGINE.md` describes the replacement and the intentional appearance reset for retired recipes. Earlier wardrobe verification claims have been retired with that implementation.

