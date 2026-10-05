package dev.villagefriends;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;

/** A settlement's stable origin is independent of its optional, movable marker. */
public record VillageRecord(String id, String name, int x, int y, int z, int radius, boolean marked, int mx, int my, int mz) {
    public static final Codec<VillageRecord> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("id").forGetter(VillageRecord::id), Codec.STRING.fieldOf("name").forGetter(VillageRecord::name),
            Codec.INT.fieldOf("x").forGetter(VillageRecord::x), Codec.INT.fieldOf("y").forGetter(VillageRecord::y), Codec.INT.fieldOf("z").forGetter(VillageRecord::z),
            Codec.intRange(32,512).fieldOf("radius").forGetter(VillageRecord::radius),
            Codec.BOOL.optionalFieldOf("marked",false).forGetter(VillageRecord::marked),
            Codec.INT.optionalFieldOf("mx",0).forGetter(VillageRecord::mx), Codec.INT.optionalFieldOf("my",0).forGetter(VillageRecord::my), Codec.INT.optionalFieldOf("mz",0).forGetter(VillageRecord::mz)
    ).apply(i,VillageRecord::new));
    public boolean contains(BlockPos pos) { return Math.abs((long)pos.getX()-x) <= radius && Math.abs((long)pos.getZ()-z) <= radius && Math.abs((long)pos.getY()-y) <= 80; }
    public long distance(BlockPos pos) { long dx=(long)pos.getX()-x,dz=(long)pos.getZ()-z; return dx*dx+dz*dz; }
    public VillageRecord marker(BlockPos pos, String newName) { return new VillageRecord(id,newName,x,y,z,radius,true,pos.getX(),pos.getY(),pos.getZ()); }
    public VillageRecord unmarked() { return new VillageRecord(id,name,x,y,z,radius,false,mx,my,mz); }
}
