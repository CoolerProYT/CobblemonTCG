package com.coolerpromc.cobblemontcg.reward;

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
