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

