package com.coolerpromc.cobblemontcg;

import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.common.NeoForge;

@Mod(value = Constants.MODID, dist = Dist.CLIENT)
public class NeoForgeCobblemonTCGClient {
    public NeoForgeCobblemonTCGClient(IEventBus eventBus) {
        CobblemonTCGClient.init();
        NeoForge.EVENT_BUS.addListener((ClientTickEvent.Post event) -> CobblemonTCGClient.tick());
    }
}
