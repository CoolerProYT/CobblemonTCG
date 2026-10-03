package com.coolerpromc.cobblemontcg.platform.services;

import com.coolerpromc.cobblemontcg.reward.DailyPackData;
import com.coolerpromc.cobblemontcg.reward.MilestoneData;
import net.minecraft.server.level.ServerPlayer;

public interface IPlayerDataHelper {
    DailyPackData getDailyPackData(ServerPlayer player);
    void setDailyPackData(ServerPlayer player, DailyPackData data);
    MilestoneData getMilestoneData(ServerPlayer player);
    void setMilestoneData(ServerPlayer player, MilestoneData data);
}
