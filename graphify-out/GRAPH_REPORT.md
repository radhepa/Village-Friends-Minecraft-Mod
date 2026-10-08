# Graph Report - Village-Friends-Minecraft-Mod  (2026-10-08)

## Corpus Check
- 282 files · ~346,837 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .properties 2, .jar 1)

## Summary
- 4439 nodes · 11475 edges · 243 communities (122 shown, 121 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 732 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8d13a6c0`
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
- numpy
- org.spongepowered.asm.mixin.injection.Inject
- wardrobe.py
- GuardController
- wardrobe/paint.py
- Profession
- Clip
- Street
- Wardrobe and outfit engine
- math
- parts.py
- json
- GuardProgression
- Outfit
- WardrobeLayer.java
- com.google.gson.JsonObject
- workstations.py
- org.junit.jupiter.api.Test
- net.minecraft.server.level.ServerLevel
- FriendshipState
- kit_female.py
- DialogueBank
- VillageRecord
- Wardrobe
- TavernClient.java
- AnimationPackTest
- ResidentLife
- civic.py
- Bone
- random
- kit_m04.py
- sys
- PaletteID
- ResidentRenderState
- ResidentNames
- ResidentMotion
- village_design/kit.py
- create_village_structures.py
- Skirt
- GuardProgress
- ColorPalette
- .runTest
- WardrobeTest
- ResidentSkins
- LedgerPayload
- .runTest
- simulate.py
- com.mojang.serialization.Codec
- Village Friends README
- .runTest
- BondState
- animations/preview.py
- Patronage
- net.minecraft.core.BlockPos
- kit_m07.py
- Society
- StructuresGameTest
- Seat
- .animateFace
- .texture
- Procedural Plains Village (villagefriends:village)
- film.py
- Townsfolk
- .runTest
- GuardDamageLedger
- .runTest
- View
- AnimationClip
- CHANGELOG.md
- net.minecraft.client.gui.GuiGraphicsExtractor
- .profile
- Block
- VillageBlocks
- .detail
- net.minecraft.world.level.block.state.BlockState
- kit_m01.py
- AnimationTrack
- Chemistry
- .key
- ResidentModel.java
- furniture.py
- Wardrobe Python Module Pipeline (tools/wardrobe)
- kit_f04.py
- SocietyTest
- VillageLifeGameTest
- .assembleOutfit
- argparse
- .affinity
- wardrobe/kit.py
- Emote
- .perform
- net.minecraft.world.item.ItemStack
- kit_m03.py
- Village days verification (2.14.0)
- kit_f07.py
- net.minecraft.world.entity.npc.villager.Villager
- ArrivalBanner
- FriendshipPayload
- .state
- Dialogue
- org.spongepowered.asm.mixin.Mixin
- net.minecraft.client.gui.components.Button
- Box
- kit_m05.py
- tavern_preview.py
- kit_f03.py
- .target
- kit_f02.py
- File format
- re
- rot_matrix
- strand
- shade
- kit_m06.py
- net.minecraft.world.entity.schedule.Activity
- .runTest
- kit_m10.py
- .block
- kit_m08.py
- TavernClient
- net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext
- kit_f01.py
- kit_f06.py
- .runTest
- Treatment
- kit_m02.py
- GuardArrowMixin.java
- arm_blk
- leg_blk
- kit_f05.py
- ResidentSampleGameTest
- Scene
- back_drape
- bare_feet
- check
- flecks
- VillagerCompanionMixin.java
- hood_down
- lacing
- lozenge
- mail
- toggles
- tartan
- .register
- tippets
- kit_f10.py
- skirt_panels
- wraps
- stripes
- toe_pieces
- How a batch is built
- VillageProfessions
- .runTest
- FriendshipLevels
- Model
- Concepts
- .send
- .box
- BodyPart
- dining.py
- io
- clipped
- seated.py
- chat.py
- bar.py
- FoundationPreviewScreen
- render
- Resident movement, animation packs and eyes
- belt
- flaps
- footwear
- legs
- embroider
- neckline
- sleeves

## God Nodes (most connected - your core abstractions)
1. `Build` - 77 edges
2. `Society` - 65 edges
3. `Taverns` - 62 edges
4. `Block` - 52 edges
5. `Face` - 48 edges
6. `FriendshipScreen` - 47 edges
7. `GuardController` - 46 edges
8. `Workstations` - 45 edges
9. `Profession` - 45 edges
10. `textures()` - 45 edges

## Surprising Connections (you probably didn't know these)
- `Focused Client GameTest Flags` --references--> `FriendshipGameTest`  [AMBIGUOUS]
  DEVELOPMENT.md → src/gametest/java/dev/villagefriends/FriendshipGameTest.java
- `Phase 2 Structures Verification` --references--> `StructuresGameTest`  [INFERRED]
  PHASE2.md → src/gametest/java/dev/villagefriends/StructuresGameTest.java
- `In-Game Village Gallery (-PvillageGallery)` --references--> `VillageGalleryGameTest`  [INFERRED]
  BUILDING_EDITING.md → src/gametest/java/dev/villagefriends/VillageGalleryGameTest.java
- `Initial Guard Equipment (UUID-selected iron/chainmail)` --references--> `GuardController`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardController.java
- `villager_predators Entity Tag` --shares_data_with--> `GuardController`  [INFERRED]
  GUARDS.md → src/main/java/dev/villagefriends/GuardController.java

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Resident Clip Posing Flow (director, library, poser, models)** — src_client_java_dev_villagefriends_client_residentlife_residentlife, src_main_java_dev_villagefriends_animation_animationlibrary_animationlibrary, src_client_java_dev_villagefriends_client_residentposer_residentposer, src_client_java_dev_villagefriends_client_residentanimation_residentanimation, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, src_client_java_dev_villagefriends_client_residentarmormodel_residentarmormodel [EXTRACTED 1.00]
- **Village Building Pipeline (design -> blueprint -> NBT)** — building_editing_design_programs, tools_design_village, building_editing_layered_blueprints, tools_create_village_structures, building_editing_village_layout_json [EXTRACTED 1.00]
- **Guard Progression Architecture** — src_main_java_dev_villagefriends_guardprogress_guardprogress, src_main_java_dev_villagefriends_guarddamageledger_guarddamageledger, src_main_java_dev_villagefriends_guardprogression_guardprogression, guards_guard_progression, guards_damage_based_xp_credit [EXTRACTED 1.00]
- **Wardrobe Rendering Pipeline (bake, atlas, pose worn pieces)** — src_client_java_dev_villagefriends_client_residentskins_residentskins, src_client_java_dev_villagefriends_client_outfitatlas_outfitatlas, src_client_java_dev_villagefriends_client_wardrobelayer_wardrobelayer, src_client_java_dev_villagefriends_client_residentmodel_residentmodel, outfit_engine_palette_lock [EXTRACTED 1.00]
- **Phase 1 Foundation Registration Sequence** — src_main_java_dev_villagefriends_villagefoundation_villagefoundation, src_main_java_dev_villagefriends_villageblocks_villageblocks, src_main_java_dev_villagefriends_villageitems_villageitems, src_main_java_dev_villagefriends_villageblockentities_villageblockentities, src_main_java_dev_villagefriends_villageprofessions_villageprofessions [INFERRED 0.85]

## Communities (243 total, 121 thin omitted)

### Community 0 - "Face"
Cohesion: 0.07
Nodes (11): dags(), gathers(), lozenges(), mail(), overlay_dags(), quilt_lines(), splotch(), stripes() (+3 more)

### Community 1 - "kit_casual.py"
Cohesion: 0.06
Nodes (17): chest_pocket(), collar_points(), crew_neck(), jeans(), leather_belt(), long_sleeves(), placket(), plain_tee() (+9 more)

### Community 2 - "anime_female.py"
Cohesion: 0.07
Nodes (22): aim(), bow(), braided_bun(), bubble_face(), bun(), _caps(), coil_face(), combed() (+14 more)

### Community 3 - "FriendshipScreen"
Cohesion: 0.13
Nodes (3): DockButton, FriendshipScreen, ReplyButton

### Community 4 - "net.minecraft.server.level.ServerPlayer"
Cohesion: 0.12
Nodes (5): Choice, NarrativeEngine, Question, TalkWorld, VillageFriends

### Community 5 - "anime_male.py"
Cohesion: 0.07
Nodes (20): cel_box(), cel_face(), chain(), clump(), coil_face(), combed_face(), cornrow(), cornrow_path() (+12 more)

### Community 6 - "workstations/paint.py"
Cohesion: 0.09
Nodes (50): archives_front(), arrow(), barrel_end(), blank(), bolt_end(), bottle(), brass(), burlap() (+42 more)

### Community 7 - "Build"
Cohesion: 0.05
Nodes (17): cart(), haystack(), tree_birch(), tree_oak(), well(), woodpile(), apiary(), farm_beets() (+9 more)

### Community 8 - "kit_male.py"
Cohesion: 0.13
Nodes (6): fur(), fur_face(), herringbone(), ribbing(), sash(), shoulder_cape()

### Community 9 - "numpy"
Cohesion: 0.11
Nodes (21): envelope(), finish(), glottal(), hum(), make_ui(), make_voice(), resonator(), voiced() (+13 more)

### Community 10 - "org.spongepowered.asm.mixin.injection.Inject"
Cohesion: 0.20
Nodes (5): Initial Guard Equipment (UUID-selected iron/chainmail), VillagerEventMixin, GuardArmorMixin, GuardTradeDisplayMixin, WorkAtPoiMixin

### Community 11 - "wardrobe.py"
Cohesion: 0.09
Nodes (25): build(), build_all(), catalog(), compatible(), Garment, hex_rgb(), json_text(), key_rgba() (+17 more)

### Community 12 - "GuardController"
Cohesion: 0.14
Nodes (5): Combat, GuardController, Incident, RecentAttack, Probe

### Community 13 - "wardrobe/paint.py"
Cohesion: 0.11
Nodes (19): band(), button(), cap(), cloth_shade(), curls_box(), curls_face(), fabric(), grid() (+11 more)

### Community 15 - "Profession"
Cohesion: 0.06
Nodes (30): Profession, ADVENTURER, APOTHECARY, ARCHER, ARMORER, BARD, BUTCHER, CARPENTER (+22 more)

### Community 17 - "Street"
Cohesion: 0.08
Nodes (22): market_stalls(), lamp_bench(), avenue(), avenue_bend(), bend_left(), bend_right(), crossroads(), end_fade() (+14 more)

### Community 18 - "Wardrobe and outfit engine"
Cohesion: 0.14
Nodes (12): Mix and match, Palette lock, Pieces, Professions, Recipes and genders, Rendering, Verification, Wardrobe and outfit engine (+4 more)

### Community 19 - "math"
Cohesion: 0.12
Nodes (18): base(), bell_frame(), big_oak(), _dir(), fountain(), fountain_square(), gazebo(), lamp_ring() (+10 more)

### Community 20 - "parts.py"
Cohesion: 0.07
Nodes (23): block(), is_air(), along(), beam_ring(), bench(), door_cells(), floor(), foundation() (+15 more)

### Community 21 - "json"
Cohesion: 0.08
Nodes (17): Layered JSON Blueprints (tools/village_blueprints), Foundation Catalog (foundation-catalog.json), Room/Structure Catalog (structure-catalog.json), merge(), recipe(), save(), tag(), save() (+9 more)

### Community 22 - "GuardProgression"
Cohesion: 0.13
Nodes (4): Combat Profession Lock, Guard Level Progression (0-50), GuardProgressGameTest, GuardProgression

### Community 23 - "Outfit"
Cohesion: 0.13
Nodes (3): Garment, HairColor, Outfit

### Community 24 - "WardrobeLayer.java"
Cohesion: 0.14
Nodes (4): ResidentArmorModel, Baked, Shown, WardrobeLayer

### Community 26 - "com.google.gson.JsonObject"
Cohesion: 0.25
Nodes (5): Mirror, FREE, HAND, NEVER, AnimationPack

### Community 27 - "workstations.py"
Cohesion: 0.16
Nodes (20): alchemical_press(), archery_target(), archives(), blockstate(), boxes(), check(), designs(), drinks_barrel() (+12 more)

### Community 28 - "org.junit.jupiter.api.Test"
Cohesion: 0.11
Nodes (4): CommunityTest, RoadmapTest, RoutineTest, Daily routines

### Community 29 - "net.minecraft.server.level.ServerLevel"
Cohesion: 0.12
Nodes (5): House, Order, Patron, Runner, Taverns

### Community 30 - "FriendshipState"
Cohesion: 0.06
Nodes (13): Friendship Forgiveness for Player Hits, Gifts and Promises, Per-Player Co-op Relationship State, Relationship Tiers (New Neighbor to Best Friend), Milestone 7: Romance and Family (future), Shared Activities (Walk, Picnic, Exploration, Gathering), FriendshipBook, FriendshipState (+5 more)

### Community 31 - "kit_female.py"
Cohesion: 0.04
Nodes (30): arm_rings(), bells(), bodice(), buttons(), chemise(), cloak(), collar_flat(), cuffs() (+22 more)

### Community 32 - "DialogueBank"
Cohesion: 0.07
Nodes (14): Village Friends 2.14.0 — Village days, working workstations and 5,898 pieces of dialogue, Answer, DialogueBank, Context, Line, Talk, DialogueBankTest, TalkTest (+6 more)

### Community 33 - "VillageRecord"
Cohesion: 0.07
Nodes (9): Random-Spread Structure Placement, Hometown Names and Settlements, Village Marker, VillageBook, VillageMarkerBlock, VillageNames, VillageRecord, Arrival (+1 more)

### Community 34 - "Wardrobe"
Cohesion: 0.13
Nodes (6): Village Friends 2.8.0 — Casual medieval and anime hair expansion, Gender, FEMALE, MALE, NON_BINARY, Wardrobe

### Community 37 - "AnimationPackTest"
Cohesion: 0.12
Nodes (10): Authoring Village Life, How the director chooses, Resident animation packs, Village Life (pack 1), Village Friends 2.15.0 — Village Life grows to 349 clips, Village Friends 2.19.0 — The tavern, AnimationPackTest, TavernPackTest (+2 more)

### Community 38 - "ResidentLife"
Cohesion: 0.06
Nodes (8): Village Life Animation Pack (99 clips), Playing, ResidentLife, AnimationCast, Role, AnimationFilmGameTest, AnimationPackGameTest, ResidentBehavior

### Community 39 - "civic.py"
Cohesion: 0.08
Nodes (23): apothecary(), chapel(), crenellate(), garrison(), grave(), library(), plaque(), tavern() (+15 more)

### Community 40 - "Bone"
Cohesion: 0.13
Nodes (10): ResidentPoser, Bone, BODY, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG (+2 more)

### Community 42 - "random"
Cohesion: 0.10
Nodes (26): market_garden(), cottage(), family_house(), farmhouse(), garden(), kitchen(), path(), tall_house() (+18 more)

### Community 43 - "kit_m04.py"
Cohesion: 0.05
Nodes (18): baldric(), chain(), diag(), hanging(), key_shape(), lamellar(), lames(), leg_prop() (+10 more)

### Community 44 - "sys"
Cohesion: 0.10
Nodes (20): Foundation Asset Generation Pipeline, icon(), item_sprite(), raster(), uniform(), bubble(), dots(), emote_sheet() (+12 more)

### Community 45 - "PaletteID"
Cohesion: 0.13
Nodes (12): PaletteID, ASH_AND_TEAL, DESERT_SUN, FOREST_AND_HEARTH, ROYAL_VELVET, RUSTIC_TWEED, SAGE_AND_TERRACOTTA, SCHOLARLY_PLUM (+4 more)

### Community 46 - "ResidentRenderState"
Cohesion: 0.13
Nodes (3): ResidentAnimation, ResidentRenderer, ResidentRenderState

### Community 47 - "ResidentNames"
Cohesion: 0.07
Nodes (14): Narrative Content Pack (content.json), Four-Chapter Personal Stories, Conditions, Data, NarrativeContent, Personality, Request, Story (+6 more)

### Community 48 - "ResidentMotion"
Cohesion: 0.10
Nodes (12): Shared Gait Function (resident and armor models), Living Villagers (walking styles, breathing, articulated eyes), AnimationPreviewScreen, Gait, CURIOUS, EASY, MEASURED, NIMBLE (+4 more)

### Community 49 - "village_design/kit.py"
Cohesion: 0.22
Nodes (13): bid(), can_take(), stairs_at(), full_cube(), gate_connects(), is_fence(), is_gate(), is_pane() (+5 more)

### Community 50 - "create_village_structures.py"
Cohesion: 0.09
Nodes (14): Byte, check_lot(), location(), main(), payload(), pool(), pool_name(), pool_spec() (+6 more)

### Community 51 - "Skirt"
Cohesion: 0.10
Nodes (5): band(), pleats(), Skirt, tier(), trim()

### Community 53 - "ColorPalette"
Cohesion: 0.08
Nodes (11): Ten Master Palettes, Sims-style Men's and Women's Wardrobes, ColorPalette, MasterPalettes, Motion, FLAP_BACK, FLAP_FRONT, NONE (+3 more)

### Community 55 - "WardrobeTest"
Cohesion: 0.08
Nodes (18): Fit, FEMALE, MALE, UNISEX, WardrobeTest, Guard defense verification (2.9.0), Guard progression verification (2.10.0), Guard spawn egg verification (2.10.1) (+10 more)

### Community 56 - "ResidentSkins"
Cohesion: 0.15
Nodes (3): Entry, Loaded, ResidentSkins

### Community 57 - "LedgerPayload"
Cohesion: 0.12
Nodes (9): VillageFriendsClient, ActionPayload, EmotePayload, Detail, Entry, LedgerPayload, Tie, LedgerRequestPayload (+1 more)

### Community 60 - "simulate.py"
Cohesion: 0.20
Nodes (14): Village Layout Simulation, Replacement Pools and required_pools, Structure Processors (worn roads, plank bridges, weathered stone), In-Game Village Gallery (-PvillageGallery), Village Layout Config (tools/village_layout.json, format 2), assemble(), draw(), load() (+6 more)

### Community 63 - "Village Friends README"
Cohesion: 0.22
Nodes (9): Editing the Plains Village, graphify, Village Friends, Village Friends Developer Handoff, Knights and Archers Guide, Phase 1 Implementation: Registry & Item Foundation, Phase 2 Structures: Worldgen & Structures, Village Friends README (+1 more)

### Community 65 - "BondState"
Cohesion: 0.18
Nodes (3): Resident-to-Resident Connections, BondBook, BondState

### Community 67 - "animations/preview.py"
Cohesion: 0.18
Nodes (8): draw(), load_pack(), main(), pose(), render_frame(), Resident, sample(), Track

### Community 68 - "Patronage"
Cohesion: 0.10
Nodes (18): Choice, Kind, ARMCHAIR, BENCH, CHAIR, STOOL, Mood, Neighbor (+10 more)

### Community 69 - "net.minecraft.core.BlockPos"
Cohesion: 0.21
Nodes (4): Spot, Stand, Tavern, TavernSurvey

### Community 70 - "kit_m07.py"
Cohesion: 0.07
Nodes (14): baldric(), coil(), disc(), dust(), hang(), leg_shell(), outer(), patch() (+6 more)

### Community 71 - "Society"
Cohesion: 0.14
Nodes (3): News, Society, SocietyBook

### Community 74 - ".animateFace"
Cohesion: 0.35
Nodes (4): Eyes and face, EyeStyle, SOFT_GLINT, STARLIT

### Community 75 - ".texture"
Cohesion: 0.13
Nodes (3): HairFaceGameTest, FaceDetails, HandcraftedFaceTest

### Community 77 - "Procedural Plains Village (villagefriends:village)"
Cohesion: 0.23
Nodes (12): Civic Slots (priority 5), Village Design Kit (kit.py, parts.py, roads.py), Building Design Programs (DESIGNS = {name: function}), Lot Contract (building_entrance jigsaw), Lots (homes, workshops, decorations, empty gaps), Village Jigsaw Graph, Six Guaranteed Civic Buildings, Enclosed Bedrooms (+4 more)

### Community 78 - "film.py"
Cohesion: 0.24
Nodes (8): card(), font(), main(), emit(), fade(), hold(), play(), scene_frames()

### Community 80 - ".runTest"
Cohesion: 0.19
Nodes (7): Phase 1 Foundation Gameplay Verification, Master Specification (Codex roadmap), 17 New Foundation Blocks, Codex Phase 1: Registry & Item Foundation, Phase 2 Structures Verification, Codex Phase 2: Worldgen & Structures, FoundationGameTest

### Community 81 - "GuardDamageLedger"
Cohesion: 0.20
Nodes (5): Damage-Based Guard XP Credit, GuardDamageLedger, Hit, Credit, GuardDamageLedgerTest

### Community 83 - "View"
Cohesion: 0.12
Nodes (10): AnimationShowcaseScreen, Cell, Cell, OutfitPreviewScreen, View, BACK, FRONT, HEAD (+2 more)

### Community 84 - "AnimationClip"
Cohesion: 0.13
Nodes (4): AnimationLayer, AnimationPacks, AnimationClip, AnimationLibrary

### Community 85 - "CHANGELOG.md"
Cohesion: 0.08
Nodes (20): 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.5.0, 2.6.0, Male asset registry — Phase 2 (+12 more)

### Community 88 - "Block"
Cohesion: 0.04
Nodes (49): Block, BREAKFAST, DEFEND, EVENING, HOBBY, LESSONS, LUNCH, LUNCH_HOME (+41 more)

### Community 89 - "VillageBlocks"
Cohesion: 0.15
Nodes (4): Registration Order (blocks, items, block entities, professions), VillageBlocks, VillageFoundation, VillageItems

### Community 90 - ".detail"
Cohesion: 0.17
Nodes (3): Gossip, Relations, Dialogue

### Community 91 - "net.minecraft.world.level.block.state.BlockState"
Cohesion: 0.04
Nodes (30): Patrols, Command Desk Controls and Shields (future), Empty Block Entity Integration Hooks, Future Spatial Bed Scanner, ApothecaryCotBlockEntity, CommandDeskBlockEntity, FoundationBlock, FoundationEntityBlock, Kind (+22 more)

### Community 92 - "kit_m01.py"
Cohesion: 0.07
Nodes (14): gathers(), hanging_basket(), leg_tube(), mud(), outer(), patch(), piebald(), rod() (+6 more)

### Community 94 - "Chemistry"
Cohesion: 0.18
Nodes (7): Chemistry, Conversation window, Friendship levels, The model, Village Ledger, Village life: families, love, friendship levels, speech bubbles and the Village Ledger, Where things live

### Community 97 - "furniture.py"
Cohesion: 0.12
Nodes (17): blockstate(), boxes(), check(), cloth(), cloth_tacks(), cushion(), designs(), dump() (+9 more)

### Community 98 - "Wardrobe Python Module Pipeline (tools/wardrobe)"
Cohesion: 0.13
Nodes (9): Locked One-Piece Outfits (locked_to), Supreme Casual Line (t101-t120, b101-b120), Wardrobe Python Module Pipeline (tools/wardrobe), back_fan(), bangs(), lock(), ring_shell(), sidelocks() (+1 more)

### Community 99 - "kit_f04.py"
Cohesion: 0.07
Nodes (9): back_prop(), front_prop(), lamellae(), lames(), mud(), quilt_rows(), Rod, shaft() (+1 more)

### Community 100 - "SocietyTest"
Cohesion: 0.18
Nodes (6): Village Friends 2.13.0 — Village life and new faces, FriendshipLevelsTest, GossipTest, SocietyTest, Village life verification (2.13.0), Verification

### Community 103 - "argparse"
Cohesion: 0.13
Nodes (15): Editable Name Pools (tools/name_pools.json), build(), load(), main(), validate(), sine(), check(), main() (+7 more)

### Community 105 - "wardrobe/kit.py"
Cohesion: 0.15
Nodes (5): arm_bone(), arm_x(), leg_bone(), leg_ring(), roll()

### Community 106 - "Emote"
Cohesion: 0.10
Nodes (16): Bubble, EmoteBubbles, Pending, Emote, ANGER, BLUSH, DOTS, EXCLAIM (+8 more)

### Community 107 - ".perform"
Cohesion: 0.24
Nodes (3): Song, Songbook, Note

### Community 111 - "net.minecraft.world.item.ItemStack"
Cohesion: 0.09
Nodes (6): VillageLedgerItem, VillageMealItem, WorkstationBlockEntity, Combo, Daily, Workstations

### Community 112 - "kit_m03.py"
Cohesion: 0.09
Nodes (10): coil(), drips(), gloss(), knit_stockings(), leg_piece(), low_shoes(), rope(), rope_box() (+2 more)

### Community 113 - "Village days verification (2.14.0)"
Cohesion: 0.14
Nodes (4): CommunityGameTest, FriendshipGameTest, RoadmapGameTest, Village days verification (2.14.0)

### Community 114 - "kit_f07.py"
Cohesion: 0.09
Nodes (10): dust(), front_hung(), legs_both(), patch(), prop(), rope(), rope_box(), strap() (+2 more)

### Community 115 - "net.minecraft.world.entity.npc.villager.Villager"
Cohesion: 0.13
Nodes (4): GuardPatrols, Squad, ResidentRoutines, Spot

### Community 116 - "ArrivalBanner"
Cohesion: 0.08
Nodes (5): Village Friends 2.18.0 — Names that fit, and arriving in a village, ArrivalBanner, ArrivalGameTest, Line, VillageArrival

### Community 119 - "Dialogue"
Cohesion: 0.24
Nodes (3): Conversation Window (Talk/Story/Journal/Time/Travel tabs), Wordless Human-like Hum Voices, Dialogue

### Community 120 - "org.spongepowered.asm.mixin.Mixin"
Cohesion: 0.17
Nodes (5): CompanionPortalMixin, InjuredBodyMixin, SleepInBedRoutineMixin, VillagerFamilyMixin, VillagerMakeLoveMixin

### Community 122 - "Box"
Cohesion: 0.11
Nodes (3): strip_line(), Box, Layer

### Community 123 - "kit_m05.py"
Cohesion: 0.09
Nodes (9): cord_end(), dust(), grime(), hose(), knee_patch(), leg_prop(), over_panels(), soft_shoes() (+1 more)

### Community 124 - "tavern_preview.py"
Cohesion: 0.19
Nodes (11): bar_patron(), check(), holds_dish(), load(), main(), probe(), Scene, seated() (+3 more)

### Community 132 - "kit_f03.py"
Cohesion: 0.11
Nodes (10): basket(), cord(), front_prop(), net(), net_box(), rope(), rope_box(), wet_hem() (+2 more)

### Community 134 - "kit_f02.py"
Cohesion: 0.11
Nodes (9): back_prop(), cord(), hung(), lace(), prop(), ring(), sheen(), specks() (+1 more)

### Community 135 - "File format"
Cohesion: 0.25
Nodes (7): File format, body(), Editing the wardrobe, Genders and locked sets, Rules the compiler enforces, Workflow, Writing a piece

### Community 136 - "re"
Cohesion: 0.38
Nodes (10): boxes(), check_text(), compile_all(), count(), fail(), main(), parse_answer(), read_lines() (+2 more)

### Community 137 - "rot_matrix"
Cohesion: 0.14
Nodes (9): axis(), braid(), curve(), finish(), link(), local(), plait_path(), _step() (+1 more)

### Community 138 - "strand"
Cohesion: 0.14
Nodes (7): fall(), fringe(), point(), pointed(), points(), strand(), world()

### Community 139 - "shade"
Cohesion: 0.17
Nodes (7): checks(), lacing(), motif(), scatter(), dark_seams(), darken_rows(), shade()

### Community 140 - "kit_m06.py"
Cohesion: 0.11
Nodes (8): brocade(), chain_links(), fleece(), fur_patch(), hose(), lower_legs(), robe_skirts(), blk()

### Community 143 - "kit_m10.py"
Cohesion: 0.11
Nodes (7): arm_ring(), cable(), channels(), leg_ring(), outer(), patch(), tie()

### Community 145 - "kit_m08.py"
Cohesion: 0.11
Nodes (8): brocade(), coat_skirt(), crossed_collar(), fringe(), hanging_tail(), pleats(), roundel(), tassel()

### Community 146 - "TavernClient"
Cohesion: 0.15
Nodes (9): Nearby, TavernClient, Phase, CARRY, DONE, DRINK, EAT, WAIT (+1 more)

### Community 148 - "kit_f01.py"
Cohesion: 0.13
Nodes (7): bundle(), cut_ends(), handle(), produce(), stalks(), twist(), wicker()

### Community 149 - "kit_f06.py"
Cohesion: 0.12
Nodes (7): bow(), charm(), cut_velvet(), prop(), tablet_band(), tablet_column(), train()

### Community 151 - "Treatment"
Cohesion: 0.16
Nodes (8): Future Real-Time Knockout Controller, Medical Treatment Contract, Downed Companion Rescue, MedicalSupplyItem, Treatment, BANDAGE_WRAP, REVIVAL_TONIC, SMELLING_SALTS

### Community 152 - "kit_m02.py"
Cohesion: 0.14
Nodes (5): apron_panel(), bar(), bib(), dashes(), hoop()

### Community 153 - "GuardArrowMixin.java"
Cohesion: 0.20
Nodes (5): Unlimited Safe Archer Arrows, Automatic Village Defense (Knights and Archers), villager_predators Entity Tag, GuardArrowMixin, GuardMeleeMixin

### Community 156 - "kit_f05.py"
Cohesion: 0.15
Nodes (5): beads(), dangle(), fixed(), glass(), lap_panel()

### Community 157 - "ResidentSampleGameTest"
Cohesion: 0.26
Nodes (3): Focused Client GameTest Flags, Resident, ResidentSampleGameTest

### Community 158 - "Scene"
Cohesion: 0.17
Nodes (4): corners(), diced(), Scene, turned()

### Community 163 - "VillagerCompanionMixin.java"
Cohesion: 0.21
Nodes (6): Guard Equipment Exchange (Equip held item), Bread, Stew and Coffee Consumables, 24 New Items and 41 Recipes, Wearable Uniforms and Rain Gear, Adventure Companions (Follow/Wait/Return home), VillagerCompanionMixin

### Community 172 - "kit_f10.py"
Cohesion: 0.18
Nodes (4): cord(), frills(), lambswool(), panel_prop()

### Community 177 - "How a batch is built"
Cohesion: 0.20
Nodes (10): How a batch is built, Outfit templates, Read first, in this order, Rules for shared files, Save progress as you go, Seeds, Style rules (non-negotiable), The META block (+2 more)

### Community 190 - "VillageProfessions"
Cohesion: 0.27
Nodes (3): Native Trade Sets (50 sets, 100 offers), Ten New Professions and Workstations, VillageProfessions

### Community 193 - "Model"
Cohesion: 0.20
Nodes (4): bar_stool(), fireside_armchair(), Model, tavern_chair()

### Community 194 - "Concepts"
Cohesion: 0.20
Nodes (9): Concepts, f02: Women, crafts and trades (tf/bf 086–110). Seeds 52000–52999. Outfit file female_f02.json, f06: Women, noble court and town (tf/bf 186–210). Seeds 56000–56999. Outfit file female_f06.json, f08: Women, the wider medieval world (tf/bf 236–260). Seeds 58000–58999. Outfit file female_f08.json, f09: Women, festivals, ceremony and seasons (tf/bf 261–285). Seeds 59000–59999. Outfit file female_f09.json, m02: Men, craft guilds and workshops (t/b 146–170). Seeds 32000–32999. Outfit file male_m02.json, m06: Men, nobles, court and town officials (t/b 246–270). Seeds 36000–36999. Outfit file male_m06.json, m09: Men, festivals, seasons and ceremony (t/b 321–345). Seeds 39000–39999. Outfit file male_m09.json (+1 more)

### Community 197 - "BodyPart"
Cohesion: 0.25
Nodes (7): BodyPart, HEAD, LEFT_ARM, LEFT_LEG, RIGHT_ARM, RIGHT_LEG, TORSO

### Community 199 - "io"
Cohesion: 0.29
Nodes (3): Missing, preview(), preview_textures()

### Community 200 - "clipped"
Cohesion: 0.40
Nodes (3): clipped(), clipped_scalp(), fade()

### Community 205 - "render"
Cohesion: 0.50
Nodes (4): render(), at(), project(), rotate()

### Community 206 - "Resident movement, animation packs and eyes"
Cohesion: 0.50
Nodes (4): Animation packs, Gaits, Resident movement, animation packs and eyes, Verification

## Ambiguous Edges - Review These
- `FriendshipGameTest` → `Focused Client GameTest Flags`  [AMBIGUOUS]
  DEVELOPMENT.md · relation: references
- `GuardArmorMixin` → `Initial Guard Equipment (UUID-selected iron/chainmail)`  [AMBIGUOUS]
  GUARDS.md · relation: references

## Knowledge Gaps
- **228 isolated node(s):** `Loaded`, `FRONT`, `BACK`, `HEAD`, `HEAD_BACK` (+223 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1316 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **121 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `FriendshipGameTest` and `Focused Client GameTest Flags`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Wardrobe Python Module Pipeline (tools/wardrobe)` connect `Wardrobe Python Module Pipeline (tools/wardrobe)` to `kit_casual.py`, `anime_female.py`, `anime_male.py`, `kit_male.py`, `wardrobe/kit.py`, `wardrobe.py`, `Procedural Plains Village (villagefriends:village)`, `ColorPalette`, `Village Friends README`, `kit_female.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **What connects `Loaded`, `FRONT`, `BACK` to the rest of the system?**
  _228 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Face` be split into smaller, more focused modules?**
  _Cohesion score 0.07007575757575757 - nodes in this community are weakly interconnected._
- **What is the exact relationship between `GuardArmorMixin` and `Initial Guard Equipment (UUID-selected iron/chainmail)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Sims-style Men's and Women's Wardrobes` connect `ColorPalette` to `WardrobeLayer.java`, `Wardrobe Python Module Pipeline (tools/wardrobe)`, `Wardrobe`, `Village Friends README`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `kit_casual.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06116642958748222 - nodes in this community are weakly interconnected._