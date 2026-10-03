package com.coolerpromc.cobblemontcg.platform.util;

import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.world.entity.player.Player;

public record FabricClientPayloadContext(ClientPlayNetworking.Context context) implements PayloadContext {
    @Override
    public Player player() {
        return context.player();
    }

    @Override
    public void execute(Runnable runnable) {
        context.client().execute(runnable);
    }
}
