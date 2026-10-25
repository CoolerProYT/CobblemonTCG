package com.coolerpromc.cobblemontcg.platform.util;

import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.world.entity.player.Player;

public record FabricServerPayloadContext(ServerPlayNetworking.Context context) implements PayloadContext {
    @Override
    public Player player() {
        return context.player();
    }

    @Override
    public void execute(Runnable runnable) {
        context.server().execute(runnable);
    }
}
