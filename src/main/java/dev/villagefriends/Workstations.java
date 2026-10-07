package dev.villagefriends;

import dev.villagefriends.WorkstationBlock.Station;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.network.Filterable;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.entity.projectile.arrow.AbstractArrow;
import net.minecraft.world.entity.projectile.arrow.Arrow;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.component.WrittenBookContent;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import static dev.villagefriends.VillageFriends.*;

/**
 * What each profession's workstation does, for players and for the resident who works there.
 *
 * <ul>
 * <li>Training Dummy: strike it to measure your hits and combos. Knights train on it and gain guard experience.</li>
 * <li>Archery Target: arrows score 1-10 by how close they land to the bullseye. Archers practice on it.</li>
 * <li>Kitchen Stove: cooks raw food twice as fast as a campfire. The cook makes a dish of the day here, one helping per visitor.</li>
 * <li>Drinks Barrel and Tap Stand: press apples or berries into cider, brew cocoa into coffee, and pour mugs. The tavern keeper restocks them.</li>
 * <li>Alchemical Press: press flowers and berries, then bottle an Herbal Tonic. The apothecary tends anyone hurt nearby.</li>
 * <li>Easel: paint the canvas with dyes and take the painting home. The painter works on a new picture every day.</li>
 * <li>Music Stand: play a tune that lifts everyone's spirits (Haste) and makes the neighbors cheer. The bard performs here.</li>
 * <li>Sewing Table: mend leather, bows, rods and elytra with string; unravel wool. The tailor mends the guards' armor.</li>
 * <li>Sawmill: saw logs into half again as many planks, planks into sticks. The carpenter leaves offcuts to take.</li>
 * <li>Archives: read the village chronicle, or copy it into a book. Study near the scholar for experience.</li>
 * </ul>
 */
public final class Workstations {
    /** Herbs that fit in the press. */
    private static final List<Item> HERBS = List.of(Items.SWEET_BERRIES, Items.GLOW_BERRIES, Items.KELP, Items.FERN, Items.LARGE_FERN, Items.MOSS_BLOCK,
            Items.SHORT_GRASS, Items.VINE, Items.SEAGRASS, Items.SPORE_BLOSSOM, Items.LILY_PAD);
    private static final int MAX_DRINKS = 16, MAX_HERBS = 12, MAX_OFFCUTS = 16, HERBS_PER_TONIC = 3, TRAINING_CAP = 15, STUDY_CAP = 30;

    private record Combo(long last, int hits, float total) {}
    private static final Map<UUID, Combo> combos = new HashMap<>();
    /** Per resident or player per day: training XP gained, experience studied. */
    private record Daily(long day, double amount) {}
    private static final Map<UUID, Daily> trained = new HashMap<>(), studied = new HashMap<>();
    /** Who last worked at a station, for "Mira's dish of the day". */
    private static final Map<GlobalPos, String> keepers = new HashMap<>();
    private record Note(ResourceKey<Level> level, BlockPos pos, long at, Holder<SoundEvent> sound, float pitch) {}
    private static final List<Note> notes = new ArrayList<>();

    public static void clear() { combos.clear(); trained.clear(); studied.clear(); keepers.clear(); notes.clear(); }

    // -- players using stations --------------------------------------------------------------------

    public static InteractionResult use(Station station, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, ItemStack stack) {
        if (player.isSpectator()) return InteractionResult.PASS;
        if (level.isClientSide()) return InteractionResult.SUCCESS;
        var server = (ServerLevel) level; var p = (ServerPlayer) player;
        if (!(level.getBlockEntity(pos) instanceof WorkstationBlockEntity e)) return InteractionResult.PASS;
        boolean creative = player.getAbilities().instabuild;
        return switch (station) {
            case TRAINING_DUMMY -> tell(p, "Strike the dummy to measure your hits. Sneak to pick it up.");
            case ARCHERY_TARGET -> tell(p, "Shoot it with arrows: the closer to the bullseye, the higher the score.");
            case KITCHEN_STOVE -> stove(server, pos, p, e, stack, creative);
            case DRINKS_BARREL -> drinks(server, pos, p, e, stack, creative, true);
            case TAP_STAND -> drinks(server, pos, p, e, stack, creative, false);
            case ALCHEMICAL_PRESS -> press(server, pos, p, e, stack, creative);
            case EASEL_CANVAS -> easel(server, state, pos, p, e, stack, creative);
            case MUSIC_STAND -> music(server, pos, p, e, stack);
            case SEWING_TABLE -> sew(server, pos, p, stack, creative);
            case SAWMILL -> saw(server, pos, p, e, stack, creative);
            case ARCHIVES -> archives(server, pos, p, stack, creative);
        };
    }
    private static InteractionResult tell(ServerPlayer p, String message) {
        p.sendSystemMessage(Component.literal(message), true); return InteractionResult.SUCCESS_SERVER;
    }
    private static void take(ItemStack stack, int count, boolean creative) { if (!creative) stack.shrink(count); }
    private static void give(ServerPlayer p, ItemStack stack) { if (!p.getInventory().add(stack)) drop(p, stack); }
    /** Swaps one held item for another, the way filling a bottle does. */
    private static void swap(ServerPlayer p, ItemStack held, ItemStack result, boolean creative) {
        if (!creative) held.shrink(1);
        give(p, result);
    }
    private static String keeper(ServerLevel level, BlockPos pos, String fallback) { return keepers.getOrDefault(GlobalPos.of(level.dimension(), pos), fallback); }
    private static long today(ServerLevel level) { return day(level); }

    private static InteractionResult stove(ServerLevel level, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack, boolean creative) {
        if (!stack.isEmpty()) {
            var food = creative ? stack.copy() : stack;
            if (!e.cook(level, food)) {
                if (e.items().stream().noneMatch(ItemStack::isEmpty)) return tell(p, "The stove is full. Wait for something to finish cooking.");
                return InteractionResult.TRY_WITH_EMPTY_HAND;
            }
            level.playSound(null, pos, SoundEvents.CAMPFIRE_CRACKLE, SoundSource.BLOCKS, 1, 1.4F);
            return tell(p, "Cooking " + e.items().stream().filter(s -> !s.isEmpty()).count() + " of 4. Cooked food pops out on top.");
        }
        long today = today(level);
        if (e.mealDay == today && !e.served.contains(p.getUUID().toString())) {
            e.served.add(p.getUUID().toString()); e.changed();
            boolean stew = today % 2 == 1;
            give(p, new ItemStack(VillageItems.get(stew ? "hearty_stew" : "fresh_village_bread"), stew ? 1 : 2));
            level.playSound(null, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, .6F, .8F);
            return tell(p, keeper(level, pos, "The cook") + "'s dish of the day: " + (stew ? "hearty stew" : "fresh village bread") + ". Enjoy!");
        }
        if (e.cooking()) {
            int left = 0;
            for (int i = 0; i < WorkstationBlockEntity.SLOTS; i++) if (!e.items().get(i).isEmpty()) left = Math.max(left, e.total[i] - e.progress[i]);
            return tell(p, "Something smells good. Ready in about " + Math.max(1, left / 20) + "s.");
        }
        return tell(p, e.mealDay == today ? "You've had today's dish. The cook makes another tomorrow." : "Put raw food on the stove to cook it. The cook makes a dish of the day here.");
    }

    private static InteractionResult drinks(ServerLevel level, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack, boolean creative, boolean barrel) {
        String drink = barrel ? "cider" : "coffee";
        int add = barrel ? stack.is(Items.APPLE) ? 2 : stack.is(Items.SWEET_BERRIES) || stack.is(Items.GLOW_BERRIES) ? 1 : 0 : stack.is(Items.COCOA_BEANS) ? 2 : 0;
        if (add > 0) {
            if (e.stock >= MAX_DRINKS) return tell(p, "It's full to the brim: " + e.stock + " mugs of " + drink + ".");
            e.stock = Math.min(MAX_DRINKS, e.stock + add); take(stack, 1, creative); e.changed();
            level.playSound(null, pos, barrel ? SoundEvents.HONEY_BLOCK_SLIDE : SoundEvents.BREWING_STAND_BREW, SoundSource.BLOCKS, .8F, 1.1F);
            return tell(p, (barrel ? "Pressed into cider. " : "Brewing. ") + e.stock + " mug" + (e.stock == 1 ? "" : "s") + " of " + drink + " ready.");
        }
        if (stack.is(VillageItems.get("empty_coffee_mug"))) {
            if (e.stock <= 0) return tell(p, "It's run dry. Add " + (barrel ? "apples or berries" : "cocoa beans") + ", or wait for the tavern keeper.");
            e.stock--; e.changed();
            swap(p, stack, new ItemStack(VillageItems.get(barrel ? "mug_of_cider" : "steaming_coffee_mug")), creative);
            level.playSound(null, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, 1, barrel ? .9F : 1.2F);
            return tell(p, "You pour a mug of " + drink + ". " + e.stock + " left.");
        }
        if (!stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        return tell(p, e.stock + " mug" + (e.stock == 1 ? "" : "s") + " of " + drink + ". Bring an empty mug; " + (barrel ? "apples and berries make more cider." : "cocoa beans make more coffee."));
    }

    static boolean herb(ItemStack stack) { return stack.is(net.minecraft.tags.BlockItemTags.FLOWERS.item()) || HERBS.stream().anyMatch(stack::is); }
    private static InteractionResult press(ServerLevel level, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack, boolean creative) {
        if (herb(stack)) {
            if (e.stock >= MAX_HERBS) return tell(p, "The press is packed full of herbs. Bottle a tonic first.");
            e.stock++; e.changed();
            level.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, stack.getItem()), pos.getX() + .5, pos.getY() + .55, pos.getZ() + .5, 8, .15, .05, .15, .05);
            take(stack, 1, creative);
            level.playSound(null, pos, SoundEvents.HONEY_BLOCK_SLIDE, SoundSource.BLOCKS, .8F, 1.4F);
            return tell(p, "Pressed. Herbs: " + e.stock + "/" + MAX_HERBS + (e.stock >= HERBS_PER_TONIC ? ". Bring a glass bottle for a tonic." : "."));
        }
        if (stack.is(Items.GLASS_BOTTLE)) {
            if (e.stock < HERBS_PER_TONIC) return tell(p, "Press " + (HERBS_PER_TONIC - e.stock) + " more herb" + (HERBS_PER_TONIC - e.stock == 1 ? "" : "s") + " first: flowers, berries, ferns or kelp.");
            e.stock -= HERBS_PER_TONIC; e.changed();
            swap(p, stack, tonic(), creative);
            level.playSound(null, pos, SoundEvents.BOTTLE_FILL, SoundSource.BLOCKS, 1, 1);
            return tell(p, "You bottle an Herbal Tonic. Herbs left: " + e.stock + ".");
        }
        if (!stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        return tell(p, "Herbs: " + e.stock + "/" + MAX_HERBS + ". Press three flowers, berries, ferns or kelp, then bottle an Herbal Tonic.");
    }
    /** A gentle healing draught: a few seconds of regeneration. */
    public static ItemStack tonic() {
        var stack = new ItemStack(Items.POTION);
        stack.set(DataComponents.POTION_CONTENTS, new PotionContents(Optional.empty(), Optional.of(0x6DB36B),
                List.of(new MobEffectInstance(MobEffects.REGENERATION, 220, 0)), Optional.of("herbal_tonic")));
        stack.set(DataComponents.CUSTOM_NAME, Component.literal("Herbal Tonic").withStyle(s -> s.withItalic(false)));
        return stack;
    }

    /** The painting a dye makes when it finishes a sketch: blues paint the sea, greens the hills... */
    static int paintingFor(Item dye) {
        String id = net.minecraft.core.registries.BuiltInRegistries.ITEM.getKey(dye).getPath();
        int art = switch (id) {
            case "orange_dye", "yellow_dye" -> 0;           // sunset over the hills
            case "white_dye", "light_gray_dye", "cyan_dye" -> 1; // mountain lake
            case "black_dye", "gray_dye", "purple_dye" -> 2;  // the village at night
            case "red_dye", "pink_dye", "magenta_dye" -> 3;   // flowers in a vase
            case "brown_dye" -> 4;                            // portrait of a neighbor
            case "blue_dye", "light_blue_dye" -> 5;           // ship at sea
            default -> 6;                                     // a creeper in the meadow
        };
        return WorkstationBlock.FIRST_PAINTING + art;
    }
    private static InteractionResult easel(ServerLevel level, BlockState state, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack, boolean creative) {
        int art = state.getValue(WorkstationBlock.ART);
        boolean dye = stack.is(net.minecraft.tags.ItemTags.DYES);
        if (dye && art < WorkstationBlock.FIRST_PAINTING) {
            int next = art == 0 ? WorkstationBlock.SKETCH : paintingFor(stack.getItem());
            level.setBlock(pos, state.setValue(WorkstationBlock.ART, next), 3); take(stack, 1, creative);
            level.playSound(null, pos, SoundEvents.BRUSH_GENERIC, SoundSource.BLOCKS, 1, 1.2F);
            return tell(p, next == WorkstationBlock.SKETCH ? "You sketch the outline. One more dye to finish it." : "Finished! Take it down with an empty hand.");
        }
        if (stack.is(VillageItems.get("paintbrush")) && art >= WorkstationBlock.FIRST_PAINTING) {
            int next = WorkstationBlock.FIRST_PAINTING + (art - WorkstationBlock.FIRST_PAINTING + 1) % WorkstationBlock.PAINTINGS;
            level.setBlock(pos, state.setValue(WorkstationBlock.ART, next), 3);
            level.playSound(null, pos, SoundEvents.BRUSH_GENERIC, SoundSource.BLOCKS, 1, 1);
            return tell(p, "A few bold strokes, and it's a different picture.");
        }
        if (!stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        if (art >= WorkstationBlock.FIRST_PAINTING) {
            level.setBlock(pos, state.setValue(WorkstationBlock.ART, 0), 3); e.paint = 0; e.changed();
            give(p, new ItemStack(Items.PAINTING));
            level.playSound(null, pos, SoundEvents.PAINTING_PLACE, SoundSource.BLOCKS, 1, 1);
            return tell(p, "You take down the finished painting. Hang it somewhere nice.");
        }
        return tell(p, art == 0 ? "A fresh canvas. Paint it with dyes, or let the painter work on it." : "A sketch. Add any dye to finish the painting.");
    }

    private static InteractionResult music(ServerLevel level, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack) {
        long now = level.getGameTime();
        if (now < e.quietUntil) return tell(p, "Let the last song finish first.");
        var instrument = stack.is(VillageItems.get("lute")) ? SoundEvents.NOTE_BLOCK_GUITAR : stack.is(Items.BELL) || stack.is(Items.GOLD_INGOT) ? SoundEvents.NOTE_BLOCK_BELL
                : stack.is(Items.AMETHYST_SHARD) ? SoundEvents.NOTE_BLOCK_CHIME : stack.is(Items.BAMBOO) || stack.is(Items.SUGAR_CANE) ? SoundEvents.NOTE_BLOCK_FLUTE : SoundEvents.NOTE_BLOCK_HARP;
        var song = Songbook.SONGS.get((int) Math.floorMod(now / 20 + p.getUUID().hashCode(), Songbook.SONGS.size()));
        int length = perform(level, pos, song, instrument, true);
        e.quietUntil = now + length + 40; e.changed();
        return tell(p, "♪ You play \"" + song.title() + "\" and the neighbors cheer.");
    }
    /** Plays a song from the stand; everyone nearby feels livelier and the residents around enjoy it. */
    private static int perform(ServerLevel level, BlockPos pos, Songbook.Song song, Holder<SoundEvent> instrument, boolean inspire) {
        long now = level.getGameTime(); int t = 0;
        for (var note : song.notes()) { notes.add(new Note(level.dimension(), pos, now + t, instrument, Songbook.pitch(note[0]))); t += note[1]; }
        var area = new net.minecraft.world.phys.AABB(pos).inflate(12);
        for (var v : level.getEntitiesOfClass(Villager.class, area, v -> v.isAlive() && !v.isSleeping())) {
            VillageSocieties.emote(v, Emote.NOTE, 10 + v.getRandom().nextInt(30));
            if (v.getRandom().nextInt(3) == 0) level.broadcastEntityEvent(v, (byte) 14);
        }
        if (inspire) for (var player : level.getEntitiesOfClass(ServerPlayer.class, area, pl -> !pl.isSpectator()))
            player.addEffect(new MobEffectInstance(MobEffects.HASTE, 1200, 0, false, true));
        return t;
    }

    /** Items a tailor can mend with thread: leather, bows, rods, elytra and the like. */
    static boolean tailorable(ItemStack stack) {
        if (!stack.isDamageableItem()) return false;
        var repairable = stack.get(DataComponents.REPAIRABLE);
        if (repairable != null && (repairable.isValidRepairItem(new ItemStack(Items.LEATHER)) || repairable.isValidRepairItem(new ItemStack(Items.PHANTOM_MEMBRANE))
                || repairable.isValidRepairItem(new ItemStack(Items.STRING)))) return true;
        return stack.is(Items.BOW) || stack.is(Items.CROSSBOW) || stack.is(Items.FISHING_ROD) || stack.is(Items.CARROT_ON_A_STICK) || stack.is(Items.WARPED_FUNGUS_ON_A_STICK) || stack.is(Items.ELYTRA);
    }
    private static InteractionResult sew(ServerLevel level, BlockPos pos, ServerPlayer p, ItemStack stack, boolean creative) {
        if (stack.is(ItemTags.WOOL)) {
            take(stack, 1, creative); give(p, new ItemStack(Items.STRING, 3));
            level.playSound(null, pos, SoundEvents.SHEEP_SHEAR, SoundSource.BLOCKS, .8F, 1.2F);
            return tell(p, "You unravel the wool into three lengths of string.");
        }
        if (tailorable(stack)) {
            if (!stack.isDamaged()) return tell(p, "That's in fine shape already.");
            int step = Math.max(1, stack.getMaxDamage() / 4), used = 0;
            do {
                if (!creative && !useString(p)) break;
                stack.setDamageValue(Math.max(0, stack.getDamageValue() - step)); used++;
            } while (p.isShiftKeyDown() && stack.isDamaged());
            if (used == 0) return tell(p, "You need string to mend that. Wool unravels into string here.");
            level.playSound(null, pos, SoundEvents.WOOL_BREAK, SoundSource.BLOCKS, .8F, 1.4F);
            return tell(p, "Mended" + (stack.isDamaged() ? " a quarter" : "") + " with " + used + " string." + (stack.isDamaged() && !p.isShiftKeyDown() ? " Sneak to mend it all at once." : ""));
        }
        if (!stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        return tell(p, "Mend leather, bows, rods and elytra here with string. Wool unravels into string.");
    }
    private static boolean useString(ServerPlayer p) {
        var inventory = p.getInventory();
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            var s = inventory.getItem(i);
            if (s.is(Items.STRING)) { s.shrink(1); return true; }
        }
        return false;
    }

    /** What sawing one item yields: half again as many as the crafting grid gives. */
    static int sawn(int crafted) { return crafted + crafted / 2; }
    private static InteractionResult saw(ServerLevel level, BlockPos pos, ServerPlayer p, WorkstationBlockEntity e, ItemStack stack, boolean creative) {
        if (stack.isEmpty()) {
            if (e.stock > 0) {
                give(p, new ItemStack(Items.STICK, e.stock));
                String text = "You gather " + e.stock + " sticks from " + keeper(level, pos, "the carpenter") + "'s offcuts.";
                e.stock = 0; e.changed();
                return tell(p, text);
            }
            return tell(p, "Saw logs into half again as many planks, and planks into sticks. The carpenter leaves offcuts here.");
        }
        ItemStack result;
        if (stack.is(ItemTags.PLANKS)) result = new ItemStack(Items.STICK, 3);
        else {
            var input = CraftingInput.of(1, 1, List.of(stack.copyWithCount(1)));
            var recipe = level.recipeAccess().getRecipeFor(RecipeType.CRAFTING, input, level);
            if (recipe.isEmpty() || !(stack.is(ItemTags.LOGS) || stack.is(Items.BAMBOO_BLOCK) || stack.is(Items.STRIPPED_BAMBOO_BLOCK))) return InteractionResult.TRY_WITH_EMPTY_HAND;
            var crafted = recipe.get().value().assemble(input);
            result = crafted.copyWithCount(sawn(crafted.getCount()));
        }
        int times = p.isShiftKeyDown() ? stack.getCount() : 1;
        var particle = new ItemParticleOption(ParticleTypes.ITEM, stack.getItem());
        for (int i = 0; i < times; i++) give(p, result.copy());
        take(stack, times, creative);
        level.sendParticles(particle, pos.getX() + .5, pos.getY() + 1, pos.getZ() + .5, 12, .2, .1, .2, .05);
        level.playSound(null, pos, SoundEvents.AXE_STRIP.value(), SoundSource.BLOCKS, 1, .8F);
        level.playSound(null, pos, SoundEvents.UI_STONECUTTER_TAKE_RESULT, SoundSource.BLOCKS, .8F, 1);
        return tell(p, "Sawn into " + result.getCount() * times + " " + result.getHoverName().getString().toLowerCase(java.util.Locale.ROOT) + ".");
    }

    private static InteractionResult archives(ServerLevel level, BlockPos pos, ServerPlayer p, ItemStack stack, boolean creative) {
        var record = VillageSettlements.discover(level, pos);
        if (stack.is(Items.BOOK) || stack.is(Items.WRITABLE_BOOK)) {
            if (record == null) return tell(p, "These archives don't belong to any village yet.");
            var society = VillageSocieties.society(level, record.id());
            var pages = chronicle(record.name(), society, today(level));
            var book = new ItemStack(Items.WRITTEN_BOOK);
            book.set(DataComponents.WRITTEN_BOOK_CONTENT, new WrittenBookContent(Filterable.passThrough("Chronicle of " + record.name()), keeper(level, pos, "The Archives"), 0,
                    pages.stream().map(page -> Filterable.passThrough((Component) Component.literal(page))).toList(), true));
            swap(p, stack, book, creative);
            level.playSound(null, pos, SoundEvents.BOOK_PAGE_TURN, SoundSource.BLOCKS, 1, 1);
            return tell(p, "You copy out the Chronicle of " + record.name() + ".");
        }
        if (!stack.isEmpty()) return InteractionResult.TRY_WITH_EMPTY_HAND;
        level.playSound(null, pos, SoundEvents.BOOK_PAGE_TURN, SoundSource.BLOCKS, 1, .9F);
        VillageLedger.openAt(p, pos);
        return InteractionResult.SUCCESS_SERVER;
    }
    /** The village's story so far, a page at a time: its people, then its news from the beginning. */
    static List<String> chronicle(String village, dev.villagefriends.social.Society society, long today) {
        var pages = new ArrayList<String>();
        var page = new StringBuilder("THE CHRONICLE OF\n" + village.toUpperCase(java.util.Locale.ROOT) + "\n\nKept in the village archives, day " + (today + 1) + ".\n\n");
        if (society == null || society.everyone().isEmpty()) { page.append("No entries yet. Every village has to start somewhere."); pages.add(page.toString()); return pages; }
        page.append(society.living().size()).append(" residents call it home.");
        pages.add(page.toString());
        var news = new ArrayList<>(society.news());
        page = new StringBuilder();
        for (var n : news) {
            String line = "Day " + (n.day() + 1) + ": " + n.headline(society) + "\n\n";
            if (page.length() + line.length() > 230) { pages.add(page.toString()); page = new StringBuilder(); }
            page.append(line);
            if (pages.size() >= 40) break;
        }
        if (!page.isEmpty()) pages.add(page.toString());
        if (news.isEmpty()) pages.add("The village is quiet. The scholar is waiting for something worth writing down.");
        return pages;
    }

    // -- the training dummy and the archery target -------------------------------------------------

    /** Striking the dummy measures the hit instead of breaking it; sneak to pick it up. */
    public static InteractionResult attack(Player player, Level level, InteractionHand hand, BlockPos pos, Direction direction) {
        if (player.isSpectator() || player.isShiftKeyDown() || hand != InteractionHand.MAIN_HAND) return InteractionResult.PASS;
        if (!(level.getBlockState(pos).getBlock() instanceof WorkstationBlock b) || b.station() != Station.TRAINING_DUMMY) return InteractionResult.PASS;
        if (level.isClientSide() || !(player instanceof ServerPlayer p)) return InteractionResult.SUCCESS;
        long now = level.getGameTime();
        var previous = combos.get(p.getUUID());
        // Holding the button repeats the attack every tick; one swing counts once.
        if (previous != null && now - previous.last() < 6) return InteractionResult.SUCCESS;
        float charge = p.getAttackStrengthScale(.5F);
        float hit = (float) p.getAttributeValue(Attributes.ATTACK_DAMAGE) * (.2F + charge * charge * .8F);
        p.resetAttackStrengthTicker();
        var combo = previous != null && now - previous.last() <= 60 ? new Combo(now, previous.hits() + 1, previous.total() + hit) : new Combo(now, 1, hit);
        combos.put(p.getUUID(), combo);
        var server = (ServerLevel) level; boolean strong = charge > .9F;
        server.sendParticles(strong ? ParticleTypes.CRIT : ParticleTypes.DAMAGE_INDICATOR, pos.getX() + .5, pos.getY() + 1.1, pos.getZ() + .5, strong ? 10 : 3, .2, .2, .2, .1);
        server.playSound(null, pos, strong ? SoundEvents.PLAYER_ATTACK_STRONG : SoundEvents.PLAYER_ATTACK_WEAK, SoundSource.PLAYERS, 1, 1);
        server.playSound(null, pos, SoundEvents.ARMOR_STAND_HIT, SoundSource.BLOCKS, .8F, .9F + server.getRandom().nextFloat() * .2F);
        p.sendSystemMessage(Component.literal(String.format(java.util.Locale.ROOT, "%s %.1f damage", strong ? "Full swing!" : "Hit:", hit)
                + (combo.hits() > 1 ? String.format(java.util.Locale.ROOT, " · combo ×%d · %.1f total", combo.hits(), combo.total()) : "")), true);
        return InteractionResult.SUCCESS;
    }
    /** Rings from the bullseye out: 10, 8, 6, 4, 2, and 1 for clipping the edge. {@code u}, {@code v} are pixels from the center. */
    public static int targetScore(double u, double v) {
        double d = Math.sqrt(u * u + v * v);
        return d <= 1.2 ? 10 : d <= 2.6 ? 8 : d <= 4 ? 6 : d <= 5.4 ? 4 : d <= 6.8 ? 2 : 1;
    }
    /** The target face is centered at 8,9 (pixels) on the block's front. */
    public static void targetHit(Level level, BlockState state, BlockHitResult hit, Projectile projectile) {
        if (!(level instanceof ServerLevel server) || !(projectile instanceof AbstractArrow)) return;
        var facing = state.getValue(WorkstationBlock.FACING);
        if (hit.getDirection() != facing) return;
        var local = hit.getLocation().subtract(Vec3.atLowerCornerOf(hit.getBlockPos()));
        double across = switch (facing) { case NORTH -> 1 - local.x; case SOUTH -> local.x; case EAST -> 1 - local.z; default -> local.z; };
        int score = targetScore(across * 16 - 8, local.y * 16 - 9);
        var pos = hit.getBlockPos();
        server.sendParticles(score == 10 ? ParticleTypes.TOTEM_OF_UNDYING : ParticleTypes.CRIT, hit.getLocation().x, hit.getLocation().y, hit.getLocation().z, score == 10 ? 14 : 5, .1, .1, .1, .15);
        server.playSound(null, pos, score == 10 ? SoundEvents.ARROW_HIT_PLAYER : SoundEvents.WOOD_HIT, SoundSource.BLOCKS, 1, score == 10 ? 1.2F : 1);
        if (projectile.getOwner() instanceof ServerPlayer p)
            p.sendSystemMessage(Component.literal(score == 10 ? "Bullseye! 10 points" : score + (score == 1 ? " point" : " points") + (score >= 8 ? " - so close!" : "")), true);
    }

    // -- residents at work -------------------------------------------------------------------------

    /** A resident has just worked at their job site (vanilla calls this every half a minute or so while they're there). */
    public static void worked(ServerLevel level, Villager v) {
        var site = v.getBrain().getMemory(MemoryModuleType.JOB_SITE).filter(g -> g.dimension() == level.dimension()).map(GlobalPos::pos).orElse(null);
        if (site == null || !(level.getBlockState(site).getBlock() instanceof WorkstationBlock block)) return;
        if (!(level.getBlockEntity(site) instanceof WorkstationBlockEntity e)) return;
        keepers.put(GlobalPos.of(level.dimension(), site), firstName(name(v)));
        var state = level.getBlockState(site); long now = level.getGameTime(), today = today(level);
        double cx = site.getX() + .5, cy = site.getY() + .5, cz = site.getZ() + .5;
        switch (block.station()) {
            case TRAINING_DUMMY -> {
                v.swingForAttack(InteractionHand.MAIN_HAND);
                level.sendParticles(ParticleTypes.CRIT, cx, cy + .6, cz, 8, .2, .25, .2, .1);
                level.playSound(null, site, SoundEvents.ARMOR_STAND_HIT, SoundSource.BLOCKS, .9F, 1);
                train(v, 1.5, today);
            }
            case ARCHERY_TARGET -> { if (GuardController.isGuard(v)) practice(level, v, site, state); }
            case KITCHEN_STOVE -> {
                e.warmUntil = now + 2400;
                if (e.mealDay != today) { e.mealDay = today; e.served.clear(); }
                e.changed();
                level.sendParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE, cx, cy + .7, cz, 2, .1, .1, .1, .01);
            }
            case DRINKS_BARREL, TAP_STAND -> { if (e.stock < MAX_DRINKS) { e.stock = Math.min(MAX_DRINKS, e.stock + 4); e.changed(); } }
            case ALCHEMICAL_PRESS -> tend(level, v, site);
            case EASEL_CANVAS -> {
                int art = state.getValue(WorkstationBlock.ART);
                if (art >= WorkstationBlock.FIRST_PAINTING) break; // Finished, waiting for someone to take it home.
                e.paint += 20 + v.getRandom().nextInt(15);
                int next = e.paint >= 100 ? WorkstationBlock.FIRST_PAINTING + v.getRandom().nextInt(WorkstationBlock.PAINTINGS) : e.paint >= 30 ? WorkstationBlock.SKETCH : 0;
                if (next >= WorkstationBlock.FIRST_PAINTING) e.paint = 0;
                if (next != art) level.setBlock(site, state.setValue(WorkstationBlock.ART, next), 3);
                e.changed();
                level.playSound(null, site, SoundEvents.BRUSH_GENERIC, SoundSource.BLOCKS, .7F, 1.2F);
            }
            case MUSIC_STAND -> {
                if (now < e.quietUntil) break;
                var song = Songbook.SONGS.get(v.getRandom().nextInt(Songbook.SONGS.size()));
                e.quietUntil = now + perform(level, site, song, SoundEvents.NOTE_BLOCK_GUITAR, false) + 200; e.changed();
            }
            case SEWING_TABLE -> {
                for (var guard : level.getEntitiesOfClass(Villager.class, v.getBoundingBox().inflate(12), GuardController::isGuard))
                    for (var slot : List.of(EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET)) {
                        var armor = guard.getItemBySlot(slot);
                        if (armor.isDamaged()) armor.setDamageValue(Math.max(0, armor.getDamageValue() - Math.max(1, armor.getMaxDamage() / 10)));
                    }
                level.playSound(null, site, SoundEvents.WOOL_BREAK, SoundSource.BLOCKS, .6F, 1.5F);
            }
            case SAWMILL -> {
                if (e.stock < MAX_OFFCUTS) { e.stock = Math.min(MAX_OFFCUTS, e.stock + 2); e.changed(); }
                level.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, net.minecraft.world.level.block.Blocks.OAK_PLANKS.defaultBlockState()), cx, cy + .55, cz, 10, .2, .05, .2, .05);
                level.playSound(null, site, SoundEvents.AXE_STRIP.value(), SoundSource.BLOCKS, .8F, .7F);
            }
            case ARCHIVES -> {
                for (var player : level.getEntitiesOfClass(ServerPlayer.class, v.getBoundingBox().inflate(8), pl -> !pl.isSpectator())) {
                    var had = studied.get(player.getUUID());
                    double so = had == null || had.day() != today ? 0 : had.amount();
                    if (so >= STUDY_CAP) continue;
                    player.giveExperiencePoints(3); studied.put(player.getUUID(), new Daily(today, so + 3));
                    player.sendSystemMessage(Component.literal("You study the archives with " + firstName(name(v)) + ". (+3 experience)"), true);
                }
                level.playSound(null, site, SoundEvents.BOOK_PAGE_TURN, SoundSource.BLOCKS, .8F, 1);
            }
        }
    }
    private static String firstName(String name) { int space = name.indexOf(' '); return space > 0 ? name.substring(0, space) : name; }
    /** Practice earns a guard a little experience, up to a cap each day; real fights matter more. */
    private static void train(Villager v, double xp, long today) {
        if (!GuardController.isGuard(v)) return;
        var had = trained.get(v.getUUID());
        double so = had == null || had.day() != today ? 0 : had.amount();
        if (so >= TRAINING_CAP) return;
        GuardProgression.train(v, Math.min(xp, TRAINING_CAP - so));
        trained.put(v.getUUID(), new Daily(today, so + xp));
    }
    /** An archer looses a blunt practice arrow at their target. */
    private static void practice(ServerLevel level, Villager v, BlockPos site, BlockState state) {
        var facing = state.getValue(WorkstationBlock.FACING);
        var aim = Vec3.atCenterOf(site).add(facing.getStepX() * .45, .07, facing.getStepZ() * .45);
        var from = v.getEyePosition();
        if (from.distanceTo(aim) < 2.5 || !level.clip(new net.minecraft.world.level.ClipContext(from, aim, net.minecraft.world.level.ClipContext.Block.COLLIDER,
                net.minecraft.world.level.ClipContext.Fluid.NONE, v)).getBlockPos().equals(site)) {
            // Too close or something in the way: they just sight along the arrow instead.
            v.swingForAttack(InteractionHand.MAIN_HAND); train(v, 1, today(level)); return;
        }
        var arrow = new Arrow(level, v, new ItemStack(Items.ARROW), new ItemStack(Items.BOW));
        arrow.pickup = AbstractArrow.Pickup.DISALLOWED; arrow.setBaseDamage(0);
        target(arrow).setAttached(GUARD_ARROW_TARGET, "practice");
        var d = aim.subtract(arrow.position());
        arrow.shoot(d.x, d.y + Math.sqrt(d.x * d.x + d.z * d.z) * .06, d.z, 1.4F, 2);
        level.addFreshEntity(arrow);
        level.playSound(null, v.blockPosition(), SoundEvents.ARROW_SHOOT, SoundSource.NEUTRAL, .8F, 1);
        train(v, 1.5, today(level));
    }
    /** The apothecary looks after anyone hurt nearby: neighbors heal, visitors get a soothing salve. */
    private static void tend(ServerLevel level, Villager apothecary, BlockPos site) {
        for (var other : level.getEntitiesOfClass(Villager.class, apothecary.getBoundingBox().inflate(8), o -> o.isAlive() && o.getHealth() < o.getMaxHealth())) {
            other.heal(4);
            level.sendParticles(ParticleTypes.HEART, other.getX(), other.getY() + 2, other.getZ(), 1, .1, .1, .1, 0);
        }
        for (var player : level.getEntitiesOfClass(ServerPlayer.class, apothecary.getBoundingBox().inflate(6), p -> !p.isSpectator() && p.getHealth() < p.getMaxHealth() * .75F)) {
            player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 120, 0));
            player.sendSystemMessage(Component.literal(firstName(name(apothecary)) + " dabs a salve on your scrapes."), true);
        }
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER, site.getX() + .5, site.getY() + 1, site.getZ() + .5, 4, .2, .1, .2, 0);
        level.playSound(null, site, SoundEvents.BREWING_STAND_BREW, SoundSource.BLOCKS, .5F, 1.3F);
    }

    /** Plays out scheduled song notes. */
    public static void tick(MinecraftServer server) {
        if (notes.isEmpty()) return;
        var due = new ArrayList<Note>();
        for (var it = notes.iterator(); it.hasNext(); ) {
            var note = it.next(); var level = server.getLevel(note.level());
            if (level == null) { it.remove(); continue; }
            if (level.getGameTime() >= note.at()) { due.add(note); it.remove(); }
        }
        for (var note : due) {
            var level = server.getLevel(note.level());
            level.playSound(null, note.pos(), note.sound().value(), SoundSource.RECORDS, 1.4F, note.pitch());
            level.sendParticles(ParticleTypes.NOTE, note.pos().getX() + .5, note.pos().getY() + 1.4, note.pos().getZ() + .5, 0, note.pitch() / 2.0, 0, 0, 1);
        }
    }
    private Workstations() {}
}
