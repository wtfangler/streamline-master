package dev.streamline.loader.mixin;

import dev.streamline.loader.SlmLoader;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.LevelLoadingScreen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * World loading (joining a world, changing dimension): the same backdrop, with the bar following the
 * screen's own terrain progress. Vanilla's text and bar are skipped only when the backdrop was actually
 * drawn; the screen's logic (tracking, closing, narration) is untouched.
 */
@Mixin(LevelLoadingScreen.class)
public abstract class LevelLoadingScreenMixin {
    @Shadow private float smoothedProgress;

    @Inject(method = "extractRenderState", at = @At("HEAD"), cancellable = true)
    private void streamlineLoader$brand(GuiGraphicsExtractor g, int mouseX, int mouseY, float partial, CallbackInfo ci) {
        if (SlmLoader.draw(Minecraft.getInstance(), g, g.guiWidth(), g.guiHeight(), 1f, smoothedProgress)) ci.cancel();
    }
}
