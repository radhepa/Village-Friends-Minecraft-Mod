package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import org.junit.jupiter.api.Test;

class ResidentMotionTest {
    @Test void residentIdentityKeepsItsGaitAndCrowdsHaveVariety() {
        var random=new Random(76018);var gaits=EnumSet.noneOf(ResidentMotion.Gait.class);
        var phases=new HashSet<Float>();
        for(int n=0;n<1000;n++) {
            var id=new UUID(random.nextLong(),random.nextLong());
            int seed=ResidentMotion.seed(id);
            assertEquals(seed,ResidentMotion.seed(UUID.fromString(id.toString())));
            gaits.add(ResidentMotion.gait(seed));phases.add(ResidentMotion.phase(seed));
            assertTrue(ResidentMotion.variation(seed)>=.94F && ResidentMotion.variation(seed)<=1.06F);
        }
        assertEquals(6,gaits.size());assertTrue(phases.size()>800);
    }
    @Test void blinksAreShortSmoothAndNeighborsDoNotBlinkInUnison() {
        int[] seeds={ResidentMotion.seed(new UUID(10,20)),ResidentMotion.seed(new UUID(30,40)),ResidentMotion.seed(new UUID(50,60))};
        int closed=0,independent=0;float previous=ResidentMotion.blink(0,seeds[0]);
        for(int frame=0;frame<24000;frame++) {
            float age=frame*.025F,blink=ResidentMotion.blink(age,seeds[0]);
            assertTrue(Float.isFinite(blink) && blink>=0 && blink<=1);
            assertTrue(Math.abs(blink-previous)<.04F,"No abrupt eyelid jump between frames");
            if(blink>.05F)closed++;
            if(blink>.9F && ResidentMotion.blink(age,seeds[1])<.05F && ResidentMotion.blink(age,seeds[2])<.05F)independent++;
            previous=blink;
        }
        assertTrue(closed>100 && closed<1800,"Eyes spend most of their time open");
        assertTrue(independent>0,"Crowd members blink at individual moments");
    }
}
