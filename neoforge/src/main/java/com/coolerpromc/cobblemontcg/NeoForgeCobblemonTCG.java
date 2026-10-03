package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.command.TcgCommands;
import com.coolerpromc.cobblemontcg.network.HandledCustomPacketPayload;
import com.coolerpromc.cobblemontcg.platform.NeoForgePlayerDataHelper;
import com.coolerpromc.cobblemontcg.platform.NeoForgeRegistryHelper;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.NeoForgePayloadContext;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.AddReloadListenerEvent;
import net.neoforged.neoforge.event.OnDatapackSyncEvent;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

@Mod(Constants.MODID)
public class NeoForgeCobblemonTCG {
    public NeoForgeCobblemonTCG(IEventBus eventBus) {
        CobblemonTCG.init();
        NeoForgeRegistryHelper.register(eventBus);
        NeoForgePlayerDataHelper.register(eventBus);

        eventBus.addListener(NeoForgeCobblemonTCG::onRegisterPayloadHandlers);
        NeoForge.EVENT_BUS.addListener(NeoForgeCobblemonTCG::onAddReloadListeners);
        NeoForge.EVENT_BUS.addListener(NeoForgeCobblemonTCG::onRegisterCommands);
        NeoForge.EVENT_BUS.addListener(NeoForgeCobblemonTCG::onDatapackSync);
    }

    private static void onRegisterPayloadHandlers(RegisterPayloadHandlersEvent event) {
        CobblemonTCG.initPayloadType();
        NeoForgePayloadRegistrar registrar = new NeoForgePayloadRegistrar(event.registrar("1"));
        Services.REGISTRY.applyClientboundPayloadRegistrations(registrar::registerClientbound);
    }

    private static void onAddReloadListeners(AddReloadListenerEvent event) {
        CobblemonTCG.initReloadListener();
        Services.RELOAD_LISTENERS.applyServerReloadListenerRegistrations((id, listener) -> event.addListener(listener));
    }

    private static void onRegisterCommands(RegisterCommandsEvent event) {
        TcgCommands.register(event.getDispatcher());
    }

    private static void onDatapackSync(OnDatapackSyncEvent event) {
        event.getRelevantPlayers().forEach(CobblemonTCG::syncTcgData);
    }

    private record NeoForgePayloadRegistrar(PayloadRegistrar registrar) {
        private <T extends HandledCustomPacketPayload> void registerClientbound(CustomPacketPayload.Type<T> type, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec) {
            registrar.playToClient(type, streamCodec, (payload, context) -> payload.handle(new NeoForgePayloadContext(context)));
        }
    }
}
