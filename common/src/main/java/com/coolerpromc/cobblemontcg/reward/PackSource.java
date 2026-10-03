package com.coolerpromc.cobblemontcg.reward;

/**
 * Where a booster pack came from. Everything except {@link #COMMAND} counts as a reward and is
 * subject to the rewards toggle and the daily cap.
 */
public enum PackSource {
    COMMAND,
    LOOT,
    CAPTURE,
    LEVEL_UP,
    DEX_PROGRESS;

    public boolean isReward() {
        return this != COMMAND;
    }
}
