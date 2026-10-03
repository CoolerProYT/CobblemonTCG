package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.services.IPlayerDataHelper;
import com.coolerpromc.cobblemontcg.reward.DailyPackData;
import com.coolerpromc.cobblemontcg.reward.MilestoneData;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.server.level.ServerPlayer;

@SuppressWarnings("UnstableApiUsage")
public class FabricPlayerDataHelper implements IPlayerDataHelper {
    public static final AttachmentType<DailyPackData> DAILY_PACKS = AttachmentRegistry.<DailyPackData>builder()
            .persistent(DailyPackData.CODEC)
            .copyOnDeath()
            .initializer(() -> DailyPackData.EMPTY)
            .buildAndRegister(Constants.id("daily_packs"));
    public static final AttachmentType<MilestoneData> MILESTONES = AttachmentRegistry.<MilestoneData>builder()
            .persistent(MilestoneData.CODEC)
            .copyOnDeath()
            .initializer(() -> MilestoneData.EMPTY)
            .buildAndRegister(Constants.id("reward_milestones"));

    @Override
    public DailyPackData getDailyPackData(ServerPlayer player) {
        return player.getAttachedOrElse(DAILY_PACKS, DailyPackData.EMPTY);
    }

    @Override
    public void setDailyPackData(ServerPlayer player, DailyPackData data) {
        player.setAttached(DAILY_PACKS, data);
    }

    @Override
    public MilestoneData getMilestoneData(ServerPlayer player) {
        return player.getAttachedOrElse(MILESTONES, MilestoneData.EMPTY);
    }

    @Override
    public void setMilestoneData(ServerPlayer player, MilestoneData data) {
        player.setAttached(MILESTONES, data);
    }
}
