# Knights and archers

Adult Village Friends knights and archers defend villagers automatically. Knights use swords; archers draw and fire bows, approach targets outside shooting range, and retreat from enemies within four blocks. Idle guards retain ordinary jobs, trades, sleep and social behavior. NoAI residents and children do not fight.

Guards scan within 16 blocks twice per second. They attack zombies, husks, drowned, zombie villagers, pillagers, vindicators, evokers, ravagers, illusioners and zoglins. Other mobs qualify while targeting villagers, or for 30 seconds after damaging one. Creepers are always excluded. An idle skeleton or spider is not a target simply because it is hostile to players. A data pack can replace `data/villagefriends/tags/entity_type/villager_predators.json`; the creeper exclusion still applies.

An unforgiven player hit on any villager alerts all eligible guards within 16 blocks. This includes player-owned arrows. Forgiveness uses the victim's effective **Friend** tier or above, including the shared-experience gate and migrated friendships. Friendship with the responding guards does not excuse harming a different resident. Forgiven hits still cause damage and the existing loss of trust. Creative and Spectator players are not combat targets.

Each guard remembers each aggressor for 60 seconds of server ticks; additional unforgiven hits refresh that player's timer. Combat stays within 32 blocks of the guard's starting point. Guards return there afterward using normal pathfinding. They do not load distant chunks, teleport, build bridges or clear terrain. Unreachable fights eventually give way to a return attempt; targets and anger clear when the guard unloads or the server restarts.

Each new guard receives a weapon and four armor pieces, with exactly two iron and two chainmail pieces selected by its UUID. Existing equipped slots are preserved. A saved initialization marker prevents reloads, conversion/cure, upgrades or breakage from regenerating gear. Weapons and armor use native durability, enchantments and damage protection. A knight without a weapon can punch; an archer without a bow cannot shoot. Home guards retain ordinary villager death/conversion behavior.

## Exchange equipment

Talk to a guard, open **Travel**, hold equipment and choose **Equip held item**. Peaceful players need neither friendship nor recruitment. Knights accept swords; archers accept bows; both accept ordinary head, chest, leg and foot armor, including upgrades or lower tiers. Recruited guards accept exchanges only from their traveling owner. Fighting, downed and activity participants cannot exchange equipment.

One physical item is consumed even in Creative. The previous piece returns to your inventory, or drops beside you if the inventory is full. Durability, enchantments and other components are preserved. An invalid item is kept. Equipment appears on both world residents and the conversation portrait.

Archers have unlimited ordinary arrows. Their generated arrows cannot be collected. They check the firing path and their arrows cannot injure villagers, iron golems or players other than the intended target, even if somebody moves into a shot after it is fired. Guards use the same combat roles while recruited; **Wait** permits defense without pursuit, and companion downing/rescue remains available.

Patrol assignments, Command Desk controls, shields and additional combat jobs remain future work.

## Development checks

Run `gradlew.bat build` for packaging/unit checks, and `gradlew.bat runClientGameTest -PguardsOnly` for the focused native gameplay fixture. Use `-PcompanionsOnly` for the existing friendship and companion regressions and `-PfoundationOnly` for profession/trade checks. The default gameplay run also includes the guard test. Test worlds and screenshots are development artifacts; building does not install the mod into the player's launcher profile.
