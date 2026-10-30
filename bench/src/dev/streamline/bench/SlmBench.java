package dev.streamline.bench;

import java.io.IOException;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.Difficulty;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.LevelSettings;
import net.minecraft.world.level.WorldDataConfiguration;
import net.minecraft.world.level.levelgen.WorldOptions;
import net.minecraft.world.level.levelgen.presets.WorldPresets;

/**
 * A fixed, repeatable benchmark run, identical in any pack it is dropped into.
 *
 * Active only when the game directory holds slm-bench.txt (its first line is the label written into the
 * results, e.g. "SLM" or "FO"). It opens, or on first use creates, the world "SLM Benchmark" from a fixed
 * seed, puts the player in spectator mode at a fixed height above spawn, then:
 * warm-up 20 s, "static" 30 s looking at a fixed angle, "flight" 60 s along +X at 10 blocks/s (chunk
 * building, the scene that decides whether the game stutters). Frame times of each scene go to
 * slm-bench/&lt;label&gt;-&lt;time&gt;-&lt;scene&gt;.csv in the PresentMon column layout bench.py reads, and the game quits.
 */
public final class SlmBench {
    public static final String WORLD = "SLM Benchmark";
    private static final long SEED = 7_355_608L;
    private static final double HEIGHT = 130.0, SPEED = 0.5; // blocks per tick: 10 blocks/s
    private static final float YAW = -90f, PITCH = 20f;       // facing +X, slightly down
    private static final int WARMUP = 400, STATIC = 600, FLIGHT = 1200; // ticks

    private static Boolean active;
    private static String label = "pack";
    private static int stage, ticks;
    private static boolean opening;
    private static double x0, z0;
    private static FrameRecorder recorder;
    private static final String STAMP = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss"));

    private SlmBench() { }

    private static void log(String s) { System.out.println("[SLM-BENCH] " + s); }

    public static boolean active(Minecraft mc) {
        if (active == null) {
            Path marker = mc.gameDirectory.toPath().resolve("slm-bench.txt");
            active = Files.isRegularFile(marker);
            if (active) {
                try {
                    String first = Files.readAllLines(marker, StandardCharsets.UTF_8).stream().findFirst().orElse("").trim();
                    if (!first.isEmpty()) label = first.replaceAll("[^A-Za-z0-9._-]", "_");
                } catch (IOException ignored) { }
                log("active, label " + label);
            }
        }
        return active;
    }

    /** Called from Minecraft.runTick: one call per frame. */
    public static void frame() {
        if (recorder != null) recorder.frame(System.nanoTime());
    }

    private static void command(MinecraftServer server, String text) {
        server.execute(() -> server.getCommands().performPrefixedCommand(server.createCommandSourceStack(), text));
    }

    private static void tp(MinecraftServer server, double x, double z) {
        command(server, String.format(Locale.ROOT, "tp @p %.2f %.1f %.2f %.1f %.1f", x, HEIGHT, z, YAW, PITCH));
    }

    private static void open(Minecraft mc) {
        opening = true;
        var flows = mc.createWorldOpenFlows();
        if (mc.getLevelSource().levelExists(WORLD)) {
            log("opening " + WORLD);
            flows.openWorld(WORLD, () -> { log("ERROR world open cancelled"); mc.stop(); });
        } else {
            log("creating " + WORLD + " from seed " + SEED);
            LevelSettings settings = new LevelSettings(WORLD, GameType.CREATIVE,
                    new LevelSettings.DifficultySettings(Difficulty.PEACEFUL, false, false), true, WorldDataConfiguration.DEFAULT);
            flows.createFreshLevel(WORLD, settings, new WorldOptions(SEED, true, false),
                    WorldPresets::createNormalWorldDimensions, mc.gui.screen());
        }
    }

    public static void tick(Minecraft mc) {
        if (!active(mc) || stage == 99) return;
        try {
            if (mc.level == null || mc.player == null) {
                if (!opening && mc.gui.overlay() == null && mc.gui.screen() instanceof TitleScreen) open(mc);
                return;
            }
            if (mc.gui.screen() != null) return; // world still loading, or a menu is open
            MinecraftServer server = mc.getSingleplayerServer();
            if (server == null) return;
            ticks++;
            switch (stage) {
                case 0 -> {
                    x0 = Math.floor(mc.player.getX());
                    z0 = Math.floor(mc.player.getZ());
                    command(server, "gamemode spectator @p");
                    command(server, "time set 6000");
                    command(server, "weather clear 100000");
                    tp(server, x0, z0);
                    log(String.format(Locale.ROOT, "start at %.0f %.0f %.0f, warm-up %d s", x0, HEIGHT, z0, WARMUP / 20));
                    next();
                }
                case 1 -> { if (ticks >= WARMUP) { record(mc, "static"); next(); } }
                case 2 -> { if (ticks >= STATIC) { save(mc); record(mc, "flight"); next(); } }
                case 3 -> {
                    tp(server, x0 + ticks * SPEED, z0);
                    if (ticks >= FLIGHT) { save(mc); log("finished"); stage = 99; mc.stop(); }
                }
                default -> { }
            }
        } catch (Throwable t) {
            log("ERROR " + t);
            t.printStackTrace(System.out);
            stage = 99;
            mc.stop();
        }
    }

    private static void next() { stage++; ticks = 0; }

    private static void record(Minecraft mc, String scene) {
        recorder = new FrameRecorder(scene);
        log("recording " + scene);
    }

    private static void save(Minecraft mc) throws IOException {
        FrameRecorder r = recorder;
        recorder = null;
        if (r == null) return;
        Path dir = mc.gameDirectory.toPath().resolve("slm-bench");
        Files.createDirectories(dir);
        Path csv = dir.resolve(label + "-" + STAMP + "-" + r.scene + ".csv");
        try (Writer w = Files.newBufferedWriter(csv, StandardCharsets.UTF_8)) {
            w.write("Application,MsBetweenPresents\n");
            for (int i = 0; i < r.size; i++) w.write(String.format(Locale.ROOT, "minecraft,%.4f%n", r.times[i]));
        }
        log(String.format(Locale.ROOT, "%s: %d frames, avg %.1f FPS -> %s", r.scene, r.size, r.avgFps(), csv.getFileName()));
    }

    /** Frame-to-frame times in milliseconds, kept in a growing primitive array so recording allocates almost nothing. */
    static final class FrameRecorder {
        final String scene;
        double[] times = new double[8192];
        int size;
        long last = -1;

        FrameRecorder(String scene) { this.scene = scene; }

        void frame(long now) {
            if (last >= 0) {
                if (size == times.length) times = java.util.Arrays.copyOf(times, size * 2);
                times[size++] = (now - last) / 1_000_000.0;
            }
            last = now;
        }

        double avgFps() {
            double total = 0;
            for (int i = 0; i < size; i++) total += times[i];
            return total > 0 ? 1000.0 * size / total : 0;
        }
    }
}
