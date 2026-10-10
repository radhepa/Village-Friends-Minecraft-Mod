# Knights and archers

Adult Village Friends knights and archers defend villagers automatically. Knights use swords; archers draw and fire bows, approach targets outside shooting range, and retreat from enemies within four blocks. Idle guards retain ordinary jobs, trades, sleep and social behavior. NoAI residents and children do not fight.

Guards scan within 16 blocks twice per second. They attack zombies, husks, drowned, zombie villagers, pillagers, vindicators, evokers, ravagers, illusioners and zoglins. Other mobs qualify while targeting villagers, or for 30 seconds after damaging one. Creepers are always excluded. An idle skeleton or spider is not a target simply because it is hostile to players. A data pack can replace `data/villagefriends/tags/entity_type/villager_predators.json`; the creeper exclusion still applies.

**On village grounds there is no waiting.** When a player or a mob hurts a resident inside a village, every guard of that village within 64 blocks (awake, or asleep within 24 blocks) is called out at once: they get up from the tavern table or out of bed and run straight at the attacker, seen or not, and chase it up to 80 blocks from where they stood. On village grounds friendship excuses nothing.

Out in the wild, an unforgiven player hit on any villager alerts all eligible guards within 16 blocks. This includes player-owned arrows. Forgiveness uses the victim's effective **Friend** tier or above, including the shared-experience gate and migrated friendships. Friendship with the responding guards does not excuse harming a different resident. Forgiven hits still cause damage and the existing loss of trust. Creative and Spectator players are not combat targets.

Each guard remembers each aggressor for 60 seconds of server ticks; additional unforgiven hits refresh that player's timer. Combat stays within 32 blocks of the guard's starting point. Guards return there afterward using normal pathfinding. They do not load distant chunks, teleport, build bridges or clear terrain. Unreachable fights eventually give way to a return attempt; targets and anger clear when the guard unloads or the server restarts.

Each new guard receives a weapon and four armor pieces, with exactly two iron and two chainmail pieces selected by its UUID. Existing equipped slots are preserved. A saved initialization marker prevents reloads, conversion/cure, upgrades or breakage from regenerating gear. Weapons and armor use native durability, enchantments and damage protection. A knight without a weapon can punch; an archer without a bow cannot shoot. A guard who would die is knocked out instead, like every resident (see **Knockouts** below).

## Guard levels

For battle testing, find **Knight Spawn Egg** and **Archer Spawn Egg** in Creative's **Spawn Eggs** tab, or use `/give @s villagefriends:knight_spawn_egg` and `/give @s villagefriends:archer_spawn_egg`. Both create ordinary adult `minecraft:villager` residents with the requested profession, normal armor/weapon and a saved generated level of 15–30. They also work in dispensers. A point of native trading XP keeps their jobs without nearby workstations; guard XP starts at zero and the first qualifying kill still records the combat lock. These eggs have no Survival crafting recipe.

Knights and Archers have their own combat level, independent of trading levels and friendship. Generated guards and existing guards migrating to this release start at a saved, UUID-seeded level from 15 to 30, weighted toward the middle. An ordinary resident who later becomes a Knight at a Training Dummy or an Archer at an Archery Target starts at level 0. Reloading or changing jobs never rerolls the level.

The maximum level is 50. Each level adds 0.2 maximum HP and 0.5% direct damage after native weapon/enchantment calculations, before the victim's protection. Arrows remember the level when fired. Speed, attack cooldowns, bow draw time, accuracy and armor stay at their normal values, so equipment upgrades remain valuable.

| Level | Maximum health with ordinary equipment | Damage bonus |
|---|---:|---:|
| 0 | 20 HP | 0% |
| 15 | 23 HP | 7.5% |
| 30 | 26 HP | 15% |
| 50 | 30 HP | 25% |

Advancing from level `L` requires `20 + 3L` guard XP. Surplus and fractional XP carry forward; level 50 stops gaining XP. Ordinary qualifying threats provide 10 XP, pillagers 15, vindicators/illusioners/zoglins 20, evokers 30 and ravagers 50. XP is awarded only on death and split by actual health damage contributed during the preceding 30 seconds. Player and other damage take their portion of the denominator; players retain normal Minecraft XP drops. A guard still earns its share when another guard or a player delivers the killing blow. Creepers, players, passive animals and unrelated player-hostile mobs give no guard XP.

The first qualifying killing blow permanently locks the guard's current Knight or Archer profession, including kills with its arrows. Assists do not lock the role. Vanilla trade-based job locking also remains. Before combat locking, progress survives switching guard roles or temporarily taking another job; the stat bonuses apply only while an adult Knight or Archer.

Conversation titles show the guard's level; the Journal lists XP, bonuses and combat-lock status. Levels and locks survive recruitment, downing, save/reload and conversion/cure. Leveling raises health capacity without healing or reviving a guard, and never replaces broken equipment. Initial migration preserves the existing health percentage. Temporary damage contributions clear on unload/restart.

## Exchange equipment

Talk to a guard, open **Travel**, hold equipment and choose **Equip held item**. Peaceful players need neither friendship nor recruitment. Knights accept swords; archers accept bows; both accept ordinary head, chest, leg and foot armor, including upgrades or lower tiers. Recruited guards accept exchanges only from their traveling owner. Fighting, downed and activity participants cannot exchange equipment.

One physical item is consumed even in Creative. The previous piece returns to your inventory, or drops beside you if the inventory is full. Durability, enchantments and other components are preserved. An invalid item is kept. Equipment appears on both world residents and the conversation portrait.

Archers have unlimited ordinary arrows. Their generated arrows cannot be collected. They check the firing path and their arrows cannot injure villagers, iron golems or players other than the intended target, even if somebody moves into a shot after it is fired. Guards use the same combat roles while recruited; **Wait** permits defense without pursuit, and companion downing/rescue remains available.

## Night patrols

Guards on the night watch (about half of them, from 18:00 until 08:00) walk a loop around their village in squads of two or three instead of wandering alone. A village is the set of guards who share a bell; every five seconds the roster is rebuilt from the loaded guards. If fewer than two of a village's guards keep the night watch, the next guards on the roster (ordered by their UUID seed) are called up from 19:00 until dawn, so any village with two or more guards always has a squad out. A village with a single guard keeps them standing watch beside the bell rather than walking alone.

The squad leader walks eight checkpoints in a ring 11–28 blocks around the bell, skipping roofs, water and drops; the others follow a pace behind, side by side. The leader waits whenever someone falls more than ten blocks behind, and moves on from a checkpoint it can't reach after 30 seconds. Patrols use the villager brain's own walking, so doors still open. A guard who spots a threat fights it with the rules above and rejoins the squad afterward.

**Mounted night patrols (Stablehand).** When their village has a stable anywhere in it (it usually stands on the outer streets), knights on the night watch walk to a free stable horse of their own village (the village's or a resident's, never a player's), mount it and ride the same patrol. An all-mounted squad trots (1.4x) and keeps a wider gap; a mixed squad keeps the walkers' pace. When the watch ends they ride back to the stall and get off, or get off where they are if the ride takes too long, and loose stable horses drift home when no player is near. Knights only fetch a horse for the night watch, never for a raid or a call-out. See [STABLEHAND.md](STABLEHAND.md).

## When a resident is struck down

When a player knocks out a resident, the neighbors who are about panic: everyone awake in the same village (or within 40 blocks out in the wild) drops what they're doing, leaves the tavern or their game, and runs home to their own house (or their bed, or simply away from the player if they have no home) at vanilla's panic speed. They stay indoors for a minute, then get on with their day. Guards don't run; they are called out (see above). The alarm happens in any game mode, but Creative and Spectator players can't be attacked.

## Raid response

During a raid at or near their village, guards don't hide. Their routine becomes **Defending the village**: sleeping guards wake, the raid alarm, the bell's call to hide and panic are ignored, and they muster in a ring around the bell. Once the first wave arrives they head for the nearest raider within 48 blocks of the bell, and normal guard combat takes over when one comes into range. When the raid ends (victory, defeat or stopped) they return to their routine. Recruited guards stay with their companion; knocked-out guards stay down.

## Knockouts

No resident dies from an ordinary fatal blow. They are **knocked out** instead: they lie on the ground hurt, eyes closed, with their equipment, memories and friendships intact. Nothing can hurt them, and every mob that was after them loses interest at once and ignores them until they are back on their feet (revived by a player or the apothecary). Zombies can't convert them. They don't speak: no hums, no speech bubbles, no conversation.

They must be revived within **a day of play: 24 real hours of game ticks**. The clock counts only while the world is running; it stops when nobody is playing, and if their chunk is unloaded when time runs out it catches up when the chunk loads. Right-click a knocked-out resident to check how long they have left. To treat them, right-click while holding:

| Item | Effect |
|---|---|
| Smelling Salts | Wakes them with 20% health |
| Revival Tonic | Wakes them with full health |
| Bandage Wrap | Adds 12 hours (up to two days left) |

One item is used per treatment (not in Creative). Reviving someone earns their trust and a memory. The village apothecary also helps: an awake apothecary within 32 blocks walks over to a knocked-out neighbor and dresses their wounds once, adding 12 hours. If nobody revives them in time, they **die permanently**, and nearby players and anyone who knew them are told. The void and `/kill` still kill outright.

Recruited companions keep their own gentler rule (downed for a minute, then they recover at home), but they lie on the ground the same way, mobs ignore them the same way, and they don't talk either: right-clicking one shows a silent note with **Help them up** and **Take them home**.

Command Desk controls, shields and additional combat jobs remain future work.

## Development checks

Run `gradlew.bat build` for packaging/unit checks, and `gradlew.bat runClientGameTest -PguardsOnly` for the focused native gameplay fixture. `-Ptests=VillageAlarmGameTest` covers the panic, the village call-out, mobs leaving the downed alone and the silent downed companion. `-Ptests=KnockoutGameTest` covers knockouts, treatment, permanent death, the apothecary, downed companions, night squads and the raid muster, with screenshots. Use `-PcompanionsOnly` for the existing friendship and companion regressions and `-PfoundationOnly` for profession/trade checks. The default gameplay run also includes the guard test. Test worlds and screenshots are development artifacts; building does not install the mod into the player's launcher profile.
