# Knights and archers

Adult Village Friends knights and archers defend villagers automatically. Knights use swords; archers draw and fire bows, approach targets outside shooting range, and retreat from enemies within four blocks. Idle guards retain ordinary jobs, trades, sleep and social behavior. NoAI residents and children do not fight.

Guards scan within 16 blocks twice per second. They attack zombies, husks, drowned, zombie villagers, pillagers, vindicators, evokers, ravagers, illusioners and zoglins. Other mobs qualify while targeting villagers, or for 30 seconds after damaging one. Creepers are always excluded. An idle skeleton or spider is not a target simply because it is hostile to players. A data pack can replace `data/villagefriends/tags/entity_type/villager_predators.json`; the creeper exclusion still applies.

An unforgiven player hit on any villager alerts all eligible guards within 16 blocks. This includes player-owned arrows. Forgiveness uses the victim's effective **Friend** tier or above, including the shared-experience gate and migrated friendships. Friendship with the responding guards does not excuse harming a different resident. Forgiven hits still cause damage and the existing loss of trust. Creative and Spectator players are not combat targets.

Each guard remembers each aggressor for 60 seconds of server ticks; additional unforgiven hits refresh that player's timer. Combat stays within 32 blocks of the guard's starting point. Guards return there afterward using normal pathfinding. They do not load distant chunks, teleport, build bridges or clear terrain. Unreachable fights eventually give way to a return attempt; targets and anger clear when the guard unloads or the server restarts.

Each new guard receives a weapon and four armor pieces, with exactly two iron and two chainmail pieces selected by its UUID. Existing equipped slots are preserved. A saved initialization marker prevents reloads, conversion/cure, upgrades or breakage from regenerating gear. Weapons and armor use native durability, enchantments and damage protection. A knight without a weapon can punch; an archer without a bow cannot shoot. Home guards retain ordinary villager death/conversion behavior.

## Guard levels

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

Patrol assignments, Command Desk controls, shields and additional combat jobs remain future work.

## Development checks

Run `gradlew.bat build` for packaging/unit checks, and `gradlew.bat runClientGameTest -PguardsOnly` for the focused native gameplay fixture. Use `-PcompanionsOnly` for the existing friendship and companion regressions and `-PfoundationOnly` for profession/trade checks. The default gameplay run also includes the guard test. Test worlds and screenshots are development artifacts; building does not install the mod into the player's launcher profile.
