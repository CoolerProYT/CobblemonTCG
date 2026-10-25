package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.block.entity.ModBlockEntities;
import com.coolerpromc.cobblemontcg.client.CardBinderScreen;
import com.coolerpromc.cobblemontcg.client.CardDisplayStandRenderer;
import com.coolerpromc.cobblemontcg.client.CardStandBuyerScreen;
import com.coolerpromc.cobblemontcg.client.CardStandOwnerScreen;
import com.coolerpromc.cobblemontcg.menu.ModMenuTypes;
import com.coolerpromc.cobblemontcg.network.HandledCustomPacketPayload;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.FabricClientPayloadContext;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.client.rendering.v1.BlockEntityRendererRegistry;
import net.minecraft.client.gui.screens.MenuScreens;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

public class FabricCobblemonTCGClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        CobblemonTCGClient.init();
        MenuScreens.register(ModMenuTypes.CARD_BINDER.get(), CardBinderScreen::new);
        MenuScreens.register(ModMenuTypes.CARD_STAND_OWNER.get(), CardStandOwnerScreen::new);
        MenuScreens.register(ModMenuTypes.CARD_STAND_BUYER.get(), CardStandBuyerScreen::new);
        BlockEntityRendererRegistry.register(ModBlockEntities.CARD_DISPLAY_STAND.get(), CardDisplayStandRenderer::new);
        ClientTickEvents.END_CLIENT_TICK.register(client -> CobblemonTCGClient.tick());
        Services.REGISTRY.applyClientboundPayloadRegistrations(FabricCobblemonTCGClient::registerPayloadReceiver);
    }

    private static <T extends HandledCustomPacketPayload> void registerPayloadReceiver(CustomPacketPayload.Type<T> type, StreamCodec<? super RegistryFriendlyByteBuf, T> streamCodec) {
        ClientPlayNetworking.registerGlobalReceiver(type, (payload, context) -> payload.handle(new FabricClientPayloadContext(context)));
    }
}
