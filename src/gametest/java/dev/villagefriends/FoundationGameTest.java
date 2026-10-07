package dev.villagefriends;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.gametest.v1.world.TestWorldSave;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.PoiTypeTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.village.poi.PoiTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;

@SuppressWarnings("UnstableApiUsage")
public final class FoundationGameTest implements FabricClientGameTest {
    private static void check(boolean ok,String reason) { if (!ok) throw new AssertionError(reason); }
    private static JsonObject resource(String path) {
        try (var stream=FoundationGameTest.class.getResourceAsStream("/"+path)) {
            if (stream==null) throw new AssertionError("Missing resource: "+path);
            return JsonParser.parseReader(new InputStreamReader(stream,StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (java.io.IOException e) { throw new AssertionError(e); }
    }
    private static ItemStack ingredient(JsonElement json) {
        if (json.isJsonObject()) {
            var potion=new ItemStack(Items.POTION);potion.set(DataComponents.POTION_CONTENTS,new PotionContents(Potions.AWKWARD));return potion;
        }
        String id=json.getAsString();
        if (id.equals("#minecraft:planks")) return new ItemStack(Items.OAK_PLANKS);
        if (id.equals("#minecraft:wool")) id="minecraft:white_wool";
        return new ItemStack(BuiltInRegistries.ITEM.getValue(Identifier.parse(id)));
    }
    private static CraftingInput input(JsonObject recipe) {
        var stacks=new ArrayList<ItemStack>();
        if (recipe.has("pattern")) {
            var pattern=recipe.getAsJsonArray("pattern");var key=recipe.getAsJsonObject("key");
            for (var line:pattern) for (char symbol:line.getAsString().toCharArray())
                stacks.add(symbol==' '?ItemStack.EMPTY:ingredient(key.get(String.valueOf(symbol))));
            return CraftingInput.of(pattern.get(0).getAsString().length(),pattern.size(),stacks);
        }
        for (var entry:recipe.getAsJsonArray("ingredients")) stacks.add(ingredient(entry));
        while (stacks.size()<9) stacks.add(ItemStack.EMPTY);
        return CraftingInput.of(3,3,stacks);
    }
    private static void blockEntityChecks(TestSingleplayerContext w, List<BlockPos> positions) {
        var level=w.getConnection().getServerLevel();
        String[] names={"house_plaque","notice_board","command_desk","apothecary_cot"};
        Class<?>[] types={HousePlaqueBlockEntity.class,NoticeBoardBlockEntity.class,CommandDeskBlockEntity.class,ApothecaryCotBlockEntity.class};
        for (int n=0;n<names.length;n++) {
            var entity=level.getBlockEntity(positions.get(n));
            check(types[n].isInstance(entity),"Placed/reloaded "+names[n]+" has its own block entity");
            check(entity.getType().isValid(level.getBlockState(positions.get(n))),"Block entity type recognizes its block");
        }
    }
    @Override public void runTest(ClientGameTestContext c) {
        c.getInput().resizeWindow(1400,900);c.runOnClient(client->{client.options.guiScale().set(2);client.resizeGui();});
        var catalog=resource("data/villagefriends/villagefriends/foundation-catalog.json");
        var residents=new ArrayList<UUID>();var entityPositions=new ArrayList<BlockPos>();TestWorldSave saved;
        try (var w=c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();w.getServer().runCommand("time set 2000");w.getServer().runCommand("gamemode creative @a");
            w.getServer().runOnServer(server->{
                var level=w.getConnection().getServerLevel();var player=w.getConnection().getServerPlayer();
                check(VillageProfessions.JOBS.size()==10&&VillageBlocks.all().size()==17&&VillageItems.all().size()==27,"Full registry includes the two guard spawn eggs and the Village Ledger");
                for (String job:VillageProfessions.JOBS) {
                    var profession=BuiltInRegistries.VILLAGER_PROFESSION.getOrThrow(VillageProfessions.key(job)).value();
                    for (String workstation:VillageProfessions.workstations(job)) for (var state:VillageBlocks.get(workstation).getStateDefinition().getPossibleStates()) {
                        var poi=PoiTypes.forState(state).orElseThrow();
                        check(poi.is(VillageProfessions.poiKey(job))&&poi.is(PoiTypeTags.ACQUIRABLE_JOB_SITE),"Every rotated job site maps to its profession and discovery tag");
                        check(profession.heldJobSite().test(poi)&&profession.acquirableJobSite().test(poi),"Held/acquirable job predicates agree");
                    }
                    for (int rank=1;rank<=5;rank++) {
                        var v=new Villager(EntityTypes.VILLAGER,level);v.setPos(player.position());
                        v.setVillagerData(v.getVillagerData().withProfession(BuiltInRegistries.VILLAGER_PROFESSION.getOrThrow(VillageProfessions.key(job))).withLevel(rank));
                        check(v.getOffers().size()==2,"Both native trade offers load for "+job+" level "+rank);
                        for (var offer:v.getOffers()) check(!offer.getResult().isEmpty(),"Trade produces a real registered item");
                    }
                }
                for (var block:List.of(Blocks.BARREL,Blocks.LOOM,Blocks.LECTERN))
                    check(PoiTypes.forState(block.defaultBlockState()).orElseThrow().unwrapKey().orElseThrow().identifier().getNamespace().equals("minecraft"),"Vanilla workstation ownership preserved");
                for (var entry:catalog.getAsJsonArray("recipes")) {
                    String name=entry.getAsString();var definition=resource("data/villagefriends/recipe/"+name+".json");
                    var recipe=(CraftingRecipe)server.getRecipeManager().byKey(ResourceKey.create(Registries.RECIPE,VillageBlocks.id(name))).orElseThrow(()->new AssertionError("Recipe did not load: "+name)).value();
                    var input=input(definition);check(recipe.matches(input,level),"Authored inputs craft "+name);
                    var result=recipe.assemble(input);check(result.is(BuiltInRegistries.ITEM.getValue(VillageBlocks.id(name)))&&result.getCount()==definition.getAsJsonObject("result").get("count").getAsInt(),"Correct craft result/count: "+name);
                    if (name.equals("revival_tonic")) {
                        var water=new ItemStack(Items.POTION);water.set(DataComponents.POTION_CONTENTS,new PotionContents(Potions.WATER));
                        check(!recipe.matches(CraftingInput.of(3,1,List.of(new ItemStack(Items.GOLDEN_APPLE),new ItemStack(Items.GLISTERING_MELON_SLICE),water)),level),"Revival Tonic rejects water potions");
                    }
                }
                int n=0;
                for (var entry:VillageBlocks.all().entrySet()) {
                    var pos=player.blockPosition().offset(n%9*2-8,0,5+n/9*3);n++;
                    level.setBlock(pos.below(),Blocks.OAK_PLANKS.defaultBlockState(),3);
                    var stack=new ItemStack(entry.getValue());player.setItemInHand(InteractionHand.MAIN_HAND,stack);
                    var context=new BlockPlaceContext(player,InteractionHand.MAIN_HAND,stack,new BlockHitResult(Vec3.atCenterOf(pos.below()),Direction.UP,pos.below(),false));
                    ((BlockItem)stack.getItem()).place(context);
                    check(level.getBlockState(pos).is(entry.getValue()),"Block item actually places "+entry.getKey());
                    var drops=Block.getDrops(level.getBlockState(pos),level,pos,level.getBlockEntity(pos));
                    check(drops.size()==1&&drops.get(0).is(entry.getValue().asItem()),"Breaking block returns its item: "+entry.getKey());
                    // Decorative fixture job sites must not compete with the acquisition check.
                    level.removeBlock(pos,false);
                }
                n=0;
                for (String name:List.of("house_plaque","notice_board","command_desk","apothecary_cot")) {
                    var pos=player.blockPosition().offset(n++*2-3,0,-3);entityPositions.add(pos);level.setBlock(pos,VillageBlocks.get(name).defaultBlockState(),3);
                }
                blockEntityChecks(w,entityPositions);
                ((HousePlaqueBlockEntity)level.getBlockEntity(entityPositions.get(0))).scanForBeds();
                ((NoticeBoardBlockEntity)level.getBlockEntity(entityPositions.get(1))).refreshNotices();
                ((CommandDeskBlockEntity)level.getBlockEntity(entityPositions.get(2))).updatePatrolAssignments();
                ((ApothecaryCotBlockEntity)level.getBlockEntity(entityPositions.get(3))).updatePatient();
                player.setItemInHand(InteractionHand.MAIN_HAND,ItemStack.EMPTY);
            });
            // Vanilla unemployed villagers may claim ANY nearby free job site. Offer one
            // site at a time, so this tests each new job without assuming candidate order.
            for (String job:VillageProfessions.JOBS) {
                UUID resident=w.getServer().computeOnServer(server->{
                    var level=w.getConnection().getServerLevel();var player=w.getConnection().getServerPlayer();
                    var pos=player.blockPosition().offset(0,0,16);
                    level.setBlock(pos,VillageBlocks.get(VillageProfessions.workstations(job).getFirst()).defaultBlockState(),3);
                    var v=new Villager(EntityTypes.VILLAGER,level);v.setPos(pos.getX()+.5,pos.getY(),pos.getZ()-2.5);v.setAge(0);
                    v.setItemSlot(EquipmentSlot.CHEST,new ItemStack(VillageItems.get(job+"_uniform")));
                    level.addFreshEntity(v);residents.add(v.getUUID());return v.getUUID();
                });
                boolean acquired=false;
                for (int attempt=0;attempt<60;attempt++) {
                    acquired=w.getServer().computeOnServer(server->{
                        var v=(Villager)w.getConnection().getServerLevel().getEntity(resident);
                        return v!=null&&VillageFriends.profession(v).equals(job);
                    });
                    if (acquired) break;
                    c.waitTicks(10);
                }
                check(acquired,"Unemployed resident naturally acquires "+job+" at its isolated workstation");
                w.getServer().runOnServer(server->{
                    var level=w.getConnection().getServerLevel();var player=w.getConnection().getServerPlayer();
                    var v=(Villager)level.getEntity(resident);
                    check(v.getOffers().size()==2,"Naturally acquired "+job+" can trade");v.setNoAi(true);
                    level.removeBlock(player.blockPosition().offset(0,0,16),false);
                    int n=residents.size()-1;v.setPos(player.getX()+(n%5-2)*2,player.getY(),player.getZ()+6+n/5*2);
                });
            }
            w.getServer().runCommand("gamemode survival @a");
            w.getServer().runOnServer(server->{
                var level=w.getConnection().getServerLevel();var p=w.getConnection().getServerPlayer();p.setHealth(10);
                var bread=new ItemStack(VillageItems.get("fresh_village_bread"));bread.finishUsingItem(level,p);check(p.getHealth()==12,"Village bread heals two health");
                var stew=new ItemStack(VillageItems.get("hearty_stew"));check(stew.finishUsingItem(level,p).is(Items.BOWL)&&p.getHealth()==18,"Stew heals and returns a bowl");
                var coffee=new ItemStack(VillageItems.get("steaming_coffee_mug"));check(coffee.finishUsingItem(level,p).is(VillageItems.get("empty_coffee_mug"))&&p.hasEffect(MobEffects.SPEED),"Coffee applies speed and returns its mug");
                p.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(VillageItems.get("rain_cloak")));p.getMainHandItem().use(level,p,InteractionHand.MAIN_HAND);
                check(p.getItemBySlot(EquipmentSlot.CHEST).is(VillageItems.get("rain_cloak")),"Rain cloak equips in the chest slot");
            });
            w.getServer().runCommand("gamemode creative @a");
            c.runOnClient(client->{
                var gallery=new ArrayList<ItemStack>();VillageBlocks.all().values().forEach(block->gallery.add(new ItemStack(block)));VillageItems.all().values().forEach(item->gallery.add(new ItemStack(item)));
                for (var stack:gallery) check(!stack.getHoverName().getString().startsWith("item.villagefriends.")&&!stack.getHoverName().getString().startsWith("block.villagefriends."),"Every item has a readable localized name");
                client.gui.setScreen(new FoundationPreviewScreen(gallery));
            });
            c.waitTicks(5);c.takeScreenshot("village-friends-phase1-content");c.runOnClient(client->client.gui.setScreen(null));
            saved=w.getWorldSave();
        }
        try (var w=saved.open()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runOnServer(server->{
                blockEntityChecks(w,entityPositions);
                for (int n=0;n<residents.size();n++) {
                    var v=(Villager)w.getConnection().getServerLevel().getEntity(residents.get(n));
                    check(v!=null&&VillageFriends.profession(v).equals(VillageProfessions.JOBS.get(n)),"New profession survives save/reload");
                    check(v.getOffers().size()==2&&v.getItemBySlot(EquipmentSlot.CHEST).is(VillageItems.get(VillageProfessions.JOBS.get(n)+"_uniform")),"Trades and uniform survive save/reload");
                }
            });
        }
        VillageFriends.LOGGER.info("FOUNDATION GAMEPLAY PASSED: 10 natural profession acquisitions, 17 block placements/loot, 27 items, 41 craft recipes, exact awkward potion ingredient, 100 trade offers, meals/coffee/equipment, rendered asset gallery and block entity/profession save/reload.");
    }
}
