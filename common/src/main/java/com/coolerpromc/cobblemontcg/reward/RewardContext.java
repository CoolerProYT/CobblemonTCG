package com.coolerpromc.cobblemontcg.reward;

import net.minecraft.server.level.ServerPlayer;

import java.util.Optional;

public record RewardContext(ServerPlayer player, Optional<Integer> level, Optional<String> species, Optional<Boolean> shiny,
                            Optional<Boolean> firstCatch, Optional<Integer> dexEntries, Optional<Integer> dexTotal,
                            Optional<Integer> previousLevel) {
    public static RewardContext of(ServerPlayer player) {
        return new RewardContext(player, Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty(), Optional.empty());
    }

    public static RewardContext capture(ServerPlayer player, String species, int level, boolean shiny, boolean firstCatch) {
        return new RewardContext(player, Optional.of(level), Optional.of(species), Optional.of(shiny), Optional.of(firstCatch), Optional.empty(), Optional.empty(), Optional.empty());
    }

    public static RewardContext levelUp(ServerPlayer player, String species, int previousLevel, int level, boolean shiny) {
        return new RewardContext(player, Optional.of(level), Optional.of(species), Optional.of(shiny), Optional.empty(), Optional.empty(), Optional.empty(), Optional.of(previousLevel));
    }

    public static RewardContext dexProgress(ServerPlayer player, String species, int entries, int total) {
        return new RewardContext(player, Optional.empty(), Optional.of(species), Optional.empty(), Optional.empty(), Optional.of(entries), Optional.of(total), Optional.empty());
    }
}
