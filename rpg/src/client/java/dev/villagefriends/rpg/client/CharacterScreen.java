package dev.villagefriends.rpg.client;

import dev.villagefriends.rpg.Attr;
import dev.villagefriends.rpg.Balance;
import dev.villagefriends.rpg.Bestiary;
import dev.villagefriends.rpg.Life;
import dev.villagefriends.rpg.Rpg;
import dev.villagefriends.rpg.RpgActionPayload;
import dev.villagefriends.rpg.Sheet;
import dev.villagefriends.rpg.Skill;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.Level;

import java.util.ArrayList;
import java.util.List;

/** The character sheet (K): overview, attributes, skills, bestiary and jobs. Reads the synced sheet live. */
public final class CharacterScreen extends Screen {
    private static final String[] TABS = {"Overview", "Attributes", "Skills", "Bestiary", "Jobs"};
    private static final int BG = 0xEE16110C, EDGE = 0xFFC9A75E, INK = 0xFFF4E6C3, DIM = 0xFF9C8B6A, GOOD = 0xFF7FD36B,
            GOLD = 0xFFE0B04A, PURPLE = 0xFFC28BF0, BAR = 0xFF3A2E1E;
    private static int tab;
    private int x0, y0, w, h, scroll;
    private Sheet seen;

    public CharacterScreen() { super(Component.literal("Character")); }
    private Sheet sheet() { return minecraft == null || minecraft.player == null ? Sheet.NEW : Rpg.sheet(minecraft.player); }

    @Override protected void init() {
        w = Math.min(width - 16, 410); h = Math.min(height - 16, 240); x0 = (width - w) / 2; y0 = (height - h) / 2;
        seen = sheet();
        int tw = (w - 12) / TABS.length;
        for (int i = 0; i < TABS.length; i++) {
            int t = i;
            var b = addRenderableWidget(Button.builder(Component.literal(TABS[i]), p -> { tab = t; scroll = 0; rebuildWidgets(); }).bounds(x0 + 6 + i * tw, y0 + 6, tw - 2, 16).build());
            b.active = tab != i;
        }
        var s = seen;
        if (tab == 1) {
            for (int i = 0; i < Attr.values().length; i++) {
                var a = Attr.values()[i];
                var b = addRenderableWidget(Button.builder(Component.literal("+"), p -> send("spend", a.id())).bounds(x0 + w - 24, row(i) - 2, 16, 12).build());
                b.active = s.points() > 0 && s.attr(a) < Balance.ATTR_CAP;
            }
            int cost = Life.respecCost(s.level());
            var r = addRenderableWidget(Button.builder(Component.literal("Unlearn"), p -> send("respec", "")).bounds(x0 + w - 70, y0 + 27, 62, 14).build());
            r.active = s.spentPoints() > 0;
            r.setTooltip(Tooltip.create(Component.literal("Refund every attribute point for " + cost + " emeralds.")));
        }
        if (tab == 4) {
            for (int i = 0; i < s.quests().size(); i++) {
                var q = s.quests().get(i);
                addRenderableWidget(Button.builder(Component.literal("Abandon"), p -> send("abandon", q.id())).bounds(x0 + w - 62, y0 + 36 + i * 38, 54, 14).build());
            }
        }
    }
    private int row(int i) { return y0 + 46 + i * 18; }
    private void send(String action, String arg) { if (ClientPlayNetworking.canSend(RpgActionPayload.TYPE)) ClientPlayNetworking.send(new RpgActionPayload(action, arg)); }

    @Override public void tick() { if (sheet() != seen) rebuildWidgets(); }
    @Override public boolean isPauseScreen() { return false; }
    @Override public boolean mouseScrolled(double mx, double my, double sx, double sy) {
        if (tab == 3) { scroll = Math.clamp(scroll - (int) Math.signum(sy), 0, Math.max(0, Bestiary.FAMILIES.size() - bestiaryRows())); return true; }
        return super.mouseScrolled(mx, my, sx, sy);
    }
    private int bestiaryRows() { return Math.max(1, (h - 44) / 24); }

    @Override public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        g.fill(0, 0, width, height, 0x88000000);
        g.fill(x0, y0, x0 + w, y0 + h, BG);
        g.outline(x0, y0, w, h, EDGE);
    }
    @Override public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float delta) {
        super.extractRenderState(g, mouseX, mouseY, delta);
        var s = sheet();
        switch (tab) {
            case 0 -> overview(g, s);
            case 1 -> attributes(g, s, mouseX, mouseY);
            case 2 -> skills(g, s, mouseX, mouseY);
            case 3 -> bestiary(g, s, mouseX, mouseY);
            default -> jobs(g, s);
        }
    }

    private void overview(GuiGraphicsExtractor g, Sheet s) {
        int x = x0 + 10, y = y0 + 30;
        g.text(font, "Level " + s.level() + "  " + Balance.title(s.level()), x, y, GOLD, true);
        boolean max = s.level() >= Balance.MAX_LEVEL;
        bar(g, x, y + 12, 170, max ? 1 : s.xp() / (double) Balance.need(s.level()), GOLD);
        g.text(font, max ? "Max level" : s.xp() + " / " + Balance.need(s.level()) + " XP", x, y + 18, DIM, false);
        g.text(font, "Unspent points: " + s.points(), x, y + 32, s.points() > 0 ? GOOD : INK, false);
        g.text(font, "Jobs done: " + s.mark("quests_done") + "   Active: " + s.quests().size() + "/" + Balance.maxQuests(s.level()), x, y + 44, INK, false);
        int legends = s.masteries(), tiers = 0;
        for (var f : Bestiary.FAMILIES) tiers += s.tier(f);
        g.text(font, "Bestiary: " + tiers + "/" + Bestiary.FAMILIES.size() * 5 + " tiers, " + legends + " Legend", x, y + 56, INK, false);
        int skills = 0; for (var sk : Skill.values()) skills += s.skill(sk);
        g.text(font, "Skill levels: " + skills + "/" + Skill.values().length * Balance.SKILL_CAP, x, y + 68, INK, false);
        String next = s.level() < 10 ? "Reach level 10 to be called an Adventurer." : s.level() < 30 ? "Level 30 lets you take a 4th job." : s.level() < 60 ? "Level 60 lets you take a 5th job." : "The road goes ever on.";
        wrap(g, next, x, y + 86, 170, DIM);

        // Derived numbers, worked out the same way the server does.
        var p = minecraft.player; int rx = x0 + w / 2 + 6, ry = y0 + 30;
        boolean nether = p.level().dimension() == Level.NETHER;
        double melee = Balance.meleeBase(s.level()) + Balance.STR_MELEE * s.attr(Attr.STRENGTH);
        double proj = 1 + Balance.PRE_PROJECTILE * s.attr(Attr.PRECISION) + Balance.ARCHERY_DAMAGE * s.skill(Skill.ARCHERY) + s.perk("damage", "projectile");
        double hunger = Math.max(Balance.MIN_HUNGER, Balance.hungerRate(s.level()) * (1 - Balance.END_HUNGER * s.attr(Attr.ENDURANCE)));
        int rec = Balance.recoveryInterval(s.attr(Attr.RECOVERY));
        String[][] rows = {
                {"Max health", fmt(p.getMaxHealth()) + " (" + fmt(p.getMaxHealth() / 2) + " hearts)"},
                {"Melee damage", "x" + fmt(melee) + " (swords +" + pct(Balance.SWORD_DAMAGE * s.skill(Skill.SWORDS)) + ", axes +" + pct(Balance.AXE_DAMAGE * s.skill(Skill.AXES)) + ")"},
                {"Projectile damage", "x" + fmt(proj)},
                {"Critical strike", pct(Balance.PRE_CRIT * s.attr(Attr.PRECISION)) + " for +50%"},
                {"Attack speed", "+" + pct(Balance.DEX_SPEED * s.attr(Attr.DEXTERITY))},
                {"Bonus armor", "+" + fmt(Balance.TOU_ARMOR * s.attr(Attr.TOUGHNESS)) + " / +" + fmt(Balance.TOU_TOUGHNESS * s.attr(Attr.TOUGHNESS) + Balance.DEFENSE_TOUGHNESS * s.skill(Skill.DEFENSE)) + " tough"},
                {"Move speed", "+" + pct(Balance.AGI_SPEED * s.attr(Attr.AGILITY) + Balance.ATHLETICS_SPEED * s.skill(Skill.ATHLETICS))},
                {"Hunger drain", "x" + fmt(hunger)},
                {"Mining speed", "x" + fmt(Balance.mineBase(s.level()) + s.perk("mine", "")) + " before tool skills"},
                {"Experience", "+" + pct(Balance.WIS_XP * s.attr(Attr.WISDOM))},
                {"Bonus loot", pct(Balance.LUCK_LOOT * s.attr(Attr.LUCK))},
                {"Recovery", rec == 0 ? "none" : "half a heart every " + fmt(rec / 20.0) + "s"},
                {"Nether bonus", nether ? "+" + pct(s.perk("damage", "nether")) : "-"}};
        for (int i = 0; i < rows.length; i++) {
            g.text(font, rows[i][0], rx, ry + i * 11, DIM, false);
            g.text(font, font.plainSubstrByWidth(rows[i][1], x0 + w - rx - 90), rx + 86, ry + i * 11, INK, false);
        }
    }

    private void attributes(GuiGraphicsExtractor g, Sheet s, int mx, int my) {
        g.text(font, "Points to spend: " + s.points(), x0 + 10, y0 + 30, s.points() > 0 ? GOOD : INK, true);
        for (int i = 0; i < Attr.values().length; i++) {
            var a = Attr.values()[i]; int y = row(i), v = s.attr(a);
            g.text(font, a.label, x0 + 10, y, INK, false);
            bar(g, x0 + 80, y + 2, 70, v / (double) Balance.ATTR_CAP, v >= Balance.ATTR_CAP ? GOLD : GOOD);
            g.text(font, v + "/" + Balance.ATTR_CAP, x0 + 156, y, v > 0 ? INK : DIM, false);
            g.text(font, font.plainSubstrByWidth(a.perPoint + " per point", w - 220), x0 + 192, y, DIM, false);
        }
    }

    private void skills(GuiGraphicsExtractor g, Sheet s, int mx, int my) {
        int y0s = y0 + 30, rowH = Math.max(12, Math.min(14, (h - 36) / Skill.values().length));
        for (int i = 0; i < Skill.values().length; i++) {
            var sk = Skill.values()[i]; int y = y0s + i * rowH, lv = s.skill(sk);
            var prog = Balance.skillProgress(s.skillXp(sk));
            g.text(font, sk.label, x0 + 10, y, INK, false);
            g.text(font, String.valueOf(lv), x0 + 98, y, lv >= Balance.SKILL_CAP ? GOLD : INK, false);
            bar(g, x0 + 114, y + 3, 50, prog[0] / (double) prog[1], lv >= Balance.SKILL_CAP ? GOLD : 0xFF6FB7E0);
            g.text(font, font.plainSubstrByWidth(lv == 0 ? sk.howToTrain : sk.effect(lv), w - 182), x0 + 172, y, lv == 0 ? DIM : INK, false);
            if (mx >= x0 + 8 && mx < x0 + w - 8 && my >= y - 1 && my < y + rowH - 1)
                g.setTooltipForNextFrame(Component.literal(sk.label + " " + lv + "/" + Balance.SKILL_CAP + "\nTrain: " + sk.howToTrain
                        + "\nNow: " + sk.effect(lv) + (lv < Balance.SKILL_CAP ? "\nNext level: " + prog[0] + "/" + prog[1] : "")), mx, my);
        }
    }

    private void bestiary(GuiGraphicsExtractor g, Sheet s, int mx, int my) {
        int rows = bestiaryRows(), y = y0 + 30;
        for (int i = scroll; i < Math.min(Bestiary.FAMILIES.size(), scroll + rows); i++, y += 24) {
            var f = Bestiary.FAMILIES.get(i); int k = s.kills(f.id()), t = f.tier(k), next = f.next(k);
            g.text(font, f.label(), x0 + 10, y, t >= 5 ? GOLD : t > 0 ? INK : DIM, false);
            g.text(font, Balance.tierName(t) + " - " + k + " kills" + (next > 0 ? ", next at " + next : ""), x0 + 130, y, t > 0 ? PURPLE : DIM, false);
            var perks = new ArrayList<String>();
            for (var p : f.perks()) perks.add((t >= p.tier() ? "" : "[" + Balance.tierName(p.tier()) + "] ") + p.name());
            g.text(font, font.plainSubstrByWidth("+" + 2 * t + "% dmg, -" + 2 * t + "% taken  |  " + String.join(", ", perks), w - 24), x0 + 14, y + 10, t >= 3 ? GOOD : DIM, false);
            if (mx >= x0 + 8 && mx < x0 + w - 8 && my >= y - 1 && my < y + 22) {
                var lines = new ArrayList<String>(List.of(f.label() + " (" + f.rarity().name().toLowerCase() + ")", "Tiers at " + join(f.rarity().tiers) + " kills"));
                for (var p : f.perks()) lines.add((t >= p.tier() ? "Unlocked " : "At " + Balance.tierName(p.tier()) + ": ") + p.name() + " - " + p.desc());
                g.setTooltipForNextFrame(Component.literal(String.join("\n", lines)), mx, my);
            }
        }
        g.text(font, (scroll + 1) + "-" + Math.min(Bestiary.FAMILIES.size(), scroll + rows) + " of " + Bestiary.FAMILIES.size() + " (scroll)", x0 + w - 110, y0 + h - 12, DIM, false);
    }

    private void jobs(GuiGraphicsExtractor g, Sheet s) {
        if (s.quests().isEmpty()) {
            wrap(g, "No jobs yet. Talk to a villager with a trade (farmers, smiths, guards, clerics, librarians, fishermen and more) and ask \"Any work for me?\". "
                    + "Each villager has one job a day. Jobs pay experience, emeralds and friendship.", x0 + 10, y0 + 34, w - 20, DIM);
            return;
        }
        for (int i = 0; i < s.quests().size(); i++) {
            var q = s.quests().get(i); int y = y0 + 34 + i * 38;
            g.text(font, q.label() + "  (" + q.have() + "/" + q.need() + ")", x0 + 10, y, q.done() ? GOOD : INK, false);
            bar(g, x0 + 10, y + 11, 120, q.have() / (double) q.need(), q.done() ? GOOD : GOLD);
            g.text(font, q.done() ? "Ready! Return to " + q.giverName() : "For " + q.giverName() + (q.job().isEmpty() ? "" : ", " + q.job().replace('_', ' ')), x0 + 136, y + 9, q.done() ? GOOD : DIM, false);
            g.text(font, "Reward: " + q.xp() + " XP, " + q.emeralds() + " emeralds, +" + q.friendship() + " friendship (before Bartering)", x0 + 10, y + 20, DIM, false);
        }
    }

    // -- helpers -----------------------------------------------------------------------------------
    private void bar(GuiGraphicsExtractor g, int x, int y, int width, double f, int color) {
        g.fill(x, y, x + width, y + 4, BAR);
        g.fill(x, y, x + (int) Math.round(width * Math.clamp(f, 0, 1)), y + 4, color);
    }
    private void wrap(GuiGraphicsExtractor g, String text, int x, int y, int width, int color) {
        for (var line : font.split(Component.literal(text), width)) { g.text(font, line, x, y, color, false); y += 10; }
    }
    private static String fmt(double v) { return v == Math.rint(v) ? String.valueOf((long) v) : String.valueOf(Math.round(v * 100) / 100.0); }
    private static String pct(double v) { return Math.round(v * 1000) / 10.0 + "%"; }
    private static String join(int[] a) { var out = new StringBuilder(); for (int v : a) out.append(out.isEmpty() ? "" : "/").append(v); return out.toString(); }
}
