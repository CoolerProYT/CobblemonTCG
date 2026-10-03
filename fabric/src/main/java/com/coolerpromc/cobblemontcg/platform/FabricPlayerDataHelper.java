package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.services.IPlayerDataHelper;
import com.coolerpromc.cobblemontcg.reward.DailyPackData;
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

    @Override
    public DailyPackData getDailyPackData(ServerPlayer player) {
        return player.getAttachedOrElse(DAILY_PACKS, DailyPackData.EMPTY);
    }

    @Override
    public void setDailyPackData(ServerPlayer player, DailyPackData data) {
        player.setAttached(DAILY_PACKS, data);
    }
}
