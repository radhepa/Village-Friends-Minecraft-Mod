# Graph Report - Village-Friends-Minecraft-Mod  (2026-10-07)

## Corpus Check
- 223 files · ~254,964 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .properties 2, .jar 1)

## Summary
- 3450 nodes · 9078 edges · 190 communities (93 shown, 97 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 620 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8deb36e8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Face
- kit_casual.py
- anime_female.py
- FriendshipScreen
- net.minecraft.server.level.ServerPlayer
- anime_male.py
- workstations/paint.py
- Build
- kit_male.py
- wardrobe/preview.py
- GuardController.java
- wardrobe.py
- net.minecraft.world.entity.npc.villager.Villager
- wardrobe/paint.py
- Profession
- Clip
- Street
- Wardrobe and outfit engine
- plazas.py
- parts.py
- argparse
- GuardProgression
- Outfit
- WardrobeLayer.java
- Mirror
- workstations.py
- org.junit.jupiter.api.Test
- net.minecraft.world.level.block.state.BlockState
- FriendshipState
- kit_female.py
- Talk
- net.minecraft.server.level.ServerLevel
- Wardrobe
- ResidentBehavior
- AnimationFilmGameTest
- ResidentLife
- Bone
- FriendshipScreen.java
- random
- GuardPolicy
- json
- PaletteID
- ResidentRenderState
- NarrativeContent
- ResidentMotion
- village_design/kit.py
- create_village_structures.py
- Skirt
- GuardProgress
- Motion
- .runTest
- WardrobeTest
- net.minecraft.resources.Identifier
- LedgerPayload
- .runTest
- simulate.py
- com.mojang.serialization.Codec
- Village Friends README
- .runTest
- BondState
- animations/preview.py
- ResidentNames
- FoundationBlock.java
- FriendshipGameTest
- Society
- com.google.gson.JsonObject
- WorkstationBlockEntity
- .animateFace
- .texture
- Procedural Plains Village (villagefriends:village)
- film.py
- Townsfolk
- .key
- GuardDamageLedger
- .runTest
- View
- AnimationClip
- CHANGELOG.md
- net.minecraft.client.gui.GuiGraphicsExtractor
- .target
- Block
- net.minecraft.world.item.Item
- .mention
- WorkstationBlock.java
- catalog.py
- AnimationTrack
- Chemistry
- .runTest
- ResidentModel
- numpy
- Wardrobe Python Module Pipeline (tools/wardrobe)
- AnimationShowcaseScreen
- SocietyTest
- .runTest
- .assembleOutfit
- farms.py
- wardrobe/kit.py
- Emote
- Workstations.java
- net.minecraft.world.item.ItemStack
- AnimationPackGameTest
- .runTest
- GossipTest
- net.minecraft.core.BlockPos
- .onInitializeClient
- FriendshipPayload
- .state
- Dialogue
- .apply
- net.minecraft.client.gui.components.Button
- Box
- SharedHistory
- AnimationPreviewScreen
- DialogueBank
- .day
- Weather
- File format
- dialogue.py
- finish
- strand
- shade
- Day
- Routine
- .runTest
- VillageLedger.java
- .block
- Place
- net.minecraft.world.InteractionHand
- VillageGalleryGameTest
- rot_matrix
- neck
- Village days: routines, weather, working workstations and written dialogue
- roll
- plate
- over_flaps
- arm_blk
- leg_blk
- CLAUDE.md
- Codex Phase 2: Worldgen & Structures
- fur_face
- back_drape
- bare_feet
- check
- flecks
- herringbone
- hood_down
- lacing
- lozenge
- mail
- toggles
- tartan
- shoulder_cape
- tippets
- sash
- skirt_panels
- wraps
- stripes
- toe_pieces
- ribbing

## God Nodes (most connected - your core abstractions)
1. `Build` - 77 edges
2. `Society` - 63 edges
3. `FriendshipScreen` - 47 edges
4. `GuardController` - 46 edges
5. `Profession` - 45 edges
6. `textures()` - 45 edges
7. `Face` - 44 edges
8. `VillageFriends` - 42 edges
9. `Workstations` - 41 edges
10. `Block` - 39 edges

## Surprising Connections (you probably didn't know these)
- `Focused Client GameTest Flags` --references--> `FriendshipGameTest`  [AMBIGUOUS]
  DEVELOPMENT.md → src/gametest/java/dev/villagefriends/FriendshipGameTest.java
- `Phase 2 Structures Verification` --references--> `StructuresGameTest`  [INFERRED]
  PHASE2.md → src/gametest/java/dev/villagefriends/StructuresGameTest.java
- `In-Game Village Gallery (-PvillageGallery)` --references--> `VillageGalleryGameTest`  [INFERRED]
  BUILDING_EDITING.md → src/gametest/java/dev/villagefriends/VillageGalleryGameTest.java
- `Initial Guard Equipment (UUID-selected iron/chainmail)` --references--> `GuardController`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardController.java
- `Combat Profession Lock` --references--> `GuardProgression`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardProgression.java

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Resident Clip Posing Flow (director, library, poser, models)** — src_client_java_dev_villagefriends_client_residentlife_residentlife, src_main_java_dev_villagefriends_animation_animationlibrary_animationlibrary, src_client_java_dev_villagefriends_client_residentposer_residentposer, src_client_java_dev_villagefriends_client_residentanimation_residentanimation, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, src_client_java_dev_villagefriends_client_residentarmormodel_residentarmormodel [EXTRACTED 1.00]
- **Village Building Pipeline (design -> blueprint -> NBT)** — building_editing_design_programs, tools_design_village, building_editing_layered_blueprints, tools_create_village_structures, building_editing_village_layout_json [EXTRACTED 1.00]
- **Guard Progression Architecture** — src_main_java_dev_villagefriends_guardprogress_guardprogress, src_main_java_dev_villagefriends_guarddamageledger_guarddamageledger, src_main_java_dev_villagefriends_guardprogression_guardprogression, guards_guard_progression, guards_damage_based_xp_credit [EXTRACTED 1.00]
- **Wardrobe Rendering Pipeline (bake, atlas, pose worn pieces)** — src_client_java_dev_villagefriends_client_residentskins_residentskins, src_client_java_dev_villagefriends_client_outfitatlas_outfitatlas, src_client_java_dev_villagefriends_client_wardrobelayer_wardrobelayer, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, outfit_engine_palette_lock [EXTRACTED 1.00]
- **Phase 1 Foundation Registration Sequence** — src_main_java_dev_villagefriends_villagefoundation_villagefoundation, src_main_java_dev_villagefriends_villageblocks_villageblocks, src_main_java_dev_villagefriends_villageitems_villageitems, src_main_java_dev_villagefriends_villageblockentities_villageblockentities, src_main_java_dev_villagefriends_villageprofessions_villageprofessions [INFERRED 0.85]

## Communities (190 total, 97 thin omitted)

### Community 0 - "Face"
Cohesion: 0.06
Nodes (13): dags(), lozenges(), mail(), overlay_dags(), quilt_lines(), smocking(), splotch(), stripes() (+5 more)

### Community 1 - "kit_casual.py"
Cohesion: 0.06
Nodes (17): chest_pocket(), collar_points(), crew_neck(), jeans(), leather_belt(), long_sleeves(), placket(), plain_tee() (+9 more)

### Community 2 - "anime_female.py"
Cohesion: 0.07
Nodes (21): aim(), bow(), braided_bun(), bubble_face(), bun(), _caps(), coil_face(), combed() (+13 more)

### Community 3 - "FriendshipScreen"
Cohesion: 0.13
Nodes (3): DockButton, FriendshipScreen, ReplyButton

### Community 4 - "net.minecraft.server.level.ServerPlayer"
Cohesion: 0.12
Nodes (4): NarrativeEngine, Question, TalkWorld, VillageFriends

### Community 5 - "anime_male.py"
Cohesion: 0.07
Nodes (17): chain(), clipped(), clipped_scalp(), coil_face(), cornrow(), cornrow_path(), fade(), loc_face() (+9 more)

### Community 6 - "workstations/paint.py"
Cohesion: 0.09
Nodes (50): archives_front(), arrow(), barrel_end(), blank(), bolt_end(), bottle(), brass(), burlap() (+42 more)

### Community 7 - "Build"
Cohesion: 0.06
Nodes (15): grave(), market_garden(), cart(), flowerbed(), haystack(), tree_birch(), tree_oak(), well() (+7 more)

### Community 9 - "wardrobe/preview.py"
Cohesion: 0.15
Nodes (12): Canvas, composite(), cube_quads(), figure(), label(), layering(), main(), render() (+4 more)

### Community 10 - "GuardController.java"
Cohesion: 0.05
Nodes (16): Guard Equipment Exchange (Equip held item), Initial Guard Equipment (UUID-selected iron/chainmail), Adventure Companions (Follow/Wait/Return home), VillagerEventMixin, BrainRoutineMixin, CompanionPortalMixin, GuardArmorMixin, GuardArrowMixin (+8 more)

### Community 11 - "wardrobe.py"
Cohesion: 0.08
Nodes (25): build(), build_all(), catalog(), compatible(), Garment, hex_rgb(), json_text(), key_rgba() (+17 more)

### Community 12 - "net.minecraft.world.entity.npc.villager.Villager"
Cohesion: 0.12
Nodes (8): Unlimited Safe Archer Arrows, Automatic Village Defense (Knights and Archers), villager_predators Entity Tag, Combat, GuardController, Incident, RecentAttack, Probe

### Community 13 - "wardrobe/paint.py"
Cohesion: 0.12
Nodes (18): band(), button(), cap(), cloth_shade(), curls_box(), curls_face(), fabric(), hair_box() (+10 more)

### Community 15 - "Profession"
Cohesion: 0.06
Nodes (32): Resident, ResidentSampleGameTest, Profession, ADVENTURER, APOTHECARY, ARCHER, ARMORER, BARD (+24 more)

### Community 17 - "Street"
Cohesion: 0.08
Nodes (22): lamp_bench(), avenue(), avenue_bend(), bend_left(), bend_right(), crossroads(), end_fade(), end_gate() (+14 more)

### Community 18 - "Wardrobe and outfit engine"
Cohesion: 0.22
Nodes (8): Mix and match, Palette lock, Pieces, Professions, Recipes and genders, Rendering, Verification, Wardrobe and outfit engine

### Community 19 - "plazas.py"
Cohesion: 0.11
Nodes (19): sine(), market_stalls(), base(), bell_frame(), big_oak(), _dir(), fountain(), fountain_square() (+11 more)

### Community 20 - "parts.py"
Cohesion: 0.07
Nodes (24): market_hall(), block(), is_air(), along(), beam_ring(), bench(), door_cells(), floor() (+16 more)

### Community 21 - "argparse"
Cohesion: 0.09
Nodes (16): Layered JSON Blueprints (tools/village_blueprints), Editable Name Pools (tools/name_pools.json), build(), load(), main(), validate(), main(), main() (+8 more)

### Community 23 - "Outfit"
Cohesion: 0.08
Nodes (9): ColorPalette, Garment, Kind, BOTTOM, HAIR, TOP, HairColor, Outfit (+1 more)

### Community 24 - "WardrobeLayer.java"
Cohesion: 0.12
Nodes (11): ResidentArmorModel, Baked, Shown, WardrobeLayer, BodyPart, HEAD, LEFT_ARM, LEFT_LEG (+3 more)

### Community 26 - "Mirror"
Cohesion: 0.50
Nodes (4): Mirror, FREE, HAND, NEVER

### Community 27 - "workstations.py"
Cohesion: 0.09
Nodes (25): alchemical_press(), archery_target(), archives(), auto_uv(), blockstate(), boxes(), check(), designs() (+17 more)

### Community 29 - "net.minecraft.world.level.block.state.BlockState"
Cohesion: 0.12
Nodes (8): Patrols, Command Desk Controls and Shields (future), Empty Block Entity Integration Hooks, Future Spatial Bed Scanner, ApothecaryCotBlockEntity, CommandDeskBlockEntity, HousePlaqueBlockEntity, NoticeBoardBlockEntity, VillageBlockEntities

### Community 30 - "FriendshipState"
Cohesion: 0.15
Nodes (4): Per-Player Co-op Relationship State, FriendshipBook, FriendshipState, FriendshipTest

### Community 31 - "kit_female.py"
Cohesion: 0.04
Nodes (25): arm_rings(), bells(), buttons(), cloak(), collar_flat(), cuffs(), fur(), fur_box() (+17 more)

### Community 32 - "Talk"
Cohesion: 0.12
Nodes (6): Context, Line, Talk, TalkTest, flower(), Dialogue

### Community 33 - "net.minecraft.server.level.ServerLevel"
Cohesion: 0.09
Nodes (6): Random-Spread Structure Placement, Hometown Names and Settlements, Village Marker, VillageMarkerBlock, VillageNames, VillageSettlements

### Community 34 - "Wardrobe"
Cohesion: 0.15
Nodes (6): Village Friends 2.8.0 — Casual medieval and anime hair expansion, Gender, FEMALE, MALE, NON_BINARY, Wardrobe

### Community 38 - "AnimationFilmGameTest"
Cohesion: 0.18
Nodes (3): AnimationCast, Role, AnimationFilmGameTest

### Community 40 - "Bone"
Cohesion: 0.12
Nodes (10): ResidentPoser, Bone, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG (+2 more)

### Community 42 - "random"
Cohesion: 0.08
Nodes (35): apothecary(), chapel(), crenellate(), garrison(), library(), plaque(), tavern(), workshop() (+27 more)

### Community 43 - "GuardPolicy"
Cohesion: 0.11
Nodes (8): Friendship Forgiveness for Player Hits, Gifts and Promises, Relationship Tiers (New Neighbor to Best Friend), Milestone 7: Romance and Family (future), Shared Activities (Walk, Picnic, Exploration, Gathering), GiftPreferences, GuardPolicy, GuardPolicyTest

### Community 44 - "json"
Cohesion: 0.11
Nodes (18): Foundation Asset Generation Pipeline, icon(), merge(), recipe(), save(), tag(), save(), item_sprite() (+10 more)

### Community 45 - "PaletteID"
Cohesion: 0.12
Nodes (12): PaletteID, ASH_AND_TEAL, DESERT_SUN, FOREST_AND_HEARTH, ROYAL_VELVET, RUSTIC_TWEED, SAGE_AND_TERRACOTTA, SCHOLARLY_PLUM (+4 more)

### Community 46 - "ResidentRenderState"
Cohesion: 0.13
Nodes (3): ResidentRenderer, ResidentRenderState, ResidentAppearance

### Community 47 - "NarrativeContent"
Cohesion: 0.18
Nodes (8): Narrative Content Pack (content.json), Four-Chapter Personal Stories, Conditions, Data, NarrativeContent, Personality, Request, Story

### Community 48 - "ResidentMotion"
Cohesion: 0.13
Nodes (11): Shared Gait Function (resident and armor models), Living Villagers (walking styles, breathing, articulated eyes), Gait, CURIOUS, EASY, MEASURED, NIMBLE, SPRIGHTLY (+3 more)

### Community 49 - "village_design/kit.py"
Cohesion: 0.22
Nodes (13): bid(), can_take(), stairs_at(), full_cube(), gate_connects(), is_fence(), is_gate(), is_pane() (+5 more)

### Community 50 - "create_village_structures.py"
Cohesion: 0.08
Nodes (17): Replacement Pools and required_pools, Structure Processors (worn roads, plank bridges, weathered stone), Village Layout Config (tools/village_layout.json, format 2), Byte, check_lot(), location(), main(), payload() (+9 more)

### Community 51 - "Skirt"
Cohesion: 0.10
Nodes (5): band(), pleats(), Skirt, tier(), trim()

### Community 53 - "Motion"
Cohesion: 0.40
Nodes (5): Motion, FLAP_BACK, FLAP_FRONT, NONE, SWAY

### Community 54 - ".runTest"
Cohesion: 0.21
Nodes (3): Focused Client GameTest Flags, OutfitGameTest, OutfitTemplate

### Community 55 - "WardrobeTest"
Cohesion: 0.09
Nodes (17): Fit, FEMALE, MALE, UNISEX, WardrobeTest, Guard defense verification (2.9.0), Guard progression verification (2.10.0), Guard spawn egg verification (2.10.1) (+9 more)

### Community 56 - "net.minecraft.resources.Identifier"
Cohesion: 0.15
Nodes (3): Entry, Loaded, ResidentSkins

### Community 57 - "LedgerPayload"
Cohesion: 0.14
Nodes (8): ActionPayload, EmotePayload, Detail, Entry, LedgerPayload, Tie, LedgerRequestPayload, Where things live

### Community 60 - "simulate.py"
Cohesion: 0.27
Nodes (11): Village Layout Simulation, In-Game Village Gallery (-PvillageGallery), assemble(), draw(), load(), main(), overlaps(), placed_box() (+3 more)

### Community 63 - "Village Friends README"
Cohesion: 0.32
Nodes (7): Editing the Plains Village, Village Friends Developer Handoff, Knights and Archers Guide, Phase 1 Implementation: Registry & Item Foundation, Phase 2 Structures: Worldgen & Structures, Village Friends README, Village Friends 2.12.0 Fabric Mod

### Community 64 - ".runTest"
Cohesion: 0.14
Nodes (4): Persistent Resident Identity (stable ID), CommunityGameTest, CompanionState, ResidentProfile

### Community 65 - "BondState"
Cohesion: 0.16
Nodes (3): Resident-to-Resident Connections, BondBook, BondState

### Community 67 - "animations/preview.py"
Cohesion: 0.18
Nodes (8): draw(), load_pack(), main(), pose(), render_frame(), Resident, sample(), Track

### Community 68 - "ResidentNames"
Cohesion: 0.26
Nodes (3): Data, Pool, ResidentNames

### Community 69 - "FoundationBlock.java"
Cohesion: 0.08
Nodes (9): FoundationBlock, FoundationEntityBlock, Kind, APOTHECARY_COT, COMMAND_DESK, HOUSE_PLAQUE, NOTICE_BOARD, VillageBlocks (+1 more)

### Community 71 - "Society"
Cohesion: 0.15
Nodes (3): News, Society, Tie

### Community 72 - "com.google.gson.JsonObject"
Cohesion: 0.18
Nodes (3): StructuresGameTest, View, Vec3

### Community 74 - ".animateFace"
Cohesion: 0.23
Nodes (8): Animation packs, Eyes and face, Gaits, Resident movement, animation packs and eyes, Verification, EyeStyle, SOFT_GLINT, STARLIT

### Community 75 - ".texture"
Cohesion: 0.13
Nodes (4): HairFaceGameTest, FaceDetails, HandcraftedFaceTest, Starlit and Soft Glint faces verification (2.13.0)

### Community 77 - "Procedural Plains Village (villagefriends:village)"
Cohesion: 0.19
Nodes (14): Civic Slots (priority 5), Village Design Kit (kit.py, parts.py, roads.py), Building Design Programs (DESIGNS = {name: function}), Lot Contract (building_entrance jigsaw), Lots (homes, workshops, decorations, empty gaps), Village Jigsaw Graph, Native Trade Sets (50 sets, 100 offers), Ten New Professions and Workstations (+6 more)

### Community 78 - "film.py"
Cohesion: 0.22
Nodes (8): card(), font(), main(), emit(), fade(), hold(), play(), scene_frames()

### Community 81 - "GuardDamageLedger"
Cohesion: 0.18
Nodes (7): Combat Profession Lock, Damage-Based Guard XP Credit, Guard Level Progression (0-50), GuardDamageLedger, Hit, Credit, GuardDamageLedgerTest

### Community 83 - "View"
Cohesion: 0.18
Nodes (8): Cell, OutfitPreviewScreen, View, BACK, FRONT, HEAD, HEAD_BACK, WALK

### Community 84 - "AnimationClip"
Cohesion: 0.11
Nodes (5): AnimationLayer, AnimationClip, AnimationLibrary, AnimationPack, AnimationPackTest

### Community 85 - "CHANGELOG.md"
Cohesion: 0.09
Nodes (19): 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0, 2.6.0, Male asset registry — Phase 2 (+11 more)

### Community 88 - "Block"
Cohesion: 0.07
Nodes (25): Block, BREAKFAST, EVENING, HOBBY, LESSONS, LUNCH, LUNCH_HOME, LUNCH_TAVERN (+17 more)

### Community 89 - "net.minecraft.world.item.Item"
Cohesion: 0.08
Nodes (18): Phase 1 Foundation Gameplay Verification, Future Real-Time Knockout Controller, Bread, Stew and Coffee Consumables, Medical Treatment Contract, 17 New Foundation Blocks, 24 New Items and 41 Recipes, Registration Order (blocks, items, block entities, professions), Codex Phase 1: Registry & Item Foundation (+10 more)

### Community 91 - "WorkstationBlock.java"
Cohesion: 0.08
Nodes (14): Canvas, Station, ALCHEMICAL_PRESS, ARCHERY_TARGET, ARCHIVES, DRINKS_BARREL, EASEL_CANVAS, KITCHEN_STOVE (+6 more)

### Community 92 - "catalog.py"
Cohesion: 0.28
Nodes (3): Foundation Catalog (foundation-catalog.json), Room/Structure Catalog (structure-catalog.json), designs()

### Community 97 - "numpy"
Cohesion: 0.31
Nodes (9): envelope(), finish(), glottal(), hum(), make_ui(), make_voice(), resonator(), voiced() (+1 more)

### Community 98 - "Wardrobe Python Module Pipeline (tools/wardrobe)"
Cohesion: 0.10
Nodes (13): Locked One-Piece Outfits (locked_to), Supreme Casual Line (t101-t120, b101-b120), Wardrobe Python Module Pipeline (tools/wardrobe), back_fan(), bangs(), cel_box(), cel_face(), lock() (+5 more)

### Community 102 - ".assembleOutfit"
Cohesion: 0.19
Nodes (5): Ten Master Palettes, Sims-style Men's and Women's Wardrobes, MasterPalettes, OutfitFactory, OutfitEngineTest

### Community 103 - "farms.py"
Cohesion: 0.24
Nodes (7): farm_beets(), farm_mixed(), farm_wheat(), field(), paddock(), pumpkin_patch(), scarecrow()

### Community 105 - "wardrobe/kit.py"
Cohesion: 0.09
Nodes (8): belt(), flaps(), footwear(), leg_bone(), leg_ring(), legs(), neckline(), sleeves()

### Community 106 - "Emote"
Cohesion: 0.11
Nodes (16): Bubble, EmoteBubbles, Pending, Emote, ANGER, BLUSH, DOTS, EXCLAIM (+8 more)

### Community 107 - "Workstations.java"
Cohesion: 0.11
Nodes (3): Song, Songbook, Note

### Community 114 - "GossipTest"
Cohesion: 0.19
Nodes (7): GossipTest, Conversation window, Friendship levels, Speech bubbles, Verification, Village Ledger, Village life: families, love, friendship levels, speech bubbles and the Village Ledger

### Community 115 - "net.minecraft.core.BlockPos"
Cohesion: 0.13
Nodes (5): ResidentRoutines, Spot, VillageBook, VillageRecord, Combo

### Community 118 - ".state"
Cohesion: 0.24
Nodes (3): CompanionController, Outing, Choice

### Community 119 - "Dialogue"
Cohesion: 0.24
Nodes (3): Conversation Window (Talk/Story/Journal/Time/Travel tabs), Wordless Human-like Hum Voices, Dialogue

### Community 122 - "Box"
Cohesion: 0.12
Nodes (3): strip_line(), Box, Layer

### Community 132 - "DialogueBank"
Cohesion: 0.17
Nodes (3): Answer, DialogueBank, DialogueBankTest

### Community 134 - "Weather"
Cohesion: 0.14
Nodes (7): Plan, Weather, CLEAR, CLEARING, RAIN, SNOW, THUNDER

### Community 135 - "File format"
Cohesion: 0.15
Nodes (11): Authoring Village Life, File format, How the director chooses, Resident animation packs, Village Life (pack 1), body(), Editing the wardrobe, Genders and locked sets (+3 more)

### Community 136 - "dialogue.py"
Cohesion: 0.38
Nodes (10): boxes(), check_text(), compile_all(), count(), fail(), main(), parse_answer(), read_lines() (+2 more)

### Community 137 - "finish"
Cohesion: 0.19
Nodes (7): axis(), braid(), curve(), finish(), link(), plait_path(), _step()

### Community 138 - "strand"
Cohesion: 0.17
Nodes (6): fall(), fringe(), point(), pointed(), points(), strand()

### Community 139 - "shade"
Cohesion: 0.17
Nodes (7): checks(), lacing(), motif(), scatter(), dark_seams(), darken_rows(), shade()

### Community 140 - "Day"
Cohesion: 0.24
Nodes (6): Chronotype, EARLY_BIRD, NIGHT_OWL, REGULAR, Day, Slot

### Community 145 - "Place"
Cohesion: 0.25
Nodes (7): Place, BELL, HOBBY, HOME, TAVERN, VILLAGE, WORK

### Community 148 - "rot_matrix"
Cohesion: 0.29
Nodes (3): local(), world(), rot_matrix()

### Community 149 - "neck"
Cohesion: 0.33
Nodes (3): bodice(), chemise(), neck()

### Community 150 - "Village days: routines, weather, working workstations and written dialogue"
Cohesion: 0.33
Nodes (6): Daily routines, Verification, Village days: routines, weather, working workstations and written dialogue, Weather, Where things live, Workstations

### Community 151 - "roll"
Cohesion: 0.40
Nodes (3): arm_bone(), arm_x(), roll()

### Community 157 - "Codex Phase 2: Worldgen & Structures"
Cohesion: 0.67
Nodes (3): Master Specification (Codex roadmap), Phase 2 Structures Verification, Codex Phase 2: Worldgen & Structures

## Ambiguous Edges - Review These
- `FriendshipGameTest` → `Focused Client GameTest Flags`  [AMBIGUOUS]
  DEVELOPMENT.md · relation: references
- `GuardArmorMixin` → `Initial Guard Equipment (UUID-selected iron/chainmail)`  [AMBIGUOUS]
  GUARDS.md · relation: references

## Knowledge Gaps
- **200 isolated node(s):** `Loaded`, `FRONT`, `BACK`, `HEAD`, `HEAD_BACK` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 962 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **97 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `FriendshipGameTest` and `Focused Client GameTest Flags`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Wardrobe Python Module Pipeline (tools/wardrobe)` connect `Wardrobe Python Module Pipeline (tools/wardrobe)` to `kit_casual.py`, `anime_female.py`, `anime_male.py`, `.assembleOutfit`, `kit_male.py`, `wardrobe/kit.py`, `wardrobe.py`, `Procedural Plains Village (villagefriends:village)`, `Village Friends README`, `kit_female.py`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **What connects `Loaded`, `FRONT`, `BACK` to the rest of the system?**
  _200 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Face` be split into smaller, more focused modules?**
  _Cohesion score 0.06156156156156156 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `GuardArmorMixin` and `Initial Guard Equipment (UUID-selected iron/chainmail)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Sims-style Men's and Women's Wardrobes` connect `.assembleOutfit` to `WardrobeLayer.java`, `Wardrobe Python Module Pipeline (tools/wardrobe)`, `Wardrobe`, `Village Friends README`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Should `kit_casual.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06116642958748222 - nodes in this community are weakly interconnected._