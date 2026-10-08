package dev.villagefriends;

import dev.villagefriends.routine.Routine;
import dev.villagefriends.social.Calendar;
import dev.villagefriends.social.Society;
import java.util.*;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.item.ItemStack;
import static dev.villagefriends.VillageFriends.*;

/**
 * Birthdays on the village calendar ({@link Calendar}). On a resident's birthday the village hears about
 * it in the morning, they wear a party hat, greet you with birthday lines and treasure gifts twice as much;
 * in the evening their family and friends gather by the bell for a party with music, confetti and cake,
 * and anyone who comes gets a slice. Children love every party.
 *
 * <p>Bond flags: {@code birthday_wish:<year>} you wished them a happy birthday that year,
 * {@code birthday_party:<year>} you came to their party, {@code birthday_gift:<year>} you gave a birthday gift.
 */
public final class Birthdays {
    /** Whether a resident is celebrating their birthday today: shared with clients for the party hat. */
    public static final AttachmentType<Boolean> BIRTHDAY = AttachmentRegistry.create(Identifier.fromNamespaceAndPath("villagefriends", "birthday"),
            b -> b.syncWith(ByteBufCodecs.BOOL, AttachmentSyncPredicate.all()));
    /** The cake comes out a little before the party ends. */
    static final int CAKE_TIME = Routine.at(17, 45);
    /** Who is invited to today's parties in one village. */
    private record Guests(long day, Set<String> hosts, Set<String> guests) {}
    private static final Map<String, Guests> guestLists = new HashMap<>();
    /** "residentId|day" for parties that already had their cake. */
    private static final Set<String> caked = new HashSet<>();

    public static void register() {
        ServerTickEvents.END_SERVER_TICK.register(Birthdays::tick);
    }
    public static void clear() { guestLists.clear(); caked.clear(); }

    // -- who is celebrating -------------------------------------------------------------------------

    /** Whether today is this resident's birthday (server side). */
    public static boolean celebrating(Villager v) {
        var society = VillageSocieties.of(v); var t = society == null ? null : society.get(VillageSocieties.id(v));
        return t != null && t.home() && Calendar.isBirthday(t.birthday(), day(v.level()));
    }
    /** Whether a resident wears the party hat (client side, from the synced flag). */
    public static boolean wearingHat(Villager v) { return Boolean.TRUE.equals(target(v).getAttached(BIRTHDAY)); }
    private static Guests guests(Villager v, Society society, long today) {
        var home = target(v).getAttached(HOME);
        String key = home.dimension() + "|" + home.village();
        var known = guestLists.get(key);
        if (known != null && known.day() == today) return known;
        var hosts = new HashSet<String>(); var guests = new HashSet<String>();
        for (var host : society.celebrants(today)) {
            hosts.add(host.id());
            for (var t : society.living()) {
                if (!t.home() || t.id().equals(host.id())) continue;
                // Family, their sweetheart, good friends, and every child in the village.
                if (!t.adult() || !society.relation(host.id(), t.id()).isEmpty() || host.partner().equals(t.id())
                        || society.affinity(host.id(), t.id(), today) >= 35 || society.affinity(t.id(), host.id(), today) >= 35) guests.add(t.id());
            }
        }
        var list = new Guests(today, Set.copyOf(hosts), Set.copyOf(guests));
        guestLists.put(key, list);
        return list;
    }
    /** The routine with a birthday party in it, if this resident is hosting one or invited to one right now. */
    public static Routine.Plan party(Villager v, Routine.Plan plan, int time) {
        if (!Routine.partyTime(time)) return plan;
        var society = VillageSocieties.of(v);
        if (society == null) return plan;
        long today = day(v.level());
        var list = guests(v, society, today);
        if (list.hosts().isEmpty()) return plan;
        String id = VillageSocieties.id(v);
        boolean host = list.hosts().contains(id);
        if (!host && !list.guests().contains(id)) return plan;
        return Routine.party(plan, time, host);
    }

    // -- the day ------------------------------------------------------------------------------------

    private static void tick(MinecraftServer server) {
        int tick = server.getTickCount();
        if (tick % 100 == 37) for (var v : List.copyOf(CompanionController.loaded)) hat(v);
        if (tick % 40 == 13) for (var v : List.copyOf(CompanionController.loaded)) if (wearingHat(v) && "party".equals(target(v).getAttached(ROUTINE))) celebrate(v);
        if (tick % 1200 == 0) caked.removeIf(key -> Long.parseLong(key.substring(key.indexOf('|') + 1)) < day(server.overworld()) - 1);
    }
    /** Puts the party hat on (or takes it off) as birthdays come and go. */
    private static void hat(Villager v) {
        if (!v.isAlive() || v.isRemoved()) return;
        boolean today = celebrating(v);
        if (today != wearingHat(v)) {
            if (today) target(v).setAttached(BIRTHDAY, true); else target(v).removeAttached(BIRTHDAY);
            if (today) VillageSocieties.emote(v, Emote.SPARKLE, v.getRandom().nextInt(20));
        }
    }
    /** Music, confetti and cheering around the guest of honor; at cake time, a slice for everyone who came. */
    private static void celebrate(Villager host) {
        if (!(host.level() instanceof ServerLevel level) || host.isSleeping()) return;
        var random = host.getRandom();
        var party = new ArrayList<Villager>();
        for (var v : CompanionController.loaded)
            if (v != host && v.isAlive() && v.level() == level && v.distanceToSqr(host) < 12 * 12 && "party".equals(target(v).getAttached(ROUTINE))) party.add(v);
        double x = host.getX(), y = host.getY(), z = host.getZ();
        level.sendParticles(ParticleTypes.NOTE, x + random.nextGaussian() * .8, y + 2.3, z + random.nextGaussian() * .8, 0, random.nextFloat(), 0, 0, 1);
        if (!party.isEmpty()) {
            var guest = party.get(random.nextInt(party.size()));
            level.sendParticles(ParticleTypes.HAPPY_VILLAGER, guest.getX(), guest.getY() + 1.8, guest.getZ(), 3, .35, .3, .35, .02);
            if (random.nextInt(3) == 0) VillageSocieties.emote(guest, switch (random.nextInt(4)) { case 0 -> Emote.HEART; case 1 -> Emote.EXCLAIM; default -> Emote.NOTE; }, random.nextInt(20));
        }
        if (random.nextInt(4) == 0) level.sendParticles(ParticleTypes.FIREWORK, x, y + 2.6, z, 8, .45, .25, .45, .04);
        int time = ResidentRoutines.timeOfDay(level); long today = day(level);
        if (time < CAKE_TIME || !caked.add(VillageSocieties.id(host) + "|" + today)) return;
        // Cake time: the candles go out, everyone cheers, and the cake goes around.
        level.sendParticles(ParticleTypes.FIREWORK, x, y + 2.4, z, 40, .7, .5, .7, .12);
        level.sendParticles(ParticleTypes.TOTEM_OF_UNDYING, x, y + 1.6, z, 30, .9, .6, .9, .25);
        level.playSound(null, host.blockPosition(), SoundEvents.FIREWORK_ROCKET_TWINKLE, SoundSource.NEUTRAL, 1F, 1.1F);
        level.playSound(null, host.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.NEUTRAL, .6F, 1.4F);
        VillageSocieties.emote(host, Emote.HEART, 0);
        for (var guest : party) VillageSocieties.emote(guest, random.nextBoolean() ? Emote.EXCLAIM : Emote.SPARKLE, 4 + random.nextInt(16));
        int year = Calendar.year(today);
        for (var player : level.players()) {
            if (player.isSpectator() || player.distanceToSqr(host) > 16 * 16) continue;
            var b = bond(host, player);
            if (b.has("birthday_party:" + year)) continue;
            saveBond(host, player, b.flag("birthday_party:" + year).trust(3).remember(today, "You came to my birthday party."));
            reward(host, player, 10);
            giveItem(player, "villagefriends:birthday_cake_slice", 1);
            player.sendSystemMessage(Component.literal(name(host) + " blows out the candles! You get a slice of birthday cake. (+10 friendship)").withStyle(ChatFormatting.LIGHT_PURPLE), false);
        }
    }

    // -- conversation -------------------------------------------------------------------------------

    private static boolean child(Villager v) { return v.isBaby(); }
    /** A birthday greeting from the guest of honor, or news of someone else's party; null for an ordinary day. */
    static String greeting(Villager v, ServerPlayer p) {
        var society = VillageSocieties.of(v);
        if (society == null) return null;
        long today = day(v.level()); var self = society.get(VillageSocieties.id(v));
        if (self == null) return null;
        var random = v.getRandom();
        if (self.home() && Calendar.isBirthday(self.birthday(), today)) {
            int level = FriendshipLevels.level(state(v, p), bond(v, p));
            String pool = child(v) ? "baby.greet.birthday" : level >= FriendshipLevels.HEART_TO_HEART && random.nextBoolean() ? "greet.birthday.close" : "greet.birthday";
            return TalkWorld.say(v, p, pool, Map.of());
        }
        if (!society.celebrants(today).isEmpty() && random.nextInt(3) == 0)
            return TalkWorld.say(v, p, child(v) ? "baby.party" : "greet.party", Map.of());
        int until = Calendar.daysUntil(self.birthday(), today);
        if (until >= 1 && until <= 3 && random.nextInt(3) == 0) return TalkWorld.say(v, p, child(v) ? "baby.birthday.soon" : "birthday.soon", Map.of());
        return null;
    }
    /** Birthday chat instead of the usual, now and then; null otherwise. */
    static String chat(Villager v, ServerPlayer p, String topic) {
        if (!topic.equals("chat")) return null;
        var society = VillageSocieties.of(v);
        if (society == null) return null;
        long today = day(v.level()); var self = society.get(VillageSocieties.id(v));
        if (self == null) return null;
        var random = v.getRandom();
        if (self.home() && Calendar.isBirthday(self.birthday(), today))
            return "party".equals(target(v).getAttached(ROUTINE)) && !child(v) ? TalkWorld.say(v, p, "birthday.party.host", Map.of())
                    : random.nextBoolean() ? TalkWorld.say(v, p, child(v) ? "baby.greet.birthday" : "greet.birthday", Map.of()) : null;
        if (!society.celebrants(today).isEmpty() && random.nextInt(5) < 2) return TalkWorld.say(v, p, child(v) ? "baby.party" : "chat.party", Map.of());
        int until = Calendar.daysUntil(self.birthday(), today);
        if (until >= 1 && until <= 5 && random.nextInt(4) == 0) return TalkWorld.say(v, p, child(v) ? "baby.birthday.soon" : "birthday.soon", Map.of());
        return null;
    }
    /** " · Birthday today!" for the conversation's status line. */
    static String status(Villager v) { return celebrating(v) ? " · Birthday today!" : ""; }
    /** "Happy birthday!" on their birthday, once a year. */
    static List<FriendshipPayload.Choice> choices(Villager v, ServerPlayer p) {
        if (!celebrating(v) || bond(v, p).has("birthday_wish:" + Calendar.year(day(v.level())))) return List.of();
        return List.of(new FriendshipPayload.Choice("birthday_wish", "Happy birthday!", true));
    }
    static boolean handle(ServerPlayer p, Villager v, String action) {
        if (!action.equals("birthday_wish")) return false;
        long today = day(v.level()); int year = Calendar.year(today);
        var b = bond(v, p);
        if (!celebrating(v) || b.has("birthday_wish:" + year)) {
            show(p, v, "talk", NarrativeEngine.greeting(v, p), "You already wished them a happy birthday.", false); return true;
        }
        saveBond(v, p, b.flag("birthday_wish:" + year).trust(3).remember(today, "You wished me a happy birthday."));
        reward(v, p, 8);
        String line = TalkWorld.say(v, p, child(v) ? "baby.birthday.thanks" : "birthday.thanks", Map.of());
        show(p, v, "talk", line != null ? line : "You remembered! Thank you. That's the best start to a birthday.",
                "+8 friendship. Birthday gifts count double today.", false, Emote.HEART);
        return true;
    }

    /** What a present means on someone's birthday: the value, their reply and how they remember it. */
    /** {@code status} follows the friendship gained on the status line. */
    record Gift(int value, String reply, String memory, String status, Emote mood) {}
    /**
     * A gift given on the recipient's birthday counts double, a cake or a birthday card counts as their
     * favorite thing, and the first birthday gift each year is remembered. Null on other days, except
     * for a birthday card, which is sweet but early (or late).
     */
    static Gift gift(Villager v, ServerPlayer p, String item, int value, boolean loved) {
        boolean card = item.equals("villagefriends:birthday_card"), cake = item.equals("minecraft:cake");
        long today = day(v.level());
        if (!celebrating(v)) {
            if (!card) return null;
            var society = VillageSocieties.of(v); var self = society == null ? null : society.get(VillageSocieties.id(v));
            String when = self == null ? "" : " My birthday is " + Calendar.birthdayDate(self.birthday()) + ", " + Calendar.when(Calendar.daysUntil(self.birthday(), today)) + ".";
            return new Gift(3, "A birthday card? For me? It isn't my birthday yet, but I'll keep it on the mantel." + when,
                    "You gave me a birthday card, a little early.", "Save cards for their birthday!", Emote.BLUSH);
        }
        int doubled = (card || cake ? 14 : value) * 2;
        if (doubled == 0) return null;
        String pool = child(v) ? "baby.birthday.gift" : card ? "birthday.card" : cake ? "birthday.cake" : loved ? "birthday.gift.loved" : "birthday.gift";
        String reply = TalkWorld.say(v, p, pool, Map.of());
        int year = Calendar.year(today);
        var b = bond(v, p);
        if (!b.has("birthday_gift:" + year)) saveBond(v, p, b.flag("birthday_gift:" + year));
        dev.villagefriends.deed.Deeds.birthdayGift(p, v);
        return new Gift(doubled, reply != null ? reply : "A birthday present! You shouldn't have. Well... I'm glad you did.",
                "You gave me " + itemName(item) + " for my birthday.", "A birthday gift means twice as much!",
                loved || card || cake ? Emote.HEART : Emote.SPARKLE);
    }

    private Birthdays() {}
}
