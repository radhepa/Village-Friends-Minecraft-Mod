package dev.villagefriends.client;

import dev.villagefriends.fishing.Catches;
import dev.villagefriends.fishing.Fish;
import dev.villagefriends.fishing.FishTable;
import dev.villagefriends.fishing.FishingNet;
import dev.villagefriends.fishing.Minigame;
import dev.villagefriends.fishing.TrophyMount;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.renderer.RenderPipelines;
import net.fabricmc.fabric.api.client.rendering.v1.BlockEntityRendererRegistry;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;

/**
 * Tall Tales Fishing on the client: the catch-bar minigame beside the crosshair (it runs the same simulation the
 * server set up, {@link Minigame}, from the player holding the use button, and reports how it went), the contest
 * board in the corner of the screen, the angler's journal ({@link JournalScreen}) and the trophy mount's fish
 * ({@link TrophyMountRenderer}). Residents' rods and lines are drawn by {@link AnglingClient}.
 */
public final class FishingClient implements ClientModInitializer {
    private static final Identifier FRAME = id("fishing/minigame/frame"), ZONE = id("fishing/minigame/zone"), FISH = id("fishing/minigame/fish"),
            LEGEND = id("fishing/minigame/fish_legendary"), TREASURE = id("fishing/minigame/treasure");
    static final int FRAME_W = 40, FRAME_H = 152, TRACK_X = 6, TRACK_Y = 6, TRACK_W = 16, TRACK_H = 140, METER_X = 28, METER_W = 6;

    private static Minigame game;
    private static FishingNet.MinigameStart start;
    private static boolean reported, firstTime = true, untilReleased;
    private static int endedAt = -1, ticks;
    private static FishingNet.ContestBoard board = FishingNet.ContestBoard.HIDDEN;

    static Identifier id(String path) { return Identifier.fromNamespaceAndPath("villagefriends", path); }

    @Override public void onInitializeClient() {
        ClientPlayNetworking.registerGlobalReceiver(FishingNet.MinigameStart.TYPE, (payload, context) -> context.client().execute(() -> begin(payload)));
        ClientPlayNetworking.registerGlobalReceiver(FishingNet.MinigameEnd.TYPE, (payload, context) -> context.client().execute(FishingClient::stop));
        ClientPlayNetworking.registerGlobalReceiver(FishingNet.OpenJournal.TYPE, (payload, context) -> context.client().execute(() -> context.client().gui.setScreen(new JournalScreen())));
        ClientPlayNetworking.registerGlobalReceiver(FishingNet.ContestBoard.TYPE, (payload, context) -> context.client().execute(() -> board = payload));
        ClientTickEvents.END_CLIENT_TICK.register(FishingClient::tick);
        ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> client.execute(() -> { stop(); board = FishingNet.ContestBoard.HIDDEN; }));
        HudElementRegistry.attachElementAfter(VanillaHudElements.CROSSHAIR, id("fishing_minigame"), FishingClient::drawMinigame);
        HudElementRegistry.attachElementBefore(VanillaHudElements.CHAT, id("fishing_contest"), FishingClient::drawBoard);
        BlockEntityRendererRegistry.register(TrophyMount.TYPE, TrophyMountRenderer::new);
        AnglingClient.register();
    }

    /** For game tests: play the minigame like a decent player (allowing for the zone's momentum) instead of reading the use button. */
    public static boolean autoplay;
    /** The game in progress, or null (for game tests). */
    public static Minigame game() { return game; }

    /** True while the catch bar is up (and until the use button is let go after it): the use button doesn't use the rod. */
    public static boolean active() { return game != null || untilReleased; }

    static void begin(FishingNet.MinigameStart s) {
        start = s;
        game = new Minigame(s.seed(), Fish.Behavior.byId(s.behavior()), s.difficulty(), s.tuning());
        reported = false; endedAt = -1;
        var client = Minecraft.getInstance();
        client.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.NOTE_BLOCK_PLING.value(), s.legendary() ? .7F : 1.2F, .6F));
    }
    static void stop() { if (game != null) untilReleased = true; game = null; start = null; endedAt = -1; }

    private static void tick(Minecraft client) {
        ticks++;
        if (untilReleased && !client.options.keyUse.isDown()) untilReleased = false;
        if (game == null) return;
        if (client.player == null || client.isPaused()) return;
        if (!game.done()) {
            boolean holding = autoplay ? game.barPos() + game.zone() / 2 + game.barSpeed() * 6 > game.fishPos() + Minigame.FISH / 2
                    : client.options.keyUse.isDown() && client.gui.screen() == null;
            if (holding) firstTime = false;
            game.tick(holding);
            if (game.fishInZone() && ticks % 7 == 0)
                client.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.FISHING_BOBBER_RETRIEVE, 1.6F + game.progress() * .4F, .12F));
            return;
        }
        if (!reported) {
            reported = true; endedAt = ticks;
            ClientPlayNetworking.send(new FishingNet.MinigameResult(game.won(), game.won() && game.perfect(), game.treasureCaught()));
            client.getSoundManager().play(SimpleSoundInstance.forUI(game.won() ? SoundEvents.PLAYER_LEVELUP : SoundEvents.FISHING_BOBBER_SPLASH, game.won() ? 1.5F : .8F, .4F));
        }
        if (ticks - endedAt > 20) stop();
    }

    // -- the catch bar ----------------------------------------------------------------------------

    private static void drawMinigame(GuiGraphicsExtractor g, DeltaTracker delta) {
        if (game == null || start == null) return;
        var font = Minecraft.getInstance().font;
        float pt = delta.getGameTimeDeltaPartialTick(false);
        int x = Math.min(g.guiWidth() / 2 + 46, g.guiWidth() - FRAME_W - 4), y = Math.max(4, g.guiHeight() / 2 - FRAME_H / 2);
        float s = TRACK_H / Minigame.TRACK;
        g.blitSprite(RenderPipelines.GUI_TEXTURED, FRAME, x, y, FRAME_W, FRAME_H);
        int zoneY = y + TRACK_Y + Math.round(game.barPos(pt) * s), zoneH = Math.max(6, Math.round(game.zone() * s));
        g.blitSprite(RenderPipelines.GUI_TEXTURED, ZONE, x + TRACK_X, zoneY, TRACK_W, zoneH);
        if (game.treasureShown()) {
            int ty = y + TRACK_Y + Math.round(game.treasurePos() * s) - 6;
            g.blitSprite(RenderPipelines.GUI_TEXTURED, TREASURE, x + TRACK_X + 2, ty, 12, 12);
            int w = Math.round(12 * game.treasureProgress());
            if (w > 0) g.fill(x + TRACK_X + 2, ty + 13, x + TRACK_X + 2 + w, ty + 14, 0xFFF2C14E);
        }
        boolean in = game.fishInZone();
        int jitter = !game.done() && !in ? (ticks % 4 < 2 ? 1 : -1) : 0;
        int fy = y + TRACK_Y + Math.round((game.fishPos(pt) + Minigame.FISH / 2) * s) - 8;
        g.blitSprite(RenderPipelines.GUI_TEXTURED, start.legendary() ? LEGEND : FISH, x + TRACK_X + jitter, fy, 16, 16);
        float progress = game.progress(pt);
        int h = Math.round(TRACK_H * progress);
        g.fill(x + METER_X, y + TRACK_Y + TRACK_H - h, x + METER_X + METER_W, y + TRACK_Y + TRACK_H, meter(progress));
        String title = game.done() ? game.won() ? "Caught!" : "It got away!" : start.legendary() ? "Legendary!" : "Fish on!";
        int color = game.done() ? game.won() ? 0xFF7EE787 : 0xFFE0705C : start.legendary() ? 0xFFF2C14E : 0xFFF4E6C3;
        g.centeredText(font, title, x + FRAME_W / 2, y - 11, color);
        if (firstTime && !game.done()) g.centeredText(font, "Hold use to lift the bar", x + FRAME_W / 2, y + FRAME_H + 3, 0xFFD8C08A);
    }
    /** Red when nearly lost, through yellow, to green when nearly caught. */
    private static int meter(float p) {
        int r, gr;
        if (p < .5F) { r = 0xE0; gr = Math.round(0x40 + p * 2 * 0x9F); }
        else { r = Math.round(0xE0 - (p - .5F) * 2 * 0x90); gr = 0xDF; }
        return 0xFF000000 | r << 16 | gr << 8 | 0x48;
    }

    // -- the contest board ----------------------------------------------------------------------------

    private static void drawBoard(GuiGraphicsExtractor g, DeltaTracker delta) {
        var b = board;
        if (!b.show()) return;
        var font = Minecraft.getInstance().font;
        int w = 180, lines = Math.max(1, b.top().size()) + (b.place() > 5 ? 1 : 0);
        int x = g.guiWidth() - w - 4, y = 4, h = 26 + lines * 10 + 4;
        g.fill(x, y, x + w, y + h, 0x90101820);
        g.fill(x, y, x + w, y + 1, 0xFF6FA8C8);
        g.text(font, b.village(), x + 5, y + 4, 0xFFF4E6C3, false);
        g.text(font, b.status(), x + 5, y + 14, 0xFF9FC6D8, false);
        int ly = y + 26;
        if (b.top().isEmpty()) g.text(font, "No catches yet.", x + 5, ly, 0xFFB0B0B0, false);
        var self = Minecraft.getInstance().player == null ? "" : Minecraft.getInstance().player.getUUID().toString();
        for (int i = 0; i < b.top().size(); i++, ly += 10) {
            var e = b.top().get(i);
            Fish f = FishTable.get(e.fish());
            String line = (i + 1) + ". " + e.name() + " · " + (f == null ? e.fish() : f.name()) + " " + Catches.cm(e.size());
            g.text(font, font.plainSubstrByWidth(line, w - 10), x + 5, ly, e.key().equals(self) ? 0xFFF2C14E : i == 0 ? 0xFFFFFFFF : 0xFFD0D0D0, false);
        }
        if (b.place() > 5) g.text(font, font.plainSubstrByWidth("You: " + dev.villagefriends.fishing.Contest.ordinal(b.place()) + " · " + b.best(), w - 10), x + 5, ly, 0xFFF2C14E, false);
    }
}
