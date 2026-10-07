# Village life: families, love, friendship levels, speech bubbles and the Village Ledger

Version 2.13 makes every village a small community. Residents know everyone in their village, keep a relationship meter with each of them, may arrive with family, slowly fall in love, marry and have children, and talk about all of it. Players see this through numbered friendship levels, Tomodachi Life–style speech bubbles over residents' heads, a rebuilt conversation window and the Village Ledger.

## Where things live

| Piece | Code |
|---|---|
| Census, meters, families, romance and news (pure, unit-tested) | `src/main/java/dev/villagefriends/social/` (`Society`, `Townsfolk`, `Tie`, `News`, `Chemistry`, `Relations`, `Gossip`) |
| Keeping societies in step with the world | `VillageSocieties` (registration, households, births, deaths, curses, daily life, social emotes, announcements) |
| Friendship levels | `FriendshipLevels` |
| Ledger pages | `VillageLedger`, `VillageLedgerItem`, `LedgerPayload`, `LedgerRequestPayload`; client `LedgerScreen` |
| Speech bubbles | `Emote`, `EmotePayload`; client `EmoteBubbles` (state and animation) and `ResidentRenderer.submitBubble` (world) |
| Conversation window | client `FriendshipScreen` |
| Breeding hooks | `mixin/VillagerFamilyMixin` (records parents), `mixin/VillagerMakeLoveMixin` (relatives and committed residents) |
| Art | `tools/social_assets.py` writes `textures/gui/emotes.png`, the ledger item art, model and recipe |

Each village's `Society` is saved on the level that records the village (`villagefriends:societies`), keyed by village ID. A society is created when the first resident's hometown is confirmed (natural villages and Village Marker settlements alike). Villagers without a hometown simply have no society; every feature falls back gracefully.

## The model

**Relationship meters (-100 to 100).** Only real shared history is stored. A meter is computed from:

- *chemistry* (`Chemistry.chemistry`, -1 to 1): a stable random spark for the pair, plus a bonus for the same personality (shared hobby) and the personality matrix (`MATCHES`), plus a little for warmhearted residents;
- *time known*: strangers start at 3 and approach their pair's target over the days since the later of them settled (`1 - e^(-days/40)`);
- *days together*: each day two loaded residents stand within six blocks adds half a point, up to 40 days (`Tie`);
- *quarrels*: a fresh quarrel costs 30 points, healing by one a day.

Family starts at its target: parents and children about 78, siblings about 66 (they bicker), extended family about 50, sweethearts 86, spouses 92. Labels come from `Relations.feeling` (Rivals, Not close, Neighbors, Friendly, Friends, Good friends, Best friends) or the family word (`Relations.kin`, gendered from the resident's appearance; non-binary residents get neutral words).

**Love.** Two residents can fall in love only if both are adults at home, single, not related by blood within three steps (parents, siblings, grandparents, aunts and uncles, cousins), both romantic, and attracted to each other. Then:

- each pair has its own time to love, `Chemistry.loveDays`: 50 to 1,000 days of knowing each other, spread evenly;
- at 60% of that time, if their meter is at least 40, one is *smitten* (a secret crush that close friends can hear about);
- when the time comes and the meter is at least 50, they become sweethearts. At most one couple forms per village per day;
- sweethearts marry after 30 to 150 days if their meter stays at 65 or more.

About one resident in five is not romantic and never falls in love (`ROMANTIC_PERCENT`). Attraction is set per resident (`Chemistry.attraction`): most men and women are drawn to the other gender, about one in eleven to their own, about one in eleven to anyone; non-binary residents are drawn to anyone. Pairs that never click never fall in love. In tests, a village of 20 adults saw its first couple between day 75 and day 270, and 2 to 6 couples over 1,000 days, with 8 to 16 residents still single.

**Families.** When a natural village is first found, each unvisited newcomer who `bringsFamily` (55%) joins the household of the nearest other new arrival within 20 blocks who also does: two compatible single adults usually as a married couple (70%), otherwise siblings; an adult and a child as parent and child (marrying a single parent where compatible); two children as siblings. A newcomer who still has their generated name takes the household's surname (restricted surnames stay with eligible complexions). Babies record both parents when vanilla breeding creates them, join their family and take a parent's surname. Relatives never breed with each other, and a resident in love breeds only with their partner.

**Days.** A village lives its days whenever some of its residents are loaded. If the village was unloaded for a while, it catches up on up to 30 days at once (`CATCH_UP`), so time away still counts toward love without a burst of events. Deaths settle a tick later, so a villager killed by a zombie is recorded as cursed (curable), not dead.

**News.** Births, romances, weddings, deaths, curses and cures, newcomers, quarrels and new friendships become `News`. The 40 latest are kept. Big events are announced in chat to players in the village. Residents tell news from their own point of view (`Gossip.tell`).

## Dialogue

`Gossip` turns the society into lines:

- `mention` adds a neighbor to everyday chat, work and adventure talk (partner, family, best friend, rival, a coworker in the same job);
- `news` answers *Any village news?* (friendship level 3): fresh news first; close friends (level 6) also hear who is smitten with whom; otherwise who has been spending time together;
- `heart` answers *Anyone special?* (level 5): married, sweethearts, widowed, a crush, happily single or not interested, then their family;
- `greeting` adds a breathless "Did you hear?" on the first hello after big news;
- `about` feeds the Journal and the Ledger.

Lines name real residents. Add variants by extending the `pick(...)` lists; keep them pronoun-free where possible (`Relations.pronouns` exists for when a line needs one).

## Friendship levels

`FriendshipLevels` splits the five existing tiers into ten levels at 5, 15, 28, 40, 58, 80, 105, 140, 170 and 200 points, each tier spanning two levels. The story gates still decide how far points alone go: without a shared experience you stop at level 3, before the personal confession at 5, and before finishing the story at 7. Earned legacy tiers keep their floor. Each level has a name and unlocks something:

| Level | Name | Unlocks |
|---|---|---|
| 1 | Familiar Face | They remember you between visits |
| 2 | Acquaintance | Favorite things; time together |
| 3 | Friendly Neighbor | Village news |
| 4 | Friend | Adventures; picnic invitations |
| 5 | Good Friend | Heart-to-heart talks |
| 6 | Close Friend | Village secrets (crushes) |
| 7 | Trusted Friend | They wave you over with a heart |
| 8 | Best Friend | Best-friend greetings |
| 9 | Kindred Spirit | A small daily gift matching their hobby |
| 10 | Lifelong Friend | A friend for life |

The conversation celebrates a new level once (`seen_level:N` bond flag). The player's last known level with each resident is kept on the player (`villagefriends:acquaintances`) for the Ledger.

## Speech bubbles

`Emote` lists twelve bubbles: EXCLAIM, QUESTION, HEART, NOTE, ANGER, SWEAT, DOTS, SLEEP, SPARKLE, IDEA, GLOOM and BLUSH. They appear:

- when neighbors standing close together strike up a conversation (`VillageSocieties.chat`): hearts for couples, a blush for a crush, music for friends and family, sparks for rivals or a recent quarrel, dots and question marks for acquaintances;
- in conversation, as the mood of each reply (laughter, a loved gift, a declined one, news, a heart-to-heart, a level-up);
- when a resident greets you (!), sleeps (Zz), is hurt, or shows vanilla hearts, anger, happiness or raid sweat;
- when a trusted friend (level 7) sees you, or a friend has fresh news (an idea bubble);
- when family and close friends mourn a death, and when parents have a baby.

Each bubble pops in with an overshoot, bobs, animates its symbol (the "!" shakes, "?" tilts, hearts beat, notes sway, dots cycle, "Zz" drifts) and pops out with a soft pop sound. Bubbles render above the name tag, always full-bright, and are left out of portraits.

To change the art, edit `tools/social_assets.py` (symbols are fill masks; outlines are added automatically) and run `python tools/social_assets.py --preview`; the preview lands in `build/previews/emotes_preview.png`. Sheet layout: three 32px bubbles on row 0 (speech, thought, shout), then 16px symbols from y=32 in `Emote` order, with three DOTS frames.

## Conversation window

The resident stays visible in the world (no blur). At the bottom, a dialogue box holds their live portrait, a name ribbon colored by personality with job, personality and hometown, the typed line and a status line. Replies float as numbered bubbles on the right (keys 1–6). A dock switches between Talk, Story, Time, Travel and Journal and holds Give gift (showing the held item and gifts left), Trade, Village (the Ledger at their page) and Goodbye; wide screens label the buttons. A card in the corner shows the level, ten hearts with the next one filling, and what the next level needs. Button names are unchanged for game tests.

## Village Ledger

Craft one from a book, an ink sac and paper, or right-click a Notice Board. Inside a village it lists every resident (living first) with job, family or love life and your friendship level. Click a resident for their page: personality, how long they have lived there, partner, family, closest friend and rival, their favorite gift once you are acquaintances, a secret crush once you are close friends, and a meter for how they feel about every neighbor. Without a selection, the right page shows village news.

## Verification

- `gradlew test` runs `SocietyTest` (traits, meters, households, births, slow love across 1,100 days, crushes, deaths and curses, codecs, bounds), `GossipTest` and `FriendshipLevelsTest`.
- `gradlew runClientGameTest -PvillageLifeOnly` runs `VillageLifeGameTest` in Minecraft and saves screenshots named `village-life-*`.
- `gradlew runClientGameTest -Ptests=VillageLifeGameTest,CommunityGameTest` runs any chosen gameplay tests by class name.
