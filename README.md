# Village Friends 2.12.0

A Fabric mod for Minecraft Java Edition 26.3. Your villagers have names, individual preferences, persistent memories, written personal stories, and player-shaped appearances. Build trust, spend time together, and invite a friend on an Overworld adventure. Conversations work offline, with no AI account or service fees.

The mod includes the master specification's **Phase 1 registry and item foundation**: ten professions with distinct workstations and five levels of trades, 17 new blocks, 24 items, and 41 recipes. Place a new workstation near an unemployed adult to let them acquire its job. Find the content in vanilla creative tabs or craft it in Survival. The implementation plan and integration details are in [PHASE1.md](PHASE1.md).

**Phase 2 adds naturally generated, procedural villages** in plains and meadows. A fountain square, village green or market square is ringed by the tavern, garrison and watchtower, workshop, chapel and graveyard, apothecary and library. Winding streets lead past timber-framed homes, trade workshops, farms and gatehouses, so no two villages are alike. Every village has all ten new professions; tradespeople for the vanilla jobs find work in its smithy, butcher, fletcher and other workshops. New villages appear in newly generated chunks; existing villages remain available. Find one with `/locate structure villagefriends:village`. See [PHASE2.md](PHASE2.md) for the layouts, commands and future room-scanner fixtures.

Each building is an independent template written as a small design program and compiled to its own blueprint. Edit or replace one through its blueprint and pool; [BUILDING_EDITING.md](BUILDING_EDITING.md) gives the workflow and the lot contract.

**Wardrobe:** residents dress from Sims-style men's and women's wardrobes. Men choose from 80 hairstyles, 120 tops and 120 bottoms; women from 50 hairstyles, 60 tops and 60 bottoms. Everything is drawn as palette-locked pixel art with 3D collars, pauldrons, skirts, hoods, cloaks and hair. Clothing is casual medieval village wear, plus a plain modern casual line for men, and hair is anime-inspired. Each profession has its own outfits for both sets. Tops and bottoms mix freely, except a few locked one-piece outfits such as gowns and habits. Every outfit uses one of ten master palettes. The names remain available; Indian names are eligible for brown/dark complexions. See [OUTFIT_ENGINE.md](OUTFIT_ENGINE.md).

**Living villagers:** six subtle walking styles give residents their own cadence, stride, shoulder swing and balance. Breathing, a slow shift of weight and a wandering gaze keep quiet moments alive. Faces are young pixel art with one of two eye styles, Starlit or Soft Glint, in each resident's original eye colors; women's faces add a lash wing, arched brows, rosy lips and blush. Eyes blink at individual moments and make small glances toward someone nearby. Children get lighter, quicker steps; clothing and armor follow the movement. See [ANIMATION_EDITING.md](ANIMATION_EDITING.md).

**Village Life animation pack:** residents decide what to do from moment to moment, choosing from 99 animation clips. They stretch, yawn, hum, scratch their heads and kick pebbles; practice their trade (smiths hammer, farmers hoe, clerics pray, cooks stir, tailors stitch, knights stand guard) and a hobby that fits their personality; chat with a neighbor beside them, taking turns to speak and listen; wave, bow or salute when you walk up; gesture while you talk, laugh at your jokes, cheer for a favorite gift and shake their heads at one they dislike; hunch in the rain and shiver in the snow. Children hop, twirl, play airplane and peekaboo. About one resident in nine is left-handed. Resource packs can add more packs; see [ANIMATION_PACKS.md](ANIMATION_PACKS.md).

Bread and stew restore health; coffee grants a short speed boost. Rain cloaks, ponchos and uniforms can be worn or equipped on companions. Medical supplies, bench seating, cot treatment, administrative blocks and tools provide foundations for later behavior. Their full AI and interaction systems and spatial bed scanner are later work. Knights and Archers receive combat equipment and defend villagers automatically; other professions use ordinary villager behavior.

For battle testing, **Knight Spawn Egg** and **Archer Spawn Egg** are in Creative's **Spawn Eggs** tab. They create ordinary equipped adult villagers at levels 15–30, work in dispensers, and keep their jobs without nearby workstations. Commands: `/give @s villagefriends:knight_spawn_egg` and `/give @s villagefriends:archer_spawn_egg`. See [GUARDS.md](GUARDS.md) for combat and progression rules.

## Play on this computer

For this build, replace the older Village Friends JAR in the profile's `mods` folder with `build/libs/village-friends-2.12.0.jar`. Building alone does not replace the installed mod.

Open the Minecraft Launcher, choose **Village Friends - 26.3**, and press Play. Under Installations, enable Modded if the profile is hidden. Right-click an awake villager to meet them.

The existing profile uses `%APPDATA%\.minecraft\instances\VillageFriends`. The update keeps that profile, its Java installation, and its worlds. Authorized releases back up the previous mod and this instance's saves in a dated `%APPDATA%\.minecraft\backups\VillageFriends-<version>-<timestamp>` folder before installation.

## Your friendship journey

The conversation window keeps its wood-and-parchment design and a live portrait of the resident, including their equipment. Dialogue types out with soft blips (Space finishes a line), and residents speak in wordless, human-like hums instead of vanilla villager sounds. Use these tabs:

| Tab | What you can do |
|---|---|
| Talk | Talk about daily life, work, adventures, or jokes. Repair trust with an apology after harmful actions or a broken promise. |
| Story | Listen to a four-chapter personal story, help with a request, hear a confession, and choose encouragement or a practical first step. |
| Journal | Read the latest 24 shared memories, preferences, resident friendships, and story requirements. Scroll long text with the mouse wheel. |
| Time | Take a walk, share a picnic, explore together, or invite nearby neighbors to a gathering. |
| Travel | Recruit a companion, choose Follow or Wait, exchange equipment, rescue them, or send them home. |

Stories progress through experiences and visits on different Minecraft days. The bundled stories open their confession after **three visiting days** and their final choice after **five visiting days and 60 trust**. A completed story earns a small gift from the resident. Additional requests share the same project and remember who actually supplied the materials. There are no request deadlines.

Your first conversation each day gives four points. The first story request gives 20, the confession gives 16, the ending gives 30, and each of the two additional requests gives 16. A completed shared activity gives eight points and five trust once per day. Additional activities still create distinct memories. There is no penalty for taking a break from the game.

| Relationship | Points plus shared history |
|---|---|
| New Neighbor | 0 |
| Acquaintance | 15 |
| Friend | 40 and a shared experience |
| Close Friend | 80 and the personal confession |
| Best Friend | 140 and the completed story across at least five visiting days |

Points stop at 200. Gifts alone cannot unlock the upper tiers. Stories, requests, visits, and activities can earn those tiers without repeated gifting. Existing unlocked tiers from 1.1.0 are preserved even if the new story has not yet been completed.

## Gifts and promises

Hold a gift in your main hand and choose Give gift. Survival consumes one accepted item; Creative keeps it. Each player may give a resident three gifts per day. Individual loved items earn 14 points; other accepted gifts use the original job preferences, with a two-point variety bonus for changing gift types. Rejected gifts consume neither the item nor the gift allowance. Check About this resident or the gift tooltip for preferences.

Promises are optional. Explicitly withdrawing a promise reduces trust by five; harming a resident reduces trust by 15. An apology begins repair, and positive experiences can rebuild trust. Your permanent story milestones remain recorded. This does not make ordinary villagers immortal.

Choose Trade or sneak-right-click for vanilla trading. Custom name tags and spawn eggs keep their normal behavior. Jobs, trade offers, breeding, and ordinary work behavior remain vanilla when a resident is at home.

## Shared activities

Activities unlock at 15 points and at least 30 trust. They occupy your one companion slot while active. Close the conversation window to move, then talk to the resident again and choose Finish our outing.

- **Walk:** at least 15 seconds together and eight blocks from where you started.
- **Picnic:** offer one bread, apple, or cookie; spend at least 15 seconds together nearby.
- **Exploration:** at least 30 seconds together and 32 blocks from where you started.
- **Gathering:** offer picnic food with at least two other adult residents nearby. Up to six neighbors join for at least 20 seconds.

Residents form up to 16 persistent connections with other residents they spend days near. Shared hobbies and values help these connections grow. Their nearby neighbors appear in conversation and the journal. Friends may invite you to a picnic; invitations are limited to one per player per Minecraft day.

## Adventure companions

An adult resident can join you after becoming a Friend, reaching the second story chapter, and building at least 50 trust. Only one resident can travel with a player, and a resident can have only one traveling owner.

Follow uses Minecraft pathfinding. Wait holds their current position. Return home moves them safely back near where they were recruited and restores their previous work behavior. Companions use basic melee attacks to defend against hostile mobs attacking them or their owner. They remember a fight and the return from an outing.

Hold a vanilla sword, axe, or ordinary armor piece and choose Equip held item. One physical item is exchanged, even in Creative. Previous equipment is returned to your inventory, or dropped beside you if it is full. Equipment is displayed on the live portrait and survives save/reload.

A recruited companion's lethal injury leaves them **downed**, with their identity and equipment intact. Right-click and choose Help them up to rescue them. Further damage is blocked while downed. After one minute without rescue they recover at home and remember the interrupted outing. If their owner dies, disconnects, or leaves the Overworld, they return home. Unloaded residents reconcile their owner state when their chunk next loads.

Adult Knights and Archers use specialized village defense, including ranged bow attacks. Generated guards start at levels 15–30; newly trained guards start at 0. Defeating actual villager threats earns damage-based guard XP up to level 50, with small health/damage bonuses. Their first qualifying killing blow locks their profession. Read their level and progress in conversation and the Journal.

Peaceful players can exchange their role's weapon or armor without recruitment; recruited guards accept only their owner's exchanges. See [GUARDS.md](GUARDS.md) for progression, predators, friendship forgiveness, pursuit limits and unlimited arrows.

This release supports Overworld travel. Companions cannot use portals while recruited. Nether/End travel, patrols, larger parties, romance, marriage, and family are future expansions. Activities interrupted by a server restart end safely without awarding completion. Pathfinding still needs a reachable route; this mod does not build bridges, clear blocks, or alter terrain.

## Persistent residents and co-op

Each resident has a stable ID independent of their entity UUID and profession. Their saved profile includes personality, hobby, values, loved and disliked gifts, story assignment, and appearance recipe. Zombie conversion and curing transfer identity, relationships, shared outcomes, and names. Vanilla conversion transfers equipment.

Affection, trust, visits, private choices, and memories belong to each player separately. Physical requests belong to the resident: the first supplier gets the reward and retains credit. Another player receives a recap and keeps their supplies, then builds their own shared experiences. The server validates choices, quest progress, recruitment, and exchanges. Both clients and the server need the mod for co-op features.

## Children and hometowns

Baby villagers have a larger head relative to their short body, small hands and feet, young faces, and child-friendly clothing. Phase 3 children use 24 casual top variants and the expanded jeans library; earlier recipes retain their six play-clothes. Adult beards, work outfits, and accessories are replaced during childhood. The live portrait uses the same child model and skin as the world. When a child grows up, they reveal their saved adult look; identity, hometown, friendship and memories stay intact.

Enter a naturally generated village to discover its stable generated name. A small welcome message appears within five seconds. Loaded locals receive hovering names like **Liora Ash of Willowhaven**, mention their hometown in conversations, and list it under Journal → About this resident. Talking to a resident discovers their natural village immediately. Existing first/last or custom names remain the base of the full name.

For a player-built settlement, craft and place a **Village Marker**. The marker recognizes an existing settlement or creates one covering 96 blocks horizontally from its center. Its carved house symbol makes it easy to spot. Right-click it to read the village name and number of loaded residents. Unloaded residents join when they are loaded near a discovered settlement.

Craft one marker with **three planks (any type), one oak sign and one copper ingot**:

```text
Plank | Oak sign | Plank
      | Copper  |
      | Plank   |
```

To choose or change a village name, name the marker in an **anvil**, then place it in that village. Names may contain up to 48 characters. Place an unnamed marker to accept the generated name. A placed marker can be broken and moved; breaking it never deletes the settlement or its residents' origins. No markers or terrain edits are placed automatically.

Each resident keeps their first assigned hometown when traveling or moving away. Renaming the village updates its residents' suffix when they load, without appending it twice or changing their underlying identity. Name tags can still change the personal part of a resident's name. Conversion and curing preserve hometown membership as well as friendship. Players on the same server share settlement names.

## Clothing and hair

Men and women dress from their own wardrobes; non-binary residents choose from both. The men's set has 120 outfits:
- **Originals:** Knight-Errant, Trailblazer, Arcanist, Farmhand, Merchant, Mariner, Smith, Ranger, Minstrel and Pilgrim, and the 2.8 casual-medieval outfits from Villager to Student.
- **Trades and roles:** farriers, millers, monks, heralds, lords, men-at-arms, Norsemen, desert nomads, morris dancers and others.
- **Supreme casual:** a modern line of plain tees and tunics in five colors each, polos, oxford, henley and denim shirts, five jeans, two baggy jeans, chinos, slacks, cargos and joggers.

The women's set has 60 outfits. They run from village lass, milkmaid, brewster and fishwife to huntress, shieldmaiden, lady knight, nun, sun priestess, star mage, coin dancer and court lady.

A profession picks from its fitting outfits. Each outfit pairs a top and a bottom, and residents often swap in any compatible bottom from their set, Sims-style. Armor, fancy hose, kilts and sandals have rules. A few outfits are locked sets whose top and bottom are always worn together, such as gowns, habits, the jester's motley and the green man. One master palette colors the whole outfit: primary, secondary, accent, leather, metal and ink, each with hand-shaded pixel ramps. Hair comes in 80 men's and 50 women's volumetric styles and ten natural colors. They are anime-inspired, with pointed bangs, sidelocks, a sheen ring, braids, buns, curls, coils, locs and tails, but no gravity-defying spikes. Hair is chosen once per resident so a new job never changes it. Coat skirts, aprons and tabards move with the stride; ponytails and tassels sway. Armor hides conflicting clothing and hair. World residents and conversation portraits share the renderer.

Recipes keep their existing format: saved residents keep complexion, gender, palette and identity and are redressed from the expanded wardrobe. To edit or add clothing, see [WARDROBE_EDITING.md](WARDROBE_EDITING.md).

## Content packs and development

All 12 personalities, eight four-chapter arcs, 24 requests, gift preferences, dialogue, and story visit/trust conditions live in:

`src/main/resources/data/villagefriends/villagefriends/content.json`

Each story has a `conditions` object with `confessionVisits`, `endingVisits`, `endingTrust`, and `requireSharedExperience`. The story engine supplies the common chapter structure, journal events, and companion behavior; authored text and request content can expand without rewriting Java. A data pack can override `data/villagefriends/villagefriends/content.json` as a complete content file. `/reload` validates it, including item IDs. Invalid packs retain the previous working definitions. Removed story IDs become unavailable for those residents until restored, and never reset their saved history.

Art parts use the standard 64×64 Minecraft skin layout under `assets/villagefriends/textures/parts`. Resource packs may replace those parts. Saved recipes remain independent of resource reloads.

Requirements: **Minecraft 26.3, Fabric Loader 0.19.5+, Fabric API 0.161.0+26.3, and 64-bit Java 25**. These are already installed for this profile. Friends can use the delivered co-op ZIP's mods and instructions.

- Run `powershell -ExecutionPolicy Bypass -File .\build.ps1`, or `gradlew.bat build` with JDK 25 as JAVA_HOME. Gradle installs its own build runtime.
- `gradlew.bat runClient` starts a separate development client.
- `gradlew.bat runClientGameTest` runs real client/server interaction tests, screenshot checks, and save/reload tests. The test mod is excluded from the release JAR.
- Release output: `build/libs/village-friends-2.12.0.jar`. Install this file, not the sources JAR.
- The art generator needs Python and Pillow only when regenerating assets.

Read VERIFICATION.md for test coverage and its limits. Romance and family remain milestone 7, after the friendship systems have been used in real worlds.

MIT license. Original artwork; no Stardew Valley assets included.


