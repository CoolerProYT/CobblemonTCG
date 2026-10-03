package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.network.HandledCustomPacketPayload;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.FabricClientPayloadContext;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

public class FabricCobblemonTCGClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        CobblemonTCGClient.init();
        ClientTickEvents.END_CLIENT_TICK.register(client -> CobblemonTCGClient.tick());
        Services.REGISTRY.applyClientboundPayloadRegistrations(FabricCobblemonTCGClient::registerPayloadReceiver);
    }

    private static <T extends HandledCustomPacketPayload> void registerPayloadReceiver(CustomPacketPayload.Type<T> type, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec) {
        ClientPlayNetworking.registerGlobalReceiver(type, (payload, context) -> payload.handle(new FabricClientPayloadContext(context)));
    }
}
