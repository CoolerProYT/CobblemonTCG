package com.coolerpromc.cobblemontcg;

import com.coolerpromc.cobblemontcg.block.entity.ModBlockEntities;
import com.coolerpromc.cobblemontcg.client.CardBinderScreen;
import com.coolerpromc.cobblemontcg.client.CardDisplayStandRenderer;
import com.coolerpromc.cobblemontcg.client.CardStandBuyerScreen;
import com.coolerpromc.cobblemontcg.client.CardStandOwnerScreen;
import com.coolerpromc.cobblemontcg.menu.ModMenuTypes;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.neoforged.neoforge.common.NeoForge;

@Mod(value = Constants.MODID, dist = Dist.CLIENT)
public class NeoForgeCobblemonTCGClient {
    public NeoForgeCobblemonTCGClient(IEventBus eventBus) {
        CobblemonTCGClient.init();
        NeoForge.EVENT_BUS.addListener((ClientTickEvent.Post event) -> CobblemonTCGClient.tick());
        eventBus.addListener((RegisterMenuScreensEvent event) -> {
            event.register(ModMenuTypes.CARD_BINDER.get(), CardBinderScreen::new);
            event.register(ModMenuTypes.CARD_STAND_OWNER.get(), CardStandOwnerScreen::new);
            event.register(ModMenuTypes.CARD_STAND_BUYER.get(), CardStandBuyerScreen::new);
        });
        eventBus.addListener((EntityRenderersEvent.RegisterRenderers event) ->
                event.registerBlockEntityRenderer(ModBlockEntities.CARD_DISPLAY_STAND.get(), CardDisplayStandRenderer::new));
    }
}
