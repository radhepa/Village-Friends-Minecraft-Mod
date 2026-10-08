# Wardrobe expansion verification (2.16.0)

Verified October 8, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- `python tools/wardrobe/wardrobe.py` compiled all 832 pieces with no errors, and `--check` reports them current:
  - men: 80 hairstyles, 219 tops and 219 bottoms;
  - women: 50 hairstyles, 132 tops and 132 bottoms;
  - 351 outfit templates, every one worn by a real profession.
- Mixing coverage: 37,077 of 38,416 men's and 14,449 of 14,884 women's free pairs are allowed. There are 23 men's and 10 women's locked sets.
- Release build passed with 102 unit tests and no failures. `WardrobeTest` checks the new per-set counts, locked sets, coverage and palette lock under all ten palettes.
- `-PoutfitsOnly` passed inside Minecraft: 351 outfits, 130 hairstyles, 351 tops and 351 bottoms, with palette lock on every baked atlas texel, armor hiding and resource reload. Posing a resident took 8.8 µs, the same as with the smaller wardrobe.
- Evidence: `build/outfits-2.16.log` and `build/run/clientGameTest/screenshots/` (gallery, back and mid-stride pages for all 36 pages of outfits, and an in-world scene per page).

# Village Life animation pack, 349 clips (2.15.0)

Verified October 7, 2026 on Windows with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- `python tools/animations/animations.py --check` validated all 349 clips (340 distinct motions) and confirmed the compiled pack is current. `tools/animations/vlcheck.py` passed every one of the 16 authoring modules (feet kept under the resident, known tags only, an age on every greeting, no commas in names).
- Every new clip was reviewed in offline contact sheets (`preview.py` poses) from at least one angle while it was authored.
- Release build passed with 80 unit tests. `AnimationPackTest` now requires at least 349 clips, four work motions for every profession, three hobbies per personality, six or more clips for each reaction trigger, 20 children's games, seven rain clips and a thunder clip. Weighted picking still shows the cleric praying and the gentle hobby often among 200+ idles.
- `runClientGameTest -PanimationPack` passed twice (before and after a clip-name cleanup): every clip at three moments kept armor matched to the resident model and the feet under the resident; held items, mirroring, eyes, children, idles, neighbor chats, greetings, the conversation window and event reactions all passed. The gallery now lays residents out 20 wide and captured 18 pages.
- In-game stills reviewed for the trades, conversation gestures and children's games pages.
- The release JAR contains the 349-clip pack and no gametest classes.
- Evidence: `build/run/clientGameTest/screenshots/*animation-pack-*.png`.

# Village days verification (2.14.0)

Verified October 7, 2026 on Windows 11 with Minecraft 26.3, Fabric 0.19.5 and Java 25.

- `gradlew test` passed with 102 unit tests, including the new `RoutineTest` (10), `DialogueBankTest` (6) and `TalkTest` (6).
- `python tools/workstations/workstations.py --check`, `python tools/dialogue/dialogue.py --check` (5,898 pieces of dialogue) and `python tools/animations/animations.py --check` passed.
- `runClientGameTest -Ptests=WorkstationGameTest` passed:
  - all eleven workstations placed and photographed;
  - each one used by a player: the stove (beef cooked in half the campfire time), the barrel and tap, the press (Herbal Tonic), the easel (sketch, painting, taken home), the sawmill (6 planks a log, 3 sticks a plank, 16 at a click), the sewing table (wool unravelled, boots mended), the archives (chronicle book), the music stand (Haste), the dummy (a strike is measured; holding attack never mines it) and the target's scoring;
  - a cook, painter, tavern keeper and knight at work: dish of the day once per visitor, a finished painting, restocking, training experience;
  - a librarian asleep at midnight, sheltering awake from a thunderstorm, and back out to the bell when it clears;
  - written dialogue on every topic, a remembered answer, and an apothecary's offer that heals a hurt player through the real conversation window.
- `-Ptests=GuardSpawnEggGameTest,GuardGameTest,GuardProgressGameTest`, `FriendshipGameTest`, `CommunityGameTest`, `FoundationGameTest` (28 items), `VillageLifeGameTest`, `RoadmapGameTest`, `AnimationGameTest`, `StructuresGameTest`, `OutfitGameTest` and `HairFaceGameTest` passed: every registered gameplay test. Run in small groups: this PC was short of memory, and a full-suite run hung once and later stopped with a native out-of-memory error, not a test failure.
- Two regressions were found and fixed along the way. Questions on a first visit could replace the topic buttons the Friendship test clicks next, so residents now only quiz you from your second visiting day; offers to help still come on first meeting. Village references had dropped out of work talk and children's lines, so the earlier rule was restored, as the Community test expects.
- Evidence: `build/run/clientGameTest/screenshots/*workstations-*.png`; `python tools/workstations/workstations.py --preview` writes `build/previews/workstations.png`.


# Village life verification (2.13.0)

Verified October 7, 2026 on Linux with Minecraft 26.3, Fabric 0.19.5 and Java 25 (Temurin 25.0.4), in a headless X server with Mesa llvmpipe (OpenGL 4.5 through EGL; no sound device).

- `gradlew test` passed with 77 unit tests, including 14 new ones:
  - `SocietyTest`: deterministic traits, love times spread across 50–1,000 days, mutual meters that start polite and grow with time and shared days, households (couples, siblings, parents and children) with blood awareness, births and grandchildren/aunts/uncles, a 1,100-day village where nobody falls in love before their pair's time or with a relative, some residents stay single and sweethearts marry, crushes before love, deaths widowing partners, curses and cures, codec round trips, bounded news and capped catch-up;
  - `GossipTest`: real names, partners and children in heart-to-hearts and chat, news from each resident's point of view, the cursed-neighbor call to action, and safe lines for every resident of a simulated 400-day village;
  - `FriendshipLevelsTest`: the ten levels sit inside the five tiers at every point value, story gates cap levels, and earned tiers keep their floor.
- A diagnostic 1,000-day run of four 20-adult villages saw first couples on days 75–270, 2–6 couples and 8–16 single residents per village, and about 0.15–0.5 ms per simulated day. A first run showed quarrels every other day; their odds were cut about eightfold.
- `runClientGameTest -PcompanionsOnly` (Friendship and Roadmap) passed against the rebuilt conversation window: buttons are still found by their labels, the gift button disables after the third gift, and companions, stories, journals and save/reload are unchanged.
- `runClientGameTest -PvillageLifeOnly` passed: a marked settlement counts all six residents with mutual meters; a baby made by `Villager.getBreedOffspring` records both parents, joins their family, takes the family surname and is announced; relatives cannot breed; a level 10 friend tells the baby's news, has a heart-to-heart and gives the daily gift; the Village button opens the ledger at the resident's page and returns; six emote bubbles reach the client; the ledger item and a notice board open the ledger; a killed resident is remembered; families and news survive save/reload.
- `runClientGameTest -Ptests=VillageLifeGameTest,CommunityGameTest,FoundationGameTest,FriendshipGameTest,RoadmapGameTest` passed Village Life, Community (markers, hometown names, conversion and cure), Foundation (27 items, 41 recipes) and Friendship. Roadmap failed once in that combined run at "Abandoned companion automatically recovers at home after one minute": it waits 1,220 client ticks for a 1,200 server-tick timer, and the software-rendered client (llvmpipe on all four cores) outran the integrated server, which logged running 40–86 ticks behind. Rerun on the final code with llvmpipe limited to two threads (`LP_NUM_THREADS=2`), `-Ptests=RoadmapGameTest,VillageLifeGameTest` passed both. On a machine with a GPU the margin is not an issue.
- Screenshots reviewed: the conversation window at 427×240 and 640×400 scaled sizes, the level-up banner, journal pages, news and heart-to-heart replies, in-world bubbles above residents, and the ledger's resident and news pages. They led to fixes: the world bubble's symbol was drawn behind its bubble, dock labels were clipped, replies covered the resident on wide screens, the ledger list scrolled when everyone fit, a parent's ledger note read the relation backwards, near-strangers were called closest friends, and delayed chat replies could replace a newer bubble.
- Evidence: `build/run/clientGameTest/screenshots/*village-life-*.png` and `*village-friends-*.png`; `python tools/social_assets.py --preview` writes `build/previews/emotes_preview.png`.

# Starlit and Soft Glint faces verification (2.13.0)

Verified October 7, 2026 on Linux with Minecraft 26.3, Fabric 0.19.5 and Java 25, rendering in software (Mesa llvmpipe) under Xvfb. SDL asks for an sRGB-capable framebuffer that Xvfb does not offer, so the client ran with `SDL_OPENGL_FORCE_SRGB_FRAMEBUFFER=skip`.

- All 66 unit tests passed. `HandcraftedFaceTest` checks the even, lifelong split between Starlit and Soft Glint eyes, feminine details for women and a mix for non-binary residents, lashes that sweep from the eye's top to its bottom, wings that join the closed lash, brows clear of the lashes, and eye, lip and blush colors derived from the resident's own face.
- `runClientGameTest -PhairFacesOnly` passed for all 130 hairstyles on six complexions, alternating men and women and both eye styles. It covered the protected eye row, every face swatch, irises and pupils trimmed to the eye while glancing, lashes following the blink, wings, brows, lips and blush by gender, sleep, death, helmets and children.
- `-PanimationsOnly`, `-PanimationPack` (prayer closes the eyes; reading keeps irises inside the eye) and `-PoutfitsOnly` (palette lock on every baked texel outside the skin and face swatches, 180 outfits) passed.
- `python tools/wardrobe/wardrobe.py --check` reports 11 hair JSON files as stale on Linux both before and after this change; they differ only in the last digit of some floating-point pivots.
- Evidence: `build/run/clientGameTest/screenshots/0002_village-friends-living-eyes.png` and `0004_village-friends-expressive-portrait.png`.

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

