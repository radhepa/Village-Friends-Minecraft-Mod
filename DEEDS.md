# Deeds: residents remember what you did

Version 2.24 makes a village notice what players do there. Saving a resident, fighting off a raid, hitting a neighbor or killing the iron golem is a **deed**: the people who saw it react on the spot, everyone else hears about it over the next few days, the first conversation afterwards brings it up, and it moves the player's standing and prices. The people you saved, and their families, keep it in their Journal for good.

## Where things live

| Piece | Code |
|---|---|
| Deed kinds, worth, fading, size, prices (pure) | `deed/DeedKind` |
| One deed, how a resident knows it, a player's log, the book (pure, codecs) | `deed/Deed`, `deed/Know`, `deed/DeedLog`, `deed/DeedBook` |
| Standing and the price term (pure) | `deed/Standing` |
| How word spreads (pure, deterministic) | `deed/Rumors` |
| What a resident brings up and which dialogue pools say it (pure) | `deed/Reactions` |
| Everything in the world: hooks, witnesses, bubbles, reactions, apologies, the board and Ledger lines, prices | `deed/Deeds` |
| Prices through vanilla reputation | `mixin/VillagerReputationMixin` |
| Theft from a resident's chest (menu closed) | `mixin/ContainerCloseMixin` |
| Horse theft and returns (Stablehand) | `stable/ride/HorseDeeds`, the pure `stable/ride/TheftRule` ([STABLEHAND.md](STABLEHAND.md)) |
| Which house a block belongs to (installed by Homes) | `home/HouseBounds` |
| Dialogue | `tools/dialogue/lines/deeds.txt` (the horse deeds' pools are in `stablehand.txt`) |
| Tests | `DeedScoringTest`, `RumorTest`, `ReputationTest`; client `DeedsGameTest` (`-Ptests=DeedsGameTest -PtestHeap=2560m`, screenshots `deeds-*`) |

Each level keeps a `villagefriends:deeds` attachment (`DeedBook`, `format` 1): village id, then player UUID, then that player's `DeedLog`. It lives on the village's origin level next to the societies and notice boards; absent means nobody has done anything yet. Old worlds are not migrated (2.24 starts in a new world).

## The deeds

Worth is in tenths of a notice (`points10`; answering one notice is 10). Bad deeds fade by half every half-life; good deeds never fade. Repeats inside the merge window fold into one deed (more hits, more raiders, more items).

| Deed | Worth | Half-life | Size | Price | Merges | Hook |
|---|---|---|---|---|---|---|
| Raid defended (raider killed in the village) | +10, +2 per raider, at most +30 | - | notable | +10 | one raid | `AFTER_DEATH` of a `Raider` near a raid inside a village, killed by a player |
| Raid won | +30 | - | big | 0 (vanilla's Hero of the Village prices it) | one raid | `Deeds.tick` (every 100 ticks): each raid-defended deed of the last day names its raid (`raid:<dimension>:<id>`); once vanilla says that raid was won, the player is credited, online or not. The deed log is the tally, so a restart mid-raid loses nothing |
| Revived | +20 | - | big | +15 | - | `Knockouts.interact` (Smelling Salts, Revival Tonic) |
| Bandaged | +5 | - | small | +4 | a day | `Knockouts.interact` (Bandage Wrap) |
| Saved from a monster | +10, +15 for a child | - | notable | +8 | a day per resident | `AFTER_DEATH` of an `Enemy` mob killed by a player while it was on a resident (its target, within 4 blocks), or that hurt one recently (`GuardController.recentVictim`). A zombie only hunting villagers from afar saves nobody, and a night of fighting at the walls is one rescue per neighbor, not one per kill |
| Rescued a downed companion | +5 | - | small | +5 | a day | `CompanionController` "rescue" |
| Notice answered | 0 (counted in the board's favors) | - | small | 0 | - | `VillageQuests.complete` |
| Birthday gift | +5 | - | small | +4 | a day | `Birthdays.gift` |
| Kindness to a pet (first pat or treat of the day) | +1 | - | small | +1 | a day per pet | `VillagerPets.handleAction` |
| Returned a horse (Stablehand) | +10 | - | notable | +6 | a day per horse | `HorseDeeds` (every 40 ticks, `TheftRule`): a stolen or lost resident's or village horse brought within 8 blocks of its stall by a player who is not the thief. The thief bringing it back, or a second return of the same horse within a game day, only clears its flags. A horse is lost, not stolen, when it is more than 48 blocks out and nobody has ridden or led it for over a minute (a knight left it out, say) |
| Hit a resident | -10, -3 per hit, at most -25 | 7 days | notable | 0 (vanilla prices it) | a minute | `CompanionController.allowDamage` (once a second) |
| Knocked a resident out | -30 | 14 | big | -20 | - | `Knockouts.allowDeath`; `KnockoutState.by` remembers who |
| A resident died of it | -80 | 28 | big | -40 | - | `Knockouts.expire`, charged to `KnockoutState.by`, even offline |
| Hit the golem | -5 | 7 | small | -5 | a minute | `AFTER_DAMAGE` of a village iron golem (not player-built) |
| Killed the golem | -40 | 14 | big | -25 | - | `AFTER_DEATH`, same golems |
| Hurt a resident's pet | -15 | 7 | notable | -10 | a minute | `AFTER_DAMAGE` of a resident's cat or dog |
| Killed a resident's pet | -40 | 14 | big | -25 | - | `AFTER_DEATH`, same pets |
| Broke a resident's bed, door or workstation | -10 | 7 | notable | -8 | a day per house | `PlayerBlockBreakEvents.AFTER` where `HouseBounds.owners(pos)` names residents |
| Stole from a resident's house | -10, -1 per 8 items, at most -30 | 10 | notable | -10 | a day per house | Opening a container inside a lived-in house (`UseBlockCallback`) snapshots it and the player's pack; closing that container's menu (`ContainerCloseMixin`) counts what left it and ended up with the player. Breaking a full container there counts too |
| Stole a horse (Stablehand) | -25 | 14 | notable | -15 | - (once per theft: the horse stays flagged until it is home) | `HorseDeeds` (every 40 ticks, `TheftRule`): a player riding or leading a resident's or the village's stalled horse more than 48 blocks from its stall. The player is told at once. Hopping off at 47 blocks and straight back on is still theft, because the player had it moments before; a horse a player stabled themselves is theirs to ride anywhere |

Creative and spectator players never do deeds. A pet's deeds belong to the village it is in, or its owner's village when it has wandered off.

A log keeps the last 48 deeds. When it is full, the oldest good deed's worth is banked for good (`banked10`) before it goes; bad deeds past four half-lives are forgotten. Past the reaction window (14 days for good deeds, 28 for bad) only those who lived or saw a deed still carry it; hearsay is let go.

## Who knows

- **Those it happened to** (`INVOLVED`) know at once, and so do their living partner and family (`FAMILY`, told rather than seeing it).
- **Witnesses** (`SEEN`): loaded residents of the same village, awake and not lying hurt, within 16 blocks of the player or the victim, who can see either. Vanilla's line-of-sight sensor (`NEAREST_VISIBLE_LIVING_ENTITIES`) answers first; up to six raycasts cover residents whose senses haven't caught up. At most 16. Each pops a bubble (a heart for a kindness, a sparkle for something big, anger at violence, gloom at breaking and taking) after 0-15 ticks and turns to look at the player (`LOOK_TARGET` for three seconds).
- **Everyone else** (`HEARD`, with who told them) through `deed/Rumors`, run from `VillageSocieties.live` (every ten seconds per loaded village):
  - Neighbors standing together (within 6 blocks): when one knows and the other doesn't, the other hears it with chance 0.15 per check, three times as likely when both are at lunch, the tavern, supper at the tavern, socializing, the market or a party, twice as likely between partners, family and friends (affinity 40+).
  - Once a day (unloaded days are caught up, up to 30): everyone who knows tells their family (chance 0.5) and each neighbor they have spent at least 3 days with (0.25). In a village where people have about eight such ties, about half hear a notable deed within three days and nearly everyone within six (`RumorTest`).
  - Big deeds are village news (`News "deed:<kind>"`): the next day everyone has heard. Raids won, revivals, deaths and golems killed are announced in chat like births and weddings; the Ledger's news lists them all.
  - The dead and the cursed neither tell nor hear.

Every roll is seeded by the deed, the two residents, the day (and the check), so the same world always spreads the same way.

## Residents bring it up

The first time a resident greets the player after learning of a deed, they open with it (`NarrativeEngine.greeting`, after a notice's thanks and before birthday wishes). Only the line a conversation opens with does this: a greeting shown again (back on the Talk tab, or as the reply to a choice that is no longer available) leaves reactions and cold hellos for the next opening. They pick the deed closest to them first (it happened to them, their family, they saw it, they heard it), then the biggest, then the newest; each deed is brought up once per resident. Pools (`deed/Reactions`):

- 70%: the deed's own lines, `deed.<kind>.self`, `.family`, `.seen` or `.heard` (falling back from self to seen and from family to heard);
- 30%: the personality's take, `deed.<good|bad>.<seen|heard>.<personality>`;
- children: `baby.deed.<kind>.self`, `baby.deed.<good|bad>.family`, `baby.deed.<good|bad>.<seen|heard>`;
- after an apology: `deed.apology.remembered`.

Placeholders: `{victim}` (the first name of whoever it happened to; for pets, their owner), `{kin}` ("sister", "husband"), `{teller}` (who told them) and `{house}` (a house's name). The greeting bubble matches: heart or sparkle for good deeds, anger or gloom for bad ones. If a pool is missing, a plain built-in line is used.

**Remembered always.** Whoever was revived, saved from a monster or carried home as a downed companion keeps it in their Journal for good (`BondState.kept`, up to 12, shown first under "REMEMBERED ALWAYS"), from `deed.kept.<kind>.self`. Their family keep it too (`deed.kept.<kind>.family`), written at their next conversation, so nobody has to be loaded.

## Standing

`score10 = 10 x notices answered + banked + good deeds + bad deeds x 1/2^(age / half-life) x (1/2 if apologized)`

- **The five titles keep the board's thresholds** (0, 1, 4, 10 and 20 notices' worth): Newcomer, Helping Hand, Good Neighbor, Pillar of the Community, Hero of the village. A revival and a won raid together are worth five notices.
- **Unwelcome**, a sixth title below Newcomer, at `score10 <= -20`. Notices alone can never get you there. While Unwelcome: the board's standing line and the Ledger say so, nobody offers you work (the board shows no open notices and a note from `notice.unwelcome`; notices you already hold can still be turned in), residents greet you from `greet.unwelcome` (30% `greet.unwelcome.<personality>`, children `baby.greet.unwelcome`) and won't make small talk (`chat.unwelcome`), and there are no rewards. It wears off as bad deeds fade, with apologies and with good deeds.
- **Rewards come once**: reaching a tier higher than ever before here (`peakTier`) gives what a notice always gave (a message, better prices from everyone loaded, 8 emeralds for Pillar, Hero of the Village for the hero). Falling is only a message ("folk are wary of you"); climbing back to a tier you held before says "here again".
- The board's line adds "(they remember what you did)" while a bad deed still weighs on the score.

**Apologies.** A resident who was hurt by an unapologized bad deed (or whose family member died of one) offers "I'm sorry about what happened". It is accepted when their trust is 40 or more, the player is holding something they like or love, or three days have passed since; the deed then counts half and they say a line from `deed.apology.accept` (children `.accept.child`). Otherwise they answer from `deed.apology.cool` (children `.cool.child`) and you can try again tomorrow. The existing "I'm sorry" after a fresh hurt also apologizes for that deed, on the same terms (otherwise the deed waits for its own apology).

## Prices: one engine (the decision)

**Vanilla's villager reputation stays the only price engine; the mod adds a term to it and writes no deed gossip.** `VillagerReputationMixin` hooks `Villager.getPlayerReputation(Player)` at RETURN and adds `Deeds.reputation(villager, player)`:

`sum over the deeds this resident knows of: price x how they know it (1 involved, .8 family, .6 seen, .3 heard) x fading x (1/2 if apologized)`, clamped to -60..+40 and cached per resident and player for 100 ticks (any deed clears the cache).

- Vanilla reads `getPlayerReputation` for trade prices (`updateSpecialPrices`) and for iron golems deciding who to fight, so both follow what residents know, with the same fading as standing.
- **No double counting.** Hitting a resident already gives vanilla `MINOR_NEGATIVE` gossip (`VILLAGER_HURT`), spread by vanilla's own gossip transfer, so `hit_resident` has price weight 0. Knocked-out residents never die by vanilla's `die()` with a killer, so vanilla's `VILLAGER_KILLED` never fires for a death the mod scores. Notices keep their existing vanilla gossip (the poster's `MINOR_POSITIVE`, the tier reward's `MAJOR_POSITIVE`) and are worth 0 in the deed term.
- **Golems.** Vanilla turns golems on a player at reputation -100 or below; the -60 clamp means deeds alone never do it (repeated vanilla hits still can).
- Why: prices never disagree with what residents say; unloaded residents need no write queue; vanilla's NBT stays clean, so removing the mod leaves vanilla's numbers as they were; one small mixin instead of rewriting gossip transfer.

## Houses (Homes)

Breaking a resident's bed, door or workstation and stealing from their house ask `HouseBounds.current()` which house a block is in and who owns it; Homes installs its housing index there in `Homes.register()`. Only lived-in houses count (a house nobody lives in, or a Private one, is fair game).

- **Breaking:** a bed wrongs its owner; a workstation or either half of a door the index lists wrongs the household. Any other door in a lived-in house counts for the household too (by the time `PlayerBlockBreakEvents.AFTER` runs the door is gone, so the block that was broken decides). Everything broken in one house within a day is one deed.
- **Theft:** opening any container in a lived-in house snapshots its item counts and the player's pack; closing that container's menu (either half of a double chest) counts what left it and ended up with the player, in their pack or on the cursor (`STOLE`, `count` = items taken). A click that opened no menu, a hopper draining the chest, or another player taking from the same chest is not charged to them. Breaking a container with items in it counts them too. A house a player built belongs to whoever moved into it: keep your own house Private (sneak-use its plaque) if you keep chests there.
- `HouseRef.residents` and `owners(...)` are resident ids (the `ResidentProfile` id, as in the village census).
- `DeedsGameTest.theftAndBrokenHomes` builds a cottage with a plaque, two beds and a chest, waits for homeless residents to move in, empties the chest (screenshot `deeds-theft`) and breaks an owned bed and the top half of the door.

## Changing it

- Worth, fading, size, price and merging are the `DeedKind` constructor arguments; `DeedScoringTest` and `ReputationTest` pin the important numbers.
- Rumor rates are the constants at the top of `Rumors`; check `RumorTest.aboutHalfTheVillageHearsANotableDeedInThreeDaysAndMostInSix` after changing them.
- New deed kinds need a hook in `Deeds`, a row here, and the four kind pools (`seen`, `heard`, and `self`/`family` when someone is involved) in `tools/dialogue/lines/deeds.txt`.
