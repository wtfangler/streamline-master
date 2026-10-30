package dev.streamline.harness;

import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.gui.screens.GenericMessageScreen;
import net.minecraft.network.chat.Component;

/**
 * CI-only driver, never shipped: logs every screen the client passes through, takes screenshots of the
 * start-up overlay, the world loading screens, the world itself and the saving screen, then quits.
 */
public final class Harness {
    private static int total, waited, overlayShots, loadingShots, stage;
    private static String last = "";

    private Harness() { }

    private static void log(String text) { System.out.println("[SLM-HARNESS] " + text); }

    private static void shot(Minecraft mc, String name) {
        Screenshot.grab(mc.gameDirectory, name + ".png", mc.gameRenderer.mainRenderTarget(), 1, c -> log("saved " + name));
    }

    public static void tick(Minecraft mc) {
        if (stage == 99) return;
        if (++total > 12000) { log("ERROR timeout in state " + last); stage = 99; mc.stop(); return; }
        try {
            Object overlay = mc.gui.overlay(), screen = mc.gui.screen();
            String state = (overlay == null ? "" : "overlay " + overlay.getClass().getName() + " / ")
                    + "screen " + (screen == null ? "none" : screen.getClass().getName())
                    + (mc.level == null ? "" : " / in world");
            if (!state.equals(last)) { log("tick " + total + ": " + state); last = state; }
            if (overlay != null) {
                if (total % 8 == 0 && overlayShots < 3) shot(mc, "slm_1_startup_" + (++overlayShots));
                return;
            }
            if (mc.level == null || mc.player == null) {
                String name = screen == null ? "" : screen.getClass().getSimpleName();
                if (!name.equals("TitleScreen") && !name.isEmpty() && total % 4 == 0 && loadingShots < 4) {
                    shot(mc, "slm_2_world_" + (++loadingShots) + "_" + name);
                }
                return;
            }
            waited++;
            if (waited == 199) log("fps " + mc.getFps() + " (software rendering in CI, not a benchmark)");
            if (waited == 200) shot(mc, "slm_3_ingame");
            else if (waited == 220) mc.setScreenAndShow(new GenericMessageScreen(Component.translatable("menu.savingLevel")));
            else if (waited == 236) shot(mc, "slm_4_saving");
            else if (waited > 260) { log("finished"); stage = 99; mc.stop(); }
        } catch (Throwable t) {
            log("ERROR " + t);
            t.printStackTrace(System.out);
            stage = 99;
            mc.stop();
        }
    }
}
