package dev.villagefriends;

import dev.villagefriends.client.ArrivalBanner;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;

/** Walking into a village plays the large arrival title card; screenshots of all ten greetings. */
@SuppressWarnings("UnstableApiUsage")
public final class ArrivalGameTest implements FabricClientGameTest {
    private static void check(boolean ok, String why) { if (!ok) throw new AssertionError(why); }

    @Override public void runTest(ClientGameTestContext c) {
        try (var w = c.worldBuilder().create()) {
            w.getConnection().waitForChunksRender();
            w.getServer().runCommand("gamerule advance_time false"); w.getServer().runCommand("time set 6000");
            c.getInput().lookAt(30, 5);

            // The real path: a village is marked where the player stands and the server notices them arrive.
            w.getServer().runOnServer(s -> {
                var p = w.getConnection().getServerPlayer();
                VillageSettlements.mark(w.getConnection().getServerLevel(), p.blockPosition(), "Willowhaven");
            });
            c.waitFor(client -> "Willowhaven".equals(ArrivalBanner.showing()), 100);
            c.waitTicks(20);
            c.takeScreenshot("arrival-live");

            // Every greeting at full strength, then a long name and the fade.
            for (int v = 0; v < VillageArrival.VARIANTS; v++) {
                int variant = v;
                c.runOnClient(client -> ArrivalBanner.preview("Willowhaven", variant, 1800));
                c.waitTicks(2);
                c.takeScreenshot("arrival-" + v);
            }
            c.runOnClient(client -> ArrivalBanner.preview("Saint Aldric's Crossing upon the Thornmere Marshes", 1, 1800));
            c.waitTicks(2); c.takeScreenshot("arrival-long-name");
            c.runOnClient(client -> ArrivalBanner.preview("Briarbrook", 0, 250));
            c.waitTicks(1); c.takeScreenshot("arrival-fading-in");
            c.runOnClient(client -> ArrivalBanner.preview("Briarbrook", 0, 5200));
            c.waitTicks(1); c.takeScreenshot("arrival-fading-out");
            c.runOnClient(client -> ArrivalBanner.preview("Briarbrook", 0, 60_000));
            c.waitTicks(2);
            c.runOnClient(client -> check(ArrivalBanner.showing() == null, "The card clears itself when it has faded"));
        }
    }
}
