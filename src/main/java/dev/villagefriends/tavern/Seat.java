package dev.villagefriends.tavern;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.npc.villager.Villager;
import net.minecraft.world.entity.vehicle.DismountHelper;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;

/**
 * An invisible seat on a chair, stool or bench. Whoever sits rides it, so vanilla handles the sitting pose,
 * keeps them from being pushed around and saves them with it. It sits at the seat's surface and faces the
 * way the chair does; it goes away as soon as nobody is on it or the chair is gone, and it stands a resident
 * up who is hurt, frightened, knocked out or has somewhere else to be.
 */
public final class Seat extends Entity {
    /** How far toward the front edge of the seat a sitter perches, in blocks. */
    public static final double FORWARD = .15;
    public Seat(EntityType<? extends Seat> type, Level level) {
        super(type, level);
        noPhysics = true;
    }

    /** Sits someone down on the seat at {@code pos}, facing {@code yaw}; false if it's taken. */
    public static boolean sit(LivingEntity who, BlockPos pos, double surface, float yaw) {
        var level = who.level();
        if (occupied(level, pos)) return false;
        var seat = new Seat(Taverns.SEAT, level);
        var forward = Vec3.directionFromRotation(0, yaw);
        seat.setPos(pos.getX() + .5 + forward.x * FORWARD, pos.getY() + surface, pos.getZ() + .5 + forward.z * FORWARD);
        seat.setYRot(yaw); seat.yRotO = yaw;
        if (!level.addFreshEntity(seat)) return false;
        if (!who.startRiding(seat, true, true)) { seat.discard(); return false; }
        who.setYRot(yaw); who.setYHeadRot(yaw); who.setYBodyRot(yaw);
        return true;
    }
    public static boolean occupied(Level level, BlockPos pos) {
        return !level.getEntitiesOfClass(Seat.class, new net.minecraft.world.phys.AABB(pos), s -> s.isVehicle()).isEmpty();
    }
    /** Whether this resident (or player) is sitting on a seat. */
    public static boolean seated(Entity e) { return e.getVehicle() instanceof Seat; }
    public BlockPos seatPos() { return BlockPos.containing(getX(), getY() - .01, getZ()); }

    @Override public void tick() {
        super.tick();
        if (!(level() instanceof ServerLevel level)) return;
        if (!isVehicle() || !Taverns.seat(level, seatPos())) { ejectPassengers(); discard(); return; }
        if (getFirstPassenger() instanceof Villager v && !Taverns.mayStaySeated(v)) v.stopRiding();
    }

    // Sitters' thighs rest on the surface, so their feet go a third of their height below it.
    @Override protected void positionRider(Entity passenger, MoveFunction move) {
        move.accept(passenger, getX(), getY() - depth(passenger), getZ());
        if (passenger instanceof LivingEntity living) {
            living.setYBodyRot(getYRot());
            clamp(living);
        }
    }
    public static double depth(Entity passenger) { return passenger.getBbHeight() * .32; }
    /** Sitters can look around, but their body stays square to the table. */
    @Override public void onPassengerTurned(Entity passenger) { clamp(passenger); }
    private void clamp(Entity passenger) {
        float yaw = getYRot();
        float y = Mth.wrapDegrees(passenger.getYRot() - yaw), head = Mth.wrapDegrees(passenger.getYHeadRot() - yaw);
        float clamped = Mth.clamp(y, -100, 100), headClamped = Mth.clamp(head, -100, 100);
        if (clamped != y) { passenger.setYRot(yaw + clamped); passenger.yRotO = passenger.getYRot(); }
        if (headClamped != head) passenger.setYHeadRot(yaw + headClamped);
    }
    /** Step out to the side or back of the chair, never onto the table. */
    @Override public Vec3 getDismountLocationForPassenger(LivingEntity passenger) {
        var pos = seatPos();
        var front = Direction.fromYRot(getYRot());
        for (var side : new Direction[]{front.getClockWise(), front.getCounterClockWise(), front.getOpposite(), front}) {
            var found = DismountHelper.findSafeDismountLocation(passenger.getType(), level(), pos.relative(side), true);
            if (found != null) return found;
        }
        return super.getDismountLocationForPassenger(passenger);
    }
    @Override protected boolean canAddPassenger(Entity passenger) { return getPassengers().isEmpty(); }
    @Override protected void defineSynchedData(SynchedEntityData.Builder builder) {}
    @Override protected void readAdditionalSaveData(ValueInput input) {}
    @Override protected void addAdditionalSaveData(ValueOutput output) {}
    @Override public boolean hurtServer(ServerLevel level, DamageSource source, float amount) { return false; }
    @Override public boolean isPickable() { return false; }
    @Override public boolean isPushable() { return false; }
    @Override public boolean canBeCollidedWith(Entity other) { return false; }
}
