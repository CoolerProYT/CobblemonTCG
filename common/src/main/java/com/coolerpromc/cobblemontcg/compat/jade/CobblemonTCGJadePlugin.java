package com.coolerpromc.cobblemontcg.compat.jade;

import com.coolerpromc.cobblemontcg.block.custom.CardDisplayStandBlock;
import com.coolerpromc.cobblemontcg.client.CardDisplayStandRenderer;
import snownee.jade.api.IWailaClientRegistration;
import snownee.jade.api.IWailaPlugin;
import snownee.jade.api.WailaPlugin;

@WailaPlugin
public class CobblemonTCGJadePlugin implements IWailaPlugin {
    @Override
    public void registerClient(IWailaClientRegistration registration) {
        registration.registerBlockComponent(CardStandJadeProvider.INSTANCE, CardDisplayStandBlock.class);
        CardDisplayStandRenderer.showLabel = false;
    }
}
