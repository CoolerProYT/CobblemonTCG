package com.coolerpromc.cobblemontcg.platform.util;

import net.minecraft.world.entity.player.Player;

public interface PayloadContext {
    Player player();
    void execute(Runnable runnable);
}
