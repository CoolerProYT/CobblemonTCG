package com.coolerpromc.cobblemontcg.reward;

import net.minecraft.server.level.ServerPlayer;

import java.util.Optional;

/**
 * What a reward trigger knows about the event that fired it. Fields a trigger does not know stay empty,
 * and conditions on empty fields fail.
 */
public record RewardContext(ServerPlayer player, Optional<Integer> level, Optional<String> species, Optional<Boolean> shiny) {
    public static RewardContext of(ServerPlayer player) {
        return new RewardContext(player, Optional.empty(), Optional.empty(), Optional.empty());
    }
}
