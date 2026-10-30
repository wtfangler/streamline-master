package dev.streamline.bench.mixin;

import dev.streamline.bench.SlmBench;
import net.minecraft.client.Minecraft;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Minecraft.class)
public abstract class MinecraftMixin {
    @Inject(method = "runTick(Z)V", at = @At("HEAD"))
    private void slmBench$frame(boolean advanceGameTime, CallbackInfo ci) {
        SlmBench.frame();
    }

    @Inject(method = "tick()V", at = @At("TAIL"))
    private void slmBench$tick(CallbackInfo ci) {
        SlmBench.tick((Minecraft) (Object) this);
    }
}
