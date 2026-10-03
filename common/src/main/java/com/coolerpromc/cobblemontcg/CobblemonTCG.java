package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.config.TcgConfig;
import com.coolerpromc.cobblemontcg.creativetab.ModCreativeTabs;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.network.ClientboundTcgDataSyncPacket;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.reward.RewardRuleReloadListener;
import com.coolerpromc.cobblemontcg.sound.ModSounds;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataReloadListener;
import net.minecraft.server.level.ServerPlayer;

public class CobblemonTCG {
    private static boolean reloadListenersCollected;

    public static void init() {
        TcgConfig.init();
        ModDataComponents.init();
        ModItems.init();
        ModSounds.init();
        ModCreativeTabs.init();
    }

    public static void initReloadListener() {
        if (reloadListenersCollected) {
            return;
        }
        reloadListenersCollected = true;
        Services.RELOAD_LISTENERS.registerServerReloadListener(TcgDataReloadListener.ID, new TcgDataReloadListener());
        Services.RELOAD_LISTENERS.registerServerReloadListener(RewardRuleReloadListener.ID, new RewardRuleReloadListener());
    }

    public static void initPayloadType() {
        Services.REGISTRY.registerClientboundPayload(ClientboundTcgDataSyncPacket.TYPE, ClientboundTcgDataSyncPacket.STREAM_CODEC);
    }

    public static void syncTcgData(ServerPlayer player) {
        Services.NETWORK.sendToPlayer(player, ClientboundTcgDataSyncPacket.fromServer());
    }
}
