package com.coolerpromc.cobblemontcg.platform;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.platform.services.IPlayerDataHelper;
import com.coolerpromc.cobblemontcg.reward.DailyPackData;
import com.coolerpromc.cobblemontcg.reward.MilestoneData;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.function.Supplier;

public class NeoForgePlayerDataHelper implements IPlayerDataHelper {
    public static final DeferredRegister<AttachmentType<?>> ATTACHMENTS = DeferredRegister.create(NeoForgeRegistries.ATTACHMENT_TYPES, Constants.MODID);
    public static final Supplier<AttachmentType<DailyPackData>> DAILY_PACKS = ATTACHMENTS.register("daily_packs", () -> AttachmentType.builder(() -> DailyPackData.EMPTY).serialize(DailyPackData.CODEC).copyOnDeath().build());
    public static final Supplier<AttachmentType<MilestoneData>> MILESTONES = ATTACHMENTS.register("reward_milestones", () -> AttachmentType.builder(() -> MilestoneData.EMPTY).serialize(MilestoneData.CODEC).copyOnDeath().build());

    @Override
    public DailyPackData getDailyPackData(ServerPlayer player) {
        return player.getData(DAILY_PACKS);
    }

    @Override
    public void setDailyPackData(ServerPlayer player, DailyPackData data) {
        player.setData(DAILY_PACKS, data);
    }

    @Override
    public MilestoneData getMilestoneData(ServerPlayer player) {
        return player.getData(MILESTONES);
    }

    @Override
    public void setMilestoneData(ServerPlayer player, MilestoneData data) {
        player.setData(MILESTONES, data);
    }

    public static void register(IEventBus eventBus) {
        ATTACHMENTS.register(eventBus);
    }
}
