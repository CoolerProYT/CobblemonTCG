package com.coolerpromc.cobblemontcg.platform.util;

import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.handling.IPayloadContext;

public record NeoForgePayloadContext(IPayloadContext context) implements PayloadContext {
    @Override
    public Player player() {
        return context.player();
    }

    @Override
    public void execute(Runnable runnable) {
        context.enqueueWork(runnable);
    }
}
