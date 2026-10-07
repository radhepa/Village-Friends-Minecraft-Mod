package dev.villagefriends;

import static dev.villagefriends.VillageFriends.*;
import dev.villagefriends.animation.AnimationClip;
import java.util.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.npc.villager.VillagerProfession;

/** Test helpers that cast residents with a chosen job, personality and age for animation scenes. */
final class AnimationCast {
    record Role(String job, String personality, boolean child) {}
    private static final List<String> VARIETY = List.of("farmer", "librarian", "cleric", "fisherman", "shepherd", "cartographer",
            "tavern_keeper", "tailor", "bard", "cook", "carpenter", "painter", "mason", "butcher");

    /** The resident a clip was written for: its first listed job, personality or age requirement. */
    static Role role(AnimationClip clip, int index) {
        String job = null, personality = null; boolean child = false;
        for (var group : clip.require()) {
            var options = new TreeSet<>(group);
            if (options.contains("child")) child = true;
            for (String tag : options) {
                if (tag.startsWith("job:") && job == null) job = tag.substring(4);
                if (tag.startsWith("personality:") && personality == null) personality = tag.substring(12);
            }
        }
        if (job == null && !child) job = VARIETY.get(index % VARIETY.size());
        return new Role(child ? "none" : job, personality, child);
    }

    static ResourceKey<VillagerProfession> key(String job) {
        if (VillageProfessions.JOBS.contains(job)) return VillageProfessions.key(job);
        return ResourceKey.create(Registries.VILLAGER_PROFESSION, Identifier.withDefaultNamespace(job));
    }

    /** A stable UUID whose generated profile has this personality (or any, when null). */
    static UUID identity(Random random, String personality) {
        while (true) {
            var id = new UUID(random.nextLong(), random.nextLong());
            if (personality == null || ResidentProfile.generate(id, "").personality().equals(personality)) return id;
        }
    }

    static Villager spawn(ServerLevel level, UUID id, Role role, double x, double y, double z, float yaw, boolean ai) {
        var v = new Villager(EntityTypes.VILLAGER, level);
        v.setUUID(id); v.setPos(x, y, z); v.setNoAi(!ai);
        v.setYRot(yaw); v.yBodyRot = v.yHeadRot = yaw; v.yBodyRotO = v.yHeadRotO = yaw; v.yRotO = yaw;
        v.setAge(role.child() ? -24000 : 0);
        target(v).setAttached(PROFILE, ResidentProfile.generate(id, ResidentAppearance.generate(id)));
        if (!role.child()) {
            v.setVillagerData(v.getVillagerData().withProfession(level.registryAccess(), key(role.job())));
            v.setVillagerXp(1);
        }
        level.addFreshEntity(v);
        return v;
    }
    private AnimationCast() {}
}
