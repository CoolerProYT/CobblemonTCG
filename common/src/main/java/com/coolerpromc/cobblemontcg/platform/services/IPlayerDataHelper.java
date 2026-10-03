package com.coolerpromc.cobblemontcg.platform.services;

import com.coolerpromc.cobblemontcg.reward.DailyPackData;
import net.minecraft.server.level.ServerPlayer;

public interface IPlayerDataHelper {
    DailyPackData getDailyPackData(ServerPlayer player);
    void setDailyPackData(ServerPlayer player, DailyPackData data);
}
