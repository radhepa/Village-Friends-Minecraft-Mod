# Birthdays and notice boards

Version 2.20 gives every resident a birthday on a village calendar, with a party by the bell, and turns the Notice Board into a real village board where residents pin up notices asking for help: monster hunts, things they need for their trade, letters to carry to a neighbor, and surprises for someone's birthday.

## Where things live

| Piece | Code |
|---|---|
| The village calendar and birthdays (pure, unit-tested) | `social/Calendar.java`; `Townsfolk.born` / `birthday()`; `Society.celebrants`, `birthdays`, birthday news in `Society.advance` |
| Birthday parties in a resident's day (pure) | `Routine.Block.PARTY`, `Routine.party`, `Routine.partyTime` |
| Birthdays in the world | `Birthdays` (party hat flag, guest lists, party effects, cake time, greetings, chat, "Happy birthday!", birthday gifts) |
| Party hat | client `PartyHatLayer`; texture `textures/entity/party_hat.png` |
| Notices, boards and the player's log (pure, unit-tested) | `quest/Notice`, `quest/Board`, `quest/QuestLog`, `quest/Postings` (what gets posted and what it pays), `quest/Words` (counts and plurals) |
| Notice boards in the world | `VillageQuests` (boards, the screen's data, accept/abandon/claim, hunting, letters, rewards, standing), `NoticeBoardBlock` (`notes` state), `NoticeBoardBlockEntity` |
| Board screen | client `NoticeBoardScreen`, `NoticeBoardClient`; `NoticeBoardPayload`, `NoticeActionPayload` |
| Dialogue | `tools/dialogue/lines/birthdays.txt`, `tools/dialogue/lines/notices.txt` |
| Party animations | `tools/animations/village_life/party.py` (11 clips) |
| Board model and art | `tools/notice_board/notice_board.py`; items and the hat texture `tools/celebration_assets.py` |

Each level keeps its villages' boards (`villagefriends:notice_boards`) next to their societies. A player's notices in hand travel with them (`villagefriends:quests`, kept on death). The party hat is a synced flag (`villagefriends:birthday`).

## The calendar

Four seasons (Spring, Summer, Autumn, Winter) of 28 days, so 112 days to a year. A season is four village weeks: it always starts on a Moonday, and Market Day falls on the 7th, 14th, 21st and 28th. Day 0 of the world is Spring 1, Year 1. The Village Ledger and the notice board show the date ("Hayday, Summer 12, Year 2").

## Birthdays

Every resident has a birthday drawn from their ID; a baby born in the village has theirs on the day they were born. Birthdays show on each resident's Ledger page and in the Journal ("Birthday: Summer 12 (in 3 days)"), and the next six are listed on the village's notice board.

On the day:

- **The village hears about it.** "It's Mira Ash's birthday! Party by the bell this evening." is village news, announced in chat to players in the village. Neighbors mention it when they greet you ("Did you know it's Mira's birthday today?") and in chat.
- **They wear a party hat**, a striped cone with a pompom, all day, and greet you with birthday lines. The Ledger list shows "Birthday today!" and the conversation's status line "Birthday today!".
- **"Happy birthday!"** appears as a reply, once a year: +8 friendship, a little trust, and they remember it.
- **Gifts count double.** A whole cake or a **Birthday Card** (craft one from paper and any dye) counts as their favorite thing, so either is worth 28 friendship; their actual favorite also earns 28. A card given on another day is sweet but early: +3, and they tell you when their birthday is.
- **The party.** From 16:30 to 18:30 the birthday resident takes the evening off (even from work) and goes to the bell. Their family, their sweetheart, everyone who likes them (relationship 35 or more, either way) and every child in the village joins them. Notes float over the party, guests cheer and show hearts, and confetti bursts now and then. Rain and storms keep everyone indoors; nobody leaves their bed, the night watch or a raid for it. Party clips (clapping along, raising a cup, swaying, a jig, laughing, a cheer, humming, and a bouncy hop for children) dominate while the party is on; the guest of honor makes a wish, bows thanks and beams.
- **Cake time** at 17:45: the candles go out in a burst of fireworks and sparkles, and every player within 16 blocks gets a **Slice of Birthday Cake** (food with a short burst of speed) and +10 friendship, once a year.

Residents a few days from their birthday sometimes mention it, and from one to four days before, their sweetheart, a relative or their best friend may pin a **birthday surprise** on the notice board.

## Notice boards

Notice Boards stand in every village square (and can be crafted, as before). Right-click one to open it. A board shows how many notices are up for grabs with pinned notes on the block itself (0 to 3), so you can tell from across the square.

**What goes up.** Each morning, notices nobody took come down after three days, and up to two new ones go up; a board always has three to five notices for the taking (a brand-new board starts with four). Each resident has at most one notice up at a time. Everyone posts in their own voice, from the dialogue bank:

| Kind | What it asks | Who posts it |
|---|---|---|
| Hunt | Defeat 2–8 zombies (husks, drowned and zombie villagers count), skeletons (strays, bogged, parched), spiders (cave spiders), creepers, slimes, witches, phantoms or pillagers (vindicators and evokers count) | Adults, especially knights and archers (pillagers, witches), fletchers (skeletons), shepherds (spiders), clerics (zombies), and protective or steadfast residents |
| Wanted | Bring something for their trade: wheat for the farmer, iron for the armorer, paper for the librarian, eggs for the cook, apples for the tavern's cider, flowers for the apothecary, dyes for the painter, logs for the carpenter... Children ask for flowers, cookies, a slime ball | Anyone; each of the 25 jobs has its own list |
| Letter | Carry a sealed letter to another resident: their sweetheart, a relative, their best friend, a secret crush, or someone they quarreled with (an apology) | Adults with someone to write to |
| Birthday surprise | Bring a cake, or the guest of honor's favorite thing, for a birthday one to four days away | Their sweetheart, a relative, or their best friend |

**Taking notices.** Click a notice to read it, then **Take this notice**. You can hold three at a time, from any villages; drop one with **Pin it back up** (or the x on the board's overview) and it goes back up if its time hasn't run out. Taking a letter puts a **Sealed Letter** addressed to its recipient in your pack.

**Doing them.** Monsters count wherever you defeat them, by your hand or your arrows; the action bar shows your count and chat tells you when you're done. What was asked for counts when it's in your pack. Hand a letter to its recipient in person ("I have a letter for you"): they react to who it's from, and an apology forgives the writer's last quarrel.

**Turning them in.** At the board (**Turn it in**) or to the resident who posted it ("About your notice..."). Rewards:

- **Emeralds** by how much was asked (2–16 for hunts, 1–12 for wanted goods, 2–4 for letters, 3–5 for birthday surprises), a little experience, and a gift from the poster's trade (bread from the farmer, arrows from the fletcher, cider from the tavern keeper, a bandage wrap from the apothecary...), sometimes something special for big notices (a diamond from the smiths, a golden apple from the cleric, a rain cloak from the tailor, a village bench from the carpenter, a music disc from the bard).
- **+10 friendship** with the poster, a memory, and better prices from them (vanilla gossip). If they weren't around when you used the board, they thank you the next time you talk. Birthday surprises also earn friendship with the guest of honor.
- **Village news**: "Alex answered a notice from Mira Ash."
- **Standing in the village**, by notices answered there: Newcomer, **Helping Hand** (1), **Good Neighbor** (4, every resident gives you better prices), **Pillar of the Community** (10, more so, and eight emeralds), **Hero of _village_** (20, the best prices and Hero of the Village for two days).

With nothing selected, the board's right-hand page lists your notices in hand with their progress and the village's upcoming birthdays. **Village Ledger** opens the ledger, and **Back** returns to the board.

## Changing things

- **Words:** add lines under the pools in `tools/dialogue/lines/birthdays.txt` and `notices.txt`, then `python tools/dialogue/dialogue.py` (and `--check`). Notices may use `{mobs}`, `{wanted}`, `{recipient}`, `{celebrant}`, `{when}` and `{birthday}`; birthday chat `{celebrant}`, `{birthday}`, `{when}` and `{season}`. Pools: `greet.birthday`, `greet.birthday.close`, `birthday.thanks`, `birthday.gift`, `birthday.gift.loved`, `birthday.card`, `birthday.cake`, `birthday.soon`, `greet.party`, `chat.party`, `greet.routine.party`, `routine.party`, `birthday.party.host`, children's `baby.*` versions; `notice.hunt.<group>`, `notice.fetch.<job>`, `notice.fetch.general`, `notice.fetch.child`, `notice.letter.<kind>`, `notice.birthday`, `notice.thanks.<kind>`, `notice.thanks.later`, `letter.read.<kind>`.
- **What residents ask for and give:** `Postings.HUNTS`, `WANTS`, `CHILD_WANTS`, `GIFTS`, `CHILD_GIFTS` and `RARE`.
- **How often:** `Postings.MIN_OPEN`, `MAX_OPEN`, `NEW_PER_DAY`, `LIFETIME`; the mix of kinds in `Postings.post`.
- **Standing:** `Board.STANDING` and the effects in `VillageQuests.standing`.
- **The party:** `Routine.PARTY_START`/`PARTY_END`, guests in `Birthdays.guests`, cake time `Birthdays.CAKE_TIME`.
- **Board model and art:** edit `tools/notice_board/notice_board.py` and run it (`--check`, `--preview`, `--boxes`); never hand-edit its JSON or PNG. Items and the party hat: `python tools/celebration_assets.py`.

## Verification

- `gradlew test` runs `BirthdayTest` (the calendar, birthdays spread over the year, babies' birthdays, birthday news and gossip, party rules) and `NoticeBoardTest` (boards refresh between three and five notices, every kind of notice makes sense, taking and dropping, hunts and the quest log, plurals, codecs), along with `DialogueBankTest` (a pool for the party routine).
- `gradlew runClientGameTest -Ptests=CelebrationsGameTest` plays a birthday (party hat on server and client, the party with a child guest, cake time, a birthday wish and a doubled birthday gift) and the notice board (pinned notes, the screen and its birthdays, the three-notice limit, a zombie hunt counted kill by kill, turn-ins at the board, a letter delivered in person, standing, village news, better prices, save/reload). Screenshots are named `celebrations-*`.
