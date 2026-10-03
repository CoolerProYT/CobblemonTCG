package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.command.TcgCommands;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.FabricIdentifiableReloadListener;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.resource.ResourceManagerHelper;
import net.minecraft.server.packs.PackType;

public class FabricCobblemonTCG implements ModInitializer {
    @Override
    public void onInitialize() {
        CobblemonTCG.init();
        CobblemonTCG.initPayloadType();
        CobblemonTCG.initReloadListener();

        Services.REGISTRY.applyClientboundPayloadRegistrations(PayloadTypeRegistry.playS2C()::register);
        Services.RELOAD_LISTENERS.applyServerReloadListenerRegistrations((id, listener) ->
                ResourceManagerHelper.get(PackType.SERVER_DATA).registerReloadListener(new FabricIdentifiableReloadListener(id, listener)));

        CommandRegistrationCallback.EVENT.register((dispatcher, context, selection) -> TcgCommands.register(dispatcher));
        ServerLifecycleEvents.SYNC_DATA_PACK_CONTENTS.register((player, joined) -> CobblemonTCG.syncTcgData(player));
    }
}
